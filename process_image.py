# dice_dataset_generator.py
# This script generates a synthetic dataset for dice recognition by applying various transformations to a set of dice images.
# The goal is to create a diverse, open-source, sharable dataset suitable for training a deep learning model for a Gradio app.
# Comprehensive post-processing ensures variety, even with a small set of cellphone images, and detailed comments make it reusable.

# Import necessary libraries
import os
import random
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

# Define the input and output directories
INPUT_DIR = 'original_dice_images/'  # Directory containing original dice images (e.g., from your cellphone)
OUTPUT_DIR = 'augmented_dice_dataset/'  # Directory to save augmented images
TARGET_SIZE = (224, 224)  # Standard size for model input (common for deep learning models like CNNs)

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Define the number of augmented images to generate per original image
AUGMENTATIONS_PER_IMAGE = 50  # Adjust this to control dataset size

# List of dice types (assumes images are named with dice type prefix, e.g., 'd6_1.jpg')
DICE_TYPES = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']  # Common polyhedral dice types

# Function to load images from the input directory
def load_images(input_dir):
    """
    Loads dice images from the input directory and organizes them by dice type.
    Assumes filenames start with dice type (e.g., 'd6_1.jpg').
    """
    images = {}
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Support common image formats
            dice_type = filename.split('_')[0]  # Extract dice type from filename
            if dice_type in DICE_TYPES:
                if dice_type not in images:
                    images[dice_type] = []
                images[dice_type].append(os.path.join(input_dir, filename))
    return images

# Function to apply random rotation
def random_rotation(image):
    """
    Rotates the image by a random angle between -45 and 45 degrees to simulate different orientations.
    """
    angle = random.randint(-45, 45)
    return image.rotate(angle, expand=True)  # Expand ensures the entire rotated image is kept

# Function to apply random skewing
def random_skew(image):
    """
    Skews the image to mimic perspective changes, common in cellphone photos taken at angles.
    """
    width, height = image.size
    skew_factor = random.uniform(-0.2, 0.2)  # Moderate skew to keep it realistic
    new_width = int(width + abs(skew_factor * height))
    skewed = image.transform((new_width, height), Image.AFFINE, (1, skew_factor, 0, 0, 1, 0))
    return skewed

# Function to add Gaussian noise
def add_gaussian_noise(image):
    """
    Adds Gaussian noise to simulate real-world imperfections like graininess in cellphone images.
    """
    img_array = np.array(image)
    noise = np.random.normal(0, 25, img_array.shape)  # Mean 0, std dev 25
    noisy_img = img_array + noise
    noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)  # Ensure values stay in valid range
    return Image.fromarray(noisy_img)

# Function to apply random brightness adjustment
def random_brightness(image):
    """
    Adjusts brightness randomly to simulate different lighting conditions (e.g., indoor vs. outdoor).
    """
    factor = random.uniform(0.5, 1.5)  # Range from dimmer to brighter
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# Function to apply random contrast adjustment
def random_contrast(image):
    """
    Adjusts contrast to enhance or reduce visibility of dice features.
    """
    factor = random.uniform(0.5, 1.5)  # Range from lower to higher contrast
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# Function to apply random color balance adjustment
def random_color_balance(image):
    """
    Shifts RGB channels to simulate different camera settings or lighting hues.
    """
    r_factor = random.uniform(0.8, 1.2)
    g_factor = random.uniform(0.8, 1.2)
    b_factor = random.uniform(0.8, 1.2)
    r, g, b = image.split()  # Split into RGB channels
    r = r.point(lambda i: i * r_factor)
    g = g.point(lambda i: i * g_factor)
    b = b.point(lambda i: i * b_factor)
    return Image.merge('RGB', (r, g, b))

# Function to apply random Gaussian blur
def random_blur(image):
    """
    Applies blur to vary sharpness, simulating out-of-focus cellphone shots.
    """
    radius = random.uniform(0, 2)  # Light to moderate blur
    return image.filter(ImageFilter.GaussianBlur(radius))

# Function to randomly crop the image
def random_crop(image, crop_ratio=0.8):
    """
    Crops the image randomly to focus on different parts of the dice, increasing variety.
    """
    width, height = image.size
    new_width = int(width * crop_ratio)
    new_height = int(height * crop_ratio)
    left = random.randint(0, width - new_width)
    top = random.randint(0, height - new_height)
    right = left + new_width
    bottom = top + new_height
    return image.crop((left, top, right, bottom))

# Function to resize image to target size
def resize_image(image, size=TARGET_SIZE):
    """
    Resizes the image to a standard size for model input, using high-quality Lanczos resampling.
    """
    return image.resize(size, Image.LANCZOS)

# Augmentation pipeline
def augment_image(image):
    """
    Combines various transformations into a pipeline to create a unique augmented image.
    Each transformation is applied randomly to ensure diversity.
    """
    # Geometric transformations
    if random.random() < 0.5:
        image = random_rotation(image)
    if random.random() < 0.5:
        image = random_skew(image)
    if random.random() < 0.5:
        image = ImageOps.mirror(image)  # Horizontal flip
    if random.random() < 0.5:
        image = ImageOps.flip(image)    # Vertical flip

    # Color and lighting variations
    image = random_brightness(image)
    image = random_contrast(image)
    image = random_color_balance(image)

    # Noise and distortion
    if random.random() < 0.3:
        image = add_gaussian_noise(image)
    if random.random() < 0.3:
        image = random_blur(image)

    # Randomly crop and resize
    if random.random() < 0.5:
        crop_ratio = random.uniform(0.7, 1.0)  # Crop between 70-100% of original size
        image = random_crop(image, crop_ratio)
    image = resize_image(image)

    return image

# Function to generate augmented dataset
def generate_dataset(images, output_dir, augmentations_per_image):
    """
    Generates the augmented dataset by applying the augmentation pipeline to each original image.
    Saves results in a structured directory by dice type.
    """
    for dice_type, image_paths in images.items():
        type_output_dir = os.path.join(output_dir, dice_type)
        if not os.path.exists(type_output_dir):
            os.makedirs(type_output_dir)
        for idx, image_path in enumerate(image_paths):
            original_image = Image.open(image_path).convert('RGB')  # Ensure RGB format
            for aug_idx in range(augmentations_per_image):
                augmented_image = augment_image(original_image.copy())  # Work on a copy
                save_path = os.path.join(type_output_dir, f"{dice_type}_{idx}_{aug_idx}.jpg")
                augmented_image.save(save_path, quality=95)  # High-quality JPEG

# Main function
def main():
    """
    Executes the dataset generation process.
    """
    images = load_images(INPUT_DIR)
    if not images:
        print("No valid images found in the input directory. Please add images and try again.")
        return
    generate_dataset(images, OUTPUT_DIR, AUGMENTATIONS_PER_IMAGE)
    print(f"Augmented dataset generated in {OUTPUT_DIR} with {AUGMENTATIONS_PER_IMAGE} images per original.")

if __name__ == "__main__":
    main()