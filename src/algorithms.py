import sys
import os

def galeShapley(n, hospitalPrefs, studentPrefs):
    #Gale Shapley algorithm to find a stable matching between hospitals and students
    # Input: n, hospitalPrefs, studentPrefs
    # Output: matching, numProposals
   
    # Build student ranking dict for O(1) lookups
    studentRank = []
    for s in range(n):
        rank = {}
        for i, h in enumerate(studentPrefs[s]):
            rank[h] = i
        studentRank.append(rank)
    
    hospitalMatch = [None] * n
    studentMatch = [None] * n
    nextProposal = [0] * n
    freeHospitals = list(range(n))
    numProposals = 0
    
    while freeHospitals:
        h = freeHospitals.pop(0)
        
        if nextProposal[h] >= n:
            continue
        
        # Hospital h proposes to next student
        s = hospitalPrefs[h][nextProposal[h]] - 1
        nextProposal[h] += 1
        numProposals += 1
        
        if studentMatch[s] is None:
            # Student accepts
            hospitalMatch[h] = s
            studentMatch[s] = h
        else:
            hPrime = studentMatch[s]
            # Student compares current vs new proposal
            if studentRank[s][h + 1] < studentRank[s][hPrime + 1]:
                # Student prefers h, reject hPrime
                hospitalMatch[h] = s
                studentMatch[s] = h
                hospitalMatch[hPrime] = None
                if nextProposal[hPrime] < n:
                    freeHospitals.append(hPrime)
            else:
                # Student rejects h
                if nextProposal[h] < n:
                    freeHospitals.append(h)
    
    # Convert to 1-indexed output
    matching = {}
    for h in range(n):
        if hospitalMatch[h] is not None:
            matching[h + 1] = hospitalMatch[h] + 1
    
    return matching, numProposals

def verify_matching(n, hospital_prefs, student_prefs, matching):
    print("\nVerifying matching stability...")
    
    # Are all participants matched?
    if len(matching) != (n):
        print("\nINVALID: Not all participants have been matched.\n")
        sys.exit(1)
    
    # Convert matching dictionary to arrays for easy look up 
    hospital_to_student = [None] * (n+1) 
    student_to_hospital = [None] * (n+1) 
    for hospital, student in matching.items(): 
        hospital_to_student[hospital] = student 
        student_to_hospital[student] = hospital
    
    # Check for blocking pairs
    blocking = False
    for hospital in range(1, n+1):
        current_student = hospital_to_student[hospital]

        # Does hospital prefer s_prime over current_student?
        for s_prime in hospital_prefs[hospital - 1]:

            # Once we reach the current student, all students after are less preferred
            if s_prime == current_student:
                break

            # Student s_prime's current hospital
            h_prime = student_to_hospital[s_prime]

            # Check if s_prime prefers hospital over h_prime
            for pref in student_prefs[s_prime - 1]:
                if pref == h_prime:
                    break  # student prefers current match

                if pref == hospital:
                    print(f"\nUNSTABLE: Hospital {hospital} and Student {s_prime} are a blocking pair\n")
                    blocking = True
    if blocking:
        print("")
        sys.exit(1)
    else:
        print("VALID STABLE")


