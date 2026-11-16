import sympy as sp

def calculate_gradient(fn, n_vars):
    variables = sp.symbols(f"x_0:{n_vars}", real=True)
    local_dict = {
        f"x_{i}": variables[i]
        for i in range(n_vars)
    }

    objective = sp.sympify(fn, locals=local_dict)

    gradient = [
        sp.diff(objective, variable)
        for variable in variables
    ]

    return gradient


def build_lagrangian(fn, constraints, n_vars):

    variables = sp.symbols(f"x_0:{n_vars}", real=True)

    local_dict = {
        f"x_{i}": variables[i]
        for i in range(n_vars)
    }

    objective = sp.sympify(fn, locals=local_dict)

    lagrangian = objective

    for i, constraint in enumerate(constraints):

        multiplier = sp.Symbol(f"lambda_{i}", real=True)

        constraint_expr = sp.sympify(
            constraint,
            locals=local_dict
        )

        lagrangian += multiplier * constraint_expr

    return lagrangian


def find_lagrange_candidates(fn, constraints, n_vars):

    variables = sp.symbols(f"x_0:{n_vars}", real=True)

    local_dict = {
        f"x_{i}": variables[i]
        for i in range(n_vars)
    }

    multipliers = sp.symbols(
        f"lambda_0:{len(constraints)}",
        real=True
    )

    local_dict.update({
        f"lambda_{i}": multipliers[i]
        for i in range(len(constraints))
    })

    lagrangian = build_lagrangian(
        fn,
        constraints,
        n_vars
    )

    equations = [
        sp.diff(lagrangian, variable)
        for variable in variables
    ]

    for constraint in constraints:
        constraint_expr = sp.sympify(
            constraint,
            locals=local_dict
        )

        equations.append(constraint_expr)

    unknowns = list(variables) + list(multipliers)

    solutions = sp.solve(
        equations,
        unknowns,
        dict=True
    )

    candidates = []

    for solution in solutions:

        point = []
        valid = True

        for variable in variables:

            if variable not in solution:
                valid = False
                break

            value = sp.simplify(solution[variable])

            if value.free_symbols:
                valid = False
                break

            try:
                numeric_value = complex(sp.N(value, 30))
            except (TypeError, ValueError, OverflowError):
                valid = False
                break

            if abs(numeric_value.imag) > 1e-9:
                valid = False
                break

            point.append(float(numeric_value.real))

        if not valid:
            continue

        substitutions = dict(zip(variables, point))

        for constraint in constraints:

            constraint_expr = sp.sympify(
                constraint,
                locals=local_dict
            )

            try:
                residual = complex(
                    sp.N(
                        constraint_expr.subs(substitutions),
                        30
                    )
                )
            except (TypeError, ValueError, OverflowError):
                valid = False
                break

            if abs(residual) > 1e-7:
                valid = False
                break

        if not valid:
            continue

        duplicate = any(
            all(
                abs(a - b) <= 1e-8
                for a, b in zip(point, existing)
            )
            for existing in candidates
        )

        if not duplicate:
            candidates.append(point)

    return candidates


def Lagrange_Equality(fn, constraints, n_vars=2, minimize=True):

    candidates = find_lagrange_candidates(
        fn,
        constraints,
        n_vars
    )

    if not candidates:
        return None, None

    variables = sp.symbols(f"x_0:{n_vars}", real=True)

    local_dict = {
        f"x_{i}": variables[i]
        for i in range(n_vars)
    }

    objective = sp.sympify(fn, locals=local_dict)

    evaluated_candidates = []

    for point in candidates:

        substitutions = dict(zip(variables, point))

        value = sp.N(
            objective.subs(substitutions),
            30
        )

        evaluated_candidates.append(
            (point, float(value))
        )

    if minimize:
        best_point, best_value = min(
            evaluated_candidates,
            key=lambda item: item[1]
        )
    else:
        best_point, best_value = max(
            evaluated_candidates,
            key=lambda item: item[1]
        )

    best_point = [
        round(float(value), 4)
        for value in best_point
    ]

    best_value = round(float(best_value), 4)

    return best_point, best_value


if __name__ == "__main__":

    print(
        Lagrange_Equality(
            "x_0**2 + x_1**2",
            ["x_0 + x_1 - 2"],
            n_vars=2,
            minimize=True
        )
    )