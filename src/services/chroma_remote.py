import chromadb
from chromadb.config import Settings

chroma_client = chromadb.HttpClient(host="localhost", port=8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))