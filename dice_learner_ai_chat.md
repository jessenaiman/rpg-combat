I apologize for the misunderstanding! Since you want to visually verify the images downloaded from the internet (from the download_dice_images.ipynb script) rather than manually created ones, I’ll provide a tailored script to display those specific images after they’re downloaded into original_dice_images/. This script will focus on the internet-sourced images, assuming they’ve been saved with the expected naming convention (e.g., d6_1.jpg) from the download process. It will integrate seamlessly into your Jupyter notebook workflow and allow you to confirm the quality and correctness of the downloaded images before proceeding with augmentation and training.
Jupyter Notebook Script: verify_downloaded_dice_images.ipynb
python
# Cell 1: Import required libraries
import os
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image

# Cell 2: Script to visually verify downloaded dice images
# Define the directory containing downloaded images
INPUT_DIR = Path('original_dice_images')
DICE_TYPES = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']  # Supported dice types

def load_downloaded_images(input_dir):
    """
    Loads downloaded images from the input directory, organized by dice type.
    Assumes filenames are from the download script (e.g., 'd6_1.jpg').
    
    :param input_dir: Path object to the directory with downloaded images.
    :return: Dictionary mapping dice types to lists of image paths.
    """
    images = {dice_type: [] for dice_type in DICE_TYPES}
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            dice_type = filename.split('_')[0].lower()
            if dice_type in DICE_TYPES:
                images[dice_type].append(input_dir / filename)
    return images

def display_downloaded_samples(images, samples_per_type=3):
    """
    Displays a sample of downloaded images for each dice type for visual verification.
    
    :param images: Dictionary of dice type to list of image paths.
    :param samples_per_type: Number of images to display per dice type.
    """
    # Set up the figure with subplots
    fig, axes = plt.subplots(len(DICE_TYPES), samples_per_type, 
                            figsize=(samples_per_type * 4, len(DICE_TYPES) * 4))
    fig.suptitle('Visual Verification of Downloaded Dice Images', fontsize=16)

    # Iterate through each dice type
    for row, dice_type in enumerate(DICE_TYPES):
        image_paths = images[dice_type]
        if not image_paths:
            print(f"Warning: No downloaded images found for {dice_type}")
            for col in range(samples_per_type):
                axes[row, col].text(0.5, 0.5, f"No {dice_type} images", 
                                   ha='center', va='center')
                axes[row, col].axis('off')
            continue
        
        # Display up to 'samples_per_type' images
        for col in range(samples_per_type):
            if col < len(image_paths):
                try:
                    img = Image.open(image_paths[col])
                    axes[row, col].imshow(img)
                    axes[row, col].set_title(f"{dice_type}_{col + 1}")
                except Exception as e:
                    axes[row, col].text(0.5, 0.5, f"Error: {e}", 
                                       ha='center', va='center')
            else:
                axes[row, col].text(0.5, 0.5, "No more images", 
                                   ha='center', va='center')
            axes[row, col].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Load and display downloaded images
downloaded_images = load_downloaded_images(INPUT_DIR)
display_downloaded_samples(downloaded_images, samples_per_type=3)

# Cell 3: Print summary of downloaded images
print("Summary of downloaded images per dice type:")
for dice_type, paths in downloaded_images.items():
    print(f"{dice_type}: {len(paths)} images")
How to Use in Your Jupyter Notebook
Insert After Downloading:
Add this script to your existing notebook (e.g., dice_project.ipynb) right after the download script (download_dice_images.ipynb).
Place it in new cells following the download cells:
Cell 1: Imports (likely already present).
Cell 2: Verification script.
Cell 3: Summary output.
Run the Cells:
First, run the download script to populate original_dice_images/ with images from the internet (e.g., 5 per dice type).
Then, run these cells to display and summarize the downloaded images.
Visual Verification:
A 6x3 grid (6 dice types, 3 samples each) will appear.
Check each row to ensure:
Images correspond to the correct dice type (e.g., d6 images show six-sided dice).
Quality is sufficient (not blurry, mislabeled, or irrelevant).
No errors (e.g., corrupted files) are shown.
Proceed or Adjust:
If images look good, move to augmentation (dice_dataset_generator.py) and training.
If issues arise (e.g., wrong dice, poor quality), re-run the download script or filter out bad images manually.
Example Workflow in Your Notebook
python
# Existing Cell: Download images
!pip install requests beautifulsoup4
import requests, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

INPUT_DIR = Path('original_dice_images')
INPUT_DIR.mkdir(exist_ok=True)
DICE_TYPES = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']

def download_dice_images(num_images_per_die=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for dice_type in DICE_TYPES:
        print(f"Searching for {dice_type} images...")
        search_url = f"https://duckduckgo.com/?q={dice_type}+dice&t=h_&iar=images&iax=images&ia=images"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', limit=num_images_per_die + 10)
        img_urls = [tag.get('src') for tag in img_tags if tag.get('src')]
        for idx, img_url in enumerate(img_urls[:num_images_per_die], 1):
            try:
                if not img_url.startswith('http'):
                    img_url = urljoin(search_url, img_url)
                img_response = requests.get(img_url, headers=headers, timeout=5)
                if img_response.status_code == 200:
                    file_path = INPUT_DIR / f"{dice_type}_{idx}.jpg"
                    with open(file_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded: {file_path}")
            except:
                pass

download_dice_images(num_images_per_die=5)

# New Cell: Verify downloaded images (insert the script above here)
import matplotlib.pyplot as plt
from PIL import Image

INPUT_DIR = Path('original_dice_images')
DICE_TYPES = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']

def load_downloaded_images(input_dir):
    images = {dice_type: [] for dice_type in DICE_TYPES}
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            dice_type = filename.split('_')[0].lower()
            if dice_type in DICE_TYPES:
                images[dice_type].append(input_dir / filename)
    return images

def display_downloaded_samples(images, samples_per_type=3):
    fig, axes = plt.subplots(len(DICE_TYPES), samples_per_type, 
                            figsize=(samples_per_type * 4, len(DICE_TYPES) * 4))
    fig.suptitle('Visual Verification of Downloaded Dice Images', fontsize=16)
    for row, dice_type in enumerate(DICE_TYPES):
        image_paths = images[dice_type]
        if not image_paths:
            print(f"Warning: No downloaded images for {dice_type}")
            for col in range(samples_per_type):
                axes[row, col].text(0.5, 0.5, f"No {dice_type} images", 
                                   ha='center', va='center')
                axes[row, col].axis('off')
            continue
        for col in range(samples_per_type):
            if col < len(image_paths):
                try:
                    img = Image.open(image_paths[col])
                    axes[row, col].imshow(img)
                    axes[row, col].set_title(f"{dice_type}_{col + 1}")
                except Exception as e:
                    axes[row, col].text(0.5, 0.5, f"Error: {e}", 
                                       ha='center', va='center')
            else:
                axes[row, col].text(0.5, 0.5, "No more images", 
                                   ha='center', va='center')
            axes[row, col].axis('off')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

downloaded_images = load_downloaded_images(INPUT_DIR)
display_downloaded_samples(downloaded_images, samples_per_type=3)

print("Summary of downloaded images per dice type:")
for dice_type, paths in downloaded_images.items():
    print(f"{dice_type}: {len(paths)} images")
Notes
Purpose: This verifies only the internet-downloaded images, not manually created ones (since you’ve already checked those).
Output: A grid showing up to 3 images per dice type, with a summary of counts (e.g., d6: 5 images).
Timing: Run this right after downloading but before augmentation to catch issues early.
This script ensures you can trust the internet-sourced data before the lengthy training process, keeping your project on track. Let me know if you need further refinements!