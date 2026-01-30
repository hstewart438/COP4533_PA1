# Stable Matching (Gale-Shapley)

Implementation of the Gale-Shapley algorithm for the hospital-student stable matching problem.

## Usage

**Linux (bash):**
```bash
python src/main.py match tests/<folder>
python src/main.py match tests/<folder>/<file>.in
python src/main.py verify tests/<folder>
python src/main.py both tests/<folder>
```

**macOS:** Use `python3` instead of `python`:
```bash
python3 src/main.py match tests/<folder>
python3 src/main.py match tests/<folder>/<file>.in
python3 src/main.py verify tests/<folder>
python3 src/main.py both tests/<folder>
```

### Commands

- **match** — Accepts either a folder (which must contain exactly one `.in` file) or a path to a specific `.in` file. Runs the Gale-Shapley algorithm on that input, prints the matching, and writes the result to a `.out` file (same base name as the `.in`, in the same directory). Proposal count and runtime are printed to stderr.

- **verify** — The folder must contain `verify.in` and `verify.out`. Reads the matching from `verify.out` and checks that it is a valid stable matching for the preferences in `verify.in`. Prints `VALID STABLE` or reports if the matching is invalid.

- **both** — The folder may contain one or more `.in` files. For each `.in` file (in sorted order), runs Gale-Shapley, writes the corresponding `.out` file, and then verifies the matching is stable. Combines match and verify for each input file.

### Clearing output files

To remove all `.out` files from `tests/large_tests`:

```bash
rm tests/large_tests/*.out
```

### Testing large_tests

Run match and verify on every `.in` file in `tests/large_tests`:

```bash
python src/main.py both tests/large_tests
```

## Input Format

```
n
<n lines of hospital preferences>
<n lines of student preferences>
```

See `src/input/example.in` for reference.

## Output

Prints hospital-student pairs (1-indexed). Proposal count and runtime go to stderr.

## Performance

Runtime vs. number of inputs (from `tests/large_tests`):

![Time vs Number of Inputs](assets/time-vs-inputs.png)

**Analysis:** As the number of inputs increases, runtime (in seconds) increases. The curve is relatively flat for small inputs (e.g., up to ~64) and then steepens for larger inputs (128, 256, 512). So the algorithm takes longer as problem size grows, and the growth in time accelerates at higher input sizes rather than increasing at a constant rate.
