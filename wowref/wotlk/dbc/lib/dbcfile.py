#!/usr/bin/env python

import os
from struct import Struct

from .dtypes import *

UNICODE_BLANK = ''


class DBCRecord(object):
    "A simple object to convert a dict to an object"
    def __init__(self, d=None):
        self.data = d

    def __repr__(self):
        return "<DBCRecord %r>" % self.data

    def __getitem__(self, item):
        print('hi')
        return self.data[item]

    def __getattr__(self, item):
        item = self.data[item]
        if isinstance(item, bytes):
            item = item.decode('utf-8')
        return item


class DBCFile(object):
    """
    Base representation of a DBC file.
    """

    header_struct = Struct('4s4i')

    def __init__(self, filename, skele=None, verbose=False):
        self.filename = filename
        if not hasattr(self, 'skeleton'):
            self.skeleton = skele
        self.__create_struct()

    def __iter__(self):
        "Iterated based approach to the dbc reading"
        if not os.path.exists(self.filename):
            raise Exception("File '%s' not found" % (self.filename,))

        f = open(self.filename, 'rb')
        f_read = f.read
        # Read in header
        sig, records, fields, record_size, string_block_size = \
            self.header_struct.unpack(f_read(20))

        # Check signature
        if sig != b'WDBC':
            f.close()
            raise Exception('Invalid file type')

        self.records = records
        self.fields = fields
        self.record_size = record_size
        self.string_block_size = string_block_size

        if not self.struct:
            # If the struct doesn't exist, create a default one
            self.skeleton = Array('data', Int32, fields)
            self.__create_struct()

        # Ensure that struct and record_size is the same
        if self.struct.size != record_size:
            f.close()
            raise Exception('Struct size mismatch (%d != %d)' %
                            (self.struct.size, record_size))
        struct_unpack = self.struct.unpack

        # Read in string block
        f.seek(20 + records * record_size)
        self.string_block = f_read(string_block_size)
        f.seek(20)

        try:
            for i in range(records):
                yield self.__process_record(struct_unpack(f_read(record_size)))
        finally:
            f.close()

    def __create_struct(self):
        "Creates a Struct from the Skeleton"
        if self.skeleton:
            s = ['<']
            for item in self.skeleton:
                if isinstance(item, Array):
                    s.extend(x.c for x in item.items)
                else:
                    s.append(item.c)
            self.struct = Struct(''.join(s))
        else:
            self.struct = None

    def __process_record(self, data):
        "Processes a record (row of data)"
        output = {}
        data_iter = iter(data)
        for field in self.skeleton:
            if isinstance(field, Array):
                output[field.name] = [
                    self.__process_field(item, next(data_iter)) for item in field.items
                    if not isinstance(item, PadByte)
                ]
            elif not isinstance(field, PadByte):
                output[field.name] = self.__process_field(field, next(data_iter))
        return DBCRecord(output)

    def __process_field(self, _type, data):
        output = data
        if isinstance(_type, String):
            if data == 0:
                output = UNICODE_BLANK
            else:
                if data > self.string_block_size or self.string_block[data - 1] != 0:
                    raise Exception('Invalid string')
                output = self.string_block[data:self.string_block.find(0, data)]
        if isinstance(output, bytes):
            output = output.decode('utf-8')
        return output
