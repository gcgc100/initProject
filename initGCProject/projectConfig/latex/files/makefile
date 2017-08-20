TEX = pdflatex -shell-escape -interaction=nonstopmode -file-line-error
BIB = bibtex

.PHONY: all view

all : main.pdf

view:
	/Applications/Skim.app/Contents/MacOS/Skim main.pdf

main.pdf : main.tex main.bbl main.blg
	$(TEX) main
	$(TEX) main

main.bbl main.blg : main.bib main.aux
	$(BIB) main

main.aux : main.tex 
	$(TEX) main

main.bib : main.tex 
	$(TEX) main

clean:
	latexmk -C
	rm main.bbl
