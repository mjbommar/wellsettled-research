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
    get_text_lxml, read_xml_citation_list
from wsr.config import QA_SCOTUS_PATH


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


def test_citation_coverage(scotus):
    """
    Test the coverage of the citation parsing across all SCOTUS documents.
    """
    # Store outcomes
    outcome_data = []
    
    # Create the SCOTUS scotus = SCOTUS()
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
    
    # Create the SCOTUS scotus = SCOTUS()
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


if __name__ == "__main__":
    # Create the SCOTUS dataset
    s = SCOTUS()

    # Test the date coverage
    print("Generating QA coverage for: date")
    date_outcome = test_date_coverage(s)
    write_test_report(os.path.join(QA_SCOTUS_PATH, "date.csv"),
                      date_outcome,
                      ["file", "raw", "parsed"])

    # Test the date coverage
    print("Generating QA coverage for: citation")
    cite_outcome = test_citation_coverage(s)
    write_test_report(os.path.join(QA_SCOTUS_PATH, "citation.csv"),
                      cite_outcome,
                      ["file", "raw", "parsed"])
    