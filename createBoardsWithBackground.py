import os
import random
from PIL import Image
import numpy as np
import cv2
import io

for folder in ["data/backgrounds", "data/allBoards"]:
    if not os.path.exists(folder):
        raise Exception(f"Folder {folder} does not exist. Please run scraper and generateDB first.")

backgrounds = []
for bg in os.listdir("data/backgrounds"):
    if bg.endswith((".png", ".jpg", ".jpeg")):
        background = Image.open(f"data/backgrounds/{bg}").convert("RGBA")
        backgrounds.append(background)

boards = []
for board in os.listdir("data/allBoards"):
    if board.endswith((".png", ".jpg", ".jpeg")):
        board_img = Image.open(f"data/allBoards/{board}").convert("RGBA")
        boards.append(board_img)

if not os.path.exists("boardsYOLO"):
    os.makedirs("boardsYOLO")
if not os.path.exists("boardsYOLO/train/images"):
    os.makedirs("boardsYOLO/train/images")
if not os.path.exists("boardsYOLO/train/labels"):
    os.makedirs("boardsYOLO/train/labels")
if not os.path.exists("boardsYOLO/valid/images"):
    os.makedirs("boardsYOLO/valid/images")
if not os.path.exists("boardsYOLO/valid/labels"):
    os.makedirs("boardsYOLO/valid/labels")


def add_board_to_background(board, background, isValidation=False):
    board_size = board.size[0]  # Assuming square boards
    # change size of board randomly
    scale_factor = random.uniform(0.5, 2.0)
    board = board.resize((int(board_size * scale_factor), int(board_size * scale_factor)))
    board_size = board.size[0]

    bg_w, bg_h = background.size

    if bg_w < board_size or bg_h < board_size:
        background = background.resize((max(bg_w, board_size), max(bg_h, board_size)))
        bg_w, bg_h = background.size

    max_x = bg_w - board_size
    max_y = bg_h - board_size

    x_offset = random.randint(0, max_x)
    y_offset = random.randint(0, max_y)

    combined = background.copy()
    combined.paste(board, (x_offset, y_offset), board)

    #make label file for YOLO
    x_center = (x_offset + board_size / 2) / bg_w
    y_center = (y_offset + board_size / 2) / bg_h
    width = board_size / bg_w
    height = board_size / bg_h
    label = f"0 {x_center} {y_center} {width} {height}\n"
    folder = "valid" if isValidation else "train"
    file = open(f"boardsYOLO/{folder}/labels/board_with_bg_{i+1}.txt", "w")
    file.write(label)
    file.close()
    return combined

for i, background in enumerate(backgrounds):
    board = random.choice(boards)
    isValidation=random.randint(0, 10)<1
    combined_image = add_board_to_background(board, background, isValidation)
    folder = "valid" if isValidation else "train"
    #make image black and white
    combined_image = combined_image.convert("L").convert("RGBA")
    #add some random black and white shift
    shift = random.randint(-30, 30)
    np_image = np.array(combined_image)
    np_image = np.clip(np_image + shift, 0, 255)
    combined_image = Image.fromarray(np_image.astype('uint8'), 'RGBA')
    combined_image.save(f"boardsYOLO/{folder}/images/board_with_bg_{i+1}.png")
    if (i + 1) % 10 == 0:
        print(f"Processed {i + 1}/{len(backgrounds)} boards")
print("Done adding backgrounds to boards.")
