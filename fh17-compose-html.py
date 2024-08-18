from fasthtml.common import *
from starlette.testclient import TestClient

app, rt = fast_app(live=True)

page = Html(
    Head(Title("Title of page1")),
    Body(
        Div(
            "Some text in Div, ",
            A("A link", href="https://example.com"),
            Img(src="https://placehold.co/200"),
            cls="container",
        )
    ),
)


@app.get("/")
def homepage():
    # print(to_xml(page))
    return page


@app.get("/wrap")
def wrap():
    return Title("Page Demo"), Div(
        H1("Hello, World"), P("Some text"), P("Some more text")
    )


serve()

client = TestClient(app)
print(client.get("/").text)
print(client.get("/wrap").text)
