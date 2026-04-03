import sympy as sp
import numpy as np
from sympy.parsing.sympy_parser import (
    parse_expr, 
    standard_transformations, 
    convert_xor, 
    implicit_multiplication_application,
    function_exponentiation,
    implicit_application
)

def parse_function(func_str: str):
    """
    Parses a string representing a mathematical function into a callable Python function.
    
    :param func_str: String representation of the function (e.g., 'x**2 + sin(x)')
    :return: A callable that takes a numpy array/number and returns a numpy array/number
    """
    try:
        # Define the symbol
        x = sp.Symbol('x')
        
        # Enhanced parsing transformations to support practically any standard mathematical notation
        transformations = standard_transformations + (
            convert_xor, 
            implicit_multiplication_application, 
            function_exponentiation,  # Allows things like sin^2(x)
            implicit_application       # Allows things like sin x
        )
        
        # Extended dictionary for constants, specific base logs, and trig function aliases
        custom_dict = {
            'e': sp.E, 
            'pi': sp.pi,
            'ln': sp.log,
            'log10': lambda arg: sp.log(arg, 10),
            'log2': lambda arg: sp.log(arg, 2),
            'arcsin': sp.asin,
            'arccos': sp.acos,
            'arctan': sp.atan
        }
        
        # Parse the expression
        expr = parse_expr(func_str, local_dict=custom_dict, transformations=transformations)
        
        # Create a lambda function. We use 'numpy' module so it can broadcast over np arrays.
        callable_func = sp.lambdify(x, expr, 'numpy')
        
        # Test the callable to catch invalid Math/errors early
        test_val = callable_func(np.array([1.0, 2.0]))
        
        # If the output is a scalar (e.g., f(x) = 5), we wrap it to ensure it returns an array when given an array
        def wrapped_func(inputs):
            res = callable_func(inputs)
            if np.isscalar(res) and isinstance(inputs, np.ndarray):
                return np.full_like(inputs, res, dtype=float)
            return res

        return wrapped_func
    except Exception as e:
        raise ValueError(f"Invalid function string: '{func_str}'. Details: {e}")
