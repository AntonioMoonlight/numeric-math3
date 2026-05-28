from constants import IntegrationMethod
import matplotlib.pyplot as plt
import numpy as np


def create_function_plot(f, a, b):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(a, b, 100)
    vf = np.vectorize(f)
    try:
        y = vf(x)
    except:
        y = np.array([f(xi) if np.isfinite(f(xi)) else np.nan for xi in x])
    y_finite = y[np.isfinite(y)]

    if len(y_finite) > 0:
        y_min, y_max = np.min(y_finite), np.max(y_finite)
        p95 = np.percentile(np.abs(y_finite), 95)
        if y_max > p95 * 2:
            ax.set_ylim(y_min - 0.1, p95 * 2)

    ax.plot(x, y, color='gray', linewidth=2, label='f(x)')

    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    return fig


def create_integration_plot(f, a, b, n, method: IntegrationMethod):
    fig, ax = plt.subplots(figsize=(10, 5))
    n = int(n)

    x_fine = np.linspace(a, b, 500)
    vf = np.vectorize(f)
    y_fine = vf(x_fine)
    ax.plot(x_fine, y_fine, color='gray', linewidth=1, alpha=0.5, label='f(x)')

    y_finite = y_fine[np.isfinite(y_fine)]
    if len(y_finite) > 0:
        y_min, y_max = np.min(y_finite), np.max(y_finite)
        # Если разброс огромен (несобственный интеграл), ограничиваем по 5 и 95 перцентилям
        p_low, p_high = np.percentile(y_finite, [5, 95])
        margin = (p_high - p_low) * 0.2 if p_high != p_low else 1.0
        ax.set_ylim(min(y_min, p_low - margin), max(y_max, p_high + margin))

    h = (b - a) / n
    x_nodes = np.linspace(a, b, n + 1)

    if method in [IntegrationMethod.LEFT_RECTANGLE,
                  IntegrationMethod.RIGHT_RECTANGLE,
                  IntegrationMethod.MIDPOINT_RECTANGLE]:
        if method == IntegrationMethod.LEFT_RECTANGLE:
            x_bar = x_nodes[:-1]
        elif method == IntegrationMethod.RIGHT_RECTANGLE:
            x_bar = x_nodes[1:]
        else:
            x_bar = x_nodes[:-1] + h / 2

        y_bar = vf(x_bar)
        ax.bar(x_nodes[:-1], y_bar, width=h, align='edge', alpha=0.3,
               facecolor='skyblue', edgecolor='navy')

    elif method == IntegrationMethod.TRAPEZOIDAL:
        y_nodes = vf(x_nodes)
        ax.fill_between(x_nodes, 0, y_nodes, alpha=0.3,
                        facecolor='lightgreen', edgecolor='green')

    elif method == IntegrationMethod.SIMPSON:
        x_parts = []
        y_parts = []
        for i in range(0, n, 2):
            x_triplet = x_nodes[i:i + 3]
            y_triplet = vf(x_triplet)

            poly_coeffs = np.polyfit(x_triplet, y_triplet, 2)
            p = np.poly1d(poly_coeffs)

            y_triplet = np.nan_to_num(y_triplet, nan=0, posinf=1e6, neginf=-1e6)

            p = np.poly1d(np.polyfit(x_triplet, y_triplet, 2))
            px = np.linspace(x_triplet[0], x_triplet[2], 15)
            x_parts.extend(px);
            y_parts.extend(p(px))
            x_parts.append(None);
            y_parts.append(None)

        ax.fill_between(np.array(x_parts, dtype=float), 0, np.array(y_parts, dtype=float),
                        alpha=0.3, facecolor='plum', edgecolor='purple')

    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    return fig