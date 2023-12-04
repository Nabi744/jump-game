# Delete this file before submission

from PIL import Image, ImageEnhance

def adjust_brightness(image_path, output_path, brightness_factor):
    image = Image.open(image_path)

    enhancer = ImageEnhance.Brightness(image)
    image_brightened = enhancer.enhance(brightness_factor)

    # Save the result
    image_brightened.save(output_path)


# Example usage
input_image_path = "images/lamp/lamp_0.png"
output_image_path = "what_you_want_as_name.png"
brightness_factor = 1.5  # Adjust this value based on your desired brightness level

adjust_brightness(input_image_path, output_image_path, brightness_factor)
