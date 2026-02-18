# app.py
import cv2
import numpy as np
from flask import Flask, request, render_template_string, jsonify
from ultralytics import YOLO
from dictToFen import dict_to_fen

# --- Inicjalizacja aplikacji Flask ---
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def detect_board_and_pieces(img_stream, turn='w'):
    YOLO_BOARD_PATH = 'board.pt'
    board_detector = YOLO(YOLO_BOARD_PATH)

    YOLO_PIECE_PATH = 'piece.pt'
    piece_detector = YOLO(YOLO_PIECE_PATH)

    nparr = np.frombuffer(img_stream, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return "Błąd: Nie można odczytać obrazu."

    results = board_detector(img, verbose=False)

    final_board_dict = {}
    board_found = False

    for result in results:
        boxes = result.boxes
        if len(boxes) == 0:
            continue

        board_found = True
        box = boxes[0]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        board_img = img[y1:y2, x1:x2]

        square_size_y = board_img.shape[0] // 8
        square_size_x = board_img.shape[1] // 8

        # Inicjalizacja słownika pustymi polami
        for i in range(8):
            for j in range(8):
                square_name = chr(97 + j) + str(8 - i)
                final_board_dict[square_name] = ""

        # Detekcja figur na każdym polu
        for i in range(8):
            for j in range(8):
                square_name = chr(97 + j) + str(8 - i)
                y_start, y_end = i * square_size_y, (i + 1) * square_size_y
                x_start, x_end = j * square_size_x, (j + 1) * square_size_x
                square_img = board_img[y_start:y_end, x_start:x_end]

                if square_img.size == 0:
                    continue

                pieces = piece_detector(square_img, verbose=False)

                for piece in pieces:
                    if len(piece.boxes) > 0:
                        best_piece = sorted(piece.boxes, key=lambda b: b.conf[0], reverse=True)[0]
                        cls = int(best_piece.cls[0])
                        conf = best_piece.conf[0]
                        if conf > 0.6:  # Próg pewności
                            final_board_dict[square_name] = piece_detector.names[cls]
                            #show detected piece on the square for debugging
                            cv2.putText(square_img, piece_detector.names[cls][6:], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.imshow(f"Square {square_name}", square_img)
                            cv2.waitKey(500)  # Pokaż przez 500 ms
                            break  # Weź tylko najlepszą detekcję


    if not board_found:
        return "Nie wykryto szachownicy na obrazie."

    return dict_to_fen(final_board_dict, turn)


# --- Szablon HTML z dodanym przyciskiem "Kontynuuj w Chess.com" ---
HTML_TEMPLATE = """
<!doctype html>
<html lang="pl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Analizator Szachownicy</title>
    <style>
        body { font-family: sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 0; }
        .container { max-width: 800px; margin: 40px auto; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); background-color: #fff; border: 2px dashed #3498db; }
        h1 { text-align: center; color: #2c3e50; }
        p { text-align: center; font-size: 1.2em; color: #7f8c8d; }
        .turn-selector { display: flex; align-items: center; justify-content: center; gap: 20px; margin: 20px 0; font-size: 1.1em; }
        .result-container { margin-top: 20px; }
        .result { padding: 15px; background-color: #eafaf1; border: 1px solid #bceabc; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 1.1em; word-wrap: break-word; }
        .error { background-color: #f8d7da; border-color: #f5c6cb; color: #721c24; }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }

        /* === POCZĄTEK MODYFIKACJI === */

        .button-group { display: flex; gap: 10px; }
        .btn {
            padding: 8px 12px; font-size: 14px; cursor: pointer;
            color: white; border: none; border-radius: 4px;
            text-decoration: none; display: inline-block;
        }
        #copy-button { background-color: #3498db; }
        #copy-button:hover { background-color: #2980b9; }

        /* Styl dla przycisku Chess.com */
        #chesscom-link { background-color: #2ecc71; } /* Zielony kolor */
        #chesscom-link:hover { background-color: #27ae60; }

        /* === KONIEC MODYFIKACJI === */

        .toast {
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
            background-color: #2c3e50; color: white; padding: 15px 25px;
            border-radius: 5px; z-index: 100; opacity: 0;
            transition: opacity 0.3s ease-in-out;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Wklej zrzut ekranu szachownicy</h1>
        <p>Naciśnij Ctrl+V, aby przeanalizować obraz.</p>
        <div class="turn-selector">
            <strong>Kolej na ruch:</strong>
            <label><input type="radio" name="turn" value="w" checked> Białe</label>
            <label><input type="radio" name="turn" value="b"> Czarne</label>
        </div>
        <div class="result-container" id="result-container"></div>
    </div>
    <div id="toast" class="toast">Skopiowano!</div>

    <script>
        function showToast() {
            const toast = document.getElementById('toast');
            toast.style.opacity = '1';
            setTimeout(() => { toast.style.opacity = '0'; }, 2000);
        }

        function displayResult(fen) {
            const container = document.getElementById('result-container');
            const isError = fen.toLowerCase().includes('błąd') || fen.toLowerCase().includes('nie wykryto');
            let htmlContent = '';
            if (isError) {
                htmlContent = `<div class="result error">${fen}</div>`;
            } else if (fen === 'Przetwarzanie obrazu...') {
                htmlContent = `<div class="result">${fen}</div>`;
            } else {
                // === POCZĄTEK MODYFIKACJI ===
                // Dodajemy grupę przycisków, w tym nowy link do Chess.com
                htmlContent = `
                    <div class="result-header">
                        <h2>Wynik (FEN):</h2>
                        <div class="button-group">
                            <button id="copy-button" class="btn">Kopiuj</button>
                            <a href="#" id="chesscom-link" class="btn" target="_blank" rel="noopener noreferrer">Kontynuuj w Chess.com</a>
                        </div>
                    </div>
                    <div class="result" id="fen-output">${fen}</div>
                `;
                // === KONIEC MODYFIKACJI ===
            }
            container.innerHTML = htmlContent;

            if (!isError && fen !== 'Przetwarzanie obrazu...') {
                // === POCZĄTEK MODYFIKACJI ===
                // Logika, która buduje i przypisuje link do przycisku Chess.com
                const chessComLink = document.getElementById('chesscom-link');
                if (chessComLink) {
                    const encodedFen = encodeURIComponent(fen);
                    chessComLink.href = `https://www.chess.com/analysis?fen=${encodedFen}`;
                }
                // === KONIEC MODYFIKACJI ===

                const copyButton = document.getElementById('copy-button');
                if (copyButton) {
                    copyButton.addEventListener('click', () => {
                        const fenText = document.getElementById('fen-output').innerText;
                        navigator.clipboard.writeText(fenText).then(showToast).catch(err => {
                            console.error('Błąd kopiowania:', err);
                        });
                    });
                }
            }
        }

        window.addEventListener('paste', event => {
            const items = (event.clipboardData || event.originalEvent.clipboardData).items;
            let imageFile = null;
            for (const item of items) {
                if (item.kind === 'file' && item.type.startsWith('image/')) {
                    imageFile = item.getAsFile();
                    break;
                }
            }
            if (imageFile) {
                event.preventDefault();
                displayResult('Przetwarzanie obrazu...');
                const formData = new FormData();
                formData.append('file', imageFile, 'screenshot.png');
                const turn = document.querySelector('input[name="turn"]:checked').value;
                formData.append('turn', turn);
                fetch('/analyze', { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => { displayResult(data.fen); })
                .catch(error => {
                    console.error('Błąd:', error);
                    displayResult('Błąd: Wystąpił problem z połączeniem z serwerem.');
                });
            }
        });
    </script>
</body>
</html>
"""


# --- Trasy aplikacji Flask (bez zmian) ---
@app.route('/')
def upload_page():
    return render_template_string(HTML_TEMPLATE)


@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({'fen': 'Błąd: Serwer nie otrzymał pliku.'}), 400

    file = request.files['file']
    turn = request.form.get('turn', 'w')

    # Wczytaj strumień bajtów z przesłanego pliku
    img_stream = file.read()

    # Zdekoduj strumień do formatu obrazu, z którym może pracować OpenCV
    nparr = np.frombuffer(img_stream, np.uint8)
    img_color = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Sprawdź, czy obraz został poprawnie wczytany
    if img_color is None:
        return jsonify({'fen': 'Błąd: Nie można przetworzyć pliku obrazu.'}), 400

    # Konwertuj obraz na skalę szarości (czarno-biały)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # Konwertuj obraz z powrotem do formatu 3-kanałowego (BGR),
    # ponieważ modele YOLO zazwyczaj oczekują takiego wejścia.
    # Obraz nadal będzie wyglądał na czarno-biały.
    img_bgr_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    # Zakoduj przetworzony obraz z powrotem do strumienia bajtów (w formacie PNG)
    is_success, buffer = cv2.imencode(".png", img_bgr_gray)
    processed_img_stream = buffer.tobytes()

    # Przekaż przetworzony (czarno-biały) obraz do funkcji detekcji
    fen_result = detect_board_and_pieces(processed_img_stream, turn)

    return jsonify({'fen': fen_result})

if __name__ == '__main__':
    app.run(debug=True)