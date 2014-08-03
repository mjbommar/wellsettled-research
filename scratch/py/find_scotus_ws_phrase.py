# Standard imports
import codecs
import csv
import os
import re
from pprint import pprint

# WSR imports
from wsr.data.scotus import SCOTUS, read_xml_document, read_xml_opinion
from wsr.config import SCRATCH_PATH, SCOTUS_FILE_NAME
from wsr.process.tokenize import sentence_tokenizer
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

    # Regex to clean square brackets
    re_bracket = re.compile(r'\[(?:[^\]|]*\|)?([^\]|]*)\]')

    # Load phrase stems
    phrase_list = []
    with codecs.open(os.path.join(SCRATCH_PATH, "results",
                                  "ws_phrase_stems.csv"),
                     'r', 'utf8') as phrase_file:
        for line in phrase_file:
            phrase_list.append(tuple(line.strip().split(',')))
            print(phrase_list[-1])

    # Output to file
    instance_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                             "scotus_ws_instances.csv"),
                                'w', 'utf8')

    # Get the phrase mapping
    phrase_id = range(len(phrase_list))
    phrase_mapping = dict(zip(phrase_list, phrase_id))

    # Write the phrase mapping to disk
    phrase_mapping_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                                   "ws_phrase_mapping.csv"),
                                      'w', 'utf8')
    for phrase in phrase_mapping:
        phrase_mapping_file.write(u"\t".join([str(phrase_mapping[phrase]),
                                              ' '.join(phrase)]) + "\n")
    phrase_mapping_file.close()

    # Iterate over documents
    for file_name in scotus.scotus_document_list:
        # Get the XML document and sentence list
        try:
            doc = read_xml_document(scotus.read_document(file_name))
            sentence_list = [s.strip().replace("\n", "").replace("\r", "") \
                             for s in sentence_tokenizer \
                    .sentences_from_text(read_xml_opinion(doc))]
        except Exception, E:
            print(E)
            continue

        for sentence in sentence_list:
            # Process the sentences
            sentence_stems = tuple(process_sentence(sentence))

            # Inner loop
            for phrase in phrase_list:
                # Skip phrases that are too long
                if len(phrase) > sentence_stems:
                    continue

                if phrase[0] not in sentence_stems:
                    continue

                for offset in range(len(sentence_stems) - len(phrase) + 1):
                    if sentence_stems[offset] == phrase[0] and \
                                    phrase == sentence_stems[offset:(offset + len(phrase))]:
                        # Get the record
                        # Output
                        # Log
                        record = (file_name, str(phrase_mapping[phrase]), ",".join(sentence_stems))
                        pprint(record)
                        instance_file.write("\t".join(record) + "\n")
    # Close file
    instance_file.close()
