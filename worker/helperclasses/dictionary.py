import re


class Dictionary:
    def __init__(self):
        self.dictionary_location = 'worker/helperclasses/words.txt'

        # Read in dictionary
        temp_dict = list(line.lower().strip()
                         for line in open(self.dictionary_location))

        # Remove all words less than 3 characters (performance)
        temp_dict = [s for s in temp_dict if len(s) > 2]

        self.dictionary = set()
        for word in temp_dict:
            self.dictionary.add(self.cleanup_string(word))

    # Dictionary Analysis
    def count_words(self, word_stats):
        word_count = 0
        for word in word_stats:
            word_count += word['count']

        return word_count

    def check_for_word(self, word, strip_special=True):
        word = word.strip()

        if word in self.dictionary:
            return True
        else:
            return False

    def return_words(self, text_sample):
        words = []
        words_temp = {}
        word_count = 0

        text_sample = text_sample.lower().split()

        for word in text_sample:
            if len(word) > 2:
                if self.check_for_word(word):
                    if word in words_temp:
                        words_temp[word] += 1
                    else:
                        words_temp[word] = 1

                    word_count += 1

        for word, value in words_temp.items():
            percentage = value / word_count * 100
            words.append({'value': word, 'count': value, 'percentage': percentage})

        return words

    def cleanup_string(self, string_to_clean):
        '''
        # This was the original
        clean_string = re.sub("[^A-Za-z ]+", " ", string_to_clean)
        clean_string = re.sub("[ ]+", " ", clean_string)
        clean_string = clean_string.lower()
        '''

        # currently using this for bow
        clean_string = re.sub("[^a-zA-Z]", " ", string_to_clean)

        return clean_string
