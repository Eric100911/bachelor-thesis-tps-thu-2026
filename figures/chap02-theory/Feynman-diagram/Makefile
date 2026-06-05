# Build JaxoDraw-exported Feynman diagrams as standalone PDF assets.

SHELL := /usr/bin/env bash

LATEXMK ?= latexmk
PDFLATEX ?= pdflatex
AXOHELP ?= axohelp
PDFCROP ?= pdfcrop

SOURCES := DPS-1.tex DPS-2.tex SPS.tex TPS.tex
PDFS := $(SOURCES:.tex=.pdf)
BASENAMES := $(SOURCES:.tex=)
BUILD_DIR := build

# The original JaxoDraw article exports are wider/taller than A4.  Build on a
# deliberately large page, then crop to the actual drawing.
PAPER_WIDTH ?= 2000pt
PAPER_HEIGHT ?= 1400pt
CROP_MARGIN ?= 4

.PHONY: all check-tools clean cleanall
.SECONDARY: $(addprefix $(BUILD_DIR)/,$(SOURCES) $(PDFS))

all: check-tools $(PDFS)

check-tools:
	@command -v $(LATEXMK) >/dev/null || { echo "missing $(LATEXMK)"; exit 1; }
	@command -v $(PDFLATEX) >/dev/null || { echo "missing $(PDFLATEX)"; exit 1; }
	@command -v $(AXOHELP) >/dev/null || { echo "missing $(AXOHELP)"; exit 1; }
	@command -v $(PDFCROP) >/dev/null || { echo "missing $(PDFCROP)"; exit 1; }

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/%.tex: %.tex axodraw4j.sty | $(BUILD_DIR)
	perl -0pe 's/(\\usepackage\{axodraw4j\}\n)/$${1}\\setlength{\\paperwidth}{$(PAPER_WIDTH)}\n\\setlength{\\paperheight}{$(PAPER_HEIGHT)}\n\\pdfpagewidth=\\paperwidth\n\\pdfpageheight=\\paperheight\n/;' $< > $@

$(BUILD_DIR)/%.pdf: $(BUILD_DIR)/%.tex axodraw4j.sty
	cd $(BUILD_DIR) && TEXINPUTS=..:$${TEXINPUTS} $(LATEXMK) -pdf -pdflatex="$(PDFLATEX) -interaction=nonstopmode -halt-on-error %O %S" "$(notdir $<)"
	cd $(BUILD_DIR) && $(AXOHELP) $*
	cd $(BUILD_DIR) && TEXINPUTS=..:$${TEXINPUTS} $(LATEXMK) -pdf -pdflatex="$(PDFLATEX) -interaction=nonstopmode -halt-on-error %O %S" "$(notdir $<)"

%.pdf: %.tex axodraw4j.sty $(BUILD_DIR)/%.pdf
	$(PDFCROP) --margins $(CROP_MARGIN) $(BUILD_DIR)/$*.pdf $@

clean:
	rm -rf $(BUILD_DIR)

cleanall: clean
	rm -f $(PDFS)
