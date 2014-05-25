# Download the Stanford parser
wget http://nlp.stanford.edu/software/stanford-parser-full-2014-01-04.zip
unzip stanford-parser-full-2014-01-04.zip
mv stanford-parser-full-2014-01-04 stanford-parser

# Extract the grammar
cd stanford-parser
unzip stanford-parser-3.3.1-models.jar edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz
mv edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ./
rm -rf edu/
cd ../

# Cleanup
rm -f stanford-parser-full-2014-01-04.zip