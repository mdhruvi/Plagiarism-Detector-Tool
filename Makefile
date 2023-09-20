PYTHON = python3
TARGET = 40166396_detector
FILE1 = 
FILE2 = 

all: $(TARGET)

clean: rm -rf _pycache_

$(TARGET):
	$(PYTHON) $(TARGET).py $(FILE1) $(FILE2)
	
run: $(TARGET)
	
testPlagiarism: $(TARGET)
	@echo "Testing plagiarism test cases in ../data/plagiarismXX"
	@for file in ../data/plagiarism*; do echo "Testing $$file"; $(PYTHON) $(TARGET).py $$file/1.txt $$file/2.txt;done

testNonPlagiarism: $(TARGET)
	@echo "Testing non-plagiarism test cases in ../data/okayXX"
	@for file in ../data/okay*; do echo "Testing $$file"; $(PYTHON) $(TARGET).py $$file/1.txt $$file/2.txt;done

test: testPlagiarism testNonPlagiarism
