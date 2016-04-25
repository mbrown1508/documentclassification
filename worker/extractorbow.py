import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer
from document.models import Document
from docset.models import DocSet


class ExtractorBow:
    def __init__(self, model):
        if model.tfidf_vectoriser:
            self.vectorizer = TfidfVectorizer(analyzer=model.vec_analyzer,
                                              min_df=model.vec_min_df,
                                              tokenizer=None,
                                              preprocessor=None,
                                              stop_words=model.vec_stop_words,
                                              max_features=model.vec_max_features,
                                              ngram_range=(model.vec_ngram_range_min, model.vec_ngram_range_max),
                                              strip_accents=model.vec_strip_accents)
        else:
            self.vectorizer = CountVectorizer(analyzer=model.vec_analyzer,
                                              min_df=model.vec_min_df,
                                              tokenizer=None,
                                              preprocessor=None,
                                              stop_words=model.vec_stop_words,
                                              max_features=model.vec_max_features,
                                              ngram_range=(model.vec_ngram_range_min, model.vec_ngram_range_max),
                                              strip_accents=model.vec_strip_accents)


    # This should only be used for training
    def transform(self, set_type, documents):
        doc_set = []

        if type(documents) is Document:
            doc_set.append({'doc_type': documents.doc_type,
                            'filename': documents.filename,
                            'string': documents.clean_string})

        elif type(documents) is DocSet:
            for document in documents.train_documents.all() if set_type == 'train' else documents.test_documents.all():
                if document.clean_string is not None:
                    doc_set.append({'doc_type': document.doc_type,
                                    'filename': document.filename,
                                    'string': document.clean_string})

        else:
            raise ('You need to set document or docset!')

        doc_set = pd.DataFrame(doc_set)

        if set_type == 'train':
            self.data_features = self.vectorizer.fit_transform(doc_set['string'])
        else:
            self.data_features = self.vectorizer.transform(doc_set['string'])

        # This is the standard data set for a Extractor
        self.data_features = self.data_features.toarray()
        self.data_labels = doc_set['doc_type']
