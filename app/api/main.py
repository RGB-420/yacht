import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import regattas, editions, boats, classes, clubs, search, project, feedbacks, schedule, quality, admin_regattas, admin_club_corrections, admin_class_type_corrections, admin_owner_corrections

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(regattas.router)
app.include_router(editions.router)
app.include_router(boats.router)
app.include_router(classes.router)
app.include_router(clubs.router)
app.include_router(schedule.router)

app.include_router(search.router)

app.include_router(feedbacks.router)

app.include_router(project.router)
app.include_router(quality.router)
app.include_router(admin_regattas.router)
app.include_router(admin_club_corrections.router)
app.include_router(admin_class_type_corrections.router)
app.include_router(admin_owner_corrections.router)
