"""
This script scans through each question's text and looks for keywords found within the text.
If a keyword is made up of several words, it counts the keyword if each individual word
is found within the text

@author Luigi Patruno
@date 15 April 2015
"""
import pandas as pd
from time import time

def main():
    
    # Read in question and tag info from csv files
    question_info = pd.read_csv('../data/question_info_data.csv', index_col=0)
    tag_info = pd.read_csv('../data/tag_info_data.csv', index_col=0)


    # Remove annoying NaN value found within the tag info
    # Save the tag info back to the file to prevent this from happening in the future
    # Only needs to be run once since I'm saving the contents
    #remove = []
    #for i in range( tag_info.shape[0] ):
    #    if type(tag_info['keyword'][i]) != str:
    #        remove.append(i)
    #tag_info = tag_info.drop(tag_info.index[remove])
    #tag_info.to_csv('../data/tag_info_data.csv')
    
    
    total_keywords_found_in_text = []
    
    t0 = time()
    print 'Searching for any keywords in all question texts...\n'
    for question in question_info['question_text'].values:
        
        # To hold all keywords found
        keywords_found_in_text = []
    
        # Tokenize the question
        question_tokens = question.split()     

        # Convert to dict for faster searching
        question_tokens = {token:0 for token in question_tokens}

        for keyword in tag_info['keyword'].values:

            keyword_tokens = keyword.split()
            
            question_contains_tokens = []
            
            for token in keyword_tokens:
                if token in question_tokens:
                    question_contains_tokens.append(True)
                else:
                    question_contains_tokens.append(False)

            if all(vals == True for vals in question_contains_tokens):
                keywords_found_in_text.append(keyword)
    
        total_keywords_found_in_text.append(keywords_found_in_text)

    t1 = time()

    print 'Search complete'
    print 'Time: %f \n' % (t1 - t0)
    
    print 'Persisting new column to file ...'
    question_info['keywords_in_text'] = total_keywords_found_in_text
    question_info.to_csv('../data/question_info_data_2.csv')
    print 'Data saved to file ../data/question_info_data_2.csv'
    
if __name__ == '__main__':
    main()