import gradio as gr
from transformers import T5Tokenizer, T5ForConditionalGeneration
from src.services.chromadb_history_service import ChromaDBHistoryService


class HistoryAgent:
    def __init__(self):
        self.model_name = "google/flan-t5-xxl"
        print(f"Model: {self.model_name}")
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name, offload_folder="models")

        # Initialize the conversation history management service
        self.history = ChromaDBHistoryService()

    def generate_response(self, user_input):
        # Encode the user input
        input_ids = self.tokenizer(user_input, return_tensors="pt").input_ids
        prompt_text = self.tokenizer.decode(input_ids[0], skip_special_tokens=False)
        print(f"prompt_text: {prompt_text}")

        # Generate a response using the BART model
        outputs = self.model.generate(input_ids)
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=False)

        # Print the generated text
        print(f"generated_text: {generated_text}")

        return generated_text

    def build_interface(self):
        # Create a Gradio interface
        interface = gr.Interface(
            fn=self.generate_response,
            inputs=["text"],
            outputs=["text"],
            title=self.model_name,
            description="Basic Agent",
        )

        # Launch the Gradio interface
        interface.launch(
            share=False,
            debug=False,
        )


if __name__ == "__main__":
    # Initialize the HistoryAgent object
    bart = HistoryAgent()

    # Build the Gradio interface for user interaction
    bart.build_interface()
