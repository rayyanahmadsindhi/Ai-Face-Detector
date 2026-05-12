#!/usr/bin/env python3
"""
Test script to verify all required imports work correctly
"""

def test_imports():
    """Test if all required packages can be imported"""
    try:
        print("Testing imports...")
        
        # Test OpenCV
        import cv2
        print("✓ OpenCV imported successfully")
        print(f"  OpenCV version: {cv2.__version__}")
        
        # Test NumPy
        import numpy as np
        print("✓ NumPy imported successfully")
        print(f"  NumPy version: {np.__version__}")
        
        # Test PIL/Pillow
        from PIL import Image, ImageTk
        print("✓ PIL/Pillow imported successfully")
        
        # Test Tkinter (should be built-in)
        import tkinter as tk
        print("✓ Tkinter imported successfully")
        
        # Test threading (should be built-in)
        import threading
        print("✓ Threading imported successfully")
        
        # Test datetime (should be built-in)
        import datetime
        print("✓ Datetime imported successfully")
        
        print("\n🎉 All imports successful! The face detection app should work correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease install the required packages:")
        print("pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_camera():
    """Test if camera can be accessed"""
    try:
        import cv2
        print("\nTesting camera access...")
        
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera access successful")
            ret, frame = cap.read()
            if ret:
                print("✓ Camera can capture frames")
                print(f"  Frame size: {frame.shape[1]}x{frame.shape[0]}")
            else:
                print("❌ Camera cannot capture frames")
            cap.release()
        else:
            print("❌ Camera access failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Camera test error: {e}")
        return False

def test_face_cascade():
    """Test if face cascade can be loaded"""
    try:
        import cv2
        print("\nTesting face detection model...")
        
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if face_cascade.empty():
            print("❌ Face cascade could not be loaded")
            return False
        else:
            print("✓ Face detection model loaded successfully")
            return True
            
    except Exception as e:
        print(f"❌ Face cascade test error: {e}")
        return False

if __name__ == "__main__":
    print("AI Face Detection - Import Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test camera
        camera_ok = test_camera()
        
        # Test face cascade
        cascade_ok = test_face_cascade()
        
        print("\n" + "=" * 40)
        print("Test Summary:")
        print(f"Imports: {'✓' if imports_ok else '❌'}")
        print(f"Camera: {'✓' if camera_ok else '❌'}")
        print(f"Face Detection: {'✓' if cascade_ok else '❌'}")
        
        if imports_ok and camera_ok and cascade_ok:
            print("\n🎉 All tests passed! You can run the face detection app.")
            print("Run: python face_detector.py")
        else:
            print("\n⚠️  Some tests failed. Please check the issues above.")
    else:
        print("\n❌ Import test failed. Please install required packages first.")
