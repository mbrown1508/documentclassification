import datetime
import os

from sklearn.externals import joblib

import worker.classifier as worker
import classifier.models as model


class Cache:
    @staticmethod
    def store(model_object, classfier_object):

        if type(classfier_object) is worker.Classifier:
            # remove all possible memory
            classfier_object.data_set = None

            output_location = os.path.join('worker/cache/classifier', str(model_object.id))

            # Check the folder exists
            if not os.path.exists(output_location):
                os.makedirs(output_location)

            joblib.dump(classfier_object, os.path.join(output_location, 'classifier.pkl'))

        else:
            # This method should also be used to cache the lda models
            raise Exception('Not a valid object to cache')

    @staticmethod
    def load(model_object):
        print('Loading model')
        ## Get all the required details up-front
        if type(model_object) is model.Classifier:
            cache_root = 'worker/cache/classifier'
            type_name = 'classifier'
        else:
            raise Exception('Not a valid object to cache')

        return joblib.load(os.path.join(cache_root, str(model_object.id), type_name + '.pkl'))
