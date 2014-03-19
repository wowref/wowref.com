SHELL := /bin/sh

REPOPATH := $(CURDIR)
LOCALPATH := $(REPOPATH)/wowref
PYTHONPATH := $(LOCALPATH)
PYTHON_BIN := $(VIRTUAL_ENV)/bin

PROJECT := wowref_www
SETTINGS := devel
TEST_SETTINGS := test

DJANGO_SETTINGS_MODULE := $(PROJECT).settings.$(SETTINGS)
DJANGO_TEST_SETTINGS_MODULE := $(PROJECT).settings.$(TEST_SETTINGS)


runserver:
	$(PYTHON_BIN)/django-admin.py runserver --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)

test:
	$(PYTHON_BIN)/django-admin.py test $(APP) --settings=$(DJANGO_TEST_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
