import os
from PIL import Image

images_path = "data/input/hard-sdxl-human"
masks_path = "data/masks/Slazzer/hard-sdxl-humans"
segmented_path = "output/segmented"
images = [file for file in os.listdir(images_path) if file.endswith('.png')]

for i, image_name in enumerate(images):
    print(f"{i}/{len(images)}: Processing image {image_name}")
    image_path = os.path.join(images_path, image_name)
    raw_image = Image.open(image_path).convert("RGBA")
    mask_image_path = os.path.join(masks_path, image_name)
    mask = Image.open(mask_image_path).convert("L")

    if raw_image.size != mask.size:
        mask = mask.resize(raw_image.size)

    segmented = Image.composite(raw_image, Image.new("RGBA", raw_image.size, 0), mask)
    segmented_image_path = os.path.join(segmented_path, image_name)
    segmented.save(segmented_image_path)
    print(f"Segmented image saved as {segmented_image_path}")

