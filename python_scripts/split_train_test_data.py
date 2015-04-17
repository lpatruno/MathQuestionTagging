"""
This script splits the question set into a train and test set for the sake of consistency across analysis on different days

@author Luigi Patruno
@date 17 April 2015
"""
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split

def main():
    
    question_info = pd.read_csv('/home/vagrant/datacourse/MathQuestionTagging/data/question_info_data_2.csv', index_col=0)
    train, test = train_test_split(question_info, test_size = 0.2)
    
    train_df = pd.DataFrame(train, columns=question_info.columns)
    test_df = pd.DataFrame(test, columns=question_info.columns)
    
    train_df.to_csv('/home/vagrant/datacourse/MathQuestionTagging/data/train_data.csv')
    test_df.to_csv('/home/vagrant/datacourse/MathQuestionTagging/data/test_data.csv')
    
if __name__ == '__main__':
    main()
