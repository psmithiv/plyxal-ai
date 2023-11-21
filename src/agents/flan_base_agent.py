"""
Module for interacting with the BART language model.
"""

import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from src.services.chromadb_history_service import ChromaDBHistoryService
import textwrap


class HistoryAgent:

    def __init__(self):
        # Load the BART model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

        # Initialize the conversation history management service
        self.history = ChromaDBHistoryService()

    def bart_generate(self, user_prompt: str) -> str:
        # Retrieve relevant the corresponding conversation history from the database
        conversation_history = self.history.get_history(user_prompt)

        # Construct the prompt for BART generation
        prompt = f"Conversation History:\n{conversation_history}\nUser Prompt:{user_prompt}"
        print(f"prompt: {prompt}\n")

        # Tokenize the input prompt
        input_ids = self.tokenizer(prompt, return_tensors="pt")

        # Generate text using the BART model
        output_ids = self.model.generate(
            input_ids["input_ids"], max_length=100, num_beams=4
        )

        # Decode the generated output
        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Update conversation history with the new interaction
        self.history.save_history(user_prompt=user_prompt, generated_text=generated_text,
                                  caller="chromadb_history_service")

        print(f"\n\ngenerated_text: {generated_text}")

        return generated_text

    def build_interface(self):
        interface = gr.Interface(
            fn=self.bart_generate,
            inputs=["text"],
            outputs=["text"],
            title="BART Text Generation",
            description="Generate text using the BART language model.",
        )

        # Start the Gradio interface
        interface.launch(
            share=False,
            debug=False,
        )


if __name__ == "__main__":
    # Initialize the HistoryAgent object
    bart = HistoryAgent()

    # Build the Gradio interface for user interaction
    bart.build_interface()
