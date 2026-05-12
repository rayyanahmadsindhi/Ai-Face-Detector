# AI Face Detection Application

A real-time face detection application that uses your camera to detect faces and draws green square boundaries around them with alert notifications.

## Features

- 🎥 **Real-time Camera Access**: Uses your device's camera for live video feed
- 🔍 **AI Face Detection**: Advanced skin tone detection algorithm to identify faces
- 🟢 **Green Square Boundaries**: Draws animated green boxes around detected faces
- 🔔 **Alert Notifications**: Shows popup alerts when faces are detected
- 📊 **Live Statistics**: Displays face count and detection status
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations

## How to Use

1. **Open the Application**: Open `index.html` in your web browser
2. **Allow Camera Access**: When prompted, click "Allow" to grant camera permissions
3. **Start Detection**: Click the "Start Detection" button to begin face detection
4. **View Results**: 
   - Green square boundaries will appear around detected faces
   - Face count will update in real-time
   - Alert popups will show when new faces are detected
5. **Stop Detection**: Click "Stop Detection" to pause the detection

## Technical Details

### Face Detection Algorithm
The application uses a custom face detection algorithm that:
- Analyzes video frames for skin tone patterns
- Uses flood-fill algorithm to group skin pixels into regions
- Applies size and shape filters to identify face-like regions
- Calculates confidence scores for each detection

### Browser Compatibility
- **Chrome/Edge**: Full support with camera access
- **Firefox**: Full support with camera access
- **Safari**: Full support with camera access
- **Mobile Browsers**: Supported on iOS Safari and Android Chrome

### Performance
- Optimized for real-time performance
- Samples every 4th pixel for faster processing
- Runs detection at 10 FPS for smooth experience
- Automatic canvas resizing for different screen sizes

## File Structure

```
Ai 2/
├── index.html          # Main HTML structure
├── style.css           # CSS styling and animations
├── script.js           # JavaScript face detection logic
└── README.md           # This documentation
```

## Requirements

- Modern web browser with camera support
- HTTPS connection (required for camera access in most browsers)
- Camera permissions granted by the user

## Troubleshooting

### Camera Not Working
- Ensure you're using HTTPS (required for camera access)
- Check that camera permissions are granted
- Try refreshing the page and allowing permissions again
- Make sure no other application is using the camera

### Poor Detection Accuracy
- Ensure good lighting conditions
- Position your face clearly in the camera view
- Avoid extreme angles or partial face coverage
- The algorithm works best with clear, well-lit faces

### Performance Issues
- Close other applications using the camera
- Try reducing the browser window size
- Ensure your device has sufficient processing power

## Customization

You can customize the application by modifying:

- **Detection Sensitivity**: Adjust `faceDetectionThreshold` in `script.js`
- **Colors and Styling**: Modify CSS variables in `style.css`
- **Detection Speed**: Change the interval in the `startDetection()` method
- **Alert Duration**: Modify the timeout in `showFaceDetectedAlert()`

## Future Enhancements

Potential improvements for future versions:
- Integration with TensorFlow.js for more accurate detection
- Multiple face tracking with unique IDs
- Face recognition capabilities
- Export functionality for detected faces
- Advanced filtering and detection options

## License

This project is open source and available under the MIT License.
