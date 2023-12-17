from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class Advantage(BaseModel):
    text: str
    desc: str


class Product(BaseModel):
    id: int
    title: str
    description: str
    interest_rate: str | None = None
    category: str
    advantages: list[Advantage] | None = None
    conditions: str | None = None
    benefits: str | None = None


class Channel(BaseModel):
    id: int
    name: str
    description: str


class Client(BaseModel):
    id: int
    username: str
    gender: str
    age: float
    created_at: str


class Input(BaseModel):
    product: Product
    channel: Channel
    client: Client


ml_modules = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_modules["tokenizer"] = AutoTokenizer.from_pretrained("JohnGrace/Yakutia-KSTU_Template")
    ml_modules["model"] = AutoModelForSeq2SeqLM.from_pretrained("JohnGrace/Yakutia-KSTU_Template")
    yield

    ml_modules.clear()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def prepare_prompt_for_channel(input):
    product_data = input.product
    prompt = product_data.title
    channel = input.channel.name

    if channel in ["TMO", "EMAIL", "OFFICE_BANNER"]:
        prompt += f" | {product_data.description} | {product_data.conditions}"
        if product_data.advantages:
            prompt += " ".join([f"{adv.text}: {adv.desc}" for adv in product_data.advantages])
    if channel == "PUSH":
        prompt += f" | {product_data.description}"
    if channel == "SMS":
        prompt += f" | {product_data.conditions}"
    elif channel == "MOBILE_CHAT":
        prompt += f" | {product_data.description} | {product_data.conditions}"

    return prompt


def create_text(model, tokenizer, input):
    prompt = prepare_prompt_for_channel(input)
    data = tokenizer('<SC6>' + prompt + '\nОтвет: <extra_id_0>', return_tensors="pt")
    data = {k: v.to(model.device) for k, v in data.items()}
    output_ids = model.generate(
        **data, do_sample=True, temperature=0.6, max_new_tokens=1024, top_p=0.95, top_k=5, repetition_penalty=1.03,
        no_repeat_ngram_size=2
    )[0]
    out = tokenizer.decode(output_ids.tolist())
    out = out.replace("<s>", "").replace("</s>", "").replace('<pad><extra_id_0>', '')
    return out


@app.post("/generate")
async def generate(input: Input):
    model = ml_modules["model"]
    tokenizer = ml_modules["tokenizer"]
    text = create_text(model, tokenizer, input)
    return {"text": text}
