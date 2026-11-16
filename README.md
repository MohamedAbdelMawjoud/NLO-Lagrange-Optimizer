# Nonlinear Optimization (NLO)

## Equality-Constrained Optimization Using Lagrange Multipliers

**Course:** Nonlinear Optimization (NLO)  
**Semester:** Fall 2026  
**University:** Alexandria University  
**Faculty:** Faculty of Computers and Data Science  
**Programming Language:** Python  
**Allowed Library:** SymPy

---

## Project Overview

This project implements equality-constrained optimization using the **Lagrange Multipliers Method**.

The program constructs the Lagrangian function, derives the first-order necessary conditions, solves the resulting system of equations together with the equality constraints, and evaluates the feasible candidate points to identify the requested minimum or maximum.

The implementation supports multiple decision variables and one or more equality constraints.

## Mathematical Background

The optimization problem is defined as:

Minimize or Maximize:

\[
f(x_0,x_1,\ldots,x_n)
\]

Subject to:

\[
g_i(x)=0
\]

The Lagrangian function is constructed as:

\[
L(x,\lambda)=f(x)+\sum_{i=0}^{m-1}\lambda_i g_i(x)
\]

The first-order conditions are:

\[
\frac{\partial L}{\partial x_j}=0
\]

for every decision variable, together with all equality constraints:

\[
g_i(x)=0
\]

The resulting system is solved simultaneously to obtain feasible Lagrange candidate points.

The objective function is then evaluated at each candidate to select the smallest or largest value.

## Implemented Functions

### 1. `calculate_gradient(fn, n_vars)`

Calculates the symbolic partial derivatives of the objective function with respect to all decision variables.

**Returns:** A list of SymPy expressions representing the gradient.

### 2. `build_lagrangian(fn, constraints, n_vars)`

Constructs the Lagrangian function by combining the objective function with all equality constraints and their corresponding Lagrange multipliers.

**Returns:** A symbolic SymPy expression.

### 3. `find_lagrange_candidates(fn, constraints, n_vars)`

Solves the first-order Lagrange equations simultaneously with all equality constraints.

It filters the results to retain distinct, isolated, real, feasible candidate points and excludes the Lagrange multipliers from the returned coordinates.

**Returns:** A list of candidate coordinate lists.

### 4. `Lagrange_Equality(fn, constraints, n_vars=2, minimize=True)`

Evaluates the objective function at all feasible candidate points and selects the minimum or maximum according to the `minimize` parameter.

**Returns:**

- `best_point`: A list of Python floats.
- `best_value`: A Python float.

Numerical outputs are rounded to four decimal places. If no isolated real feasible candidate is found, the function returns `(None, None)`.

## Requirements

- Python 3.x
- SymPy

## Installation

Install SymPy using pip:

```bash
pip install sympy
```

## Usage

Import the required library and use the implemented functions:

```python
import sympy as sp

result = Lagrange_Equality(
    "x_0**2 + x_1**2",
    ["x_0 + x_1 - 2"],
    n_vars=2,
    minimize=True
)

print(result)
```

**Expected Output:**

```python
([1.0, 1.0], 2.0)
```

### Maximization Example

```python
result = Lagrange_Equality(
    "x_0",
    ["x_0**2 + x_1**2 - 1"],
    n_vars=2,
    minimize=False
)

print(result)
```

**Expected Output:**

```python
([1.0, 0.0], 1.0)
```

## Testing

The implementation can be tested using a dedicated test suite covering:

- Gradient calculation with two and three variables.
- Lagrangian construction with single and multiple constraints.
- Candidate generation with multiple real solutions.
- Minimization and maximization.
- Single-variable optimization.
- Multiple equality constraints.
- Cases with no real feasible solutions.

The tests use assertions to compare actual results against expected mathematical outputs.

## Project Structure

```text
NLO-Assignment-2/
│
├── StudentName_StudentID.py
├── README.md
└── tests/
    └── test_cases.py
```

## Implementation Restrictions

- SymPy is the only allowed external library.
- No built-in optimization algorithms are used.
- The Lagrangian construction and optimization procedure are implemented manually.
- The original required function signatures are preserved.
- No interactive input or external data files are required.

## Notes

This implementation selects the best objective value among the isolated, real, feasible Lagrange candidates.

It does not perform second-order classification or Hessian-based optimality tests.

---

**Course:** Nonlinear Optimization — Fall 2026  
**Assignment:** Task 2 — Equality-Constrained Optimization  
**Institution:** Alexandria University
