import os
from PIL import Image

images_path = "output/segmented"
background_image_path = "data/background/true-back-e5e6eb.png"
output_folder_path = "output/image_background/e5e6eb"

background = os.path.basename(background_image_path)[:-4]
segmented_images = [file for file in os.listdir(images_path) if file.endswith('.png')]
background_image = Image.open(background_image_path)
for i, seg_image_name in enumerate(segmented_images):
    print(f"{i}/{len(segmented_images)}: Processing image {seg_image_name}")
    image_path = os.path.join(images_path, seg_image_name)
    raw_image = Image.open(image_path)
    background_image = background_image.resize(raw_image.size)
    combined_image = Image.composite(raw_image, background_image, raw_image)
    output_path = os.path.join(output_folder_path, seg_image_name)
    combined_image.save(output_path)
    print(f"{i}/{len(segmented_images)}: Image {seg_image_name} added background {background}")