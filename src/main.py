import sys
import time
import os

from reader import read_input, read_output
from algorithms import galeShapley, verify_matching


        
def find_input_file(folder):
    # Find the single .in file in the folder
    in_files = []
    for f in os.listdir(folder):
        if f.endswith(".in"):
            in_files.append(f)

    if len(in_files) != 1:
        print("MATCH MODE ERROR: Folder must contain exactly one .in file.")
        sys.exit(1)

    infile = in_files[0]
    input_path = os.path.join(folder, infile)

    return infile, input_path

def write_output_file(output_path, n, matching):
    # Write output to file
    with open(output_path, "w") as f:
        f.write(f"{n}\n")
        for hospital, student in sorted(matching.items()):
            if hospital == n:
                f.write(f"{hospital} {student}")
                break
            if hospital is not None:
                f.write(f"{hospital} {student}\n")
    
    print("")
    print(f"Matching results written to {output_path}")


def run_match(folder):
    # Find the single .in file in the folder
    infile, input_path = find_input_file(folder)

    # Read input
    try:
        n, hospital_prefs, student_prefs = read_input(input_path)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Run Gale-Shapley algorithm
    start = time.perf_counter()
    matching, numProposals = galeShapley(n, hospital_prefs, student_prefs)
    end = time.perf_counter()


    # Output the final matching
    print("\nFinal Matching (Hospital Student):")
    for hospital in sorted(matching.keys()):
        print(f"{hospital} {matching[hospital]}")

    # Write output
    outfile = os.path.splitext(infile)[0] + ".out"
    output_path = os.path.join(folder, outfile)
    write_output_file(output_path, n, matching)

    print(f"\nWriting output to {output_path}")

    # Output number of proposals and runtime (to stderr)
    sys.stderr.write(f"\nNumber of proposals: {numProposals}")
    sys.stderr.write(f"\nMatching runtime: {end - start:.6f} seconds")


def run_verify(folder):
    # Must contain verify.in and verify.out
    input_path = os.path.join(folder, "verify.in")
    output_path = os.path.join(folder, "verify.out")

    if not os.path.exists(input_path):
        print("VERIFY MODE ERROR: verify.in not found in folder.")
        sys.exit(1)
    if not os.path.exists(output_path):
        print("VERIFY MODE ERROR: verify.out not found in folder.")
        sys.exit(1)

    # Load files
    try:
        n, hospital_prefs, student_prefs = read_input(input_path)
        n2, hospital_to_student, student_to_hospital = read_output(output_path)
    except ValueError as e:
        print(e)
        sys.exit(1)

    if n != n2:
        print("INVALID: Mismatch in number of participants between input and output files.")
        sys.exit(1)

    # Convert arrays to matching dict
    matching = {}
    for h in range(1, n + 1):
        matching[h] = hospital_to_student[h]

    # Run verification
    verify_matching(n, hospital_prefs, student_prefs, matching)

def run_both(folder):
    # Find the single .in file in the folder
    infile, input_path = find_input_file(folder)

    # Read input
    try:
        n, hospital_prefs, student_prefs = read_input(input_path)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Run Gale-Shapley algorithm
    start = time.perf_counter()
    matching, numProposals = galeShapley(n, hospital_prefs, student_prefs)
    end = time.perf_counter()

    # Output the final matching
    print("\nFinal Matching (Hospital Student):")
    for hospital in sorted(matching.keys()):
        print(f"{hospital} {matching[hospital]}")

    # Output number of proposals and runtime (to stderr)
    sys.stderr.write(f"\nNumber of proposals: {numProposals}")
    sys.stderr.write(f"\nMatching runtime: {end - start:.6f} seconds\n")

    # Write output
    outfile = os.path.splitext(infile)[0] + ".out"
    output_path = os.path.join(folder, outfile)

    write_output_file(output_path, n, matching)

    # Verify the matching stability
    verify_matching(n, hospital_prefs, student_prefs, matching)
    


def main():
    if len(sys.argv) != 3:
        print("Command Usage:")
        print("  python main.py match <folder>")
        print("  python main.py verify <folder>")
        print("  python main.py both <folder>")
        sys.exit(1)

    mode = sys.argv[1]
    folder = sys.argv[2]

    if not os.path.isdir(folder):
        print(f"ERROR: Folder '{folder}' does not exist.")
        sys.exit(1)

    if mode == "match":
        run_match(folder)
    elif mode == "verify":
        run_verify(folder)
    elif mode == "both":
        run_both(folder)
    else:
        print("ERROR: Mode must be 'match', 'verify', or 'both'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
