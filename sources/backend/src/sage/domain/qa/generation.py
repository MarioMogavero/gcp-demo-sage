"""Generation step of the RAG pipeline: build the grounded prompt, call the LLM."""

from pathlib import Path

from sage.domain.qa.models import Chunk
from sage.integrations.llm.generate import generate_text

from google.cloud import storage

_PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "answer_prompt.txt").read_text(
    encoding="utf-8"
)
_NO_DOCUMENTS_CONTEXT = (
    "Nessun documento disponibile (base di conoscenza non ancora popolata o non configurata)."
)


def build_prompt(question: str, chunks: list[Chunk]) -> str:
    context = (
        "\n\n".join(f"[{chunk.source}] {chunk.text}" for chunk in chunks)
        if chunks
        else _NO_DOCUMENTS_CONTEXT
    )
    
    storage_client = storage.Client()

    bucket_name = "its-ict-mario-mogavero-instructions"
    blob_name = "istruzioni.md"
    
    # Recupera il bucket
    bucket = storage_client.bucket(bucket_name)
    # Recupera il blob (il file) all'interno del bucket
    blob = bucket.blob(blob_name)
    # Legge il contenuto del file come testo (stringa formattata in UTF-8)
    contenuto = blob.download_as_text()
    
    question_instruction = question+ "\n\n" + contenuto
    return _PROMPT_TEMPLATE.format(context=context, question=question_instruction)


async def generate_answer(question: str, chunks: list[Chunk]) -> str:
    prompt = build_prompt(question, chunks)
    return await generate_text(prompt)
