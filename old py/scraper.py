import os
import shutil

import requests


# scrape pieces
def scrape_pieces():
    pieces_list = {}
    f = open("../data/forScraper/rodzajeFigur.txt", "r")
    for x in f:
        x = x.strip()
        if x[0] == "b":
            pieces_list[x] = x[1:]
        elif x[0] == "w":
            pieces_list[x] = x[1:].upper()
    f.close()
    print(pieces_list)
    fig_types = []
    f = open("../data/forScraper/figury.txt", "r")
    for x in f:
        x = x.strip()
        fig_types.append(x)
    f.close()
    print(fig_types)
    DELETE = True
    if os.path.exists("../data/figures") and DELETE == True:
        shutil.rmtree("../data/figures", ignore_errors=True)
    for piece in pieces_list:
        for fig_type in fig_types:
            fig_type = fig_type.lower()
            if not os.path.exists("data/figures/" + fig_type):
                os.makedirs("data/figures/" + fig_type)
            url = f"https://images.chesscomfiles.com/chess-themes/pieces/{fig_type}/150/{piece}.png"
            file = open(f"data/figures/{fig_type}/{piece}.png", "wb")
            file.write(requests.get(url).content)
            file.close()
            print(f"Downloaded {piece} with type {fig_type}")
    print("Done")
    return

def scrape_boards():
    board_types=[]
    f = open("../data/forScraper/plansze.txt", "r")
    for x in f:
        x = x.strip()
        board_types.append(x)
    f.close()
    print(board_types)
    DELETE = True
    if os.path.exists("../data/boards") and DELETE == True:
        shutil.rmtree("../data/boards", ignore_errors=True)
    for board in board_types:
        board = board.lower()
        if not os.path.exists("../data/boards"):
            os.makedirs("../data/boards")
        url = f"https://images.chesscomfiles.com/chess-themes/boards/{board}/200.png"
        file = open(f"data/boards/{board}.png", "wb")
        file.write(requests.get(url).content)
        file.close()
        print(f"Downloaded {board}")
    print("Done")
    return

scrape_pieces()
scrape_boards()