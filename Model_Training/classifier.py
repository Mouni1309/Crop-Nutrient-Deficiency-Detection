from ultralytics import YOLO
import os
import shutil
import random

# Define your paths
source_dir = 'datasets/rice_plant_lacks_nutrients'
output_dir = 'datasets/split_dataset'

# Split ratios
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

# Make sure output directories exist
for split in ['train', 'val', 'test']:
    for class_name in os.listdir(source_dir):
        os.makedirs(os.path.join(output_dir, split, class_name), exist_ok=True)

# Loop through each class
for class_name in os.listdir(source_dir):
    class_path = os.path.join(source_dir, class_name)
    images = os.listdir(class_path)
    random.shuffle(images)

    train_split = int(len(images) * train_ratio)
    val_split = int(len(images) * (train_ratio + val_ratio))

    train_images = images[:train_split]
    val_images = images[train_split:val_split]
    test_images = images[val_split:]

    # Move files
    for image in train_images:
        shutil.copy(os.path.join(class_path, image),
                    os.path.join(output_dir, 'train', class_name, image))
    for image in val_images:
        shutil.copy(os.path.join(class_path, image),
                    os.path.join(output_dir, 'val', class_name, image))
    for image in test_images:
        shutil.copy(os.path.join(class_path, image),
                    os.path.join(output_dir, 'test', class_name, image))

print("Dataset split complete!")

model = YOLO('yolov8m-cls.pt')




result = model.train(data = 'datasets\split_dataset', epochs = 10, batch = 128)