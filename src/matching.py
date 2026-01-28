import sys
import time


def read_input(file):
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


def main():
    if len(sys.argv) < 2:
        print("Include an input file to run program.")
        sys.exit(1)

    file = sys.argv[1]

    try:
        n, hospital_prefs, student_prefs = read_input(file)
    except ValueError as e:
        print(e)
        sys.exit(1)

    start = time.perf_counter()

    # Run Gale-Shapley algorithm
    matching, numProposals = galeShapley(n, hospital_prefs, student_prefs)

    end = time.perf_counter()

    # Output the final matching
    for hospital in sorted(matching.keys()):
        print(f"{hospital} {matching[hospital]}")
    
    # Optionally output number of proposals and runtime (to stderr)
    sys.stderr.write(f"Number of proposals: {numProposals}\n")
    sys.stderr.write(f"Matching runtime: {end - start:.6f} seconds\n")


if __name__ == "__main__":
    main()
