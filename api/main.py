import os
from fastapi import FastAPI

from api.routes import regattas, editions, boats, classes, clubs, project

docs_url = os.getenv("PROJECT_DOCS_URL")


app = FastAPI(
        title="Regatta Data API",
        description=f"""
            API for sailing regatta data

            Project documentation:
                {docs_url}
        """,
        version="1.0"
    )

app.include_router(regattas.router)
app.include_router(editions.router)
app.include_router(boats.router)
app.include_router(classes.router)
app.include_router(clubs.router)

app.include_router(project.router)