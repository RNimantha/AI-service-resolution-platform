"""Thin HTTP adapters for RAG; ingestion behavior stays in rag_service."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.main.app.controller.dependencies.rag_dependencies import get_text_document_loader
from src.main.app.controller.schemas.document_preview_request import DocumentPreviewRequest
from src.main.app.controller.schemas.document_preview_response import DocumentPreviewResponse
from src.main.app.services.rag_service import TextDocumentLoader

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/documents/preview", response_model=DocumentPreviewResponse)
def preview_document(
    request: DocumentPreviewRequest,
    loader: Annotated[TextDocumentLoader, Depends(get_text_document_loader)],
) -> DocumentPreviewResponse:
    """Preview submitted text in memory without indexing or model inference."""
    try:
        document = loader.load(title=request.title, content=request.content)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error)
        ) from error

    return DocumentPreviewResponse(
        document_id=document.document_id,
        title=document.title,
        source=document.source,
        character_count=document.character_count,
        word_count=document.word_count,
        preview=document.preview,
    )
