import os

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["project"])

PROJECT_DOCS_URL = os.getenv("PROJECT_DOCS_URL")

@router.get("/project")
def project_docs():
    return RedirectResponse(
        url = PROJECT_DOCS_URL
    )