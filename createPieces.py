#create dataset from yolo using figures from piecesForYolo/pieces and pieces from piecesForYolo/board
import os
import random
from PIL import Image
import numpy as np
import cv2
import io

if not os.path.exists("piecesYOLO"):
    os.makedirs("piecesYOLO")
if not os.path.exists("piecesYOLO/train/images"):
    os.makedirs("piecesYOLO/train/images")
if not os.path.exists("piecesYOLO/train/labels"):
    os.makedirs("piecesYOLO/train/labels")
if not os.path.exists("piecesYOLO/valid/images"):
    os.makedirs("piecesYOLO/valid/images")
if not os.path.exists("piecesYOLO/valid/labels"):
    os.makedirs("piecesYOLO/valid/labels")

pieces = []
for piece in os.listdir("piecesForYolo/pieces"):
    if piece.endswith((".png", ".jpg", ".jpeg")):
        piece_img = Image.open(f"piecesForYolo/pieces/{piece}").convert("RGBA")
        pieces.append((piece_img, piece.split(".")[0]))  # Store image and its label
boards = []
for board in os.listdir("piecesForYolo/board"):
    if board.endswith((".png", ".jpg", ".jpeg")):
        board_img = Image.open(f"piecesForYolo/board/{board}").convert("RGBA")
        boards.append(board_img)

classes={
    "wp":0,
    "wr":1,
    "wn":2,
    "wb":3,
    "wq":4,
    "wk":5,
    "bp":6,
    "br":7,
    "bn":8,
    "bb":9,
    "bq":10,
    "bk":11
}

def add_piece_to_board(piece, piece_label, board, isValidation=False):
    piece_size = piece.size[0]  # Assuming square pieces
    # Change size of piece randomly
    scale_factor = random.uniform(0.5, 1.0)
    piece = piece.resize((int(piece_size * scale_factor), int(piece_size * scale_factor)))
    piece_size = piece.size[0]

    board_w, board_h = board.size

    if board_w < piece_size or board_h < piece_size:
        board = board.resize((max(board_w, piece_size), max(board_h, piece_size)))
        board_w, board_h = board.size

    max_x = board_w - piece_size
    max_y = board_h - piece_size

    x_offset = random.randint(0, max_x)
    y_offset = random.randint(0, max_y)

    combined = board.copy()
    combined.paste(piece, (x_offset, y_offset), piece)

    # Make label file for YOLO
    x_center = (x_offset + piece_size / 2) / board_w
    y_center = (y_offset + piece_size / 2) / board_h
    width = piece_size / board_w
    height = piece_size / board_h

    label_line = f"{classes[piece_label]} {x_center} {y_center} {width} {height}\n"

    if isValidation:
        img_path = f"piecesYOLO/valid/images/{random.randint(100000,999999)}.png"
        label_path = img_path.replace("images", "labels").replace(".png", ".txt")
    else:
        img_path = f"piecesYOLO/train/images/{random.randint(100000,999999)}.png"
        label_path = img_path.replace("images", "labels").replace(".png", ".txt")

    # make image black and white
    combined = combined.convert("L").convert("RGBA")
    combined.save(img_path)
    with open(label_path, "w") as label_file:
        label_file.write(label_line)

    return combined

for i in range(10000):  # Generate 10,000 images
    piece, piece_label = random.choice(pieces)
    board = random.choice(boards)
    isValidation = random.randint(0, 10) < 1
    combined_image = add_piece_to_board(piece, piece_label, board, isValidation)
    if i % 100 == 0:
        print(f"Generated {i} images")

#make more knights and kings for balancing
for i in range(2000):  # Generate 2,000 more images with knights and kings
    piece, piece_label = random.choice(pieces)
    while piece_label not in ["wn", "bk", "bn", "wk"]:
        piece, piece_label = random.choice(pieces)
    board = random.choice(boards)
    isValidation = random.randint(0, 10) < 1
    combined_image = add_piece_to_board(piece, piece_label, board, isValidation)
    if i % 100 == 0:
        print(f"Generated {i} knight/king images")
print("Done")