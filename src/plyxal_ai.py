from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import argparse

SEED = 1234
MODEL_CKPT_PATH = "Qwen/Qwen-VL-Chat-Int4"
MODEL_CACHE_PATH = "/"

hello = "hello"

class Main():
    """
    PlyxalAI is a class that interacts with a pre-trained language model for text and image-based conversations.

    Args:
        seed (int, optional): The seed for random number generation. Defaults to SEED.
        ckpt_path (str, optional): The path to the pre-trained model checkpoint. Defaults to MODEL_CKPT_PATH.
        cache_path (str, optional): The path for caching model files. Defaults to MODEL_CACHE_PATH.
        message (str, optional): The text message to send to the model.
        image (str, optional): The URL of the image to send along with the message.
    """

    
    def __init__(self, seed=None, ckpt_path=None, cache_path=None, message=None, image=None):
        """
        Initializes the PlyxalAI instance with specified or default values.

        Args:
            seed (int, optional): The seed for random number generation. Defaults to None.
            ckpt_path (str, optional): The path to the pre-trained model checkpoint. Defaults to None.
            cache_path (str, optional): The path for caching model files. Defaults to None.
            message (str, optional): The text message to send to the model.
            image (str, optional): The URL of the image to send along with the message.
        """
        seed = seed if seed is not None else SEED
        ckpt_path = ckpt_path if ckpt_path is not None else MODEL_CKPT_PATH
        cache_path = cache_path if cache_path is not None else MODEL_CACHE_PATH

        print("PlyxalAI Init")
        self.set_values_and_load_models(seed, ckpt_path, cache_path)

        if message:
            response = self.send_text(message)
            print("Response:", response)
        elif image:
            response = self.send_image(image, message)
            print("Response:", response)

            
    def set_values_and_load_models(self, seed=SEED, ckpt_path=MODEL_CKPT_PATH, cache_path=MODEL_CACHE_PATH):
        """
        Sets the seed, initializes the tokenizer, and loads the pre-trained model.

        Args:
            seed (int, optional): The seed for random number generation. Defaults to SEED.
            ckpt_path (str, optional): The path to the pre-trained model checkpoint. Defaults to MODEL_CKPT_PATH.
            cache_path (str, optional): The path for caching model files. Defaults to MODEL_CACHE_PATH.
        """
        torch.manual_seed(seed)
        self.tokenizer = AutoTokenizer.from_pretrained(ckpt_path, trust_remote_code=True, cache_dir=cache_path)
        self.model = AutoModelForCausalLM.from_pretrained(ckpt_path, device_map="auto", trust_remote_code=True, resume_download=True, cache_dir=cache_path).eval()

        
    def send_text(self, message):
        """
        Sends a text message to the model and returns the response.

        Args:
            message (str): The text message to send to the model.

        Returns:
            str: The response from the model.
        """
        response, history = self.model.chat(self.tokenizer, message, history)
        return response

    
    def send_image(self, image_url, message):
        """
        Sends an image and text message to the model and returns the response.

        Args:
            image_url (str): The URL of the image to send.
            message (str): The text message to send along with the image.

        Returns:
            str: The response from the model.
        """
        query = self.tokenizer.from_list_format([
            {'image': image_url if image_url is not None else ''},
            {'text': message},
        ])
        response, history = self.model.chat(self.tokenizer, query=query, history=None, cache_dir=self.MODEL_CACHE_PATH)
        return response

def test(words):
    print(words)
    
def main():
    """
    The main entry point for the PlyxalAI Command Line Tool.

    This function parses command-line arguments, such as message and image, to interact with the PlyxalAI instance.

    Usage:
        python script_name.py --message "Your message here" --image "Image URL here"

    Arguments:
        --message (str, optional): The text message to send to PlyxalAI.
        --image (str, optional): The URL of the image to send along with the message.
    """
    parser = argparse.ArgumentParser(description='PlyxalAI Command Line Tool')
    parser.add_argument('--message', type=str, help='Message to send to PlyxalAI')
    parser.add_argument('--image', type=str, help='URL of the image to send along with the message')

    args = parser.parse_args()

    plyxal_ai = PlyxalAi(message=args.message, image=args.image)

    
if __name__ == '__main__':
    main()
