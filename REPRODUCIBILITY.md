# Reproducibility

Run from the repository root with Python 3.11 or later and Git.

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The standard-library replay checks 1,380,708 mixed rectangles across all 62 nontrivial oriented cuts of K4. For sides with at most eight assignments it uses all nonempty subsets. For larger sides it uses singletons and pairs. It checks 13,034 nonempty affine matrix/cut/charge cases and 683 exact syndrome-circuit constructions. For the four-singleton syndrome matrix it considers all 65,536 acceptance masks. The fixed-cut inequality has a nonempty retained set in 61,440 of them. The replay also checks the illustrated overlap and the one-bit boundary. [Expected output](verification/logs/replay.txt)

The graph-family and general-width arguments are in the paper. [Build the manuscript](paper/BUILD.md) · [Rebuild the animation and explorer](visualization/README.md)
