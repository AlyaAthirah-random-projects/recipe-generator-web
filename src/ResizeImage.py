from PIL import Image
import os


def resize_image(input_path, max_size=2000):
    # Open the image file
    with Image.open(input_path) as img:
        # Get original dimensions
        width, height = img.size

        # Check if the image needs to be resized
        if width > max_size or height > max_size:
            # Calculate new dimensions while maintaining aspect ratio
            if width > height:
                new_width = max_size
                new_height = int((max_size / width) * height)
            else:
                new_height = max_size
                new_width = int((max_size / height) * width)

            # Resize the image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the resized image back to the same path
            img.save(input_path)  # Save to the same input path
            print(f"Image resized to {new_width}x{new_height} and saved at {input_path}")
        else:
            print("No resizing needed. Image is within the size limit.")

