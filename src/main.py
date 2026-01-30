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


def find_all_input_files(folder):
    # Find all .in files in the folder (sorted by name)
    in_files = sorted(
        f for f in os.listdir(folder)
        if f.endswith(".in")
    )
    return [(f, os.path.join(folder, f)) for f in in_files]

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


def run_match(folder_or_file):
    # Accept either a folder (with exactly one .in) or a path to a specific .in file
    if os.path.isfile(folder_or_file):
        if not folder_or_file.endswith(".in"):
            print("MATCH MODE ERROR: File must have .in extension.")
            sys.exit(1)
        input_path = os.path.abspath(folder_or_file)
        folder = os.path.dirname(input_path)
        infile = os.path.basename(input_path)
    else:
        infile, input_path = find_input_file(folder_or_file)
        folder = folder_or_file

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

def run_both_single(folder, infile, input_path):
    """Run match + verify for one .in file."""
    try:
        n, hospital_prefs, student_prefs = read_input(input_path)
    except ValueError as e:
        print(e)
        sys.exit(1)

    start = time.perf_counter()
    matching, numProposals = galeShapley(n, hospital_prefs, student_prefs)
    end = time.perf_counter()

    print("\nFinal Matching (Hospital Student):")
    for hospital in sorted(matching.keys()):
        print(f"{hospital} {matching[hospital]}")

    sys.stderr.write(f"\nNumber of proposals: {numProposals}")
    sys.stderr.write(f"\nMatching runtime: {end - start:.6f} seconds\n")

    outfile = os.path.splitext(infile)[0] + ".out"
    output_path = os.path.join(folder, outfile)
    write_output_file(output_path, n, matching)

    verify_matching(n, hospital_prefs, student_prefs, matching)


def run_both(folder):
    # Find all .in files in the folder (supports multiple)
    in_file_list = find_all_input_files(folder)
    if not in_file_list:
        print("BOTH MODE ERROR: No .in files found in folder.")
        sys.exit(1)

    for i, (infile, input_path) in enumerate(in_file_list):
        if i > 0:
            print("\n" + "=" * 60)
        print(f"--- {infile} ---")
        run_both_single(folder, infile, input_path)
    


def main():
    if len(sys.argv) != 3:
        print("Command Usage:")
        print("  python main.py match <folder>")
        print("  python main.py match <path/to/file.in>")
        print("  python main.py verify <folder>")
        print("  python main.py both <folder>")
        sys.exit(1)

    mode = sys.argv[1]
    path_arg = sys.argv[2]

    if mode == "match":
        if not os.path.isdir(path_arg) and not os.path.isfile(path_arg):
            print(f"ERROR: Path '{path_arg}' does not exist.")
            sys.exit(1)
        run_match(path_arg)
    elif mode == "verify":
        if not os.path.isdir(path_arg):
            print(f"ERROR: Folder '{path_arg}' does not exist.")
            sys.exit(1)
        run_verify(path_arg)
    elif mode == "both":
        if not os.path.isdir(path_arg):
            print(f"ERROR: Folder '{path_arg}' does not exist.")
            sys.exit(1)
        run_both(path_arg)
    else:
        print("ERROR: Mode must be 'match', 'verify', or 'both'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
