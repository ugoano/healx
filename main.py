import os
from datetime import date

from fastapi import FastAPI, Query
from pydantic import validator

from models import Paper, get_paper_model, get_paper_models, init_es


app = FastAPI()
PAGE_SIZE = 10


@app.get("/papers/?")
async def get_papers(
    published_date: date = Query(
        None,
        description="Must be in format yyyy-mm-dd. Originally was as instructions.",
    ),
    q: str = Query(None),
    limit: int = Query(PAGE_SIZE),
    offset: int = Query(0)
):
    return get_paper_models(published_date=published_date, q=q, offset=offset, limit=limit)


@app.get("/paper/{cord_uid}")
async def get_paper(cord_uid: str):
    return get_paper_model(cord_uid)


if __name__ == "__main__":
    init_es(index_name=os.environ.get("INDEX", "paper-index"))
