import chromadb
import datetime


class ChromaDBHistoryService:

    def __init__(self):
        self.client = chromadb.Client()  # Create a ChromaDB client
        # self.client = chromadb.PersistentClient(path="./persistence") # Create a persistent ChromaDB client
        self.collection = self.client.get_or_create_collection(name="test")  # Create a collection

    def save_history(self, history_item, caller):
        self.collection.add(
            documents=[history_item],
            metadatas=[{"source": caller, "history": True}],  # Add metadata about the history
            ids=[datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")]  # Use a unique ID based on UTC timestamp
        )
        print(f"memory: {history_item}")

    def get_history(self, text: str) -> str:
        results = self.collection.query(
            query_texts=[text],  # Search for memories containing the given text
            n_results=100,  # Limit the number of results to 100
            where={"history": True}  # Filter for memories only
            # where_document={"$contains":"search_string"}  # Optional filter for specific document fields
        )

        # Loop over the documents and create a single string of the document values
        document_string = ""
        for document in results['documents'][0]:
            document_string += document

        return document_string
