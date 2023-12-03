import pygame, os

def load_images():
    images_path = os.path.join('assets','images')
    
    # Get all file names (without extension) in the directory
    image_names = [os.path.splitext(f)[0] for f in os.listdir(images_path)]
    
    image_index = {}
    
    for name in image_names:
        image_path = os.path.join(images_path, name + '.png')
        image_index[name] = pygame.image.load(image_path).convert_alpha()
    
    return image_index