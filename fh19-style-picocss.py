from fasthtml.common import *
from starlette.testclient import TestClient

# App with custom styling to override the pico defaults
css = Style(":root { --pico-font-size: 100%; --pico-font-family: Pacifico, cursive;}")
app = FastHTML(hdrs=(picolink, css))


@app.route("/")
def get():
    return Title("FastHTML is awesome"), Main(
        H1("FastHTML is awesome"), Div("so is HTMX"), cls="container"
    )


serve()

client = TestClient(app)
print(client.get("/").text)
