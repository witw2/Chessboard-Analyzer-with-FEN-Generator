#clasify piece on the board using yolov8m
from ultralytics import YOLO

# Załaduj wstępnie wytrenowany model YOLOv8.
model = YOLO('yolov8m.pt')

# Rozpocznij trening modelu
if __name__ == '__main__':
    results = model.train(
        data='configPieces.yaml',  # ścieżka do pliku konfiguracyjnego
        epochs=20,                # liczba epok (ile razy model "przejrzy" cały zbiór danych)
        imgsz=64,                # rozmiar obrazu, do którego skalowane będą zdjęcia
        batch=32,                 # ile obrazów przetwarzanych jest jednocześnie (dostosuj do pamięci VRAM)
        name='yolov8m_piece_detection' # nazwa folderu z wynikami
    )