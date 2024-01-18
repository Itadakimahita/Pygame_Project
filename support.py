from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []


    for _, __, img_files in walk(path): #got the folder in view (path, folder inside, files)
        for image in img_files:
            full_path = path + '/' + image #combine path with file name like (../graph/Grass + / + grass1.png)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


