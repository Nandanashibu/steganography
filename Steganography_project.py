from PIL import Image, ImageDraw, ImageFont
import os

def encode_image(image_path, message, text_color='red'):
    try:
        img = Image.open(image_path.strip()).convert("RGB")
    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found.")
        return
    except Exception as e:
        print(f"❌ Error opening image: {str(e)}")
        return
    
    # Create two versions
    encoded = img.copy()  # This will have only hidden data
    visible = img.copy()  # This will show the message
    
    width, height = img.size
    message += chr(0)  # End-of-message marker
    binary_message = ''.join([format(ord(char), '08b') for char in message])

    # Hide the message in both images
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index >= len(binary_message):
                break

            pixel = list(img.getpixel((x, y)))
            for i in range(3):  # R, G, B channels
                if data_index < len(binary_message):
                    new_bit = int(binary_message[data_index])
                    pixel[i] = (pixel[i] & ~1) | new_bit
                    data_index += 1

            encoded.putpixel((x, y), tuple(pixel))
            visible.putpixel((x, y), tuple(pixel))

        if data_index >= len(binary_message):
            break

    # Add visible text to the second image
    draw = ImageDraw.Draw(visible)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text_fill = (255, 0, 0) if text_color.lower() == 'red' else (255, 255, 255)
    text_position = (10, height - 30)
    draw.text(text_position, message[:-1], fill=text_fill, font=font)

    # Save both images
    base_dir = os.path.dirname(image_path)
    encoded_path = os.path.join(base_dir, "encoded_output.png")
    visible_path = os.path.join(base_dir, "visible_message.png")
    
    encoded.save(encoded_path)
    visible.save(visible_path)
    
    print(f"\n✅ Hidden message saved as '{encoded_path}'")
    print(f"✅ Visible message saved as '{visible_path}'")
    
    encoded.show()
    visible.show()


def decode_image(image_path):
    try:
        img = Image.open(image_path.strip()).convert("RGB")
    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found.")
        return
    except Exception as e:
        print(f"❌ Error opening image: {str(e)}")
        return
    
    binary_message = ''
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for i in range(3):  # R, G, B
                binary_message += str(pixel[i] & 1)

    chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
    message = ''.join(chars[:chars.index(chr(0))]) if chr(0) in chars else ''.join(chars)
    
    print("\n🔍 Decoded message:", message)


def main():
    print("📦 Steganography Tool - Hide messages in images")
    print("="*50)
    choice = input("Do you want to encode or decode an image? (e/d): ").lower()

    if choice == 'e':
        message = input("Enter the message you want to hide: ")
        while True:
            image_path = input("Enter the path to the image: ").strip('"\'')
            if os.path.exists(image_path):
                break
            print(f"❌ File not found: {image_path}")
        
        color = input("Do you want the visible text in red or white? (red/white): ").lower()
        while color not in ['red', 'white']:
            color = input("Please choose either 'red' or 'white': ").lower()

        encode_image(image_path, message, color)

    elif choice == 'd':
        while True:
            image_path = input("Enter the path to the image to decode: ").strip('"\'')
            if os.path.exists(image_path):
                break
            print(f"❌ File not found: {image_path}")
        decode_image(image_path)

    else:
        print("❌ Invalid choice. Please enter 'e' to encode or 'd' to decode.")


if __name__ == "__main__":
    main()