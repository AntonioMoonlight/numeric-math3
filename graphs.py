import matplotlib.pyplot as plt
import numpy as np
from constants import IntMethod


# --- В файле graphs.py ---

def create_integration_plot(f, a, b, n, method: IntMethod):
    # Защита от n=0 (если интеграл разошелся)
    if n <= 0:
        return plt.figure()

    MAX_PLOT_N = 1000
    n_plot = int(min(n, MAX_PLOT_N))
    if method == IntMethod.SIMPSON and n_plot % 2 != 0:
        n_plot += 1

    fig, ax = plt.subplots(figsize=(10, 5))

    def f_nan_safe(x):
        try:
            res = f(x)
            return res if np.isfinite(res) else np.nan
        except:
            return np.nan

    vf = np.vectorize(f_nan_safe)

    x_fine = np.linspace(a, b, 1000)
    y_fine = vf(x_fine)
    ax.plot(x_fine, y_fine, color='black', linewidth=1.5, alpha=0.7, label='f(x)')

    y_finite = y_fine[np.isfinite(y_fine)]
    if len(y_finite) > 0:
        p_low, p_high = np.percentile(y_finite, [5, 95])
        margin = (p_high - p_low) * 0.25 if p_high != p_low else 1.0
        ax.set_ylim(p_low - margin, p_high + margin)

    h = (b - a) / n_plot
    x_nodes = np.linspace(a, b, n_plot + 1)

    if method in [IntMethod.LEFT_RECTANGLE, IntMethod.RIGHT_RECTANGLE, IntMethod.MID_RECTANGLE]:
        if method == IntMethod.LEFT_RECTANGLE:
            x_bars = x_nodes[:-1]
        elif method == IntMethod.RIGHT_RECTANGLE:
            x_bars = x_nodes[1:]
        else:
            x_bars = x_nodes[:-1] + h / 2

        y_bars = vf(x_bars)
        ax.bar(x_nodes[:-1], y_bars, width=h, align='edge', alpha=0.3,
               color='skyblue', edgecolor='navy', label=method.label)

    elif method == IntMethod.TRAPEZOIDAL:
        y_nodes = vf(x_nodes)
        ax.fill_between(x_nodes, 0, y_nodes, alpha=0.3,
                        color='lightgreen', edgecolor='green', label=method.label)

    elif method == IntMethod.SIMPSON:
        x_parts, y_parts = [], []
        for i in range(0, n_plot, 2):
            x_sub = x_nodes[i:i + 3]
            y_sub = vf(x_sub)

            if np.any(np.isnan(y_sub)): continue

            poly = np.poly1d(np.polyfit(x_sub, y_sub, 2))
            px = np.linspace(x_sub[0], x_sub[2], 10)
            x_parts.extend(px)
            y_parts.extend(poly(px))

        if x_parts:
            ax.fill_between(x_parts, 0, y_parts, alpha=0.3,
                            color='plum', edgecolor='purple', label=method.label)

    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    return fig