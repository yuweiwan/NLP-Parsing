# NLP-Parsing
Parse sentence based on grammar.  
Command:  
python3 parse.py MODE foo.gr foo.sen  
MODE is one of these:  
– RECOGNIZER, which returns whether the sentence can be parsed according to the grammar  
– BEST-PARSE, which gives the minimum-weight parse and its weight.  
– TOTAL-WEIGHT, which gives the log2 of the total probability of a sentence according to the grammar, in bits.
