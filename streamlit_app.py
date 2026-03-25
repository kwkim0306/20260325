import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify, sympify, SympifyError

st.title("중간값 정리 시각화")

st.markdown("""
중간값 정리에 따라, 함수 f(x)가 구간 [a, b]에서 연속이고 f(a) ≠ f(b)라면,  
f(a)와 f(b) 사이의 임의의 값 k에 대해 f(c) = k를 만족하는 c ∈ (a, b)가 적어도 하나 존재합니다.

아래에서 a, b, k를 입력하고 함수를 정의하여 시각적으로 확인해보세요.
""")

# 사이드바 입력
st.sidebar.header("입력 값")
a = st.sidebar.number_input("a", value=-1.0, step=0.1)
b = st.sidebar.number_input("b", value=1.0, step=0.1)
k = st.sidebar.number_input("k", value=0.0, step=0.1)
func_str = st.sidebar.text_input("함수 f(x) (예: x**2, sin(x), x**3 - x)", value="x**2")

# 함수 파싱
x = symbols('x')
try:
    f_expr = sympify(func_str)
    f = lambdify(x, f_expr, 'numpy')
    fa = f(a)
    fb = f(b)
    st.sidebar.write(f"f(a) = {fa:.3f}")
    st.sidebar.write(f"f(b) = {fb:.3f}")
    if fa == fb:
        st.sidebar.error("f(a)와 f(b)가 같습니다. 다른 값으로 시도하세요.")
    elif not (min(fa, fb) <= k <= max(fa, fb)):
        st.sidebar.warning("k가 f(a)와 f(b) 사이에 있지 않습니다.")
    else:
        st.sidebar.success("조건 만족! 그래프를 확인하세요.")
except SympifyError:
    st.error("유효하지 않은 함수입니다. 예: x**2")
    st.stop()

# 그래프 생성
fig, ax = plt.subplots()
x_vals = np.linspace(a, b, 100)
y_vals = f(x_vals)
ax.plot(x_vals, y_vals, label=f'f(x) = {func_str}')
ax.axhline(y=k, color='red', linestyle='--', label=f'y = {k}')
ax.scatter([a, b], [fa, fb], color='blue')
ax.annotate(f'({a:.2f}, {fa:.2f})', (a, fa), textcoords="offset points", xytext=(0,10), ha='center')
ax.annotate(f'({b:.2f}, {fb:.2f})', (b, fb), textcoords="offset points", xytext=(0,10), ha='center')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown("""
### 설명
- 파란 점: (a, f(a))와 (b, f(b))
- 빨간 선: y = k
- 함수 그래프가 y = k 선과 교차하는 점이 존재함을 확인할 수 있습니다.
""")
