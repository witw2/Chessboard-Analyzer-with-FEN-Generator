def dict_to_fen(board_dict, turn='w'):
    # === POCZĄTEK MODYFIKACJI ===
    # Słownik mapujący nazwy figur na ich symbole FEN (małą literą)
    piece_to_fen_char = {
        'pawn': 'p',
        'rook': 'r',
        'knight': 'n',  # Poprawne mapowanie dla skoczka
        'bishop': 'b',
        'queen': 'q',
        'king': 'k'
    }
    # === KONIEC MODYFIKACJI ===

    fen_rows = []
    for rank in range(8, 0, -1):
        fen_row = ""
        empty_count = 0
        for file in 'abcdefgh':
            square = f"{file}{rank}"
            piece = board_dict.get(square, '')
            if piece == '':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0

                # === POCZĄTEK MODYFIKACJI ===
                # Dzielimy nazwę figury na kolor i typ, np. 'white_king' -> ('white', 'king')
                try:
                    color, piece_type = piece.split('_')

                    # Pobieramy symbol ze słownika
                    fen_char = piece_to_fen_char[piece_type]

                    # Zmieniamy wielkość litery w zależności od koloru
                    if color == 'white':
                        fen_row += fen_char.upper()
                    else:  # color == 'black'
                        fen_row += fen_char.lower()
                except (ValueError, KeyError):
                    raise ValueError(f"Unknown piece format: {piece}")
                # === KONIEC MODYFIKACJI ===

        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    fen_position = '/'.join(fen_rows)

    # Reszta funkcji pozostaje bez zmian
    castling_rights = ''
    if board_dict.get('e1') == 'white_king':
        if board_dict.get('h1') == 'white_rook':
            castling_rights += 'K'
        if board_dict.get('a1') == 'white_rook':
            castling_rights += 'Q'
    if board_dict.get('e8') == 'black_king':
        if board_dict.get('h8') == 'black_rook':
            castling_rights += 'k'
        if board_dict.get('a8') == 'black_rook':
            castling_rights += 'q'

    if not castling_rights:
        castling_rights = '-'

    en_passant = '-'
    halfmove_clock = '0'
    fullmove_number = '1'

    fen = f"{fen_position} {turn} {castling_rights} {en_passant} {halfmove_clock} {fullmove_number}"
    return fen