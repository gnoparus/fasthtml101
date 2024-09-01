from fastcore.parallel import threaded
from starlette.testclient import TestClient
from fasthtml.common import *
import uuid, os, uvicorn, requests, replicate, stripe
from PIL import Image
from dotenv import load_dotenv
from starlette.responses import RedirectResponse


app = FastHTML()
cli = TestClient(app)


## path parameters
@app.get("/user/{nm}/{gd}")
def _(nm: str, gd: str):
    return f"Good day to you, {nm} - {gd}!"


print("1: ", cli.get("/user/keng/male").text)


## regex
reg_re_param("imgext", "ico|gif|jpg|jpeg|webm")


@app.get(r"/static/{path:path}{fn}.{ext:imgext}")
def get_img(fn: str, path: str, ext: str):
    return f"Getting {fn}.{ext} from /{path}"


print("2: ", cli.get("/static/foo/bar/baz.webm").text)
print("3: ", cli.get("/static/foo/bar/baz.icox").text)  # unmatched regex


## enum
ModelName = str_enum("ModelName", "alexnet", "resnet", "lenet")


@app.get("/models/{nm}")
def model(nm: ModelName):
    return nm


print("4: ", cli.get("/models/alexnet").text)


## casting to path


@app.get("/files/{path}")
def txt(path: Path):
    return path.with_suffix(".png")


print("5: ", cli.get("/files/foo").text)


## integer with default value
fake_db = [{"name": "Foo"}, {"name": "Bar"}]


@app.get("/items/")
def read_item(idx: int | None = 0):
    return fake_db[idx]


print("6: ", cli.get("/items/?idx=1").text)
print("7: ", cli.get("/items").text)


## boolean
@app.get("/booly/")
def booly(coming: bool = True):
    # print("coming: ", coming)
    return "Coming" if coming else "Not coming"


print("8: ", cli.get("/booly/?coming=true").text)
print("9: ", cli.get("/booly/?coming=no").text)
print("10: ", cli.get("/booly/?coming=false").text)
print("11: ", cli.get("/booly/?coming=yes").text)


## Dates
@app.get("/datie/")
def datie(d: date):
    return d


date_str = "17th of May, 2020, 2p"
print("12: ", cli.get(f"/datie/?d={date_str}").text)

date_str2 = "2020-12-31, 10p"
print("13: ", cli.get(f"/datie/?d={date_str2}").text)

## Dataclass
from dataclasses import dataclass, asdict


@dataclass
class Bodie:
    a: int
    b: str


@app.route("/bodie/{nm}")
def post(nm: str, data: Bodie):
    res = asdict(data)
    res["nm"] = nm
    return res


print("13: ", cli.post("/bodie/me", data=dict(a=1, b="foo")).text)

# if __name__ == "__main__":
#     uvicorn.run(
#         "fh26-req-parameters:app",
#         host="0.0.0.0",
#         port=int(os.getenv("PORT", default=5000)),
#     )
