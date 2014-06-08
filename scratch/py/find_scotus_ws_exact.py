# Standard imports
import codecs
import os

# WSR imports
from wsr.data.scotus import SCOTUS, read_xml_document, read_xml_opinion
from wsr.config import SCRATCH_PATH
from wsr.process.tokenize import sentence_tokenizer
from wsr.process.parse import sentence_parser
from wsr.process.stem import process_sentence


def check_sentence_match(stems):
    """Check if the sentence stem sequence matches our desired
    patterns."""
    
    # Check minimum length
    if len(stems) < 3:
        return False
    
    # Require initial "it"
    if stems[0] != "it":
        return False

    # Check for "well*"
    if not stems[1].startswith('well'):
        return False
    
    # Now handle hyphen vs. space
    if '-' in stems[1]:
        tokens = stems[1].split('-')
        if tokens[1] in ['settl', 'establish']:
            return True
    elif stems[2] in ['settl', 'establish']:
        return True
    else:
        return False


if __name__ == "__main__":
    # Load the dataset
    scotus = SCOTUS()

    # Store the sentence list
    ws_list = []

    # Output to file
    sentence_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                             "exact_sentence_list.csv"),
                                'w', 'utf8')

    # Iterate over documents
    for file_name in scotus.scotus_document_list:
        # Get the XML document and sentence list
        try:
            doc = read_xml_document(scotus.read_document(file_name))
            sentence_list = [s.strip().replace("\n", "").replace("\r", "") \
                             for s in sentence_tokenizer\
                             .sentences_from_text(read_xml_opinion(doc))]
        except Exception, E:
            print(E)
            continue

        for sentence in sentence_list:
            # Process the sentences
            sentence_stems = process_sentence(sentence)
            try:
                is_match = check_sentence_match(sentence_stems)
                
                if is_match:
                    # Write
                    sentence_file.write(u'{0}\t{1}\n'\
                                        .format(file_name, unicode(sentence)\
                                                .replace("\n", " ")\
                                                .replace("\t", " ")))

            except Exception, e:
                print(e)
                print(sentence_stems)



    # Close file
    sentence_file.close()