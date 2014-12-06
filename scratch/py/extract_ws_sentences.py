# Standard imports
import codecs
import csv
import os

# WSR imports
from wsr.config import SCRATCH_PATH, CIRCUIT_FILE_NAME_LIST

if __name__ == "__main__":
    # Load WS sentence list
    instance_list = []

    header = None
    with codecs.open(os.path.join(SCRATCH_PATH, "results",
                                  "ws_matches.csv"),
                     'r', 'utf8') as phrase_file:
        for line in phrase_file:
            if header:
                instance_list.append(line.split(',')[1].strip())
            else:
                header = line

    # Open sentence file
    sentence_file = codecs.open('/nfs-data/datasets/wellsettled/sentences_20141028.txt', 'r', 'utf8', 'ignore')
    output_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                           "ws_match_sentences.txt"), "w", "utf8")

    for line in sentence_file:
        # Match sentence ID
        sentence_id = line.split("|")[1].strip()
        if sentence_id in instance_list:
            output_file.write(line.strip() + "\n")

    # Close files
    output_file.close()
    sentence_file.close()
