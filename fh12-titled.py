from fasthtml.common import *

app, rt = fast_app(live=True)


@rt("/")
def get():
    return Titled(
        "Hello App2",
        Div(P("Hello World! 111")),
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
