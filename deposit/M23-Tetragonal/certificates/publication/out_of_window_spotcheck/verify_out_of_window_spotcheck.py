#!/usr/bin/env python3
"""Adversarial out-of-window spot check for the exact tetragonal relation.

This check evaluates the homogenized relation modulo the monic degree-23
model at base values far outside the 971-point characteristic-zero proof
window and at three primes absent from the reconstruction and retained-prime
sets. It is an independent regression test, not a substitute for the exact
characteristic-zero proof.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "certificates" / "exact_tetragonal_v93"
T, V = sp.symbols("t v")
Q = sp.Poly(T * T + 23, T, domain=sp.ZZ)


def parse_integral_model() -> list[sp.Poly]:
    source = (BASE / "M23_qpair_full_rows_p100207139_v86.m").read_text()
    coefficients: dict[int, sp.Poly] = {}
    for j in range(2, 24):
        match = re.search(rf"b\[{j}\]\s*:=\s*(.*?);", source, re.S)
        if match is None:
            raise RuntimeError(f"missing coefficient b[{j}] in Magma source")
        expression = sp.sympify(
            re.sub(r"\s+", " ", match.group(1)).replace("^", "**"),
            locals={"t": T},
        )
        coefficients[j] = sp.Poly(expression, T, domain=sp.ZZ)

    model = [sp.Poly(0, T, domain=sp.ZZ) for _ in range(24)]
    model[23] = sp.Poly(1, T, domain=sp.ZZ)
    for j in range(2, 24):
        model[23 - j] = coefficients[j] * (Q ** (j - (5 * j) // 23))
    return model


def parse_adjoints() -> list[list[sp.Poly]]:
    result: list[list[sp.Poly]] = []
    for name in ("M23_H1_integer_v91.txt", "M23_H2_integer_v91.txt"):
        expression = sp.sympify((BASE / name).read_text(), locals={"t": T, "v": V})
        polynomial = sp.Poly(expression, V, domain=sp.ZZ[T])
        homogeneous: list[sp.Poly] = []
        for j in range(22):
            coefficient = sp.Poly(polynomial.nth(j), T, domain=sp.ZZ)
            if j <= 18:
                transformed = coefficient * (Q ** (18 - j))
            else:
                denominator = Q ** (j - 18)
                transformed, remainder = sp.div(coefficient, denominator, domain=sp.ZZ)
                if not remainder.is_zero:
                    raise RuntimeError(f"adjoint coefficient v^{j} is not q-divisible")
            homogeneous.append(transformed)
        result.append(homogeneous)
    return result


def parse_relation() -> list[sp.Poly]:
    data = json.loads((BASE / "M23_tetragonal_coeffs_v92.json").read_text())
    coefficients = data["primitive_integer_coeffs"]
    if len(coefficients) != 120:
        raise RuntimeError(f"expected 120 relation coefficients, found {len(coefficients)}")
    return [
        sp.Poly(sum(coefficients[5 * k + d] * T**d for d in range(5)), T, domain=sp.ZZ)
        for k in range(24)
    ]


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def check_specialization(
    t_value: int,
    prime: int,
    model_polys: list[sp.Poly],
    adjoints: list[list[sp.Poly]],
    relation_polys: list[sp.Poly],
) -> bool:
    def evaluate(poly: sp.Poly) -> int:
        return int(poly.eval(t_value)) % prime

    model = [evaluate(poly) for poly in model_polys]
    if model[23] != 1:
        raise RuntimeError("specialized model is not monic")

    h1 = trim([evaluate(poly) for poly in adjoints[0]])
    h2 = trim([evaluate(poly) for poly in adjoints[1]])
    relation = [evaluate(poly) for poly in relation_polys]

    def add(left: list[int], right: list[int]) -> list[int]:
        result = [0] * max(len(left), len(right))
        for index, value in enumerate(left):
            result[index] = (result[index] + value) % prime
        for index, value in enumerate(right):
            result[index] = (result[index] + value) % prime
        return trim(result)

    def scale(poly: list[int], scalar: int) -> list[int]:
        return trim([(value * scalar) % prime for value in poly])

    def multiply_mod(left: list[int], right: list[int]) -> list[int]:
        product = [0] * (len(left) + len(right) - 1)
        for i, x in enumerate(left):
            for j, y in enumerate(right):
                product[i + j] = (product[i + j] + x * y) % prime
        if len(product) < 24:
            product.extend([0] * (24 - len(product)))
        for degree in range(len(product) - 1, 22, -1):
            leading = product[degree] % prime
            if leading:
                shift = degree - 23
                for index in range(23):
                    product[shift + index] = (
                        product[shift + index] - leading * model[index]
                    ) % prime
        return trim([value % prime for value in product[:23]])

    accumulator = [relation[23]]
    h2_power = [1]
    for k in range(22, -1, -1):
        h2_power = multiply_mod(h2_power, h2)
        accumulator = add(
            multiply_mod(accumulator, h1),
            scale(h2_power, relation[k]),
        )
    return accumulator == [0]


def main() -> None:
    primes = (1_000_000_007, 1_000_000_009, 1_000_000_033)
    t_values = (987_654_321, 555_444_333, 271_828_182)
    if not all(sp.isprime(prime) for prime in primes):
        raise RuntimeError("one of the declared test moduli is not prime")

    model = parse_integral_model()
    adjoints = parse_adjoints()
    relation = parse_relation()

    print("M23_OUT_OF_WINDOW_SPOTCHECK_BEGIN")
    count = 0
    for prime in primes:
        for t_value in t_values:
            passed = check_specialization(t_value, prime, model, adjoints, relation)
            count += 1
            print(f"p={prime} t={t_value} zero={passed}")
            if not passed:
                raise SystemExit(1)
    print(f"TOTAL_SUBCHECKS={count}")
    print("PROOF_WINDOW=[-485,485]")
    print("ALL_TEST_VALUES_OUTSIDE_PROOF_WINDOW=true")
    print("M23_OUT_OF_WINDOW_SPOTCHECK_PASS")


if __name__ == "__main__":
    main()
