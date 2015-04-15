"""
This script extracts the LaTeX tokens from each question and organizes these by keyword.
These tokens will be used as features for the multi-label classifiers.
New information is persisted as a pandas dataframe in file ../data/tag_info_data_2.csv

@author Luigi Patruno
@date 15 April 2015
"""
import pandas as pd
from time import time
import ast

def remove_latex_symbols(list_of_latex):
    """
    Given a list of strings of LaTeX expressions, this function returns the list with the
    strings in remove_expressions removed from the expressions
    """
    remove_expressions = ["\\(", "\\)", "\(", "\)", "\\[", "\\]"]
    latex_expressions = []

    for latex in list_of_latex:
        for remove_exp in remove_expressions:
            if remove_exp in latex:
                latex = latex.replace(remove_exp, '')
        latex_expressions.append(latex)

    return latex_expressions
    
def tokenize_latex( list_of_latex ):
    """
    Given a list of LaTeX expressions this function returns a dictionary of
    tokenized symbols and the number of times these tokens appear in the 
    expressions.
    """
    latex_count = {}
    
    latex = remove_latex_symbols(list_of_latex)
    latex_tokens = ' '.join(latex).split()
    
    for val in latex_tokens:
        token = val.replace('\\', '')
        token = token.replace('/', '')
        if token in latex_count:
            latex_count[token] += 1
        else:
            latex_count[token] = 1
            
    return latex_count
    
    
def main():
    
    question_info = pd.read_csv('../data/question_info_data_2.csv', index_col=0)
    tag_info = pd.read_csv('../data/tag_info_data.csv', index_col=0)
    
    # Loop over each question, extracting the LaTeX tokens and adding to a dynamically growing
    # structure keeping track of the LaTeX tokens that appear for each keyword and the
    # count of times each token appears
    # This is a more efficient way than looping over each of the keywords in the keyword_info structure
    # since it eliminates checking the same LaTeX expressions multiple times

    t0 = time()

    print 'Extracting LaTeX tokens for all keywords and questions...\n'

    # Dict structure to hold latex tokens for all keywords
    keyword_latex_count = {}

    for i in range( question_info.shape[0] ):
        
        question = question_info['question_text'][i]
    
        latex = ast.literal_eval( question_info['latex_expressions'][i] )
        latex_tokens = tokenize_latex( latex )
    
        keywords = ast.literal_eval( question_info['keywords'][i] )
    
        for keyword in keywords:
            # If keyword has been encountered previously, append LaTeX token counts
            # Otherwise, set the value to the latex_tokens dict
            if keyword in keyword_latex_count:
            
                for token in latex_tokens:
                    # If this token has been encountered, increment count
                    # Otherwise, set the count to the count from the latex_tokens dict
                    # Also don't count an empty string
                    if token != '':
                        if token in keyword_latex_count[keyword]:
                            keyword_latex_count[keyword][token] += latex_tokens[token]
                        else:
                            keyword_latex_count[keyword][token] = latex_tokens[token]
            else:
                keyword_latex_count[keyword] = latex_tokens

    t1 = time()

    print 'LaTeX tokenization complete'
    print 'Total time: %f' % (t1-t0)
    
    # Create new DataFrame of results, merge existing tables on the keyword column,
    # and persist this new DataFrame for  subsequent use
    tags = []
    tokens = []

    for tag in keyword_latex_count.keys():
        tags.append( tag )
        tokens.append( keyword_latex_count[tag] )
    
    tag_latex_info = pd.DataFrame({ 'keyword' : tags,\
                                    'latex_tokens' : tokens })
    
    merged_info = pd.merge(tag_info, tag_latex_info, on='keyword')
    
    merged_info.to_csv('../data/tag_info_data_2.csv')
    
    print 'Saving new information to file ../data/tag_info_data_2.csv'
    

if __name__ == '__main__':
    main() 

