# Lean certificate

**Rectangle cover injection**

For selected accepted diagonal pairs whose off-diagonal cross pairs are forbidden, choosing any covering product rectangle inside the accepting set gives an injective assignment of selected indices to rectangles.

The selection-size estimate, DNNF cover construction and exponential bounds are proved in the paper.

The principal checked declaration is `RectangleCover.selected_injection`. See [Structured bound from a fixed cut](../paper/manuscript.tex#L105) in the manuscript. [Lean source](Q515.lean) · [Verification workflow](../.github/workflows/lean.yml)

Replay with Lean 4.30.0 and its standard library from the repository root.

```sh
lean -DwarningAsError=true formalization/Q515.lean
```
