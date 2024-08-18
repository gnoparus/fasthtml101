from fasthtml.common import *
from starlette.testclient import TestClient

app, rt = fast_app()


@app.route("/", methods="get")
def home():
    return H1("Hello, World")


@app.route("/", methods=["post", "put"])
def post_or_put():
    return "got a POST or PUT request"


@app.get("/greet/{nm}")
def greet(nm: str):
    return f"Good day to you, {nm}!"


client = TestClient(app)
print(client.get("/").text)
print(client.post("/").text)
print(client.put("/").text)
print(client.get("/greet/Keng").text)
