# Makefile for ThuThesis-based thesis workspace

PACKAGE = thuthesis
THESIS  = thuthesis-chiwang-bachelor-tps
EXAMPLE = thuthesis-example
SPINE   = spine

SOURCES = $(PACKAGE).ins $(PACKAGE).dtx
CLSFILE = dtx-style.sty $(PACKAGE).cls

LATEXMK = latexmk
SHELL  := /usr/bin/env bash

# make deletion work on Windows
ifdef SystemRoot
	RM = del /Q
else
	RM = rm -f
endif

.PHONY: all all-dev clean cleanall distclean dist thesis example viewthesis viewexample doc viewdoc cls check save test FORCE_MAKE

thesis: $(THESIS).pdf

all: thesis

all-dev: doc all

example: $(EXAMPLE).pdf

cls: $(CLSFILE)

$(CLSFILE): $(SOURCES)
	xetex $(PACKAGE).ins

doc: $(PACKAGE).pdf

$(PACKAGE).pdf: cls FORCE_MAKE
	$(LATEXMK) $(PACKAGE).dtx

$(THESIS).pdf: cls FORCE_MAKE
	$(LATEXMK) $(THESIS)

$(EXAMPLE).pdf: FORCE_MAKE
	$(LATEXMK) $(EXAMPLE)

viewdoc: doc
	$(LATEXMK) -pv $(PACKAGE).dtx

viewthesis: thesis
	$(LATEXMK) -pv $(THESIS)

viewexample: example
	$(LATEXMK) -pv $(EXAMPLE)

save:
ifeq ($(target),)
	bash testfiles/save.sh
else
	bash testfiles/save.sh $(target)
endif

test:
ifeq ($(target),)
	l3build check
else
	bash testfiles/test.sh $(target)
endif

clean:
	$(LATEXMK) -c $(PACKAGE).dtx $(THESIS) $(EXAMPLE)
	-@$(RM) -rf *~ missfont.log main-survey.* main-translation.* _markdown_thuthesis* thuthesis.markdown.*

cleanall: clean
	-@$(RM) $(PACKAGE).pdf $(THESIS).pdf $(EXAMPLE).pdf

distclean: cleanall
	-@$(RM) $(CLSFILE)
	-@$(RM) -r dist

check: FORCE_MAKE
ifeq ($(version),)
	@echo "Error: version missing: \"make [check|dist] version=X.Y.Z\""; exit 1
else
	@[[ $(shell grep -E -c '$(version) Tsinghua University Thesis Template|\\def\\version\{$(version)\}' thuthesis.dtx) -eq 3 ]] || (echo "bump version with \"l3build tag\" before release"; exit 1)
endif

dist: check all-dev
	l3build ctan --config utils/build-ctan
	python3 utils/create_release.py --version="v$(version)"
