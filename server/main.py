from fastapi import FastAPI
from scout.scout import search_free_streams
from bid.bidder import get_recommendations

app = FastAPI()

@app.post("/search")
async def search(data: dict):
    title = data["title"]
    free = search_free_streams(title)
    recs = get_recommendations(title, free)
    return {"recommendations": recs}
