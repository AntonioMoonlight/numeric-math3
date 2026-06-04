import math
from enum import Enum

class IntMethod(Enum):
    LEFT_RECTANGLE = ("Левые прямоугольники", 1)
    RIGHT_RECTANGLE = ("Правые прямоугольники", 1)
    MID_RECTANGLE = ("Средние прямоугольники", 2)
    TRAPEZOIDAL = ("Трапеции", 2)
    SIMPSON = ("Симпсон", 4)

    def __init__(self, label, k):
        self.label = label
        self.k = k

FUNCTIONS = {
        "3x³ - 2x² - 7x - 8": lambda x: 3 * x ** 3 - 2 * x ** 2 - 7 * x - 8,
        "exp(-x^2/2)": lambda x: math.exp(- x**2 / 2),
        "1 / sqrt(|x|)": lambda x: 1 / math.sqrt(abs(x)),
        "1 / sqrt(x)": lambda x: 1 / math.sqrt(x),
        "1 / x": lambda x: 1 / x
    }
