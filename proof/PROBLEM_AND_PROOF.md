# Problem and proof

Can every strong approximation of a Tseitin code still require exponential DNNF size when disjunctions may overlap? The error counts false positives and false negatives relative to the number of codewords. [Exact source question](https://alexisdec.github.io/assets/pdf/thesis_deColnet.pdf#page=74)

1. On the cubic hard family, each variable tree has an edge cut where the largest rectangle contained wholly in the code is exponentially sparse.
2. A pair belongs to the code when its partial parity vectors match. The true part of any mixed rectangle splits into matching syndrome blocks. Each block is small by the hard-cut bound, and Cauchy–Schwarz bounds their total by the square root of the rectangle size times the block cap.
3. A single rectangle contained in the accepting set has at most the global number of false positives. This converts the square-root inequality into an exponential upper bound on true points per hard-cut rectangle.
4. Each accepted assignment yields a trace vtree. At its hard cut, the corresponding gate induces one accepting rectangle. Each gate can be chosen once in a cover, and the total true points that must be covered are a fixed fraction of the code.

For a general nonempty affine binary code, the number of matched syndrome blocks is exactly the exponential of the cut's rank width. The same inequality gives the ordinary bound. To strengthen the structured bound, sample one point per matched block, discard rejected ones, and find many retained points with rejected cross-pairs. A deterministic circuit can also build the exact code by combining feasible syndrome states bottom up. [Full proof](../paper/manuscript.pdf)
