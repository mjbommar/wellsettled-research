# Standard imports
import codecs
import csv
import difflib
import os
import pandas
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

    # Load phrase stems
    phrase_list = []
    with codecs.open(os.path.join(SCRATCH_PATH, "results",
                                  "ws_phrase_stems.csv"),
                     'r', 'utf8') as phrase_file:
        for line in phrase_file:
            phrase_list.append(tuple(line.strip().split(',')))

    # Get the phrase mapping
    phrase_id = range(len(phrase_list))
    phrase_mapping = dict(zip(phrase_list, phrase_id))
    phrase_matcher_mapping = {}
    for phrase_stems in phrase_list:
        phrase_matcher_mapping[phrase_mapping[phrase_stems]] = difflib.SequenceMatcher(None, phrase_stems, None)

    # Open sentence file
    sentence_file = codecs.open('/nfs-data/datasets/wellsettled/sentences_20141028.txt', 'r', 'utf8', 'ignore')

    # Iterate over sentence file
    max_lines = 10000000000000
    current_line = 0

    ws_matches = []

    for line in sentence_file:
        # Check line
        if current_line < max_lines:
            current_line += 1

            if current_line % 10000 == 0:
                pandas.DataFrame(ws_matches).to_csv('ws_matches.csv', encoding='utf-8')

        else:
            break

        # Split line into tokens and assign
        tokens = [token.strip() for token in line.split('|')[1:]]
        try:
            sentence_id, case_caption, case_date, sentence = tokens
        except ValueError, e:
            print(tokens)
            print(e)
            continue

        # Get stems
        sentence_stems = tuple(process_sentence(re_bracket.sub(r'\1', sentence)))
        if len(sentence_stems) <= 0:
            continue

        for phrase_stems in phrase_list:
            # Skip short mismatches
            if phrase_stems[0] not in sentence_stems or len(phrase_stems) > sentence_stems:
                continue

            # Build matcher
            s = difflib.SequenceMatcher(None, sentence_stems, phrase_stems)
            for b in s.get_matching_blocks():
                if b[2] == len(phrase_stems):
                    print(sentence_stems)
                    print(phrase_stems)
                    print("-")
                    ws_matches.append((sentence_id, case_caption, case_date, phrase_mapping[phrase_stems]))

    pandas.DataFrame(ws_matches).to_csv('ws_matches.csv', encoding='utf-8')

    # Close file
    sentence_file.close()
