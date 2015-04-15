"""
This script scans through each of the tagged questions, extracts the question data, such as the 
question text and embedded LaTeX expressions, extracts keyword usage data such as the number
of times a keyword appears for a question as well as the paths to the questions in which
a keyword appears, and persists this information as pandas DataFrames for future analysis.

@author Luigi Patruno
@date April 14 2015
"""
import re
from time import time
import pandas as pd

def get_keywords(question_file_lines):
    """
    This function accepts file contents of a tagged question file, extracts the keywords,
    and returns a python list of these.
    @params
        - string of question file contents
    @return
        - python list of question keywords
    """

    for line in question_file_lines:
        
        if line.startswith('##'):
            
            if "KEYWORDS" in line:
                start = line.find('(')+1
                end = line.find(')')
                keyword_list = line[start:end].split(',')

                for i,tag in enumerate(keyword_list):
                    keyword_list[i] = tag.replace("'",'')
                    keyword_list[i] = keyword_list[i].strip()
                    keyword_list[i] = keyword_list[i].lower()
             
    return list(set(keyword_list))
    
    
def get_question_text(question_file_lines):
    """
    This function accepts file contents of a tagged question file and 
    extracts and returns the question text.
    @params
        - string of question file contents
    @return
        - string of question text
    """
    EOT = "EOT"
    BR = "$BR"
    BEGIN_TEXT = "BEGIN_TEXT"
    END_TEXT = "END_TEXT"

    question_text = ''
    indices = []

    for i, line in enumerate(question_file_lines):    
        if ( EOT in line or BR in line or BEGIN_TEXT in line or END_TEXT in line):
            indices.append(i)
            
    if indices:
        start_line = min(indices)
        end_line = max(indices)

        question_text = question_file_lines[ start_line + 1 : end_line]
        question_text = ' '.join(question_text)
        question_text = question_text.replace(BR, '')
        question_text = question_text.replace('\n', '')
    
    return question_text


def find_all(a_str, sub):
    """
    Find all instances of a subtring within a string
    """
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


def get_latex(question_text):
    """
    This function accepts question text, extracts the LaTeX expressions embedded within the text,
    and returns a python list of these expressions.
    @params
        - string of question text
    @return
        - python list of LaTeX expressions embedded within the text
    """
    
    latex = []

    start_eq = ["\\(", "\\["]
    end_eq = ["\\)", "\\]"]

    starts = list(find_all(question_text, start_eq[0])) + list(find_all(question_text, start_eq[1]))
    ends = list(find_all(question_text, end_eq[0])) + list(find_all(question_text, end_eq[1]))

    for i in range(len(starts)):
        try:
            latex.append( question_text[starts[i]:ends[i]+2] )
        except IndexError as e:
            latex.append( question_text[starts[i]:] )

    return latex



def main():
    
    tagged_content = '../data/tagged_paths.txt'

    tagged_paths = []

    for line in open(tagged_content, mode='r'):
        tagged_paths.append( line.replace('\n','') )
    
    print 'Number of tagged questions: %d' % len(tagged_paths)
    
    t0 = time()

    keyword_info = {}
    question_info = {'questions' : []}

    print 'Scanning all tagged questions and extracting relevant infomation...\n'

    for i, path in enumerate(tagged_paths):
        
        question_file_handle = open(path, mode='r')
        question_file_lines = question_file_handle.readlines()
        question_file_handle.close()
    
        keywords =  get_keywords(question_file_lines)
        question_text = get_question_text(question_file_lines)
    
        latex = get_latex(question_text)
    
        # Update the kquestion_info data structure
        question_dict = {'question_file_path' : path, \
                         'question_text' : question_text, \
                         'latex_expressions' : latex }
        question_info['questions'].append( question_dict )
    
        # Update the keyword_info data structure
        # Include file path to act as a foreign key between the keyword_info 
        # and question_info structs
        for keyword in keywords:
            if keyword in keyword_info:
                keyword_info[keyword]['count'] += 1
                keyword_info[keyword]['question_file_path'].append( path )
            else:
                keyword_info[keyword] = {'count' : 1, 'question_file_path' : [path]}
            
    t1 = time()

    print 'Extraction complete'
    print 'Total time: %d sec' % (t1-t0)
    print 'Total number of keywords found: %d \n' % len(keyword_info.keys())
    
    # Create a pandas dataframe with the keyword_info and persist the data to a file
    # pandas is being mean and won't let me pass the keyword_info dict so I need to 
    # extract the info as lists
    keywords = keyword_info.keys()
    counts = []
    k_paths = []

    for keyword in keywords:
        counts.append( keyword_info[keyword]['count'] )
        k_paths.append( keyword_info[keyword]['question_file_path'] )
    
    keyword_df = pd.DataFrame({'keyword': keywords, \
                       'count': counts, \
                       'question_file_path': k_paths})
                       
    # Let's do the same for the question data    
    q_paths = []
    q_text = []
    q_latex = []

    for q in question_info['questions']:
        q_paths.append( q['question_file_path'] )
        q_text.append( q['question_text'] )
        q_latex.append( q['latex_expressions'] )
    
    question_df = pd.DataFrame({'question_text': q_text, \
                               'latex_expressions': q_latex, \
                               'question_file_path': q_paths})
                               
    # Yay let's persist these structures
    tag_info_data = '../data/tag_info_data.csv'
    question_info_data = '../data/question_info_data.csv'
    
    keyword_df.to_csv(question_info_data)
    keyword_df.to_csv(tag_info_data)
    
    print 'Tag data persisted to file: %s' % tag_info_data
    print 'Question data persisted to file: %s' % question_info_data
        

if __name__ == '__main__':
    main()