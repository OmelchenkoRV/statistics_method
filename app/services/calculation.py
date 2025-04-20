import numpy as np


def compute_service_stats(price, support_cost, daily_orders, n_days):
    """
    Computes statistics for a single service.
    """
    net_margin = price - support_cost
    x_ij = daily_orders * net_margin
    W_j = daily_orders / n_days
    expected_profit = np.sum(x_ij * W_j)
    risk = np.sqrt(np.sum(W_j * (x_ij - expected_profit) ** 2))
    profit_range = (expected_profit - 2 * risk, expected_profit + 2 * risk)
    return expected_profit, risk, profit_range


def calculate_package_statistics(prices: np.ndarray,
                                 support_costs: np.ndarray,
                                 orders: dict,
                                 n_days: int):
    """
    Calculates statistics for each service and the overall package.
    """
    service_names = list(orders.keys())
    results = {}

    total_expected = 0.0
    total_risk = 0.0
    lower_sum = 0.0
    upper_sum = 0.0

    for i, service in enumerate(service_names):
        exp_profit, risk, profit_range = compute_service_stats(
            prices[i], support_costs[i], orders[service], n_days)
        results[service] = {
            'expected_profit': exp_profit,
            'risk': risk,
            'profit_range': profit_range
        }
        total_expected += exp_profit
        total_risk += risk
        lower_sum += profit_range[0]
        upper_sum += profit_range[1]

    package_stats = {
        'total_expected_profit': total_expected,
        'total_risk': total_risk,
        'overall_profit_range': (lower_sum, upper_sum)
    }

    return results, package_stats
