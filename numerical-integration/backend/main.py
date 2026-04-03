from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

from methods.trapezoidal import integrate_trapezoidal
from methods.simpson import integrate_simpson
from methods.gaussian import integrate_gaussian
from utils.parser import parse_function

app = FastAPI(title="Numerical Integration API")

class IntegrationRequest(BaseModel):
    function: str
    a: float
    b: float
    method: str
    n: int = 10

class IntegrationResponse(BaseModel):
    result: float
    x: list[float]
    y: list[float]

class CompareResponse(BaseModel):
    trapezoidal: float
    simpson: float
    gaussian: float

@app.post("/integrate", response_model=IntegrationResponse)
def compute_integral(request: IntegrationRequest):
    try:
        func = parse_function(request.function)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if request.b <= request.a:
        raise HTTPException(status_code=400, detail="Upper bound 'b' must be greater than lower bound 'a'.")

    # Generate x and y for plotting
    x_plot = np.linspace(request.a, request.b, 200)
    try:
        y_plot = func(x_plot)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error evaluating function: {e}")

    method = request.method.lower()
    
    try:
        if method == "trapezoidal":
            res = integrate_trapezoidal(func, request.a, request.b, request.n)
        elif method == "simpson":
            res = integrate_simpson(func, request.a, request.b, request.n)
        elif method == "gaussian":
            # Gaussian uses its own internal grid size usually, but we implemented fixed_quad with n=10
            res = integrate_gaussian(func, request.a, request.b)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method '{request.method}'.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return IntegrationResponse(
        result=float(res),
        x=x_plot.tolist(),
        y=y_plot.tolist()
    )


@app.post("/compare", response_model=CompareResponse)
def compare_methods(request: IntegrationRequest):
    try:
        func = parse_function(request.function)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if request.b <= request.a:
        raise HTTPException(status_code=400, detail="Upper bound 'b' must be greater than lower bound 'a'.")

    try:
        res_trap = integrate_trapezoidal(func, request.a, request.b, request.n)
        
        # ensure n is even for simpson
        n_simp = request.n if request.n % 2 == 0 else request.n + 1
        res_simp = integrate_simpson(func, request.a, request.b, n_simp)
        
        res_gauss = integrate_gaussian(func, request.a, request.b)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return CompareResponse(
        trapezoidal=float(res_trap),
        simpson=float(res_simp),
        gaussian=float(res_gauss)
    )
