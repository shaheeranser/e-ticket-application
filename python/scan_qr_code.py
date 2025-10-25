import cv2

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is not None:
        # 1. Convert the bounding box coordinates to integers
        # bbox is a NumPy array, so we use .astype(int)
        bbox_int = bbox[0].astype(int)

        # 2. Iterate over the integer coordinates to draw the lines
        for i in range(len(bbox_int)):
            pt1 = tuple(bbox_int[i])
            pt2 = tuple(bbox_int[(i + 1) % len(bbox_int)])
            
            cv2.line(
                img,
                pt1,
                pt2,
                color=(255, 0, 0),
                thickness=2,
            )
        
        if data:
            print(f"Data found: {data}")

    cv2.imshow("QR Code Scanner", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()