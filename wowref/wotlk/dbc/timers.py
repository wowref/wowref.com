from contextlib import contextmanager
import time

_indentLevel = 0


@contextmanager
def LoadTimer(name, newLine=False, prefix='APP'):
    """
        A context manager that measures how long it takes the content of the context to execute.
    """
    global _indentLevel

    print('%s>>> [%s] Loading %-21s' % (' ' * _indentLevel * 4, prefix, name), end=" ")
    if newLine:
        _indentLevel += 1
        print()
    t = time.time()
    yield None

    if newLine:
        _indentLevel -= 1
        print("%s... [OK] Loaded %s in %.2f seconds." % (' ' * _indentLevel * 4,
                                                         name, time.time() - t))
    else:
        print("[OK] Loaded in %.2f seconds." % (time.time() - t))


@contextmanager
def LoadTimerWithSuccess(target, load_name=None, prefix=None, subLoad=None):
    global _indentLevel
    if subLoad:
        print("%sloading %-26s" %
              (' ' * _indentLevel * 4, '`%s`' % target), end=" ")
    else:
        print("%s>>> [%s] Loading %s for `%s` " %
              (' ' * _indentLevel * 4, prefix, load_name, target))
        _indentLevel += 1

    start = time.time()
    try:
        yield None
    except SuccessLoadedRecords as e:
        if subLoad:
            done_prefix = ""
        else:
            _indentLevel -= 1
            done_prefix = "%s..." % (' ' * _indentLevel * 4)

        if e.numRecords is not None:
            print("%s [OK] %i records in %.2f seconds." %
                  (done_prefix, e.numRecords, time.time() - start))
        else:
            print("%s [OK] loaded in %.2f seconds." %
                  (done_prefix, time.time() - start))
    else:
        raise ValueError("Load Failed, Did Not Call SuccessLoadedRecords()")


class SuccessLoadedRecords(Exception):
    numRecords = None

    def __init__(self, numRecords=None):
        if numRecords:
            self.numRecords = numRecords
            Exception.__init__(self, "Successfully loaded %i records" % self.numRecords)
        else:
            Exception.__init__(self)


def LoadedRecords(numRecords=None):
    raise SuccessLoadedRecords(numRecords)
