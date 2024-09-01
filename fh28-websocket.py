from fasthtml.common import *
import uuid, os, uvicorn, requests, replicate, stripe
import time

app = FastHTML(ws_hdr=True)
rt = app.route


def mk_inp():
    return Input(id="msg")


@rt("/")
async def get(request):
    cts = Div(
        Div(id="notifications"),
        Form(mk_inp(), id="form", ws_send=True),
        hx_ext="ws",
        ws_connect="/ws",
    )
    return Titled("Websocket Test", cts)


async def on_connect(send):
    print("Connected!")
    await send(Div("Hello, you have connected", id="notifications"))


async def on_disconnect(ws):
    print("Disconnected!")


@app.ws("/ws", conn=on_connect, disconn=on_disconnect)
async def ws(msg: str, send):
    await send(Div("Hello " + msg, id="notifications"))
    await sleep(2)
    return Div("Goodbye " + msg, id="notifications"), mk_inp()


if __name__ == "__main__":
    uvicorn.run(
        "fh28-websocket:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", default=5000)),
    )
