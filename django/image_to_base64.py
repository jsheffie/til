import base64
import sys

def image_to_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            # Read the binary data and encode to Base64
            encoded_bytes = base64.b64encode(image_file.read())
            # Decode to a UTF-8 string for easy handling/printing
            encoded_string = encoded_bytes.decode('utf-8')
            return encoded_string
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # python ./image_to_base64.py /Users/jds/Desktop/defect-Screenshot.png
        print("Usage: python image_to_base64.py <path_to_image>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    base64_data = image_to_base64(image_path)
    print(base64_data)  # Or write to a file: with open('output.txt', 'w') as f: f.write(base64_data)