import math
from constants import IntegrationMethod


def get_singularities(f, a, b):
    points = []
    for x in [a, b]:
        try:
            val = f(x)
            if not math.isfinite(val): points.append(x)
        except:
            points.append(x)
    return points


def check_convergence(f, sing_point, a, b):
    eps = 1e-6
    delta = eps / 2
    side = 1 if sing_point == a else -1
    try:
        v1 = abs(f(sing_point + side * eps))
        v2 = abs(f(sing_point + side * delta))
        if v1 == 0: return True

        p = math.log(v2 / v1) / math.log(2)
        return p < 1.0
    except:
        return False


def safe_eval(f, x, a, b, h):
    try:
        val = f(x)
        if math.isfinite(val): return val
    except:
        pass

    offset = h / 4
    if x <= a: return f(a + offset)
    if x >= b: return f(b - offset)
    return 0


def left_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(safe_eval(f, a + i * h, a, b, h) for i in range(n))


def right_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(safe_eval(f, a + (i + 1) * h, a, b, h) for i in range(n))


def midpoint_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(safe_eval(f, a + (i + 0.5) * h, a, b, h) for i in range(n))


def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (safe_eval(f, a, a, b, h) + safe_eval(f, b, a, b, h))
    for i in range(1, n):
        s += safe_eval(f, a + i * h, a, b, h)
    return h * s


def simpson_rule(f, a, b, n):
    if n % 2 != 0: n += 1
    h = (b - a) / n
    s = safe_eval(f, a, a, b, h) + safe_eval(f, b, a, b, h)
    for i in range(1, n):
        coeff = 4 if i % 2 != 0 else 2
        s += coeff * safe_eval(f, a + i * h, a, b, h)
    return (h / 3) * s


def integrate_with_runge(f, a, b, eps, n_start, method_name):
    methods_map = {
        IntegrationMethod.LEFT_RECTANGLE: (left_rectangles, 1),
        IntegrationMethod.RIGHT_RECTANGLE: (right_rectangles, 1),
        IntegrationMethod.MIDPOINT_RECTANGLE: (midpoint_rectangles, 2),
        IntegrationMethod.TRAPEZOIDAL: (trapezoidal_rule, 2),
        IntegrationMethod.SIMPSON: (simpson_rule, 4)
    }

    # 1. Проверка сходимости в особых точках
    for pt in get_singularities(f, a, b):
        if not check_convergence(f, pt, a, b):
            return "Интеграл расходится", 0

    func, p = methods_map[method_name]
    n = n_start
    i_n = func(f, a, b, n)

    while True:
        n *= 2
        i_2n = func(f, a, b, n)

        error = abs(i_2n - i_n) / (2 ** p - 1)
        if error < eps or n >= 1_000_000:
            return i_2n, n

        i_n = i_2n