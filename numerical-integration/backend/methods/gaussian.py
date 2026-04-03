import scipy.integrate as spi

def integrate_gaussian(f, a, b):
    """
    Computes the definite integral of function f from a to b using Gaussian Quadrature.
    
    :param f: Callable function
    :param a: Lower bound of integration
    :param b: Upper bound of integration
    :return: Approx integral value
    """
    # We use quad for stable generic gaussian quadrature evaluation
    result, _ = spi.quad(f, a, b)
    return float(result)
