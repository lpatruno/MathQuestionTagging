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

import BaselineFeatureExtractor


def main():
    print 'Works'
    
if __name__ == '__main__':
    main()