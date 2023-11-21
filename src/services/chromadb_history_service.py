import chromadb
import datetime


class ChromaDBHistoryService:

    def __init__(self):
        self.client = chromadb.Client()  # Create a ChromaDB client
        # self.client = chromadb.PersistentClient(path="./persistence") # Create a persistent ChromaDB client
        self.collection = self.client.get_or_create_collection(name="history")  # Create a collection

    def save_history(self, history_item, caller):
        self.collection.add(
            documents=[history_item],
            metadatas=[{"source": caller, "history": True}],  # Add metadata about the history
            ids=[datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")]  # Use a unique ID based on UTC timestamp
        )
        print(f"memory: {history_item}")

    def get_history(self, text: str) -> str:
        """
        Query the ChromaDB collection for memories related to a given text.

        Args:
            text (str): The text to search for in memories.

        Returns:
            str: A concatenated string of relevant history documents.
        """
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

    # def save_history(self, user_prompt: str, generated_text: str, caller: str) -> None:
    #     """
    #     Save a history to the ChromaDB collection.
    #
    #     Args:
    #         user_prompt (str): The user's prompt to the AI.
    #         generated_text (str): The AI's response to the prompt.
    #         caller (str): The source of the history (e.g., "Chat AI", "Notes").
    #     """
    #     self.collection.add(
    #         # documents=[
    #         #     # Indent the history for readability
    #         #     f"{user_prompt} | {generated_text}\n"
    #         # ],
    #         embeddings=[],
    #         metadatas=[{"source": caller, "history": True}],  # Add metadata about the history
    #         ids=[datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")]  # Use a unique ID based on UTC timestamp
    #     )
    #
    # def get_history(self, text: str) -> str:
    #     """
    #     Query the ChromaDB collection for memories related to a given text.
    #
    #     Args:
    #         text (str): The text to search for in memories.
    #
    #     Returns:
    #         str: A concatenated string of relevant history documents.
    #     """
    #     results = self.collection.query(
    #         query_texts=[text],  # Search for memories containing the given text
    #         n_results=100,  # Limit the number of results to 100
    #         where={"history": True}  # Filter for memories only
    #         # where_document={"$contains":"search_string"}  # Optional filter for specific document fields
    #     )
    #
    #     # Loop over the documents and create a single string of the document values
    #     document_string = ""
    #     for document in results['documents'][0]:
    #         document_string += document
    #
    #     return document_string
