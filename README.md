
# Image Compressor

Image Compressor is a simple Python application that allows users to compress images while maintaining quality. It supports multiple image formats and provides a user-friendly interface for uploading, compressing, and downloading images.

## Features

- Compress images with adjustable compression levels.
- Supports multiple image formats: JPEG, PNG, BMP, GIF, TIFF.
- Handles EXIF data to correct image orientation.
- Provides detailed error messages for unsupported formats, corrupted files, size/memory issues, and EXIF data issues.
- User-friendly interface with drag-and-drop support and compression level adjustment.
- Saves compressed images in a new "compressed" directory within the original image directory.

## Requirements

- Python 3.x
- tkinter
- Pillow (PIL)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/skr2270/ImageSqueezer.git
   cd image-compressor
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Use the interface:**
   - Click "Upload Image" to select images for compression.
   - Adjust the compression level using the slider.
   - Click "Download Compressed Images" to compress and save the images.

3. **Check the console output:**
   - Successful compressions and any errors encountered will be printed to the console.

## Error Handling

- **Unsupported Formats / Corrupted Files**: The application will raise an alert and log the error.
- **Size / Memory Issues**: The application will raise an alert if there is an issue related to the size or memory while compressing.
- **EXIF Data Issues**: The application will log any issues related to EXIF data but will attempt to compress the image.

## Building an Executable

To create an executable file for the application:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   pyinstaller --onefile --noconsole --name ImageSqueeze main.py
   ```

3. **Locate the executable:**
   - The executable will be created in the `dist` directory and will be named `ImageSqueeze.exe`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Pillow](https://python-pillow.org/) for image processing.
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI.
- [PyInstaller](https://www.pyinstaller.org/) for creating the executable.
