from fastapi import FastAPI
from app.scraper import scrap_url, scrap_detail_page

app = FastAPI()

@app.get("/")
def read_root():
    scrap_url()
    return {"Hello": "World"}

@app.get("/scrap")
def aa():
    scrap_detail_page()
    return {"Hello": "World"}
