from fastcore.parallel import threaded
from fasthtml.common import *
from starlette.testclient import TestClient
import os, uvicorn, requests, replicate, uuid
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from the .env file (if present)
load_dotenv()

# Replicate setup (for image generation)
replicate_api_token = os.environ["REPLICATE_API_TOKEN"]
client = replicate.Client(api_token=replicate_api_token)

tables = database("data/gens.db").t
gens = tables.gens

if not gens in tables:
    gens.create(prompt=str, id=int, folder=str, pk="id")
Generation = gens.dataclass()

# Flexbox CSS (http://flexboxgrid.com/)
gridlink = Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css",
)


# Store our generations
folder = f"gens/"
os.makedirs(folder, exist_ok=True)

app = FastHTML(hdrs=(picolink, gridlink))


@app.get("/")
def home():
    inp = Input(id="new-prompt", name="prompt", placeholder="Enter a prompt")
    add = Form(
        Group(inp, Button("Generate")),
        hx_post="/",
        target_id="gen-list",
        hx_swap="afterbegin",
    )
    gen_containers = [generation_preview(gen) for gen in gens(limit=10)]
    gen_list = Div(*reversed(gen_containers), id="gen-list", cls="row")

    return Title("Image Generation Demo"), Main(
        H1("Image Generation Demo"), add, gen_list, cls="container"
    )


def generation_preview(g: Generation):
    grid_cls = "box col-xs-12 col-sm-6 col-md-4 col-lg-3"
    image_path = f"{g.folder}/{g.id}.png"
    if os.path.exists(image_path):
        return Div(
            Card(
                Img(
                    src=image_path,
                    alt=f"Generated image for {g.prompt}",
                    cls="card-img-top",
                ),
                Div(P(B("Prompt: "), g.prompt, cls="card-text")),
                cls="card-body",
            ),
            id=f"gen-{g.id}",
            cls=grid_cls,
        )
    else:
        return Div(
            f"Generating gen {g.id} with prompt {g.prompt}...",
            id=f"gen-{g.id}",
            hx_get=f"/gens/{g.id}",
            hx_trigger="every 2s",
            hx_swap="outerHTML",
            cls=grid_cls,
        )


@app.get("/gens/{id}")
def preview(id: int):
    return generation_preview(gens.get(id))


# For images, CSS, etc.
@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str):
    return FileResponse(f"{fname}.{ext}")


@app.post("/")
def post(prompt: str):
    folder = f"data/gens/{str(uuid.uuid4())}"
    os.makedirs(folder, exist_ok=True)
    g = gens.insert(Generation(prompt=prompt, folder=folder))
    generate_and_save(g.prompt, g.id, g.folder)
    clear_input = Input(
        id="new-prompt", name="prompt", placeholder="Enter a prompt", hx_swap_oob="true"
    )
    return generation_preview(g), clear_input


# Generate an image and save it to the folder (in a separate thread)
@threaded
def generate_and_save(prompt, id, folder):
    output = client.run(
        "playgroundai/playground-v2.5-1024px-aesthetic:a45f82a1382bed5c7aeb861dac7c7d191b0fdf74d8d57c4a0e6ed7d4d0bf7d24",
        input={
            "width": 1024,
            "height": 1024,
            "prompt": prompt,
            "scheduler": "DPMSolver++",
            "num_outputs": 1,
            "guidance_scale": 3,
            "apply_watermark": True,
            "negative_prompt": "ugly, deformed, noisy, blurry, distorted",
            "prompt_strength": 0.8,
            "num_inference_steps": 25,
        },
    )
    Image.open(requests.get(output[0], stream=True).raw).save(f"{folder}/{id}.png")
    return True


if __name__ == "__main__":
    uvicorn.run(
        "fh23-image-generation:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", default=5000)),
        reload=True,
    )
