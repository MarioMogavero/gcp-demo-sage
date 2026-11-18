from google.cloud import storage
import argparse
import logging
from pathlib import Path

import sage  # noqa: F401  (triggers the .env bootstrap in sage/__init__.py)
from sage.config import get_app_config
from sage.domain.qa.chunking import split_into_chunks
from sage.integrations.firestore.chunks import add_chunk, delete_chunks_for_source
from sage.integrations.llm.embeddings import embed_text

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ingest_documents")


storage_client = storage.Client()

bucket_name = "its-ict-mario-mogavero-instructions"
blob_name = "istruzioni.md"

# Recupera il bucket
bucket = storage_client.bucket(bucket_name)
# Recupera il blob (il file) all'interno del bucket
blob = bucket.blob(blob_name)
# Legge il contenuto del file come testo (stringa formattata in UTF-8)
contenuto = blob.download_as_text()
# Stampa il contenuto a video


def ingest_file(path: Path) -> int:
    config = get_app_config()
    source = path.name
    text = path.read_text(encoding="utf-8")
    chunks = split_into_chunks(text, max_chars=config.chunk_max_chars)

    delete_chunks_for_source(source)

    for chunk in chunks:
        embedding = embed_text(chunk.text)
        add_chunk(
            chunk_id=f"{source}-{chunk.chunk_index}",
            text=chunk.text,
            embedding=embedding,
            source=source,
            section=chunk.section,
            chunk_index=chunk.chunk_index,
        )

    log.info("Indicizzato %s: %d chunk", source, len(chunks))
    return len(chunks)

print(ingest_file(blob_name))