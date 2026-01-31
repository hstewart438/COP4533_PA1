import sys
import os

def read_input(input_file):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()] # ignore empty lines with if line.strip()
    
    # check if empty
    if not lines:
        raise ValueError("\nINVALID input file: File is empty.\n")

    # check if n is an integer
    try:
        n = int(lines[0])
        if n <= 0:
            raise ValueError("\nINVALID input file: Cannot calculate matching for n<=0.\n")
    except ValueError:
        raise ValueError("\nINVALID input file: First line should be an integer.\n")

    # remove n
    lines.pop(0)  
    
    # check valid total lines
    if len(lines) != (2 * n):
        raise ValueError("\nINVALID input file: Expected 2n lines after first line.\n")

    # Read hospital preferences
    hospital_prefs = []
    for i in range(n):
        prefs = lines[i].split()
        if (len(prefs) != n):
            raise ValueError(f"\nINVALID input file: Hospital {i + 1} does not have enough student rankings.\n")

        # Check integer
        for j in range(n):
            try:
                prefs[j] = int(prefs[j])
                if prefs[j] < 1 or prefs[j] > n:
                    raise ValueError(f"\nINVALID input file: Preference value {prefs[j]} is out of range 1-{n}.\n")
            except ValueError:
                raise ValueError("\nINVALID input file: Preferences must be integers.\n")

        if len(set(prefs)) != n:
            raise ValueError(f"\nINVALID input file: Duplicate rankings found in hospital {i + 1}'s preferences.\n")
        hospital_prefs.append(prefs)

    # Read student preferences
    student_prefs = []
    for i in range(n, 2*n):
        prefs = lines[i].split()
        if (len(prefs) != n):
            raise ValueError(f"\nINVALID input file: Student {i - n + 1} does not have enough hospital rankings.\n")
        
        # Check integer
        for j in range(n):
            try:
                prefs[j] = int(prefs[j])
                if prefs[j] < 1 or prefs[j] > n:
                    raise ValueError(f"\nINVALID input file: Preference value {prefs[j]} is out of range 1-{n}.\n")
            except ValueError:
                raise ValueError("\nINVALID input file: Preferences must be integers.\n")
            
        if len(set(prefs)) != n:
            raise ValueError(f"\nINVALID input file: Duplicate rankings found in hospital {i - n + 1}'s preferences.\n")
        student_prefs.append(prefs)


    return n, hospital_prefs, student_prefs

def read_output(file):
    with open(file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()] # ignore empty lines with if line.strip()
    
    # check if empty
    if not lines:
        raise ValueError("\nINVALID output file: File is empty.\n")
    
    # get n
    n = len(lines)

    # Read matching pairs
    hospital_to_student = [None] * (n+1)
    student_to_hospital = [None] * (n+1)

    for line in lines:
        pair = line.split()
        if len(pair) != 2:
            raise ValueError("\nINVALID: output file contains line with no match pair.\n")

        try:
            hospital = int(pair[0])
            student = int(pair[1])
        except ValueError:
            raise ValueError("\nINVALID ouptut file: Matching pairs must be integers.\n")

        # Check invalid range
        if hospital < 1 or hospital > n: 
            raise ValueError(f"\nINVALID output file: Hospital {hospital} is out of range 1-{n}.\n") 
        if student < 1 or student > n: 
            raise ValueError(f"\nINVALID output file: Student {student} is out of range 1-{n}.\n") 
        
        # Check duplicates
        if hospital_to_student[hospital] is not None: 
            raise ValueError(f"\nINVALID output file: Hospital {hospital} appears more than once in output.\n") 
        if student_to_hospital[student] is not None: 
            raise ValueError(f"\nINVALID output file: Student {student} is matched more than once.\n")


        # Store match
        hospital_to_student[hospital] = student
        student_to_hospital[student] = hospital
    
    return n, hospital_to_student, student_to_hospital
