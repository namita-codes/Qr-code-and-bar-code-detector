import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

def display_help():
    print("QR Code and Barcode Scanner")
    print("Instructions:")
    print("  - Press 'q' to quit the program")
    print("  - Press 'p' to pause/resume scanning")
    print("  - Press 'c' to clear detected codes")
    print()

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    detected = False       # Flag to track if a code has been detected
    pause_scanning = False # Flag to pause scanning
    frame_count = 0        # Initialize frame count
    detected_codes = set() # Set to store detected codes
    error_count = 0        # Counter for incorrect detections

    display_help()

    while not detected:
        success, img = cap.read()
        frame_count += 1
        
        if not success:
            print("Error: Failed to capture image")
            continue  # Skip to the next iteration if capture fails

        try:
            if not pause_scanning:
                codes_in_frame = decode(img)
                if codes_in_frame:
                    for code in codes_in_frame:
                        data = code.data.decode('utf-8')
                        
                        if data not in detected_codes:
                            print(f"Detected data: {data}")
                            detected_codes.add(data)
                        
                        detected = True

                        # Draw bounding box around the code
                        pts = np.array([code.polygon], np.int32).reshape((-1, 1, 2))
                        cv2.polylines(img, [pts], True, (0, 255, 0), 5)
                        
                        # Display data near the code with a colored background
                        cv2.rectangle(img, (code.rect[0], code.rect[1] - 30), (code.rect[0] + 300, code.rect[1]), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, data, (code.rect[0] + 10, code.rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                        # Display status message
                        cv2.putText(img, "QR/BarCode Detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Wait for 3 seconds before exiting
                    print("QR Code detected. Exiting in 3 seconds...")
                    cv2.imshow('QR Code Scanner', img)
                    cv2.waitKey(3000)  # Wait for 3000 milliseconds (3 seconds)
                    break
                else:
                    error_count += 1
                    if error_count >= 500:
                        print("Error: NO QR/BARCODE DETECTED. Exiting...")
                        break
            else:
                # Display paused message
                cv2.putText(img, "Scanning Paused (Press 'p' to resume)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            continue  # Skip to the next iteration if an error occurs

        # Display frame count on the image
        cv2.putText(img, f"Frame: {frame_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Show the image with detection overlay
        cv2.imshow('QR Code Scanner', img)
        
        # Check for key press events
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break  # Quit the program

        elif key == ord('p'):
            pause_scanning = not pause_scanning  # Toggle pause/resume

        elif key == ord('c'):
            detected_codes.clear()  # Clear detected codes
            error_count = 0  # Reset error count

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
