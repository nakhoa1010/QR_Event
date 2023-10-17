import cv2
import time
def capture(image_name):
    cap = cv2.VideoCapture(0) # 0 for default webcam
    start_time = time.time()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if 10 seconds have passed
        if time.time() - start_time >= 5:
            # Save the image
            save_path = "facepath\\" + image_name 
            cv2.imwrite(save_path, frame)
            break
        # Display the resulting frame
        cv2.putText(frame, 'Wait 5 seconds', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('frame', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    path = "facepath\\" +  image_name
    return path
    cap.release()
    cv2.destroyAllWindows()
# if __name__ == "__main__":
#     print('save to: ' + capture('ID001.jpg'))
