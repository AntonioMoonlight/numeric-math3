import streamlit as st
import math
import methods
import graphs
from constants import METHOD_LABELS, functions


def main():
    st.set_page_config(page_title="Численное интегрирование", layout="wide")
    st.title("Численное интегрирование")
    st.subheader("Никифоров Антон, P3215")


    # Сайдбар
    st.sidebar.header("Параметры")

    func_name = st.sidebar.selectbox("Функция f(x)", list(functions.keys()))
    f = functions[func_name]

    a = st.sidebar.number_input("Нижний предел a", value=2.0)
    b = st.sidebar.number_input("Верхний предел b", value=3.0)
    eps = st.sidebar.number_input(
        "Требуемая точность",
        value=0.01,
        step=0.000001,
        format="%.4f"
    )
    precision = max(0, math.ceil(-math.log10(eps)))

    selected_label = st.sidebar.selectbox("Метод интегрирования", list(METHOD_LABELS.values()))
    method_id = [k for k, v in METHOD_LABELS.items() if v == selected_label][0]

    if st.sidebar.button("Рассчитать"):
        result, final_n = methods.integrate_with_runge(f, a, b, eps, 4, method_id)

        col1, col2 = st.columns(2)
        if isinstance(result, str):
            col1.metric("Результат", result)
        else:
            col1.metric("Значение интеграла", f"{result:.{precision}f}")
            col2.metric("Число разбиений", final_n)

        if 1 <= final_n <= 1000:
            fig = graphs.create_integration_plot(f, a, b, final_n, method_id)
        else:
            fig = graphs.create_function_plot(f, a, b)
        st.pyplot(fig)

if __name__ == "__main__":
    main()