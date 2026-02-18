import os
import random
import time

import PIL.Image

from board_visualise import visualise_board, fen_from_png
from separator import split_chessboard

multiplier=0.7
board_types=[]
f = open("../data/forScraper/plansze.txt", "r")
for x in f:
    x = x.strip().lower()
    board_types.append(x)
f.close()

piece_types=[]
f = open("../data/forScraper/figury.txt", "r")
for x in f:
    x = x.strip().lower()
    piece_types.append(x)
f.close()

def generateFENs():
    f = open("../data/szachy.csv", "r")
    output = open("../data/fensROB.txt", "w")
    i=0
    all=20000
    for x in f:
        if i%100==0:
            percent=i/all*100
            #make progress bar
            print(f"{percent:.2f}%")
        i += 1
        x = x.strip()
        boards=fen_from_png(x)
        for board in boards:
            output.write(board+"\n")
    f.close()
    output.close()


def generateDB():
    f = open("../data/fensROB.txt", "r")
    if not os.path.exists("../data/allBoards"):
        os.makedirs("../data/allBoards")
    i=0
    all=1232886
    start = time.time()
    for x in f:
        if i%1000==1:
            percent=i/all*100
            end = time.time()
            print(f"{percent:.2f}% {end-start:.2f}s estimated time left: {(end-start)*(all-i)/i:.2f}s")
        i += 1
        x = x.strip()
        #board=visualise_board(x, random.choice(board_types), random.choice(piece_types),size=240)
        board = visualise_board(x, "green", "neo", size=240)
        board.save(f"data/allBoards/{i}.png")
    f.close()
    print("Done")

generateDB()


def allPieces():
    testFen = "qqQQ4/kkKK4/rrRR4/bbBB4/nnNN4/ppPP4/8/8"
    squares = {"a8": "bq", "b8": "bq", "c8": "wQ", "d8": "wQ", "a7": "bk", "b7": "bk", "c7": "WK", "d7": "wK", "a6": "br",
               "b6": "br", "c6": "wR", "d6": "wR", "a5": "bb", "b5": "bb", "c5": "wB", "d5": "wB", "a4": "bn", "b4": "bn",
               "c4": "wN", "d4": "wN", "a3": "bp", "b3": "bp", "c3": "wP", "d3": "wP", "a2": "!", "b2": "!", "c2": "!", "d2": "!"}
    i=0
    maxi=len(piece_types)*len(board_types)
    if not os.path.exists("../data/pieces"):
        os.makedirs("../data/pieces")
    for piece in piece_types:
        for board in board_types:
            vis=visualise_board(testFen, board, piece, size=400)
            pieces=split_chessboard(vis)
            for square in squares:
                name=squares[square].lower()
                if not os.path.exists(f"data/pieces/{name}"):
                    os.makedirs(f"data/pieces/{name}")
                pieces[square].save(f"data/pieces/{name}/{board}_{piece}.png")
            i+=1
            print(f"{i/maxi*100:.2f}%")

