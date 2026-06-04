import streamlit as st
import math
import methods
import graphs
from constants import IntMethod, FUNCTIONS

def main():
    st.set_page_config(page_title="Численное интегрирование", layout="wide")
    st.title("Численное интегрирование")
    st.subheader("Никифоров Антон, P3215")
    st.sidebar.header("Параметры")

    func_name = st.sidebar.selectbox(r"Функция $f(x)$", list(FUNCTIONS.keys()))
    f = FUNCTIONS[func_name]

    def get_float_input(label, value, step=None, format=None):
        raw_value = st.sidebar.text_input(label, value=str(value))
        clean_value = raw_value.replace(',', '.')

        try:
            return float(clean_value)
        except ValueError:
            st.sidebar.error(f"Ошибка: '{raw_value}' не является числом.")
            return float(value)

    a = get_float_input(r"Нижний предел $a$", value=2.0)
    b = get_float_input(r"Верхний предел $b$", value=3.0)
    eps = get_float_input(r"Требуемая точность $\varepsilon$", value=0.01)
    precision = max(0, math.ceil(-math.log10(eps)))

    selected_method = st.sidebar.selectbox(
        "Метод интегрирования",
        options=list(IntMethod),
        format_func=lambda method: method.label
    )

    if st.sidebar.button("Рассчитать"):
        try:
            result, final_n = methods.integrate_with_runge(f, a, b, eps, 4, selected_method)

            col1, col2 = st.columns(2)
            if isinstance(result, str):
                col1.metric("Результат", result)
            else:
                col1.metric("Значение интеграла", f"{result:.{precision}f}")
                col2.metric("Число разбиений", final_n)

                fig = graphs.create_integration_plot(f, a, b, final_n, selected_method)
                st.pyplot(fig)

        except ValueError:
            st.error("Ошибка: Функция не определена на данном интервале.")
        except Exception as e:
            st.error(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()