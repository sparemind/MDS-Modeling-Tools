PYTHON = python3
R = Rscript

RAW_DATA = MERGED2015_16_PP.csv
ATTRIBUTES = attributes.txt
#ATTRIBUTES = academic_attributes.txt
#ATTRIBUTES = diversity_attributes.txt
FILTER = filter.py
MDS = MDS.r
ANALYZE = analyze.py
ANALYSIS_OUT = analysis.txt

model: 
	$(PYTHON) $(FILTER) $(RAW_DATA) < $(ATTRIBUTES)
	$(R) $(MDS)
	$(PYTHON) $(ANALYZE) < $(ATTRIBUTES) > $(ANALYSIS_OUT)
	cat $(ANALYSIS_OUT)

color:
	$(PYTHON) $(FILTER) $(RAW_DATA) < $(ATTRIBUTES)
	$(PYTHON) color.py
	$(R) $(MDS) colors.csv
	$(PYTHON) $(ANALYZE) < $(ATTRIBUTES) > $(ANALYSIS_OUT)
	cat $(ANALYSIS_OUT)

