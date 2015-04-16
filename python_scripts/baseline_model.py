"""
This script uses the keywords found in the question text as features to train 
classifiers for prediction.

@author Luigi Patruno
@date 16 April 2015
"""
from __future__ import division
import numpy as np
import pandas as pd
from time import time
import ast
from sklearn.cross_validation import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics import hamming_loss
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from baseline_feature_extractor import BaselineFeatureExtractor


def main():
    
    # Read in the extracted information
    question_info = pd.read_csv('../data/question_info_data_2.csv', index_col=0 )
    tag_info = pd.read_csv('../data/tag_info_data_2.csv', index_col=0 )
    
    # Split data into training and test set
    train, test = train_test_split(question_info, test_size = 0.2)
    
    # Convert string representation to list of string keywords
    x_train_raw = []
    y_train_raw = []
    y_test_raw = []

    for i in range( train.shape[0] ):
        x_train_raw.append( ast.literal_eval(train[i][4]) )
        y_train_raw.append( ast.literal_eval(train[i][0]) )

    for i in range( test.shape[0]):
        y_test_raw.append( ast.literal_eval(test[i][0]) )
        
    # Train clasifier and predict keywords
    num_feats = [50, 100, 200, 500, 1000]
    #num_feats = [50, 100, 200, 500, 1000, tag_info.shape[0]]

    num_train = []
    num_test = []
    train_feature_time = []
    test_feature_time = []
    model_train_time = []
    jaccard = []
    hamming = []
    precision = []
    recall = []
    f1 = []

    for n in num_feats:
    
        top_n_tags = tag_info.sort('count', ascending=False).head(n)
        bfe = BaselineFeatureExtractor(top_n_tags)
    
        x_train, y_train, train_zero_count, train_feat_extract_time = bfe.x_y_train(x_train_raw, y_train_raw)
        y_true, test_zero_count, test_feat_extract_time = bfe.y_true(y_test_raw)
    
        t0 = time()
        clf_LinearSVC = OneVsRestClassifier(LinearSVC()).fit(x_train, y_train)
        t1 = time()
    
        y_predict = clf_LinearSVC.predict( y_true )
    
        # Basic stats
        num_train.append(len(x_train))
        num_test.append(len(y_true))
        train_feature_time.append( train_feat_extract_time )
        test_feature_time.append( test_feat_extract_time )
        model_train_time.append( t1-t0 )
        
        # Evaluation metrics
        jaccard.append( jaccard_similarity_score(y_true, y_predict) )
        hamming.append( hamming_loss(y_true, y_predict) )
        precision.append( precision_score(y_true, y_predict, average='micro') )
        recall.append( recall_score(y_true, y_predict, average='micro') )
        f1.append( f1_score(y_true, y_predict, average='micro')  )
        
    
    
    info_df = pd.DataFrame({ 'num_feats': num_feats, \
                            'num_train': num_train, \
                            'num_test' : num_test, \
                            'train_feat_time': train_feature_time, \
                            'test_feat_time': test_feature_time, \
                            'model_time': model_train_time, \
                            'jaccard': jaccard, \
                            'hamming_loss': hamming, \
                            'precision': precision, \
                            'recall': recall, \
                            'f1': f1})
     
    print(info_df)
        
    
if __name__ == '__main__':
    main()