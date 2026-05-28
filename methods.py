import math

from constants import IntegrationMethod


def left_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))


def right_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 1) * h) for i in range(n))


def midpoint_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))


def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return h * s


def simpson_rule(f, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        coeff = 4 if i % 2 != 0 else 2
        s += coeff * f(a + i * h)
    return (h / 3) * s


def integrate_with_runge(f, a, b, eps, n_start, method_name):
    methods_map = {
        IntegrationMethod.LEFT_RECTANGLE: (left_rectangles, 1),
        IntegrationMethod.RIGHT_RECTANGLE: (right_rectangles, 1),
        IntegrationMethod.MIDPOINT_RECTANGLE: (midpoint_rectangles, 2),
        IntegrationMethod.TRAPEZOIDAL: (trapezoidal_rule, 2),
        IntegrationMethod.SIMPSON: (simpson_rule, 4)
    }

    func, p = methods_map[method_name]
    n = n_start

    i_n = func(f, a, b, n)
    while True:
        n *= 2
        i_2n = func(f, a, b, n)
        error = abs(i_2n - i_n) / (2 ** p - 1)
        if error < eps:
            return i_2n, n
        i_n = i_2n
        if n > 100:  # Защита от бесконечного цикла
            return i_2n, n


def check_convergence(f_meta, a, b):
    sing = f_meta["singularity"]
    # Если разрыв вне отрезка - интеграл обычный
    if not (a <= sing <= b):
        return True, "Сходящийся (нет разрывов)"

    # Случай 4: Принцип симметрии (зануление участка)
    if f_meta["odd_symmetry"]:
        return True, "Сходящийся (симметричный разрыв)"

    # Стандартная проверка по показателю p
    if f_meta["p"] < 1:
        return True, "Сходящийся (несобственный 2 рода)"

    return False, "Интеграл не существует"


def get_safe_value(f, x, eps_offset=1e-12):
    """Возвращает значение функции, избегая деления на ноль."""
    try:
        val = f(x)
        if math.isinf(val) or math.isnan(val):
            return f(x + eps_offset)
        return val
    except ZeroDivisionError:
        return f(x + eps_offset)

def get_lagrange_poly(pts):
    def poly(x):
        total = 0
        for i in range(len(pts)):
            xi, yi = pts[i]
            li = 1
            for j in range(len(pts)):
                if i != j:
                    xj, yj = pts[j]
                    li *= (x - xj) / (xi - xj)
            total += yi * li
        return total
    return poly