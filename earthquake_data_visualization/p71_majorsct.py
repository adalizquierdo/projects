'''                          
who is in CIS 210?
CIS 210 F18 Project 7-1

Author: Bernardo Izquierdo

Credits: None

Description: Uses file processing and data analysis to find and report information about the range of majors
represented in CIS 210 in Fall 2018.
'''
import p62_data_analysis as p6 # Imported to have access to data analysis functions

def majors_readf(fname):
    '''
    (string) -> list

    Returns a list of majors for file name inputed

    >>> majors_readf('p71_demo.txt')
    <LIST OF MAJORS>
    '''
    with open(fname, 'r') as mf:
        mf.readline()  # The two mf.readline() are used to move pointer in file in order to only get data wanted
        mf.readline()  # Look into possibly finding another way to do this
        majors = mf.read()
        majors_list = majors.split('\n') # Creats list of majors split at \n
    return majors_list

def majors_analysis(majorsli):
    '''
    (list) -> tuple

    Determines the number of distinct majors in majorsli by calling
    function genFrequencyTable to generate a dictionary of majors and
    their ocurrance. We then find the major(s) with the max occurance and
    return a tuple containing a list of most ocurring majors AND number
    of distinct majors. LIST ENTED AS ARGUMENT MUST NOT BE EMPTY.

    >>> majors_analysis(['CIS', 'CIS', 'GB'])
    (2, ['CIS'])
    >>> majors_analysis(['CIS', 'GB', 'PHYS'])
    (3, ['CIS', 'GB', 'PHYS'])
    >>> majors_analysis(['CIS'])
    (1, ['CIS'])
    '''
    dict_majors = p6.genFrequencyTable(majorsli) #generates dictionary of majors and their occurences
    frequency_list = list(dict_majors.values()) # Creates list of values (occurences of each major) in dic_majors
    mode_majors = max(frequency_list) # Finds the max of frequecy_list, which is the major with the most students
    mode_majors_names = []
    for major in dict_majors:
       if dict_majors[major] == mode_majors:
           mode_majors_names.append(major)
    number_of_majors = len(dict_majors) #This counts the number of different majors
    return (mode_majors_names, number_of_majors)

def majors_report(majors_mode, majors_ct, majorsli):
    '''
    (list, int, list) -> None

    Generates report for for inputed values. Report prints
    out all values (along with description) and returns None

    >>> majors_report(['CIS'], 1, ['CIS'])
    <report>
    '''
    print('The most common major is:', majors_mode[0])
    print('The number of different majors is:', majors_ct)
    p6.frequencyTable(majorsli)
    return None

def main():
    '''
    () -> None
    Calls: majors_readf, majors_analysis, majors_report
    Top level function for analysis of CIS 210 majors data.
    Returns None.
    '''
    fname = 'p71_majors_cis210f18.txt'
    majorsli = majors_readf(fname) #read
    majors_mode, majors_ct = majors_analysis(majorsli) #analyze
    majors_report(majors_mode, majors_ct, majorsli) #report
    return None

main()
