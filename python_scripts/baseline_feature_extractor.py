import numpy as np
import pandas as pd
from time import time
import ast

class BaselineFeatureExtractor():
    """
    This class extracts the basic features from the WebWorK questions in the Open Problem Library.
    
    These are just the occurrence of keywords within the question text itself.
    
    Sample usage:
    
        bfe = BaselineFeatureExtractor(top_n_tags)

        x_train, y_train, train_zero_count, train_feat_extract_time = bfe.x_y_train(x_train_raw, y_train_raw)
        y_true, test_zero_count, test_feat_extract_time = bfe.y_true(y_test_raw)

        clf_LinearSVC = OneVsRestClassifier(LinearSVC()).fit(x_train, y_train)
        y_predict = clf_LinearSVC.predict( y_true )

        j_score = jaccard_similarity_score(y_true, y_predict)
    """
    def __init__(self, top_keywords):
        """
        @params
            - top_tags: pandas DataFrame of sorted keywords
        """
        self.top_keywords = top_keywords
        self.num_keywords = top_keywords.shape[0]
        keywords = top_keywords['keyword'].values.tolist()
        self.keywords = { k:keywords.index(k) for k in keywords}
    
    def label_features(self, keywords):
        """
        Convert list of keyword strings to list of keyword indices
        @params
            - keywords: python list of keyword strings
        """
        features = []
        
        for keyword in keywords:
            if keyword in self.keywords:
                index = self.keywords[keyword]
                features.append(index)
        
        return features
    
    def binarize(self, indices ):
        """
        Given a list of keyword indices, returns numpy array of 
        binarized features where binarized[i] == 1 if i in indices.
        """
        binarized = [0 for i in range(self.num_keywords)]

        for i in indices:
            binarized[i] = 1

        return binarized
    
    def x_y_train( self, x_data, y_data):
        """
        Given list of input and output tags, return binary feature
        representation suitable for input into scikit-learn
        classifiers
        """
        if len(x_data) != len(y_data):
            # sanity check
            print 'len(x) != len(y)'
            return None
        
        t0 = time()
        print 'Extracting baseline features for %d training samples and %d keywords\n' % (len(x_data), self.num_keywords)
        
        x_train = []
        y_train = []
        zero_count = 0
        
        for i in range(len(x_data)):
            x_feats = self.label_features( x_data[i] )
            y_feats = self.label_features( y_data[i] )

            if x_feats and y_feats:
                x_train.append( self.binarize(x_feats) )
                y_train.append( self.binarize(y_feats) )
            else:
                zero_count += 1

        x_train = np.array(x_train)
        y_train = np.array(y_train)
        
        t1 = time()
        
        return (x_train, y_train, zero_count, t1-t0)
    
    def y_true(self, y_data ):
        """
        Given list of output tags, return binary feature representation 
        suitable for input into scikit-learn classifier predictors.
        """
        t0 = time()

        y_true = []
        zero_count = 0
        
        for i in range(len(y_data)):
            y_feats = self.label_features(y_data[i])

            if y_feats:
                y_true.append( self.binarize(y_feats) )
            else:
                zero_count += 1

        y_true = np.array(y_true)
        
        t1 = time()
        
        return (y_true, zero_count, t1-t0)