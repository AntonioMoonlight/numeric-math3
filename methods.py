import math
from constants import IntMethod

def left_rectangles(f, a, b, n, h):
    return h * sum(f(a + i * h) for i in range(n))

def right_rectangles(f, a, b, n, h):
    return h * sum(f(a + (i + 1) * h) for i in range(n))

def midpoint_rectangles(f, a, b, n, h):
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))

def trapezoidal_rule(f, a, b, n, h):
    s = (f(a) + f(b)) / 2
    for i in range(1, n):
        s += f(a + i * h)
    return h * s

def simpson_rule(f, a, b, n, h):
    if n % 2 != 0: n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 != 0 else 2) * f(a + i * h)
    return (h / 3) * s

METHOD_FUNCTIONS = {
    IntMethod.LEFT_RECTANGLE: left_rectangles,
    IntMethod.RIGHT_RECTANGLE: right_rectangles,
    IntMethod.MID_RECTANGLE: midpoint_rectangles,
    IntMethod.TRAPEZOIDAL: trapezoidal_rule,
    IntMethod.SIMPSON: simpson_rule
}

def get_safe_func(f):
    def wrapped(x):
        try:
            val = f(x)
            return val if math.isfinite(val) else None
        except (ZeroDivisionError, OverflowError):
            return None
    return wrapped


def check_divergence(f_safe, a, b):
    eps = 1e-7
    for pt, side in [(a, 1), (b, -1)]:
        v1 = f_safe(pt + side * eps)
        v2 = f_safe(pt + side * eps * 2)

        if v1 is None or v2 is None: continue  # Точка разрыва

        if abs(v1) > 1e3:  # Если значение вблизи границы очень большое
            # Оценка порядка роста p: f(x) ~ 1/x^p
            # p = log2(f(eps)/f(2*eps))
            try:
                p = math.log2(abs(v1 / v2))
                if p >= 1.0: return True  # Расходится
            except (ValueError, ZeroDivisionError):
                pass
    return False


def integrate_with_runge(f, a, b, eps, n_start, method_enum):
    f_safe = get_safe_func(f)

    if check_divergence(f_safe, a, b):
        return "Интеграл расходится", 0

    offset = 1e-9
    safe_a = a + offset if f_safe(a) is None else a
    safe_b = b - offset if f_safe(b) is None else b

    final_f = lambda x: f_safe(x) or 0

    calc_func = METHOD_FUNCTIONS[method_enum]
    k = method_enum.k
    n = n_start

    h = (safe_b - safe_a) / n
    i_n = calc_func(final_f, safe_a, safe_b, n, h)

    while n < 1_000_000:
        n *= 2
        h = (safe_b - safe_a) / n
        i_2n = calc_func(final_f, safe_a, safe_b, n, h)

        error = abs(i_2n - i_n) / (2 ** k - 1)
        if error < eps:
            return i_2n, n

        i_n = i_2n

    return i_n, n