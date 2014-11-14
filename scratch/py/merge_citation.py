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

def load_pipe_file(file_name):
    """Load a pipe-delimited file."""
    # Open file
    pipe_file = codecs.open(file_name, 'r', 'utf8')

    # Iterate and store
    data = {}
    for line in pipe_file:
        tokens = line.strip().split('|')
        data[tokens[0]] = tokens[1:]

    return data


if __name__ == "__main__":
    # Load unpublished case data
    unpublished_data = load_pipe_file(os.path.join("data", "cases_published.csv"))
    published_data = load_pipe_file(os.path.join("data", "cases_unpublished.csv"))
    scotus_data = load_pipe_file(os.path.join("data", "cases_scotus.csv"))

    #  Load district sentence files
    district_instance_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                                    "district_ws_instances.csv"),
                                       'r', 'utf8')
    district_output_file = codecs.open('district_data.csv', 'w', 'utf8')

    for line in district_instance_file:
        tokens = line.strip().split("\t")
        if tokens[0] in unpublished_data:
            tokens.extend(unpublished_data[tokens[0]])
        elif tokens[0] in published_data:
            tokens.extend(published_data[tokens[0]])
        else:
            print(tokens[0])
            continue
        district_output_file.write("\t".join(tokens) + "\n")

    district_output_file.close()

    #  Load sentence files
    circuit_instance_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                                    "circuit_ws_instances.csv"),
                                       'r', 'utf8')
    circuit_output_file = codecs.open('circuit_data.csv', 'w', 'utf8')

    for line in circuit_instance_file:
        tokens = line.strip().split("\t")
        if tokens[0] in unpublished_data:
            tokens.extend(unpublished_data[tokens[0]])
        elif tokens[0] in published_data:
            tokens.extend(published_data[tokens[0]])
        else:
            print(tokens[0])
            continue
        circuit_output_file.write("\t".join(tokens) + "\n")

    circuit_output_file.close()

    #  Load sentence files
    scotus_instance_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                                    "scotus_ws_instances.csv"),
                                       'r', 'utf8')
    scotus_output_file = codecs.open('scotus_data.csv', 'w', 'utf8')

    for line in scotus_instance_file:
        tokens = line.strip().split("\t")
        if tokens[0] in scotus_data:
            tokens.extend(scotus_data[tokens[0]])
        else:
            print(tokens[0])
            continue
        scotus_output_file.write("\t".join(tokens) + "\n")

    scotus_output_file.close()