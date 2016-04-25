from django.db import models
import hashlib
import json
import string

from worker.helperclasses.dictionary import Dictionary

class Document(models.Model):
    app_label = 'document'

    filename = models.CharField(max_length=256)
    ocr_result = models.TextField(null=True)
    string = models.TextField(null=True)
    doc_type = models.CharField(max_length=100, null=True)
    sub_doc_type = models.CharField(max_length=100, null=True)

    classification = models.CharField(max_length=100, null=True)
    confidence = models.IntegerField(null=True)

    application = models.ForeignKey('application.Application')


    # These values are generated by the create_values method
    hash = models.CharField(max_length=36, null=True)
    raw_string = models.TextField(null=True)
    clean_string = models.TextField(null=True)

    page_count = models.IntegerField(null=True)
    word_count = models.IntegerField(null=True)
    unique_word_count = models.IntegerField(null=True)
    char_count = models.IntegerField(null=True)

    upper_case_percent = models.FloatField(null=True)
    lower_case_percent = models.FloatField(null=True)
    number_percent = models.FloatField(null=True)
    symbol_percent = models.FloatField(null=True)
    space_percent = models.FloatField(null=True)


    def create_values(self, dictionary):
        self.page_count = 0

        # Load Document
        if self.string is not None:
            self.raw_string = str(self.string.encode('utf-8'))
        elif self.ocr_result is not None:
            self.extract_string_from_ocr_result(self.ocr_result)
        else:
            raise Exception('You need to pass string or ocr_result to the Document object.')

        # Setup dictionary
        if dictionary is None:
            self.dictionary = Dictionary()
        else:
            self.dictionary = dictionary

        self.clean_string = self.dictionary.cleanup_string(self.raw_string)
        words = self.dictionary.return_words(self.clean_string)
        self.word_count = self.dictionary.count_words(words)
        self.unique_word_count = len(words)

        self.calculate_char_percents()

        self.raw_string = self.raw_string.encode('utf-8')
        self.hash_string()

    ### Following Methods using during init ###

    def hash_string(self):
        hash_object = hashlib.sha512(self.raw_string)
        self.hash = hash_object.hexdigest()

    def extract_string_from_ocr_result(self, ocr_result):
        ocr_result = json.loads(ocr_result)
        if ocr_result is not None:
            # Get String
            self.raw_string = ''

            if 'pages' not in ocr_result:
                return None

            for page in ocr_result['pages']:
                self.raw_string += ' ' + page['result']

            self.page_count = len(ocr_result['pages'])
        else:
            self.raw_string = ''
            self.page_count = 0

    def calculate_char_percents(self):
        UPPER_CASE_SET = set(string.ascii_uppercase)
        LOWER_CASE_SET = set(string.ascii_lowercase)
        NUMBERS_SET = set(string.digits)

        upper_case_count = 0
        lower_case_count = 0
        numbers_count = 0
        symbols_count = 0
        space_count = 0

        for letter in self.raw_string:
            if letter in UPPER_CASE_SET:
                upper_case_count += 1
            elif letter in LOWER_CASE_SET:
                lower_case_count += 1
            elif letter in NUMBERS_SET:
                numbers_count += 1
            elif letter == ' ':
                space_count += 1
            else:
                symbols_count += 1

        self.char_count = len(self.raw_string)

        if self.char_count != 0:
            self.upper_case_percent = upper_case_count / self.char_count
            self.lower_case_percent = lower_case_count / self.char_count
            self.number_percent = numbers_count / self.char_count
            self.symbol_percent = symbols_count / self.char_count
            self.space_percent = 1 - (
                self.upper_case_percent + self.lower_case_percent + self.number_percent + self.symbol_percent)
        else:
            self.upper_case_percent = 0
            self.lower_case_percent = 0
            self.number_percent = 0
            self.symbol_percent = 0
            self.space_percent = 1