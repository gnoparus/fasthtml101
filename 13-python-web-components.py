from fasthtml.common import *

app, rt = fast_app(live=True)


def NumList(n):
    return Ul(*[Li(i) for i in range(n)])


@rt("/")
def get():
    nums = NumList(12)
    return Titled(
        "Hello App2",
        Div(P(nums)),
        P(A("hx Link", hx_get="/change")),
        P(A("Href Link", href="/change")),
    )


@rt("/change")
def get():
    return Titled(
        "Hello App3",
        Div(P("Hello World! 222")),
        P(A("hx Link", hx_get="/", hx_swap="outerHTML")),
        P(A("Href Link", href="/")),
    )


serve()
