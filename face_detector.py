import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import numpy as np
import os

class FaceDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Face Detection - Python Version")
        self.root.geometry("1000x700")
        self.root.configure(bg='#667eea')
        
        # Detection variables
        self.is_detecting = False
        self.cap = None
        self.face_cascade = None
        self.last_face_count = 0
        self.detection_thread = None
        
        # GUI variables
        self.face_count_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Ready")
        
        self.setup_ui()
        self.load_face_cascade()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#667eea')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#667eea')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, 
            text="🤖 AI Face Detection", 
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#667eea'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Real-time face detection with green boundaries",
            font=('Arial', 12),
            fg='white',
            bg='#667eea'
        )
        subtitle_label.pack()
        
        # Camera display frame
        camera_frame = tk.Frame(main_frame, bg='black', relief=tk.RAISED, bd=2)
        camera_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Video label
        self.video_label = tk.Label(
            camera_frame, 
            text="Click 'Start Detection' to begin",
            font=('Arial', 16),
            fg='white',
            bg='black',
            width=80,
            height=20
        )
        self.video_label.pack(expand=True, fill=tk.BOTH)
        
        # Control buttons frame
        controls_frame = tk.Frame(main_frame, bg='#667eea')
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Status label
        self.status_label = tk.Label(
            controls_frame,
            textvariable=self.status_var,
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#667eea'
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Buttons
        button_frame = tk.Frame(controls_frame, bg='#667eea')
        button_frame.pack(side=tk.RIGHT)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start Detection",
            command=self.start_detection,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=3
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop Detection",
            command=self.stop_detection,
            font=('Arial', 12, 'bold'),
            bg='#f44336',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        # Info panel
        info_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X)
        
        # Info title
        info_title = tk.Label(
            info_frame,
            text="Detection Information",
            font=('Arial', 14, 'bold'),
            fg='#333',
            bg='white'
        )
        info_title.pack(pady=(15, 10))
        
        # Info content
        info_content = tk.Frame(info_frame, bg='white')
        info_content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Face count
        face_count_frame = tk.Frame(info_content, bg='white')
        face_count_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            face_count_frame,
            text="Faces Detected:",
            font=('Arial', 12, 'bold'),
            fg='#666',
            bg='white'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            face_count_frame,
            textvariable=self.face_count_var,
            font=('Arial', 12, 'bold'),
            fg='#4CAF50',
            bg='white'
        ).pack(side=tk.RIGHT)
        
        # Detection status
        status_frame = tk.Frame(info_content, bg='white')
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            status_frame,
            text="Status:",
            font=('Arial', 12, 'bold'),
            fg='#666',
            bg='white'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            status_frame,
            text="Ready",
            font=('Arial', 12, 'bold'),
            fg='#4CAF50',
            bg='white'
        ).pack(side=tk.RIGHT)
        
    def load_face_cascade(self):
        """Load the Haar cascade classifier for face detection"""
        try:
            # Load face cascade
            face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            
            if self.face_cascade.empty():
                raise Exception("Failed to load face cascade")
                
            self.status_var.set("Face detection model loaded successfully")
            print("Face cascade loaded successfully")
            
        except Exception as e:
            print(f"Error loading face cascade: {e}")
            self.status_var.set("Error: Face detection model not available")
    
    def start_detection(self):
        """Start the face detection process"""
        if self.is_detecting:
            return
            
        try:
            # Initialize camera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open camera")
            
            # Set camera properties for better quality
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
            self.cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
            self.cap.set(cv2.CAP_PROP_SATURATION, 0.5)
            
            # Test camera by reading a frame
            ret, test_frame = self.cap.read()
            if not ret or test_frame is None:
                raise Exception("Camera is not working properly")
            
            print(f"Camera initialized successfully. Frame size: {test_frame.shape[1]}x{test_frame.shape[0]}")
            
            self.is_detecting = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set("Face detection active...")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            self.detection_thread.start()
            
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to start camera: {str(e)}")
            self.status_var.set("Camera error - please check your camera")
            if self.cap:
                self.cap.release()
                self.cap = None
    
    def stop_detection(self):
        """Stop the face detection process"""
        self.is_detecting = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Detection stopped")
        self.face_count_var.set("0")
        
        # Clear video display
        self.video_label.config(
            text="Click 'Start Detection' to begin",
            image=""
        )
    
    def detection_loop(self):
        """Main detection loop running in separate thread"""
        while self.is_detecting and self.cap:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect faces
                faces = self.detect_faces(frame)
                
                # Debug information
                if len(faces) > 0:
                    print(f"Faces detected: {len(faces)}")
                    for i, (x, y, w, h) in enumerate(faces):
                        print(f"  Face {i+1}: x={x}, y={y}, w={w}, h={h}, area={w*h}")
                
                # Draw face boundaries on the original frame
                frame_with_detections = self.draw_face_boundaries(frame, faces)
                
                # Update face count
                self.face_count_var.set(str(len(faces)))
                
                # Update last count (no alerts)
                self.last_face_count = len(faces)
                
                # Convert frame for tkinter display - keep original size
                frame_rgb = cv2.cvtColor(frame_with_detections, cv2.COLOR_BGR2RGB)
                
                # Get the actual video dimensions
                height, width = frame_rgb.shape[:2]
                
                # Resize to fit the display area while maintaining aspect ratio
                display_width = 640
                display_height = 480
                
                # Calculate aspect ratio
                aspect_ratio = width / height
                
                if aspect_ratio > display_width / display_height:
                    # Video is wider than display area
                    new_width = display_width
                    new_height = int(display_width / aspect_ratio)
                else:
                    # Video is taller than display area
                    new_height = display_height
                    new_width = int(display_height * aspect_ratio)
                
                # Resize frame
                frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
                
                # Convert to PhotoImage
                photo = self.cv2_to_photoimage(frame_resized)
                
                # Update GUI in main thread
                self.root.after(0, self.update_video_display, photo)
                
                # Control frame rate
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Error in detection loop: {e}")
                break
    
    def detect_faces(self, frame):
        """Detect faces in the frame using Haar cascade with improved accuracy"""
        if self.face_cascade is None:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces with balanced parameters
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,   # Standard scale factor
            minNeighbors=6,    # Moderate minNeighbors to balance accuracy and detection
            minSize=(30, 30),  # Smaller minimum size to catch more faces
            maxSize=(500, 500), # Larger maximum size
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Apply lighter validation to filter obvious false positives
        valid_faces = []
        for (x, y, w, h) in faces:
            if self.is_valid_face_light(gray, x, y, w, h):
                valid_faces.append((x, y, w, h))
        
        # If no faces pass validation, use basic filtering
        if len(valid_faces) == 0 and len(faces) > 0:
            print("No faces passed validation, using basic filtering...")
            for (x, y, w, h) in faces:
                # Very basic checks only
                aspect_ratio = w / h
                if 0.3 < aspect_ratio < 3.0 and w > 20 and h > 20:
                    valid_faces.append((x, y, w, h))
        
        # Remove overlapping detections
        valid_faces = self.remove_overlapping_faces(valid_faces)
        
        return np.array(valid_faces)
    
    def is_valid_face(self, gray, x, y, w, h):
        """Validate if the detected region is actually a face"""
        # Extract the face region
        face_region = gray[y:y+h, x:x+w]
        
        if face_region.size == 0:
            return False
        
        # Check aspect ratio (faces are roughly square-ish)
        aspect_ratio = w / h
        if aspect_ratio < 0.6 or aspect_ratio > 1.8:
            return False
        
        # Check size constraints
        if w < 40 or h < 40 or w > 300 or h > 300:
            return False
        
        # Check for face-like features using edge detection
        edges = cv2.Canny(face_region, 50, 150)
        edge_density = np.sum(edges > 0) / (w * h)
        
        # Faces should have moderate edge density (not too smooth, not too busy)
        if edge_density < 0.05 or edge_density > 0.3:
            return False
        
        # Check for symmetry (faces are roughly symmetric)
        left_half = face_region[:, :w//2]
        right_half = cv2.flip(face_region[:, w//2:], 1)
        
        # Resize to same dimensions for comparison
        min_width = min(left_half.shape[1], right_half.shape[1])
        if min_width > 10:
            left_half = left_half[:, :min_width]
            right_half = right_half[:, :min_width]
            
            # Calculate correlation between left and right halves
            correlation = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
            if correlation < 0.3:  # Too asymmetric
                return False
        
        # Check for skin-like color in the center region
        center_y, center_x = h//2, w//2
        center_region = face_region[center_y-10:center_y+10, center_x-10:center_x+10]
        
        if center_region.size > 0:
            # Check if the center region has reasonable intensity (not too dark or too bright)
            mean_intensity = np.mean(center_region)
            if mean_intensity < 30 or mean_intensity > 200:
                return False
        
        return True
    
    def is_valid_face_light(self, gray, x, y, w, h):
        """Light validation to filter obvious false positives while keeping real faces"""
        # Extract the face region
        face_region = gray[y:y+h, x:x+w]
        
        if face_region.size == 0:
            return False
        
        # Basic aspect ratio check (faces are roughly square-ish)
        aspect_ratio = w / h
        if aspect_ratio < 0.4 or aspect_ratio > 2.5:
            return False
        
        # Basic size constraints
        if w < 25 or h < 25 or w > 400 or h > 400:
            return False
        
        # Check if the region has reasonable content (not completely dark or bright)
        mean_intensity = np.mean(face_region)
        if mean_intensity < 20 or mean_intensity > 230:
            return False
        
        # Basic edge check - faces should have some edges
        edges = cv2.Canny(face_region, 30, 100)
        edge_density = np.sum(edges > 0) / (w * h)
        
        # Very lenient edge density check
        if edge_density < 0.02:
            return False
        
        return True
    
    def remove_overlapping_faces(self, faces):
        """Remove overlapping face detections, keeping the best one"""
        if len(faces) <= 1:
            return faces
        
        # Sort by area (largest first)
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        
        filtered_faces = []
        for i, (x1, y1, w1, h1) in enumerate(faces):
            is_overlapping = False
            for j, (x2, y2, w2, h2) in enumerate(filtered_faces):
                # Calculate overlap
                overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
                overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
                overlap_area = overlap_x * overlap_y
                
                area1 = w1 * h1
                area2 = w2 * h2
                overlap_ratio = overlap_area / min(area1, area2)
                
                if overlap_ratio > 0.3:  # 30% overlap threshold
                    is_overlapping = True
                    break
            
            if not is_overlapping:
                filtered_faces.append((x1, y1, w1, h1))
        
        return filtered_faces
    
    def draw_face_boundaries(self, frame, faces):
        """Draw green square boundaries around detected faces"""
        frame_with_faces = frame.copy()
        
        for i, (x, y, w, h) in enumerate(faces):
            # Draw green rectangle
            cv2.rectangle(frame_with_faces, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Draw face number and confidence
            label = f"Face {i + 1}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            
            # Background for text
            cv2.rectangle(
                frame_with_faces,
                (x, y - 30),
                (x + label_size[0] + 10, y),
                (0, 255, 0),
                -1
            )
            
            # Face number text
            cv2.putText(
                frame_with_faces,
                label,
                (x + 5, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 0),
                2
            )
            
            # Draw corner markers for better visibility
            corner_length = 20
            thickness = 3
            
            # Top-left corner
            cv2.line(frame_with_faces, (x, y), (x + corner_length, y), (0, 255, 0), thickness)
            cv2.line(frame_with_faces, (x, y), (x, y + corner_length), (0, 255, 0), thickness)
            
            # Top-right corner
            cv2.line(frame_with_faces, (x + w, y), (x + w - corner_length, y), (0, 255, 0), thickness)
            cv2.line(frame_with_faces, (x + w, y), (x + w, y + corner_length), (0, 255, 0), thickness)
            
            # Bottom-left corner
            cv2.line(frame_with_faces, (x, y + h), (x + corner_length, y + h), (0, 255, 0), thickness)
            cv2.line(frame_with_faces, (x, y + h), (x, y + h - corner_length), (0, 255, 0), thickness)
            
            # Bottom-right corner
            cv2.line(frame_with_faces, (x + w, y + h), (x + w - corner_length, y + h), (0, 255, 0), thickness)
            cv2.line(frame_with_faces, (x + w, y + h), (x + w, y + h - corner_length), (0, 255, 0), thickness)
        
        return frame_with_faces
    
    # Alert functionality removed as requested
    
    def update_video_display(self, photo):
        """Update the video display in the GUI"""
        try:
            self.video_label.config(image=photo)
            self.video_label.image = photo  # Keep a reference
        except Exception as e:
            print(f"Error updating video display: {e}")
    
    def cv2_to_photoimage(self, frame):
        """Convert OpenCV frame to PhotoImage for tkinter"""
        from PIL import Image, ImageTk
        
        # Convert numpy array to PIL Image
        image = Image.fromarray(frame)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        return photo
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_detection()
        self.root.destroy()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FaceDetectorApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
