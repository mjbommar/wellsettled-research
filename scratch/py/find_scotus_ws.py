# Standard imports
import codecs
import os

# WSR imports
from wsr.data.scotus import SCOTUS, read_xml_document, read_xml_opinion
from wsr.config import SCRATCH_PATH
from wsr.process.tokenize import sentence_tokenizer
from wsr.process.parse import sentence_parser


if __name__ == "__main__":
    # Load the dataset
    scotus = SCOTUS()

    # Store the sentence list
    ws_list = []

    # Output to file
    sentence_file = codecs.open(os.path.join(SCRATCH_PATH, "results",
                                             "sentence_list.csv"),
                                'w', 'utf8')

    # Iterate over documents
    for file_name in scotus.scotus_document_list[0:100]:
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
            if "-established" in sentence.lower():
                ws_list.append((os.path.basename(file_name),
                                True,
                                sentence))
            elif "-settled" in sentence.lower():
                ws_list.append((os.path.basename(file_name),
                                True,
                                sentence))
            elif "well established" in sentence.lower():
                ws_list.append((os.path.basename(file_name),
                                True,
                                sentence))
            elif "well settled" in sentence.lower():
                ws_list.append((os.path.basename(file_name),
                                True,
                                sentence))
            else:
                pass

    # Write out sentences with parse tree
    for ws in ws_list:
        try:
            # Parse sentence
            parse_sentence = sentence_parser.raw_parse(ws[2])
            
            # Write
            sentence_file.write('{0}\t{1}\t{2}\t{3}\n'.format(ws[0], ws[1],
                                                ws[2].replace("\n", " ")\
                                                    .replace("\t", " "),
                                                str(parse_sentence)))
        except UnicodeError:
            # Write
            sentence_file.write('{0}\n'.format(ws[0]))
            continue

    # Close file
    sentence_file.close()

