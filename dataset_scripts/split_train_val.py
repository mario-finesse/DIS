from typing import List, Tuple
import os
import shutil
from PIL import Image
from tqdm import tqdm
from sklearn.model_selection import train_test_split

def resize_image(image_path:str, new_size:Tuple[int, int]) -> Image.Image:
    image = Image.open(image_path)
    resized_image = image.resize(new_size)
    return resized_image

def create_dataset_split(image_path:str, mask_path:str, train_image_dest:str, train_mask_dest:str, val_image_dest:str, val_mask_dest:str, test_size=0.2):
    assert os.path.exists(image_path) and os.path.isdir(image_path), f"Directory does not exist: {image_path}"
    assert os.path.exists(mask_path) and os.path.isdir(mask_path), f"Directory does not exist: {mask_path}"
    assert os.path.exists(train_image_dest) and os.path.isdir(train_image_dest), f"Directory does not exist: {train_image_dest}"
    assert os.path.exists(train_mask_dest) and os.path.isdir(train_mask_dest), f"Directory does not exist: {train_mask_dest}"
    assert os.path.exists(val_image_dest) and os.path.isdir(val_image_dest), f"Directory does not exist: {val_image_dest}"
    assert os.path.exists(val_mask_dest) and os.path.isdir(val_mask_dest), f"Directory does not exist: {val_mask_dest}"

    # Get all file names in the image and mask directories
    image_names = [f.split(".")[0] for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]
    # Split the dataset into training and validation sets
    train_names, val_names = train_test_split(image_names, test_size=test_size)

    new_size = (896, 1152)
    # Function to copy files
    def copy_files(files:List[str], src_path:str, dest_path:str):
        for file in tqdm(files, desc=f"Copying {src_path} and resizing {new_size}"):
            src = os.path.join(src_path, file)
            resized_image = resize_image(src, new_size)
            dest = os.path.join(dest_path, file)
            resized_image.save(dest)
        print(f"Finished copying from {src_path} to {dest_path}")
        
    # Copy files
    train_images = [image_name + ".jpg" for image_name in train_names]
    train_masks = [image_name + ".png" for image_name in train_names]
    val_images = [image_name + ".jpg" for image_name in val_names]
    val_masks = [image_name + ".png" for image_name in val_names]
    copy_files(train_images, image_path, train_image_dest)
    copy_files(train_masks, mask_path, train_mask_dest)
    copy_files(val_images, image_path, val_image_dest)
    copy_files(val_masks, mask_path, val_mask_dest)

images = "data/input/hard-sdxl-human"
masks = "data/masks/Slazzer/hard-sdxl-humans"

train_path_image = "data/FINESSE/FINESSE-TR/im"
train_path_mask = "data/FINESSE/FINESSE-TR/gt"

val_path_image = "data/FINESSE/FINESSE-VD/im"
val_path_mask = "data/FINESSE/FINESSE-VD/gt"

create_dataset_split(images, masks, train_path_image, train_path_mask, val_path_image, val_path_mask)
