from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

class Qwen14bChat:
    """A class for interacting with the Qwen-14B chat model."""

    # Default constants
    MODEL_NAME = "Qwen/Qwen-14B-Chat"
    MODEL_CACHE_PATH = "./.model/qwen"
    SEED = 1111

    def __init__(self, model_name=None, model_cache_path=None, seed=None):
        """
        Initialize the Qwen14bChat instance.

        Args:
            model_name (str): The model name or path (default is MODEL_NAME).
            model_cache_path (str): The cache path for the model (default is MODEL_CACHE_PATH).
            seed (int): The seed for randomization (default is SEED).
        """
        self.model_name = model_name if model_name is not None else self.MODEL_NAME
        self.model_cache_path = model_cache_path if model_cache_path is not None else self.MODEL_CACHE_PATH
        self.seed = seed if seed is not None else self.SEED

        # Initialize the model and tokenizer
        self.init_model()
        self.history = None

    def init_model(self):
        """
        Initialize the model and tokenizer.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, use_safetensors=True, resume_download=True, cache_dir=self.model_cache_path
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, device_map="auto", use_safetensors=True,
        ).eval()
        
        self.model.generation_config = GenerationConfig.from_pretrained(
            self.model_name, use_safetensors=True
        )

    def send_message(self, message):
        """
        Send a message to the chat model and receive a response.

        Args:
            message (str): The input message.

        Returns:
            str: The model's response to the input message.
        """
        response, self.history = self.model.chat(self.tokenizer, message, history=self.history)

        return response

# Example usage:
# chatbot = Qwen14bChat()
# response = chatbot.send_message("Hello, how can I help you?")
# print(response)
