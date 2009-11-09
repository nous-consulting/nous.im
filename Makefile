#!/usr/bin/make
#
# Makefile for UTUTI Sandbox
#

BOOTSTRAP_PYTHON=python2.5
TIMEOUT=1
BUILDOUT = bin/buildout -t $(TIMEOUT) && touch bin/*


.PHONY: all
all: python/bin/python bin/buildout bin/twistd

python/bin/python:
	$(MAKE) BOOTSTRAP_PYTHON=$(BOOTSTRAP_PYTHON) bootstrap

bin/buildout: bootstrap.py
	$(MAKE) BOOTSTRAP_PYTHON=$(BOOTSTRAP_PYTHON) bootstrap

bin/test: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

bin/py: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

bin/twistd: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

bin/tags: buildout.cfg bin/buildout setup.py versions.cfg
	$(BUILDOUT)

tags: buildout.cfg bin/buildout setup.py bin/tags
	bin/tags

TAGS: buildout.cfg bin/buildout setup.py bin/tags
	bin/tags

ID: buildout.cfg bin/buildout setup.py bin/tags
	bin/tags

.PHONY: bootstrap
bootstrap:
	$(BOOTSTRAP_PYTHON) bootstrap.py

.PHONY: buildout
buildout:
	$(BUILDOUT)

.PHONY: test
test: bin/test
	bin/test --all

.PHONY: utest
testall: bin/test
	bin/test -u

.PHONY: ftest
ftest: bin/test
	bin/test -f --at-level 2

.PHONY: run
run: bin/twistd
	bin/twistd serve development.ini --reload --monitor-restart

.PHONY: clean
clean:
	rm -rf bin/ parts/ develop-eggs/ src/nous.im.egg-info/ python/ tags TAGS ID .installed.cfg

