import math
from enum import Enum, auto

class IntegrationMethod(Enum):
    LEFT_RECTANGLE = auto()
    RIGHT_RECTANGLE = auto()
    MIDPOINT_RECTANGLE = auto()
    TRAPEZOIDAL = auto()
    SIMPSON = auto()

METHOD_LABELS = {
    IntegrationMethod.LEFT_RECTANGLE: "Левые прямоугольники",
    IntegrationMethod.RIGHT_RECTANGLE: "Правые прямоугольники",
    IntegrationMethod.MIDPOINT_RECTANGLE: "Средние прямоугольники",
    IntegrationMethod.TRAPEZOIDAL: "Трапеции",
    IntegrationMethod.SIMPSON: "Симпсон"
}

functions = {
        "3x³ - 2x² - 7x - 8": lambda x: 3 * x ** 3 - 2 * x ** 2 - 7 * x - 8,
        "exp(-x^2/2)": lambda x: math.exp(- x**2 / 2),
        "1 / sqrt(|x|)": lambda x: 1 / math.sqrt(abs(x)) if x != 0 else float('inf'),
        "1 / sqrt(x)": lambda x: 1 / math.sqrt(x) if x > 0 else float('inf'),
        "1 / x": lambda x: 1 / x if x > 0 else float('inf')
    }
