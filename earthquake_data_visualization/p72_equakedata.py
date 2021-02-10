'''                          
Earthquake Watch
CIS 210 F18 Project 7-2

Author: Bernardo Izquierdo

Credits: None

Description: Uses file processing and data analysis to find and report information about the range of majors
represented in files that contain earthquake data.
'''
import p62_data_analysis as p6 # Imported to have access to data analysis functions

def equake_readf(fname):
    '''
    (string) -> list

    Creates a list of magnitudes of earthquakes. This by openning inputed
    file and using file read methods to access the magnitude of each earthquake.
    Returns the earthquake magnitudes as a list of strings.

    >>> equake_readf('equakes50f.txt')
    <LIST OF MAGNITUDES>
    '''
    with open(fname, 'r') as mf:
        mf.readline() #This will move pointer to second line where data starts
        mag_list = []
        for line in mf:
            line_list = line.split(',')
            mag_list.append(line_list[4])
        return mag_list

def equake_analysis(magnitudes):
    '''
    (list) -> tuple

    Calls functions from project 6 (mean, median, mode) to analyze the data
    of inputed list of magnitudes. NOTE: magnitudes in inputed list may be
    strings, so in function we convert each item to a floating number before
    running project 6 functions. Returns a tuple containing the results of the
    three functions

    >>> equake_analysis(['5.4', '5.4', '5.4'])
    (5.4, 5.4, [5.4])
    >>> equake_analysis(['5.4', '6', '6'])
    (5.8, 6, [6])
    >>> equake_analysis(['0', '0', '0'])
    (0, 0, [0])
    '''
    magnitudes_f = [] # Will be used to store magnitudes as floats
    for mag in magnitudes: # Converts magnitudes into floats and adds them to list magnitude_f
        magnitudes_f.append(float(mag))   
    mean = p6.mean(magnitudes_f)
    median = p6.median(magnitudes_f) 
    mode = p6.mode(magnitudes_f)
    return (mean, median, mode)

def equake_report(mmm, magnitudes):
    '''
    (tuple, list) -> None

    Generates a report on the list of magnitudes entered.
    Report includes the mean, median mode, and number of
    earthquakes. Prints out results along with description.
    Returns None.

    >>> equake_report((5.5, 5.5, [5.5])
    <REPORT GENERATED>
    '''
    count_eq = len(magnitudes) #counts the number of earthquakes
    print('The number of earthquakes was:', count_eq)
    print('The mean of the earthquakes was:', mmm[0])
    print('The median of the earthquakes was:', mmm[1])
    print('The mode of the earthquakes was:', mmm[2])
    p6.frequencyTable(magnitudes)
    return None
    
def main():
    '''
    () -> None
    Calls: equake_readf, equake_analysis, equake_report
    
    Top level function for earthquake data analysis.
    Returns None.
    '''
    #fname = 'equakes25f.txt'
    fname = 'equakes50f.txt'
    emags = equake_readf(fname)
    mmm = equake_analysis(emags)
    equake_report(mmm, emags)
    return None

main()
