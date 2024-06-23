from fastapi import FastAPI
from app.scraper import scrap_url, scrap_detail_page, scrap_single_page, scrap_detail_page_redirected_url
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

@app.get("/redirect-url-scrap")
def redirect_url_scrap(division: str):
    scrap_detail_page_redirected_url(division)
    return {"Hello": "World"}