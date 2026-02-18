# Chessboard Analyzer with FEN Generator

## Description
This project is a Python-based application that detects chessboards and pieces from images, generates their FEN (Forsyth-Edwards Notation) representation, and allows seamless integration with Chess.com for further analysis. The application uses Flask for the web interface, YOLOv8 for object detection, and OpenCV for image processing.

## Features
- Detects chessboards and pieces from uploaded images.
- Generates FEN notation for the detected chessboard state.
- Provides an option to continue analysis on Chess.com.
- Supports both white and black turns.
- Includes a user-friendly web interface.

## Technologies Used
- **Programming Language**: Python
- **Libraries and Tools**:
  - Flask: Web framework for the application.
  - OpenCV: Image processing library.
  - YOLOv8: Object detection model for detecting chessboards and pieces.
  - NumPy: Numerical operations.
- **Development Environment**: PyCharm.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the YOLOv8 models (`board.pt` and `piece.pt`) and place them in the project directory.

## Usage
1. Run the Flask application:
   python main.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000/`.
3. Paste a screenshot of a chessboard to analyze it.
4. Copy the generated FEN or continue analysis on Chess.com.

## Project Structure
- `main.py`: Entry point for the Flask application.
- `createPieces.py`: Script for generating training data for YOLO models.
- `trainPieceClassifier.py`: Script for training the YOLO model to detect chess pieces.
- `dictToFen.py`: Converts the detected board state into FEN notation.
- `templates/`: Contains HTML templates for the web interface.
- `static/`: Contains static files like CSS and JavaScript.

## Example Workflow
1. Upload a chessboard image.
2. The application detects the board and pieces using YOLOv8.
3. The detected board state is converted into FEN notation.
4. The FEN can be copied or used to continue analysis on Chess.com.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- YOLOv8 by Ultralytics for object detection.
- OpenCV for image processing.
- Flask for the web framework.
