.PHONY: clean

%.pdf: %.tex $(DEPENDS)
	rubber -f --pdf -s --inplace $<
	rubber-info --inplace --check $<

clean:
	rubber --clean --pdf
