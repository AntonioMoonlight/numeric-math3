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

        if v1 is None or v2 is None: continue  

        if abs(v1) > 1e3: 
            try:
                p = math.log2(abs(v1 / v2))
                if p >= 1.0: return True  
            except (ValueError, ZeroDivisionError):
                pass
    return False


def _integrate_fixed(final_f, a, b, eps, n_start, method_enum, max_n=10_000):
    calc_func = METHOD_FUNCTIONS[method_enum]
    k = method_enum.k
    n = n_start

    h = (b - a) / n
    i_n = calc_func(final_f, a, b, n, h)

    while n < max_n:
        n *= 2
        h = (b - a) / n
        i_2n = calc_func(final_f, a, b, n, h)

        error = abs(i_2n - i_n) / (2 ** k - 1)
        if error < eps:
            return i_2n, n

        i_n = i_2n

    return i_n, n


def _find_singularity(f_safe, a, b, samples=None):
    if samples is None:
        samples = max(2000, int(abs(b - a) * 1000))

    step = (b - a) / samples
    if step == 0:
        return None

    big_dyn = max(1e3, 1.0 / abs(step))

    prev_x = a
    prev_v = f_safe(a)

    for i in range(1, samples + 1):
        x = a + i * step
        v = f_safe(x)

        if v is None:
            return x

        if prev_v is not None and v is not None:
            if v * prev_v < 0:
                if abs(v) > big_dyn or abs(prev_v) > big_dyn:
                    return (x + prev_x) / 2
                if (abs(v) > 10 * abs(prev_v)) or (abs(prev_v) > 10 * abs(v)):
                    return (x + prev_x) / 2

            if abs(v) > big_dyn and abs(prev_v) > big_dyn:
                return (x + prev_x) / 2

        prev_x, prev_v = x, v

    return None


def _principal_value(f_safe, a, b, eps, n_start, method_enum, c=None):
    if c is None:
        c = _find_singularity(f_safe, a, b)
    if c is None or not (a < c < b):
        return None

    final_f = lambda x: f_safe(x) or 0
    gap = (b - a) / 100
    prev = None
    last_n = n_start

    for _ in range(12):
        left_b = c - gap
        right_a = c + gap
        if left_b <= a or right_a >= b:
            break

        val_l, n_l = _integrate_fixed(final_f, a, left_b, eps / 2, n_start, method_enum)
        val_r, n_r = _integrate_fixed(final_f, right_a, b, eps / 2, n_start, method_enum)

        val = val_l + val_r
        last_n = max(n_l, n_r)

        if prev is not None and abs(val - prev) < eps:
            return val, last_n

        prev = val
        gap /= 2

    return (prev, last_n) if prev is not None else None


def integrate_with_runge(f, a, b, eps, n_start, method_enum):
    f_safe = get_safe_func(f)

    c = _find_singularity(f_safe, a, b)
    if c is not None and a < c < b:
        pv = _principal_value(f_safe, a, b, eps, n_start, method_enum, c=c)
        if pv is not None:
            return pv

    if check_divergence(f_safe, a, b):
        pv = _principal_value(f_safe, a, b, eps, n_start, method_enum, c=c)
        if pv is not None:
            return pv
        return "Интеграл расходится", 0

    offset = 1e-9
    safe_a = a + offset if f_safe(a) is None else a
    safe_b = b - offset if f_safe(b) is None else b

    final_f = lambda x: f_safe(x) or 0

    return _integrate_fixed(final_f, safe_a, safe_b, eps, n_start, method_enum)