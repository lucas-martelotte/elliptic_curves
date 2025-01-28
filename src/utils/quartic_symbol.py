from .gaussian_integers import (
    coprime,
    factor_gaussian_integer,
    fast_modular_exp,
    gaussian_norm,
    is_unit,
    mod,
)


def quartic_symbol(a: complex, b: complex) -> complex:
    """Computes the quartic symbol [a / b]"""
    if not coprime(a, b):
        return 0
    output: complex = 1
    # print(f"Factors of {b}: {factor_gaussian_integer(b)}")
    for b_factor, b_factor_power in factor_gaussian_integer(b).items():
        if is_unit(b_factor):
            continue
        exponent = (gaussian_norm(b_factor) - 1) // 4
        curr_output: complex = 1
        for _ in range(exponent):
            curr_output = mod(curr_output * a, b_factor)
        output *= curr_output**b_factor_power
        # output *= mod(mod(a, b_factor) ** exponent, b_factor)
    assert is_unit(output)
    return output
