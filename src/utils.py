import pygame, json
import os 

SCRIPT_PATH = os.getcwd()

def get_image_surface(file_path):
    image = pygame.image.load(file_path).convert()
    return image

def readJson(file_path):
    with open(file_path, "r") as file:
        json_data = file.read()
    return json.loads(json_data)
