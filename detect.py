import cv2
from ultralytics import YOLO
from dictToFen import dict_to_fen

def detect_board_and_pieces(img=cv2.imread("test.png"), turn='w'):

    YOLO_BOARD_PATH = 'runs/detect/yolov8n_board_detection/board.pt'
    board_detector = YOLO(YOLO_BOARD_PATH)

    YOLO_PIECE_PATH = 'runs/detect/yolov8m_piece_detection/piece.pt'
    piece_detector = YOLO(YOLO_PIECE_PATH)

    results = board_detector(img, verbose=False)

    final_board_dict={}
    #cut board from image
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            board_img = img[y1:y2, x1:x2]
            cv2.imwrite("board.png", board_img)
            #split board into 64 squares in dictionary
            square_size_x = (x2 - x1) // 8
            square_size_y = (y2 - y1) // 8
            squares = {}
            for i in range(8):
                for j in range(8):
                    square_name = chr(97 + j) + str(8 - i)
                    square_img = board_img[i * square_size_y:(i + 1) * square_size_y, j * square_size_x:(j + 1) * square_size_x]
                    squares[square_name] = square_img
                    pieces=piece_detector(square_img, verbose=False)
                    for piece in pieces:
                        boxes = piece.boxes
                        detected_piece_name=""
                        for box in boxes:
                            cls = int(box.cls[0])
                            conf = box.conf[0]
                            if conf > 0.5:
                                detected_piece_name=piece_detector.names[cls]
                    final_board_dict[square_name]=detected_piece_name

    return(dict_to_fen(final_board_dict,turn))