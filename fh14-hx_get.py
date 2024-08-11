from fasthtml.common import *

app, rt = fast_app(live=True)


def NumList(n):
    return Ul(*[Li(i) for i in range(n)])


@rt("/")
def get():
    nums = NumList(12)
    return Titled("hx_get demo app", Div(P(nums), hx_get="/change"))


@rt("/change")
def get():
    return (P("Changes is certain."),)


serve()
