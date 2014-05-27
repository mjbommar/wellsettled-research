# Standard imports
import codecs
import difflib
import os
import string

# WSR imports
from wsr.data.scotus import SCOTUS, read_xml_document, read_xml_opinion
from wsr.config import SCRATCH_PATH
from wsr.process.tokenize import sentence_tokenizer, word_tokenizer,\
    english_stopwords
from wsr.process.parse import sentence_parser
from wsr.process.stem import stemmer

# Define target sentence
target_sentence = "federal court may consider collateral issues after an action is no longer pending"


def process_sentence(sentence):
    """Process a sentence by tokenizing, removing stopwords, and stemming.
    """
    # Tokenize and remove stopwords
    tokens = [word.strip(string.whitespace).strip(string.punctuation) \
                      for word in word_tokenizer.tokenize(sentence)]
    nsw_tokens = [token for token in tokens if token \
                            not in english_stopwords]

    # Stem the sentence.
    stems = [stemmer.stem(token).lower() for token in nsw_tokens]

    return stems


if __name__ == "__main__":
    # Load the dataset
    scotus = SCOTUS()

    # Store the sentence list
    ws_list = []

    # Build the target stems
    target_stems = process_sentence(target_sentence)
    print(target_stems)

    # Iterate over documents
    for file_name in scotus.scotus_document_list:
        # Get the XML document and sentence list
        try:
            doc = read_xml_document(scotus.read_document(file_name))
            sentence_list = [s.strip().replace("\n", "").replace("\r", "") \
                             for s in sentence_tokenizer\
                             .sentences_from_text(read_xml_opinion(doc))]
        except Exception:
            continue

        # Iterate over sentences and find matches
        for sentence in sentence_list:
            # Compare sentence stems and target stems
            sentence_stems = process_sentence(sentence)
            s = difflib.SequenceMatcher(None, target_stems, sentence_stems)
            match = s.find_longest_match(0, len(target_stems), 
                                 0, len(sentence_stems))
            if match.size > len(target_stems) / 2:
                print(file_name)
                print(match)
                print(target_stems[match.a:(match.a+match.size)])
            
            