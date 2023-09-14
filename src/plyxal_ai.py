import qwen_vl_int4
import argparse
    
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
    
    print("Hello World")
    
    parser = argparse.ArgumentParser(description='PlyxalAI Command Line Tool')
    parser.add_argument('--message', type=str, help='Message to send to PlyxalAI')
    parser.add_argument('--image', type=str, help='URL of the image to send along with the message')

    args = parser.parse_args()

    qwen_vl_int4.sayHi()
    # plyxal_ai = qwent_vl_int4.Main(message=args.message, image=args.image)

    
if __name__ == '__main__':
    main()
