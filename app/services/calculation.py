import numpy as np


def compute_service_stats(price, support_cost, daily_orders, n_days):
    """
    Computes statistics for a service.

    Parameters:
        price (float): Price for the service.
        support_cost (float): Cost for supporting the service.
        daily_orders (np.array): Array with the number of orders for each day.
        n_days (int): Total number of days.

    Returns:
        tuple: expected_profit (float), risk (float), profit_range (tuple)
    """
    net_margin = price - support_cost
    # Calculate daily profit: x_ij = orders * net_margin
    x_ij = daily_orders * net_margin
    # Relative frequency W_j = orders / n_days
    W_j = daily_orders / n_days
    # Expected profit for the service
    expected_profit = np.sum(x_ij * W_j)
    # Risk (standard deviation):
    risk = np.sqrt(np.sum(W_j * (x_ij - expected_profit) ** 2))
    # Profit range: [expected_profit - 2*risk, expected_profit + 2*risk]
    profit_range = (expected_profit - 2 * risk, expected_profit + 2 * risk)
    return expected_profit, risk, profit_range


def calculate_package_statistics(prices, support_costs, orders, n_days):
    """
    Calculates statistics for each service and the overall package.

    Parameters:
        prices (np.array): Array of prices for each service.
        support_costs (np.array): Array of support costs for each service.
        orders (dict): Dictionary with keys as service names and values as np.array of daily orders.
        n_days (int): Number of days.

    Returns:
        dict: A dictionary with individual service statistics and package aggregates.
    """
    service_names = list(orders.keys())
    results = {}

    total_expected = 0.0
    total_risk = 0.0
    total_range_lower = 0.0
    total_range_upper = 0.0

    # Compute stats for each service
    for i, service in enumerate(service_names):
        exp_profit, risk, profit_range = compute_service_stats(prices[i], support_costs[i], orders[service], n_days)
        results[service] = {
            'expected_profit': exp_profit,
            'risk': risk,
            'profit_range': profit_range
        }
        total_expected += exp_profit
        total_risk += risk
        total_range_lower += profit_range[0]
        total_range_upper += profit_range[1]

    package_stats = {
        'total_expected_profit': total_expected,
        'total_risk': total_risk,
        'overall_profit_range': (total_range_lower, total_range_upper)
    }

    return results, package_stats
