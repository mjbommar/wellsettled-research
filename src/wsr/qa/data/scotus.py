# -*- coding: utf-8 -*-
"""
@date 2014-05-24
@author Michael J Bommarito II <michael@bommaritollc.com>

Test the SCOTUS data QA.
"""

# Standard imports
import codecs
import csv
import os

# WSR imports
from wsr.data.scotus import SCOTUS, read_xml_document, read_xml_date,\
    get_text_lxml, read_xml_citation_list, read_xml_opinion
from wsr.config import QA_SCOTUS_PATH
import random
from wsr.process.tokenize import sentence_tokenizer
from wsr.process.parse import sentence_parser


def write_test_report(file_name, outcome_data, header=[]):
    """
    Output a test report to the file name.
    """
    # Open the file
    with codecs.open(file_name, 'w', 'utf8') as csv_file:
        # Create the writer
        csv_writer = csv.writer(csv_file, dialect=csv.excel)
        
        # Output header and rows
        csv_writer.writerow(header)
        for row in outcome_data:
            try:
                csv_writer.writerow(row)
            except UnicodeDecodeError:
                csv_writer.writerow(row[0])


def write_test_report_tab(file_name, outcome_data, header=[]):
    """
    Output a test report to the file name as a TDF, which is cleaner
    for some sloppy text data.
    """
    # Open the file
    with codecs.open(file_name, 'w', 'utf8') as tab_file:
        # Output header and rows
        tab_file.write("{0}\n".format("\t".join(header)))
        for row in outcome_data:
            try:
                tab_file.write("{0}\n".format("\t".join(row).encode("utf8")))
            except UnicodeDecodeError:
                tab_file.write("{0}\n".format(row[0]))


def test_citation_coverage(scotus):
    """
    Test the coverage of the citation parsing across all SCOTUS documents.
    """
    # Store outcomes
    outcome_data = []
    
    # Iterate over documents
    for file_name in scotus.scotus_document_list:
        # Get the document
        doc = read_xml_document(scotus.read_document(file_name))
        if doc:
            try:
                raw_value = get_text_lxml(doc.xpath(".//citation_line")[0])
                raw_value = raw_value.strip().replace("\r", "").replace("\n", "")
            except IndexError:
                raw_value = ""
        
            parsed_value = "; ".join(read_xml_citation_list(doc))
        else:
            raw_value = None
            parsed_value = None
        
        # Append to the outcome data
        outcome_data.append((os.path.basename(file_name),
                             raw_value, parsed_value))

    return outcome_data


def test_date_coverage(scotus):
    """
    Test the coverage of the date parsing across all SCOTUS documents.
    """
    # Store outcomes
    outcome_data = []
    
    # Iterate over documents
    for file_name in scotus.scotus_document_list:
        # Get the document
        doc = read_xml_document(scotus.read_document(file_name))
        if doc:
            raw_value = get_text_lxml(doc.xpath(".//date")[0])
            raw_value = raw_value.strip().replace("\r", "").replace("\n", "")
            parsed_value = read_xml_date(doc)
        else:
            raw_value = None
            parsed_value = None
        
        # Append to the outcome data
        outcome_data.append((os.path.basename(file_name),
                             raw_value, parsed_value))

    return outcome_data

def test_sentence_tokenizer(scotus):
    """
    Test handling of sentence tokenization across a random subset of 
    SCOTUS documents.
    """
    # Choose the document sample size
    num_sample = min(100, len(scotus.scotus_document_list))
    
    # Get the shuffled document list with hard-coded seed
    document_list = scotus.scotus_document_list
    random.seed(0)
    random.shuffle(document_list)
    
    # Store sentences
    sentence_list = []
    
    # Create the SCOTUS 
    for file_name in scotus.scotus_document_list[0:num_sample]:
        # Get the document and tokenize
        doc = read_xml_document(scotus.read_document(file_name)) 
        file_sentences = [s.strip().replace("\n", "").replace("\r", "") \
                             for s in sentence_tokenizer\
                             .sentences_from_text(read_xml_opinion(doc))]
        sentence_list.extend([(file_name, s) for s in file_sentences])
    
    return sentence_list 


def test_sentence_parser(scotus):
    """
    Test handling of sentence parsing across a random subset of 
    SCOTUS documents.
    """
    # Choose the document sample size
    num_sample = min(20, len(scotus.scotus_document_list))
    
    # Get the shuffled document list with hard-coded seed
    document_list = scotus.scotus_document_list
    random.seed(0)
    random.shuffle(document_list)
    
    # Store sentences
    tree_list = []
    
    # Create the SCOTUS 
    for file_name in scotus.scotus_document_list[0:num_sample]:
        # Get the document and tokenize
        doc = read_xml_document(scotus.read_document(file_name)) 
        file_sentences = [s.strip().replace("\n", "").replace("\r", "") \
                             for s in sentence_tokenizer\
                             .sentences_from_text(read_xml_opinion(doc))]
        
        #TODO: Decide if we want to batch parse with more RAM.
        num_sentences = min(20, len(file_sentences))
        random.seed(0)
        random.shuffle(file_sentences)
        file_trees = sentence_parser.raw_parse_sents(\
                                             file_sentences[0:num_sentences])
        tree_list.extend([(file_name, str(t)) for t in file_trees])
    
    return tree_list 


if __name__ == "__main__":
    # Create the SCOTUS dataset
    s = SCOTUS()

    '''
    # Test the date coverage
    print("Generating QA coverage for: date")
    date_outcome = test_date_coverage(s)
    write_test_report(os.path.join(QA_SCOTUS_PATH, "date.csv"),
                      date_outcome,
                      ["file", "raw", "parsed"])

    # Test the citation coverage
    print("Generating QA coverage for: citation")
    cite_outcome = test_citation_coverage(s)
    write_test_report(os.path.join(QA_SCOTUS_PATH, "citation.csv"),
                      cite_outcome,
                      ["file", "raw", "parsed"])
    
    # Test the sentence tokenization coverage
    print("Generating QA coverage for: sentence tokenization")
    sent_token_outcome = test_sentence_tokenizer(s)
    write_test_report_tab(os.path.join(QA_SCOTUS_PATH, 
                                       "sentence_tokenization.csv"),
                      sent_token_outcome,
                      ["file", "parsed"])
    '''
     
    # Test the sentence parsing coverage
    print("Generating QA coverage for: sentence parsing")
    sent_parse_outcome = test_sentence_parser(s)
    write_test_report_tab(os.path.join(QA_SCOTUS_PATH, 
                                       "sentence_parsing.csv"),
                      sent_parse_outcome,
                      ["file", "parsed"])
    