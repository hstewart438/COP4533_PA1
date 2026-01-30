import sys
import os

def read_input(input_file):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()] # ignore empty lines with if line.strip()
    
    # check if empty
    if not lines:
        raise ValueError("INVALID input file: File is empty.")

    # check if n is an integer
    try:
        n = int(lines[0])
        if n <= 0:
            raise ValueError("INVALID input file: Cannot calculate matching for n<=0.")
    except ValueError:
        raise ValueError("INVALID input file: First line should be an integer.")

    # remove n
    lines.pop(0)  
    
    # check valid total lines
    if len(lines) != (2 * n):
        raise ValueError("INVALID input file: Expected 2n lines after first line.")

    # Read hospital preferences
    hospital_prefs = []
    for i in range(n):
        prefs = lines[i].split()
        if (len(prefs) != n):
            raise ValueError("INVALID input file: Hospital does not have enough student rankings")

        # Check integer
        for j in range(n):
            try:
                prefs[j] = int(prefs[j])
                if prefs[j] < 1 or prefs[j] > n:
                    raise ValueError(f"INVALID input file: Preference value {prefs[j]} is out of range 1..{n}.")
            except ValueError:
                raise ValueError("INVALID input file: Preferences must be integers.")

        hospital_prefs.append(prefs)

    # Read student preferences
    student_prefs = []
    for i in range(n, 2*n):
        prefs = lines[i].split()
        if (len(prefs) != n):
            raise ValueError("INVALID input file: Student does not have enough hospital rankings")
        
        # Check integer
        for j in range(n):
            try:
                prefs[j] = int(prefs[j])
                if prefs[j] < 1 or prefs[j] > n:
                    raise ValueError(f"INVALID input file: Preference value {prefs[j]} is out of range 1..{n}.")
            except ValueError:
                raise ValueError("INVALID input file: Preferences must be integers.")
        student_prefs.append(prefs)


    return n, hospital_prefs, student_prefs

def read_output(file):
    with open(file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()] # ignore empty lines with if line.strip()
    
    # check if empty
    if not lines:
        raise ValueError("INVALID output file: File is empty.")

    # check if n is an integer
    try:
        n = int(lines[0])
        if n <= 0:
            raise ValueError("INVALID output file: Cannot calculate for n<=0.")
    except ValueError:
        raise ValueError("INVALID ouput file: First line should be an integer.")

    # remove n
    lines.pop(0)  
    
    # check valid total lines
    if len(lines) != n: 
        raise ValueError("INVALID output file: Expected exactly n matching pairs.")

    # Read matching pairs
    hospital_to_student = [None] * (n+1)
    student_to_hospital = [None] * (n+1)

    for line in lines:
        pair = line.split()
        if len(pair) != 2:
            raise ValueError("INVALID: output file does not contain n matching pairs.")

        try:
            hospital = int(pair[0])
            student = int(pair[1])
        except ValueError:
            raise ValueError("INVALID ouptut file: Matching pairs must be integers.")

        # Check invalid range
        if hospital < 1 or hospital > n: 
            raise ValueError(f"INVALID output file: Hospital {hospital} is out of range 1..{n}.") 
        if student < 1 or student > n: 
            raise ValueError(f"INVALID output file: Student {student} is out of range 1..{n}.") 
        
        # Check duplicates
        if hospital_to_student[hospital] is not None: 
            raise ValueError(f"INVALID output file: Hospital {hospital} appears more than once in output.") 
        if student_to_hospital[student] is not None: 
            raise ValueError(f"INVALID output file: Student {student} is matched more than once.")


        # Store match
        hospital_to_student[hospital] = student
        student_to_hospital[student] = hospital
    
    return n, hospital_to_student, student_to_hospital
