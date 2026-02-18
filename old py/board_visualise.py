import io
import os
import PIL.Image

import chess
import chess.pgn

board="rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
board_theme="green"
piece_theme="neo"

def visualise_board(board, board_theme="green", piece_theme="neo", size=1200):
    data=board.split(" ")
    board=data[0]
    # turn=data[1]
    # castling=data[2]
    # en_passant=data[3]
    # halfmove=data[4]
    # fullmove=data[5]
    board=board.split("/")
    board_theme=board_theme.lower()
    piece_theme=piece_theme.lower()
    rows=[]
    for row in board:
        row=list(row)
        new_row=[]
        for cell in row:
            if cell.isnumeric():
                for i in range(int(cell)):
                    new_row.append(" ")
            else:
                new_row.append(cell)
        rows.append(new_row)
    #open the board theme to pil
    board_theme=open(f"data/boards/{board_theme}.png", "rb").read()
    board_theme=PIL.Image.open(io.BytesIO(board_theme))
    board_theme=board_theme.resize((size, size))

    pieces={}
    for piece in os.listdir(f"data/figures/{piece_theme}"):
        name=piece.split(".")[0]
        if name[0]=="b":
            name=name[1:]
        elif name[0]=="w":
            name=name[1:].upper()
        #make the piece theme to pil with transparency
        pieces[name]=open(f"data/figures/{piece_theme}/{piece}", "rb").read()
        pieces[name]=PIL.Image.open(io.BytesIO(pieces[name])).convert("RGBA")
        pieces[name]=pieces[name].resize((int(size/8), int(size/8)))
    #create a new image
    board_img=PIL.Image.new("RGB", (size, size))
    #paste the board theme
    board_img.paste(board_theme, (0, 0))
    #paste the pieces
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            if cell!=" ":
                board_img.paste(pieces[cell], (int(j*(size/8)), int(i*(size/8))), pieces[cell])
    return board_img

def fen_from_png(pgn):
    # Initialize a chess board
    board = chess.Board()

    # Split the moves and play them on the board
    fen_list = [board.fen()]  # Start with the initial position
    moves = pgn.split()
    for move in moves:
        board.push_san(move)
        fen_list.append(board.fen())

    return fen_list