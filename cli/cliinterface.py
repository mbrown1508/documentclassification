__author__ = 'Matthew'
import os
import re

from time import sleep

from cli.helperclasses.climethods import *
import json
import requests


class CliInterface:

    def __init__(self):
        self.application_id = None
        self.api_url = 'http://127.0.0.1:8000'
        self.main()

    def main(self):

        while True:

            options = ['Create Application',
                       'Select Application',
                       'Add Document - json',
                       'Add Document Folder',
                       'Create DocSet',
                       'Create Model',
                       'Classify Document']

            user_selection = get_selection('\nTo get started select a option:', options)[0]

            # Run selection
            if user_selection == 1:
                self.create_application()
            elif user_selection == 2:
                self.select_application()
            elif user_selection == 3:
                self.add_document()
            elif user_selection == 4:
                self.add_document_folder()
            elif user_selection == 5:
                self.create_docset()
            elif user_selection == 6:
                self.create_model()
            elif user_selection == 7:
                self.classify_document()
            else:
                print('\nRunning', user_selection, '\n')

    def create_application(self):
        print('\nCreate Application')
        application_name = input('Please enter the application name: ')

        data = {'name': application_name}
        result = self.post('application', data)

        if 'name' in result and 'url' in result:
            self.application_id = result['id']
            print('Created')
        else:
            print('Error')
            print(result)

    def select_application(self):
        print('\nSelect Application')
        result = self.get('application', optional='page_size=100')

        if 'results' in result:
            names = [i['name'] for i in result['results']]
            options = [[i['id'], i['name']] for i in result['results']]
            selection = get_selection('Select an available application', names)[0]

            self.application_id = options[selection-1][0]

            print('Selected %s' % options[selection-1][1])

    def add_document(self):
        print('\nAdd Document - json')
        document_path = input('Please enter the document path: ')
        doc_type = input('Please enter the doc type: ')
        sub_doc_type = input('Please enter the sub doc type: ')
        filename = os.path.basename(document_path)
        ocr_result = self.open_json(document_path)

        data = {'application_id': self.application_id,
                'filename': filename,
                'ocr_result': json.dumps(ocr_result),
                'doc_type': doc_type,
                'sub_doc_type': sub_doc_type}

        result = self.synchronous('document', data)

        if "result" in result:
            print('Created - %s' % result['result'])
        else:
            print('Error')
            print(result)

    def add_document_folder(self):
        print('\nAdd Document Folder')
        folder_path = input('Please enter the document path: ')
        run_sub_doc = yes_no_question('Is there sub-docs?', False)

        tasks = []

        doc_dir = re.search(r"([^/\\]+$)", folder_path).group(1)

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                current_file_location = os.path.join(root, file)
                current_filename = os.path.split(current_file_location)[1]

                if os.path.splitext(current_filename)[1] == '.json':
                    # Get the doc_type and sub_doc_type
                    pattern = doc_dir + r"[/\\]{0,1}([^/\\]+)[\\/]([^/\\]+)[\\/]"
                    match = re.search(pattern, current_file_location)

                    if match and run_sub_doc:
                        doc_type = match.group(1)
                        sub_doc_type = match.group(2)
                        filename = os.path.basename(current_file_location)
                        ocr_result = self.open_json(current_file_location)
                        data = {'application_id': self.application_id,
                                'filename': filename,
                                'ocr_result': json.dumps(ocr_result),
                                'doc_type': doc_type,
                                'sub_doc_type': sub_doc_type}

                        result = self.post('document', data)

                        if 'url' not in result and 'task' not in result:
                            print('Error')
                            print(result)

                        tasks.append(result['task'])

                    else:
                        pattern = doc_dir + r"[/\\]{0,1}([^/\\]+)[\\/]"
                        match = re.search(pattern, current_file_location)
                        if match:
                            doc_type = match.group(1)
                            sub_doc_type = None
                            filename = os.path.basename(current_file_location)
                            ocr_result = self.open_json(current_file_location)
                            data = {'application_id': self.application_id,
                                    'filename': filename,
                                    'ocr_result': json.dumps(ocr_result),
                                    'doc_type': doc_type,
                                    'sub_doc_type': sub_doc_type}

                            result = self.post('document', data)

                            if 'url' not in result and 'task' not in result:
                                print('Error')
                                print(result)

                            tasks.append(result['task'])

        counter = 0
        for task_url in tasks:
            waiting = True
            while waiting:
                result = self.get(url=task_url)
                if 'completed' in result and result['completed'] is True:
                    counter += 1
                    waiting = False
                else:
                    sleep(1)
        print('%s Documents Added!' % counter)

    def create_docset(self):
        print('\nAsync Create DocSet')
        docset_name = input('Please enter a docset name: ')
        train_percentage = get_number('Percentage of documents to be used in the train set', 70, 1, 99)
        test_percentage = 100 - train_percentage

        data = {'application_id': self.application_id, 'name': docset_name,
                'train_percentage': train_percentage, 'test_percentage': test_percentage}
        self.synchronous('docset', data)

    def create_model(self):
        print('\nCreate Model')
        # Vars not currently set
        vec_stop_words = 'english'
        vec_analyzer = 'word'
        svc_classifier = False
        vec_strip_accents = 'ascii'

        # Get user input
        model_name = input('Please enter a model name: ')
        random_forest_classifier = yes_no_question('Use Random Forests Classifier?', True)
        forest_tree_count = get_number('How many trees?', 2000, 10, 10000)
        confidence = get_number('Initial confidence?', 0.0, 0.0, 1.0, True)
        doc_stats = yes_no_question('Use Doc Stats?', True)
        bow = yes_no_question('Use BOW?', True)
        if bow:
            tfidf_vectoriser = yes_no_question('Use tfidf?', True)
            bow_vectoriser = False if tfidf_vectoriser == True else True
        else:
            tfidf_vectoriser = None
            bow_vectoriser = None
        vec_min_df = get_number('Minimum df?', 0.001, 0.000001, 10.0, True)
        vec_max_features = get_number('Number of features?', 10000, 1, 100000)
        vec_ngram_range_min = get_number('Min ngram size?', 1, 1, 20)
        vec_ngram_range_max = get_number('Max ngram size?', 3, 1, 50)

        # Choose a document set
        docset_id = self.choose_docset_id()

        data = {'application_id': self.application_id,
                'name': model_name,
                'random_forest_classifier': random_forest_classifier,
                'forest_tree_count': forest_tree_count,
                'confidence': confidence,
                'svc_classifier': svc_classifier,
                'doc_stats': doc_stats,
                'bow': bow,
                'tfidf_vectoriser': tfidf_vectoriser,
                'bow_vectoriser': bow_vectoriser,
                'vec_analyzer': vec_analyzer,
                'vec_min_df': vec_min_df,
                'vec_stop_words': vec_stop_words,
                'vec_max_features': vec_max_features,
                'vec_ngram_range_min': vec_ngram_range_min,
                'vec_ngram_range_max': vec_ngram_range_max,
                'vec_strip_accents': vec_strip_accents,
                'docset_id': docset_id}
        self.synchronous('classifier', data)

    def classify_document(self):
        print('\nClassify Document')
        document_path = input('Please enter the location of the document: ')
        ocr_result = self.open_json(document_path)
        filename = os.path.basename(document_path)

        data = {'application_id': self.application_id,
                'filename': filename,
                'ocr_result': json.dumps(ocr_result)}

        # Get ocr result
        result = self.synchronous('classify', data)

        if "result" in result:
            classify = self.get(url=result['classify'])
            print('DocType: %s' % classify['classification'])
            print('Confidence: %s' % classify['confidence'])
            print()
        else:
            print('Error')
            print(result)

    def choose_docset_id(self):
        print('\nSelect Application')
        optional = ['application=' + str(self.application_id),
                    'page_size=100']
        result = self.get('docset', optional=optional)

        if 'results' in result:
            names = [i['name'] for i in result['results']]
            options = [[i['id'], i['name']] for i in result['results']]
            selection = get_selection('Select an available docset', names)[0]

            return options[selection-1][0]

    def open_json(self, filename):
        return json.loads(open(filename, "rb").read().decode(encoding='UTF-8'))

    def post(self, type, data):
        response = requests.post(self.api_url + '/' + type + '/', data)
        response = response.json()
        return response

    def get(self, type=None, url=None, optional=None):
        if url is None:
            get_url = self.api_url + '/' + type + '/'
        elif type is None:
            get_url = url
        else:
            raise Exception('Get requires type or url to be passed.')

        if optional is not None:
            if isinstance(optional, str):
                optional = [optional]
            get_url += '?' + '&'.join(optional)

        return requests.get(get_url).json()

    def synchronous(self, type, data):
        result = self.post(type, data)

        if 'url' in result and 'task' in result:
            print('Request Posted')
        else:
            print('Error')
            print(result)

        task_url = result['task']

        waiting = True
        while waiting:
            result = self.get(url=task_url)
            if 'completed' in result and result['completed'] is True:
                return result

            sleep(1)