import matplotlib.pyplot as plt
import methods
from constants import IntegrationMethod


def create_integration_plot(f, a, b, n, method: IntegrationMethod):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Отрисовка основной функции
    x_fine = [a + (b - a) * i / 200 for i in range(201)]
    y_fine = [f(x) for x in x_fine]
    ax.plot(x_fine, y_fine, color='gray', linewidth=1, alpha=0.5, label='f(x)')

    h = (b - a) / n

    if method in [IntegrationMethod.LEFT_RECTANGLE,
                  IntegrationMethod.RIGHT_RECTANGLE,
                  IntegrationMethod.MIDPOINT_RECTANGLE]:
        for i in range(n):
            xi = a + i * h
            if method == IntegrationMethod.LEFT_RECTANGLE:
                rect_y = f(xi)
            elif method == IntegrationMethod.RIGHT_RECTANGLE:
                rect_y = f(xi + h)
            else:
                rect_y = f(xi + h / 2)
            ax.add_patch(plt.Rectangle((xi, 0), h, rect_y, alpha=0.3,
                                       facecolor='skyblue', edgecolor='navy'))

    elif method == IntegrationMethod.TRAPEZOIDAL:
        for i in range(n):
            xi, xi1 = a + i * h, a + (i + 1) * h
            ax.fill_between([xi, xi1], [f(xi), f(xi1)], alpha=0.3,
                            facecolor='lightgreen', edgecolor='green')

    elif method == IntegrationMethod.SIMPSON:
        for i in range(0, n, 2):
            x0, x1, x2 = a + i * h, a + (i + 1) * h, a + (i + 2) * h
            pts = [(x0, f(x0)), (x1, f(x1)), (x2, f(x2))]
            para = methods.get_lagrange_poly(pts)
            x_p = [x0 + (x2 - x0) * j / 20 for j in range(21)]
            y_p = [para(x) for x in x_p]
            ax.fill_between(x_p, y_p, alpha=0.3, facecolor='plum', edgecolor='purple')

    ax.axhline(0, color='black', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    return fig