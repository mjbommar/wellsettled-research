# Standard imports
import codecs
import csv
import os
import re
from pprint import pprint

# WSR imports
from wsr.data.circuit import Circuit, read_xml_document, read_xml_opinion
from wsr.config import SCRATCH_PATH, CIRCUIT_FILE_NAME_LIST
from wsr.process.tokenize import sentence_tokenizer
from wsr.process.stem import process_sentence

if __name__ == "__main__":
    # Regex to clean square brackets
    re_bracket = re.compile(r'\[(?:[^\]|]*\|)?([^\]|]*)\]')

    #  Load sentence files
    scotus_sentence_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                                    "circuit_exact_sentence_list.csv"),
                                       'r', 'utf8')

    circuit_sentence_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                                     "circuit_exact_sentence_list.csv"),
                                        'r', 'utf8')

    # Read sentence list
    sentence_data = []
    for row in scotus_sentence_file.read().split("\n"):
        sentence_data.append(row.split("\t"))

    for row in circuit_sentence_file.read().split("\n"):
        sentence_data.append(row.split("\t"))

    # Get unique sentence set
    sentence_set = sorted(list(set([row[1] for row in sentence_data if len(row) > 1])))

    # Parse unique sentence set into stem match list
    phrase_list = []
    bad_phrase_list = []

    for sentence in sentence_set:
        # Locate initial "that" or other starting mark
        phrase_start = sentence.find("that")
        if phrase_start > 0:
            phrase = sentence[phrase_start:]
        else:
            bad_phrase_list.append(sentence)
            continue

        # Clean up a few more small items
        phrase = re_bracket.sub(r'\1', phrase)

        # Get stems
        phrase_stems = process_sentence(phrase)
        if len(phrase_stems) < 3:
            bad_phrase_list.append(sentence)
            continue

        # Check type of sentence
        phrase_list.append(tuple(phrase_stems))

    # Unique and sort
    phrase_set = list(set(phrase_list))
    print("{0} phrases identified.".format(len(phrase_set)))

    # Output phrase stems
    with codecs.open(os.path.join(SCRATCH_PATH, "results",
                                                     "ws_phrase_stems.csv"),
                    'w', 'utf8') as phrase_file:
        for phrase in phrase_set:
            phrase_file.write(",".join(phrase) + "\n")