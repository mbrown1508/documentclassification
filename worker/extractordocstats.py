import numpy as np
import pandas as pd
from document.models import Document
from docset.models import DocSet


class ExtractorDocStats:
    def __init__(self):
        # Most of the processing is done by the document class.
        # This class is here just to format the data for the classifier.
        pass

    def transform(self, set_type, documents):
        basic_info = []
        doc_stats = []

        if type(documents) is Document:
            basic_info.append({'doc_type': documents.doc_type, 'filename': documents.filename})
            doc_stats.append([documents.page_count,
                              documents.word_count,
                              documents.unique_word_count,
                              documents.char_count,
                              documents.upper_case_percent,
                              documents.lower_case_percent,
                              documents.number_percent,
                              documents.symbol_percent,
                              documents.space_percent])


        elif type(documents) is DocSet:
            for document in documents.train_documents.all() if set_type == 'train' else documents.test_documents.all():
                if document.clean_string is not None:
                    basic_info.append({'doc_type': document.doc_type, 'filename': document.filename})
                    doc_stats.append([document.page_count,
                                      document.word_count,
                                      document.unique_word_count,
                                      document.char_count,
                                      document.upper_case_percent,
                                      document.lower_case_percent,
                                      document.number_percent,
                                      document.symbol_percent,
                                      document.space_percent])

        basic_info = pd.DataFrame(basic_info)

        # This is the standard data set for a Extractor
        self.data_features = np.array(doc_stats)
        self.data_features = np.reshape(self.data_features, (-1, 9))
        self.data_labels = basic_info['doc_type']
