from fastapi import FastAPI
from app.scraper import scrap_url, scrap_detail_page, scrap_single_page
from .payload import UrlRequest

app = FastAPI()

@app.get("/")
def read_root():
    scrap_url()
    return {"Hello": "World"}

@app.get("/scrap")
def scrap():
    scrap_detail_page()
    return {"Hello": "World"}

@app.post("/scrap-url")
def scrap_url(request: UrlRequest):
    scrap_single_page(request.url)
    return {"scraped_url": request.url}

