import numpy as np

def integrate_trapezoidal(f, a, b, n):
    """
    Computes the definite integral of function f from a to b using the Trapezoidal Rule.
    
    :param f: Callable function
    :param a: Lower bound of integration
    :param b: Upper bound of integration
    :param n: Number of subintervals
    :return: Approx integral value
    """
    x = np.linspace(a, b, n + 1)
    y = f(x)
    try:
        from scipy.integrate import trapezoid
        result = trapezoid(y, x=x)
    except ImportError:
        # Fallback to numpy if scipy's trapezoid isn't available
        result = np.trapz(y, x)
    return float(result)
