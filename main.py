from fastapi import FastAPI
from app.models.request import CalculationRequest
from app.services.calculation import calculate_package_statistics
import numpy as np
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)


@app.get("/")
def read_root():
    return {"message": "Statistics service online!"}


@app.post("/compute")
def compute(request: CalculationRequest):
    logging.info("Computation request received")

    # Convert lists to numpy arrays
    prices = np.array(request.price, dtype=float)
    support_costs = np.array(request.support_cost, dtype=float)
    # Build orders dict: S1, S2, ... mapping to each row of daily_orders
    orders = {
        f"S{i + 1}": np.array(row, dtype=float)
        for i, row in enumerate(request.daily_orders)
    }

    # Calculate per-service and package-wide statistics
    per_service_stats, package_stats = calculate_package_statistics(
        prices,
        support_costs,
        orders,
        request.n_days
    )

    logging.info(f"Computation completed. Per-service: {per_service_stats}, Package: {package_stats}")

    return {
        "success": True,
        "per_service": per_service_stats,
        "package": package_stats
    }
