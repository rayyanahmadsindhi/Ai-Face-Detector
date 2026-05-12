#!/usr/bin/env python3
"""
Simple camera test script to verify camera is working
"""

import cv2
import numpy as np

def test_camera():
    """Test camera functionality"""
    print("Testing camera...")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return False
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("✓ Camera opened successfully")
    
    # Read a few frames to test
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print(f"✓ Frame {i+1}: {frame.shape[1]}x{frame.shape[0]} - {frame.dtype}")
        else:
            print(f"❌ Failed to read frame {i+1}")
            cap.release()
            return False
    
    # Test face detection
    print("\nTesting face detection...")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        print("❌ Error: Could not load face cascade")
        cap.release()
        return False
    
    print("✓ Face cascade loaded successfully")
    
    # Test detection on last frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
    
    print(f"✓ Face detection working - found {len(faces)} faces")
    
    # Show frame for 3 seconds
    print("\nShowing camera feed for 3 seconds...")
    cv2.imshow('Camera Test', frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    
    cap.release()
    print("✓ Camera test completed successfully")
    return True

if __name__ == "__main__":
    print("Camera Test Script")
    print("=" * 20)
    
    if test_camera():
        print("\n🎉 Camera is working perfectly!")
        print("You can now run the main application: python face_detector.py")
    else:
        print("\n❌ Camera test failed. Please check your camera setup.")
