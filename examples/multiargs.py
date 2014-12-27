from functools import wraps

from simpletimeit import stimeit

st = stimeit.SimpleTimeIt()

st.call_with('10, 100')
st.call_with('8000, 92833')
st.call_with('898989, 1000000000001')

@st.time_this
def divide(a, b):
    while b != 0:
        a, b = b, a % b
    return a

@st.time_this
def subtract(a, b):
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

@st.time_this
def recurse(a, b):
    if b == 0:
        return a
    else:
        return recurse(b, a % b)

if __name__ == '__main__':
    st.run()
