ALL = pulse_examples_simple.pdf pulse_examples_discrete.pdf pulse_examples_continuous.pdf pulse_examples_pwc.pdf
PDFLATEXOPTS = -file-line-error -interaction=nonstopmode -halt-on-error
PYTHON = ../.venv/bin/python

all: $(ALL)

%.pdf: %.tex
	@echo "\n** generate figure: $< -> $@"
	pdflatex $(PDFLATEXOPTS) $<

%.pdf: %.py matplotlibrc
	@echo "\n** generate figure: $< -> $@"
	$(PYTHON) $<

%.png: %.py matplotlibrc
	@echo "\n** generate figure: $< -> $@"
	$(PYTHON) $<

%.tex: %.py
	$(PYTHON) $<

pulse_examples_simple.pdf: pulse_examples.py
	@echo "\n** generate figure: $< -> $@"
	$(PYTHON) $<

pulse_examples_discrete.pdf: pulse_examples_simple.pdf

pulse_examples_continuous.pdf: pulse_examples_simple.pdf

pulse_examples_pwc.pdf: pulse_examples_simple.pdf


clean:
	@rm -f *.aux
	@rm -f *.log
	@rm -f *.toc
	@rm -f *.blg
	@rm -rf *.out
	@rm -f *.bak
	@rm -f *.ilg
	@rm -f *.snm
	@rm -f *.nav
	@rm -f *.table
	@rm -f *.dvi
	@rm -f *.fls
	@rm -f *.bbl
	@rm -f *~
	@rm -f *Notes.bib
	@rm -f *-eps-converted-to.pdf
	@rm -f *.fdb_latexmk
	@rm -f *.synctex.gz*
	@rm -f ./latexrun
	@rm -rf __pycache__

distclean: clean
	@rm -rf animate_rottai
	@rm -f opt_dynamics_*.pdf
	@rm -f guess_dynamics_*.pdf
	@rm -f cn_sim_results_*.pdf
	@rm -f fidelity_map_*.pdf
	@rm -f adiabatic_dynamics_50πps_*.pdf
	@rm -f guess_sagnac_*.pdf
	@rm -f opt_sagnac_*.pdf
	#@rm -f $(ALL)

.PHONY: all clean distclean
