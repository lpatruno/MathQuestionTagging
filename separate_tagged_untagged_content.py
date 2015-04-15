"""
This script is responsible for scanning through the WebWorK question folders and creating 
two files containing the paths to all of the tagged and untagged questions.

These files will be used for easier access to tagged content for all subsequent scripts.
@author Luigi Patruno
@date April 14 2015
"""
from __future__ import division
import glob
import os
from time import time

def get_tagged_untagged_files(base_directory, tagged_problems, untagged_problems):
    """
    Method to separate all tagged and untagged problems in the WebWorK library
    @return
        tuple containg lists of file paths to tagged and untagged problems (tagged,untagged)
    """
    NO_QUESTION = '# This file is just a pointer to the file'
    FILE_POSTFIX = '.pg'
    KEYWORD = 'KEYWORD'
    
    subfiles = glob.glob(base_directory + '/*')
    
    for file_path in subfiles:
        
        if FILE_POSTFIX not in file_path:
            # Recurse through the subdirectories
            if os.path.isdir(file_path):
                tagged_problems, untagged_problems = get_tagged_untagged_files(file_path, tagged_problems, untagged_problems)
        else:
            # Flags to check if a file is a pointer to another file or if it is a tagged question
            pointer_to_file = False
            tagged_question = False
            
            # Exclude all files that are pointers to other files
            problem_file_handle = open(file_path, mode='r')
            contents = problem_file_handle.readlines()
            problem_file_handle.close()
    
            # Parse lines of file to distinguish between pointers, tagged problems and untagged problems
            for line in contents:
                # Remove file if it's a pointer to some other file
                if NO_QUESTION in line:
                    pointer_to_file = True
                    break;
                # Set flag to true if question is tagged
                if KEYWORD in line:
                    tagged_question = True
                    break;
                    
            if tagged_question: 
                tagged_problems.append(file_path)
            elif not pointer_to_file: 
                untagged_problems.append(file_path)
        
    # Return list of tagged and untagged problems file paths
    return tagged_problems, untagged_problems
    

def main():
    
    base_directory = '/Users/luigi/Desktop/webwork-open-problem-library/OpenProblemLibrary'
    
    tagged_problems = []
    untagged_problems = []

    print 'Separating WebWork questions by tagged/untagged...\n'
    
    t0 = time()
    tagged_problems, untagged_problems = get_tagged_untagged_files(base_directory, tagged_problems, untagged_problems)
    t1 = time()
    
    num_tagged = len(tagged_problems)
    num_untagged = len(untagged_problems)
    num_total = num_tagged + num_untagged
    
    print 'Took %d seconds to complete\n' % (t1-t0)
    print 'Total number questions: %d' % num_total
    print 'Number of tagged questions: %d   Percent tagged: %f' % (num_tagged, num_tagged / num_total)
    print 'Number of untagged questions: %d   Percent untagged: %f \n' % (num_untagged, num_untagged / num_total)
    
    # Writing tagged and untagged file paths to different txt files for easy access
    print 'Writing tagged and untagged paths to file for easy access'
    
    tagged_file = 'tagged_paths.txt'
    print 'Writing tagged content to %s' % tagged_file
    tagged_write_file = open(tagged_file, mode='w')
    for f in tagged_problems:
        tagged_write_file.write(f + '\n')
    tagged_write_file.close()

    untagged_file = 'untagged_paths.txt'
    print 'Writing untagged content to %s \n' % untagged_file
    untagged_write_file = open(untagged_file, mode='w')
    for f in untagged_problems:
        untagged_write_file.write(f + '\n')    
    untagged_write_file.close()
    
if __name__ == '__main__':
    main()