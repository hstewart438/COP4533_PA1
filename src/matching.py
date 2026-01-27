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


def main():
    if len(sys.argv) < 1:
        print("Include an input file to run program.")
        sys.exit(1)

    file = sys.argv[1]

    try:
        n, hospital_prefs, student_prefs = read_input(file)
    except ValueError as e:
        print(e)
        sys.exit(1)

    #debug checking read_input
    print(n)
    print(hospital_prefs)
    print(student_prefs)

    start = time.perf_counter()

    # Run matching algo here

    end = time.perf_counter()
    print(f"Matching runtime: ", end - start, " seconds")
    

if __name__ == "__main__":
    main()
