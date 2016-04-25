import datetime
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from pandas import DataFrame
import numpy as np

from worker.extractorbow import ExtractorBow
from worker.extractordocstats import ExtractorDocStats


class Classifier:
    def __init__(self, model):
        self.bow = model.bow
        self.doc_stats = model.doc_stats
        self.confidence = model.confidence
#        self.svc_kernal = model.svc_kernal
#        self.svc_c = model.svc_c
#        self.svc_tol = model.svc_tol
#        self.svc_classifier = model.svc_classifier
        self.random_forest_classifier = model.random_forest_classifier
        self.forest_tree_count = model.forest_tree_count

        if self.bow:
            self.bow_extractor = ExtractorBow(model)
            self.bow_extractor.transform(set_type='train', documents=model.docset)
        if self.doc_stats:
            self.doc_stats_extractor = ExtractorDocStats()
            self.doc_stats_extractor.transform(set_type='train', documents=model.docset)

        # combine all the sets
        if model.bow or model.doc_stats:
            self.combine_dataframe()
        else:
            raise ('There was no dataset selected')


    def train_classifier(self):
        print('Training classifier')

        # if self.svc_classifier:
        #     self.clf = SVC(kernel=self.svc_kernal, C=self.svc_c, cache_size=2000, probability=True,
        #                    tol=self.svc_tol)
        if self.random_forest_classifier:
            self.clf = RandomForestClassifier(n_estimators=self.forest_tree_count)

        self.clf = self.clf.fit(self.data_set, self.data_set_labels)


    def combine_dataframe(self):
        self.data_set = None  # The training matrix
        self.data_set_values = None  # The training targets

        first = True

        for type in ['BOW', 'doc_stats', 'LDA']:
            if type == 'BOW' and self.bow:
                current_data_set = self.bow_extractor
            elif type == 'doc_stats' and self.doc_stats:
                current_data_set = self.doc_stats_extractor
            else:
                continue

            if first:
                self.data_set = current_data_set.data_features
                self.data_set_labels = current_data_set.data_labels
                first = False
            else:
                self.data_set = np.append(self.data_set, current_data_set.data_features, axis=1)

    # documents can be a Document or DocSet object
    def predict(self, documents):
        if documents is None:
            raise ('You have to pass a document or document_set to predict.')

        # Get all of the required features
        if self.bow:
            self.bow_extractor.transform(set_type='test', documents=documents)
        if self.doc_stats:
            self.doc_stats_extractor.transform(set_type='test', documents=documents)

        # Combine the different document features
        if self.bow or self.doc_stats:
            self.combine_dataframe()
        else:
            raise ('There was no dataset selected')

        # Predict the result
        # if self.svc_classifier:
        #     self.result = self.clf.predict(self.data_set)
        if self.random_forest_classifier:
            self.result = self.clf.predict_proba(self.data_set)


    def print_summary(self):
        # if self.svc_classifier:
        #     self.print_SVM_summary()
        if self.random_forest_classifier:
            self.print_forests_summary()


    def print_SVM_summary(self):
        # Print the results
        correct = 0
        wrong = 0

        for position in range(len(self.result)):
            if self.result[position] == self.data_set_labels[position]:
                correct += 1
            else:
                wrong += 1

        print(correct / (correct + wrong))

    def print_forests_single_doc(self, detailed=False):
        highest_score = 0
        highest_doc_type = ''
        doc_type_scores = {}
        for doc_type_index in range(len(self.clf.classes_)):
            doc_type_scores[self.clf.classes_[doc_type_index]] = self.result[0][doc_type_index]

            if self.result[0][doc_type_index] > highest_score:
                highest_score = self.result[0][doc_type_index]
                highest_doc_type = self.clf.classes_[doc_type_index]

        print('DocType: %s' % highest_doc_type)
        print('Confidence: %s' % highest_score)
        if detailed:
            print()
            print(doc_type_scores)
        print()

    def get_forests_single_doc(self, detailed=False):
        highest_score = 0
        highest_doc_type = ''
        doc_type_scores = {}
        for doc_type_index in range(len(self.clf.classes_)):
            doc_type_scores[self.clf.classes_[doc_type_index]] = self.result[0][doc_type_index]

            if self.result[0][doc_type_index] > highest_score:
                highest_score = self.result[0][doc_type_index]
                highest_doc_type = self.clf.classes_[doc_type_index]

        if detailed:
            return {'doc_type': highest_doc_type, 'confidence': highest_score, 'details': doc_type_scores}
        else:
            return {'doc_type': highest_doc_type, 'confidence': highest_score}



    def print_forests_summary(self):
        # Create result set
        results = {}
        totals = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
        output = []
        for row in range(len(self.result)):
            result_row = {}
            highest_score = 0
            highest_doc_type = ''
            for doc_type_index in range(len(self.clf.classes_)):
                result_row[self.clf.classes_[doc_type_index]] = self.result[row][doc_type_index]

                if self.result[row][doc_type_index] > highest_score:
                    highest_score = self.result[row][doc_type_index]
                    highest_doc_type = self.clf.classes_[doc_type_index]

            result_row['actual_doc_type'] = self.data_set_labels[row]
            result_row['predicted_doc_type'] = highest_doc_type
            result_row['correct'] = self.data_set_labels[row] == highest_doc_type
            result_row['predicted_percentage'] = highest_score
            result_row['filename'] = self.data_set_labels[row]

            if result_row['actual_doc_type'] not in results:
                results[result_row['actual_doc_type']] = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}

            if result_row['actual_doc_type'] == result_row['predicted_doc_type']:
                if result_row['predicted_percentage'] > self.confidence:
                    totals['tp'] += 1
                    results[result_row['actual_doc_type']]['tp'] += 1
                else:
                    totals['fn'] += 1
                    results[result_row['actual_doc_type']]['fn'] += 1
            else:
                if result_row['predicted_percentage'] > self.confidence:
                    totals['fp'] += 1
                    results[result_row['actual_doc_type']]['fp'] += 1
                else:
                    totals['tn'] += 1
                    results[result_row['actual_doc_type']]['tn'] += 1

            output.append(result_row)

        output = DataFrame(output)

        # Get time for outputs
        i = datetime.datetime.now()
        now = i.strftime('%Y-%m-%d %H-%M-%S')

        # Create output folder
        if not os.path.exists('log/classifier'):
            os.makedirs('log/classifier')

        output.to_csv('log/classifier/%s - test_results.csv' % now)

        # Print the results
        total_tested = len(output['correct'])

        for key, value in results.items():
            total = value['tp'] + value['fn'] + value['tn'] + value['fp']
            print('%s - %s/%s/%s/%s - (%0.1f%%/%0.1f%%)' % (key, value['tp'], value['fn'], value['tn'], value['fp'],
                                                            value['tp'] / total * 100, value['fp'] / total * 100))

        print('Total - %s/%s/%s/%s - (%0.1f%%/%0.1f%%)\n' % (totals['tp'], totals['fn'], totals['tn'], totals['fp'],
                                                           totals['tp'] / total_tested * 100,
                                                           totals['fp'] / total_tested * 100))

if __name__ == '__main__':
    pass
