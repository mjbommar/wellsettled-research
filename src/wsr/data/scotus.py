# -*- coding: utf-8 -*-
"""
The :mod:`wsr.data.scotus` handles reading and pre-processing the Supreme
Court dataset to extract opinion text.

Author: Michael J Bommarito II <michael@bommaritollc.com>
Date: 2014-05-24 
"""

# WSR imports
from wsr.config import SCOTUS_FILE_NAME

# Standard imports
import dateutil.parser
import lxml.etree
import zipfile


def get_text(element):
    '''
    Get text from element for references.
    '''
    # Get initial text
    text =  ' '.join([t.strip() for t in element.xpath("//text()")])
    text = text.replace('  ', ' ')
    return text


def get_text_lxml(element):
    '''
    Get text from element for references.
    '''
    # Get initial text
    return lxml.etree.tostring(element, method="text", encoding="utf8")


def read_xml_document(file_buffer):
    """
    Read the case XML document.
    """
    # Create the XML document
    try:
        xml_doc = lxml.etree.fromstring(file_buffer)
        return xml_doc
    except Exception, e:
        return None

def read_xml_docket(xml_doc):
    """
    Read the docket name from the XML document.
    """
    # Parse only the opinion_text elements
    for element in list(xml_doc):
        if element.tag == "docket":
            return get_text(element)

    return ""


def read_xml_date(xml_doc):
    """
    Read the date from the XML document.
    """
    # Parse only the opinion_text elements
    for element in list(xml_doc):
        if element.tag == "date":
            # Get the text
            date_text = get_text_lxml(element)

            try:
                date_text = date_text.lower().strip().strip(".")
                return dateutil.parser.parse(date_text).date()
            except ValueError:
                return None
            except TypeError:
                return None
        
    return None


def read_xml_citation_list(xml_doc):
    """
    Read the citation name from the XML document.
    """
    # Store citation list
    citation_list = []
    
    # Parse only the opinion_text elements
    for element in list(xml_doc):
        if element.tag == "opinion_text":
            return citation_list
        elif element.tag in ["reporter_caption", "citation_line"]:
            # Get the <citation> tags
            citation_tag_list = element.xpath(".//citation")
            for citation_tag in citation_tag_list:
                # Process text
                citation_text = get_text_lxml(citation_tag)
                citation_text = citation_text.strip()
                citation_list.append(citation_text)

    return citation_list


def read_xml_opinion(xml_doc):
    """
    Read the opinion text section of an XML document.
    """
    
    # Parse only the opinion_text elements
    for element in list(xml_doc):
        if element.tag == "opinion_text":
            return get_text(element)
    
    return ""


class SCOTUS(object):
    """
    SCOTUS data class.
    """

    def load_zip_data(self):
        """
        Load ZIP data.
        """
        # Load the list of all files
        self.scotus_file_list = self.scotus_zip_file.namelist()
        
        # Identify the list of documents that we'd actually read.
        self.scotus_document_list = sorted([file_name for file_name in \
                                        self.scotus_file_list \
                                        if file_name.lower().endswith('xml')])

    def read_document(self, file_name):
        """
        Read a document from within the ZIP file.
        """
        # Return the buffer
        return self.scotus_zip_file.read(file_name)

    def __init__(self):
        """
        Constructor
        """

        # Set SCOTUS file path
        self.scotus_file_path = SCOTUS_FILE_NAME

        # SCOTUS ZIP file
        self.scotus_zip_file = zipfile.ZipFile(self.scotus_file_path)

        # SCOTUS ZIP file list
        self.scotus_file_list = []

        # SCOTUS ZIP document list
        self.scotus_document_list = []

        # Load ZIP data
        self.load_zip_data()


if __name__ == "__main__":
    scotus = SCOTUS()
    for file_name in scotus.scotus_document_list[0:50]:
        # Print the XML doc
        print(file_name)
        doc = read_xml_document(scotus.read_document(file_name))
        print(read_xml_citation_list(doc))
