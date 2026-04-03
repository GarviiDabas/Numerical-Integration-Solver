import numpy as np

def integrate_simpson(f, a, b, n):
    """
    Computes the definite integral of function f from a to b using Simpson's Rule.
    
    :param f: Callable function
    :param a: Lower bound of integration
    :param b: Upper bound of integration
    :param n: Number of subintervals (must be even)
    :return: Approx integral value
    """
    if n % 2 != 0:
        raise ValueError("Number of subintervals (n) must be even for Simpson's Rule.")
        
    x = np.linspace(a, b, n + 1)
    y = f(x)
    try:
        from scipy.integrate import simpson
        result = simpson(y, x=x)
    except ImportError:
        from scipy.integrate import simps
        result = simps(y, x=x)
    return float(result)
