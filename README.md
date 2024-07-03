# Image Compressor

Image Compressor is a simple Python application that allows users to compress images while maintaining quality. It supports multiple image formats and provides a user-friendly interface for uploading, compressing, and downloading images.

## Features

- Select multiple images for compression
- Supports multiple image formats: JPEG, PNG, BMP, GIF, TIFF.
- Displays thumbnails of selected images
- Handles EXIF data to correct image orientation.
- Provides detailed error messages for unsupported formats, corrupted files, size/memory issues, and EXIF data issues.
- User-friendly interface with drag-and-drop support and compression level adjustment.
- Real-time progress updates for image uploading and compression
- Saves compressed images in a new "compressed" directory within the original image directory.

## Requirements

- Python 3.x
- tkinter
- Pillow (PIL)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/skr2270/ImageSqueezer.git
   cd ImageSqueezer
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

## Collaboration

We welcome contributions from the community! If you would like to contribute to this project, please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. **Commit your changes** with a descriptive commit message:
   ```bash
   git commit -m "Add feature-name"
   ```
4. **Push your branch** to your forked repository:
   ```bash
   git push origin feature-name
   ```
5. **Create a pull request** against the main repository's `master` branch.

We look forward to your contributions!

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Pillow](https://python-pillow.org/) for image processing.
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI.
- [PyInstaller](https://www.pyinstaller.org/) for creating the executable.
