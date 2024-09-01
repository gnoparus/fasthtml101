from fastcore.parallel import threaded
from starlette.testclient import TestClient
from fasthtml.common import *
import uuid, os, uvicorn, requests, replicate, stripe
from PIL import Image
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
from datetime import datetime


app = FastHTML()
cli = TestClient(app)


@app.get("/setcookie")
def setc(req):
    now = datetime.now()
    res = Response(f"Now, set to {now}")
    res.set_cookie("cookie_now", str(now))
    return res


print(cli.get("/setcookie").text)

import time

print("Sleeping for 3 seconds...")
time.sleep(3)  # Sleep for 3 seconds


@app.get("/getcookie")
def getc(cookie_now: date):

    return f"Now is {datetime.now()} but cookie was set at time {cookie_now.time()}"


print(cli.get("/getcookie").text)

# if __name__ == "__main__":
#     uvicorn.run(
#         "fh27-cookies:app",
#         host="0.0.0.0",
#         port=int(os.getenv("PORT", default=5000)),
#     )
