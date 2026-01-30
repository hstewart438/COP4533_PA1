# Stable Matching (Gale-Shapley)

Implementation of the Gale-Shapley algorithm for the hospital-student stable matching problem.

## Usage

```
bash
    python src/main.py match tests/<folder>
    python src/main.py verify tests/<folder>
    python src/main.py both tests/<folder>
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
