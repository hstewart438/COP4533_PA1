import sys
import time
import os


def read_input(input_file):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()] # ignore empty lines with if line.strip()
    
    # check if empty
    if not lines:
        raise ValueError("Invalid input file: File is empty.")

    # check if n is an integer
    try:
        n = int(lines[0])
        if n <= 0:
            raise ValueError("Invalid input file: Cannot calculate matching for n<=0.")
    except ValueError:
        raise ValueError("Invalid input file: First line should be an integer.")

    # remove n
    lines.pop(0)  
    
    # check valid total lines
    if len(lines) != (2 * n):
        raise ValueError("Invalid input file: Expected 2n lines after first line.")

    # Read hospital preferences
    hospital_prefs = []
    for i in range(n):
        prefs = lines[i].split()
        if (len(prefs) != n):
            raise ValueError("Invalid input file: Hospital does not have enough student rankings")

        # Check integer
        for j in range(n):
            try:
                prefs[j] = int(prefs[j])
            except TypeError:
                raise TypeError("Invalid input file: Preferences must be integers.")

        hospital_prefs.append(prefs)

    # Read student preferences
    student_prefs = []
    for i in range(n, 2*n):
        prefs = lines[i].split()
        if (len(prefs) != n):
            raise ValueError("Invalid input file: Student does not have enough hospital rankings")
        
        # Check integer
        for j in range(n):
            try:
                prefs[j] = int(prefs[j])
            except ValueError:
                raise ValueError("Invalid input file: Preferences must be integers.")
        student_prefs.append(prefs)


    return n, hospital_prefs, student_prefs

def read_output(file):
    with open(file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()] # ignore empty lines with if line.strip()
    
    # check if empty
    if not lines:
        raise ValueError("Invalid input file: File is empty.")

    # check if n is an integer
    try:
        n = int(lines[0])
        if n <= 0:
            raise ValueError("Invalid input file: Cannot calculate matching for n<=0.")
    except ValueError:
        raise ValueError("Invalid input file: First line should be an integer.")

    # remove n
    lines.pop(0)  
    
    # check valid total lines
    if len(lines) != n:
        raise ValueError("Invalid input file: Expected 2n lines after first line.")

    # Read matching pairs
    hospital_to_student = [None] * (n+1)
    student_to_hospital = [None] * (n+1)

    for line in lines:
        pair = line.split()
        if len(pair) != 2:
            raise ValueError("Invalid input file: Each line must contain exactly two integers.")

        try:
            hospital = int(pair[0])
            student = int(pair[1])
        except ValueError:
            raise ValueError("Invalid input file: Matching pairs must be integers.")

        hospital_to_student[hospital] = student
        student_to_hospital[student] = hospital
    
    return n, hospital_to_student, student_to_hospital

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

        # Hospital's preference list
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
                    sys.exit(1)
    if blocking:
        print("")
        sys.exit(1)
    else:
        print("\nVALID STABLE")


def main():
    if len(sys.argv) < 2:
        print("\nInclude an input file to run program.\n")
        sys.exit(1)

    input_file = sys.argv[1]

    base_name = os.path.basename(input_file)
    output_name = os.path.splitext(base_name)[0] + ".out"
    output_file = os.path.join("output", output_name) 

    try:
        n, hospital_prefs, student_prefs = read_input(input_file)
    except ValueError as e:
        print(e)
        sys.exit(1)

    start = time.perf_counter()

    # Run Gale-Shapley algorithm
    matching, numProposals = galeShapley(n, hospital_prefs, student_prefs)

    end = time.perf_counter()

    # Output the final matching
    print("\nFinal Matching (Hospital Student):")
    for hospital in sorted(matching.keys()):
        print(f"{hospital} {matching[hospital]}")

    # Write output to file
    print(f"\nWriting matching results to {output_file}...")
    with open(output_file, "w") as f:
        f.write(f"{n}\n")
        for hospital, student in sorted(matching.items()):
            if hospital == n:
                f.write(f"{hospital} {student}")
                break
            if hospital is not None:
                f.write(f"{hospital} {student}\n")
    
            
                
    # Verify the matching stability
    verify_matching(n, hospital_prefs, student_prefs, matching)
    
    # Output number of proposals and runtime (to stderr)
    sys.stderr.write(f"\nNumber of proposals: {numProposals}")
    sys.stderr.write(f"\nMatching runtime: {end - start:.6f} seconds")


if __name__ == "__main__":
    main()
