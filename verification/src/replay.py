"""Exact finite checks for the Tseitin and affine-code arguments."""

from collections import Counter
from functools import lru_cache
from itertools import combinations, product

SYMBOLS = range(4)


def syndrome(columns, assignment):
    value = 0
    for index, column in enumerate(columns):
        if assignment >> index & 1:
            value ^= column
    return value


def rank(columns):
    pivots = {}
    for value in columns:
        while value:
            bit = value.bit_length()
            if bit not in pivots:
                pivots[bit] = value
                break
            value ^= pivots[bit]
    return len(pivots)


def side_counts(syndromes):
    size = len(syndromes)
    if size <= 8:
        masks = ([index for index in range(size) if mask >> index & 1]
                 for mask in range(1, 1 << size))
    else:
        masks = (selection for count in (1, 2) for selection in combinations(range(size), count))
    return [(len(selection), Counter(syndromes[i] for i in selection)) for selection in masks]


def check_tseitin_rectangles():
    columns = tuple((1 << i) | (1 << j) for i, j in combinations(range(4), 2))
    tested = 0
    for mask in range(1, (1 << len(columns)) - 1):
        a = tuple(x for i, x in enumerate(columns) if mask >> i & 1)
        b = tuple(x for i, x in enumerate(columns) if not mask >> i & 1)
        left = tuple(syndrome(a, x) for x in range(1 << len(a)))
        right = tuple(syndrome(b, y) for y in range(1 << len(b)))
        left_total, right_total = Counter(left), Counter(right)
        block_sizes = [count * right_total[s] for s, count in left_total.items() if s in right_total]
        assert block_sizes and sum(block_sizes) == 8
        assert len(block_sizes) == 1 << (rank(a) + rank(b) - rank(columns))
        assert len(set(block_sizes)) == 1
        cap = block_sizes[0]
        for a_size, a_counts in side_counts(left):
            for b_size, b_counts in side_counts(right):
                t = sum(count * b_counts[s] for s, count in a_counts.items())
                assert t * t <= cap * a_size * b_size
                tested += 1
    return tested


def check_affine_width():
    cut_cases = 0
    for columns in product(SYMBOLS, repeat=4):
        total_rank = rank(columns)
        for mask in range(1, 15):
            left = tuple(h for i, h in enumerate(columns) if mask >> i & 1)
            right = tuple(h for i, h in enumerate(columns) if not mask >> i & 1)
            a = Counter(syndrome(left, x) for x in range(1 << len(left)))
            b = Counter(syndrome(right, y) for y in range(1 << len(right)))
            width = rank(left) + rank(right) - total_rank
            for charge in SYMBOLS:
                sizes = [count * b[s ^ charge] for s, count in a.items() if s ^ charge in b]
                if not sizes:
                    continue
                assert len(sizes) == 1 << width and len(set(sizes)) == 1
                assert sum(sizes) == 1 << (len(columns) - total_rank)
                assert all(a[s] * b[t] == sizes[0] for s in a for t in b)
                cut_cases += 1
    return cut_cases


@lru_cache(maxsize=None)
def vtrees(leaves):
    if len(leaves) == 1:
        return (leaves[0],)
    trees = []
    for mask in range(1, (1 << len(leaves)) - 1, 2):
        left = tuple(x for i, x in enumerate(leaves) if mask >> i & 1)
        right = tuple(x for i, x in enumerate(leaves) if not mask >> i & 1)
        trees += list(product(vtrees(left), vtrees(right)))
    return tuple(trees)


def check_syndrome_circuits():
    def build(tree, states, columns):
        if isinstance(tree, int):
            return (tree,), {s: {x << tree for x in range(2) if syndrome((columns[tree],), x) == s} for s in states[(tree,)]}
        left_vars, left_gates = build(tree[0], states, columns)
        right_vars, right_gates = build(tree[1], states, columns)
        variables = tuple(sorted(left_vars + right_vars))
        gates = {}
        for state in states[variables]:
            result = set()
            for (u, xa), (v, xb) in product(left_gates.items(), right_gates.items()):
                if u ^ v == state:
                    branch = {a | b for a, b in product(xa, xb)}
                    assert result.isdisjoint(branch)
                    result |= branch
            gates[state] = result
        return variables, gates

    def leaves_of(tree, available):
        if isinstance(tree, int):
            return (tree,)
        parts = tuple(sorted(leaves_of(tree[0], available) + leaves_of(tree[1], available)))
        available.add(parts)
        return parts

    cases = 0
    for n in range(1, 4):
        variables = tuple(range(n))
        for columns in product(SYMBOLS, repeat=n):
            full = [syndrome(columns, x) for x in range(1 << n)]
            for charge in set(full):
                expected = {x for x in range(1 << n) if full[x] == charge}
                for tree in vtrees(variables):
                    parts = {(x,) for x in variables}
                    leaves_of(tree, parts)
                    states = {}
                    for subset in parts:
                        supported_columns = tuple(columns[i] if i in subset else 0 for i in variables)
                        states[subset] = {syndrome(supported_columns, x) for x in expected}
                    _, actual = build(tree, states, columns)
                    assert actual[charge] == expected
                    cases += 1
    return cases


def check_all_four_syndrome_accepting_sets():
    def yes(mask, i, j):
        return bool(mask >> (4 * i + j) & 1)

    states = 0
    edges = tuple(combinations(SYMBOLS, 2))
    for mask in range(1 << 16):
        retained = tuple(i for i in SYMBOLS if yes(mask, i, i))
        y = len(retained)
        if not y:
            continue
        d = sum(yes(mask, i, j) or yes(mask, j, i) for i, j in combinations(retained, 2))
        false_count = bin(mask).count("1") - y
        assert d <= false_count
        best = 0
        for bits in range(1, 1 << y):
            candidate = {i for k, i in enumerate(retained) if bits >> k & 1}
            if all(i not in candidate or j not in candidate or not (yes(mask, i, j) or yes(mask, j, i))
                   for i, j in edges):
                best = max(best, len(candidate))
        assert best * (y + 2 * d) >= y * y
        assert best * (y + 2 * false_count) >= y * y
        states += 1
    return states


def check_example():
    code = {(i, i) for i in SYMBOLS}
    first = set(product((0, 1), (1,)))
    second = set(product((0,), (0, 1)))
    square = set(product((0, 1), repeat=2))
    assert first & second == {(0, 1)}
    assert len((first | second | code) - code) == 1
    assert len(first - code) + len(second - code) == 2
    true_count = len(square & code)
    assert true_count == 2 and len(square - code) == 2
    assert true_count**2 == len(square)
    # Nonempty one-bit affine codes are both points or either singleton.
    assert [{x for x in (0, 1) if syndrome((h,), x) == b}
            for (h, b) in ((0, 0), (1, 0), (1, 1))] == [{0, 1}, {0}, {1}]


def main():
    print(f"K4: {check_tseitin_rectangles():,} rectangles across all 62 nontrivial oriented cuts.")
    print(f"Affine fibers: {check_affine_width():,} nonempty matrix/cut/charge cases.")
    print(f"Exact syndrome circuits: {check_syndrome_circuits():,} matrix/charge/vtree cases.")
    checked = check_all_four_syndrome_accepting_sets()
    assert checked + (1 << 12) == 1 << 16
    print(f"Structured bound: {checked:,} nonempty-retained cases and 4,096 vacuous cases.")
    check_example()
    print("The four-syndrome overlap illustration and one-bit boundary cases passed.")


if __name__ == "__main__":
    main()
