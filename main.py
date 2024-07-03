import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
import os
import traceback

class ImageCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor")

        # Set up the interface
        self.label = tk.Label(root, text="Compress Image", font=("Arial", 20))
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.drag_drop_label = tk.Label(root, text="Or drag and drop an image here", font=("Arial", 12))
        self.drag_drop_label.pack(pady=5)

        self.canvas = tk.Canvas(root, width=600, height=200)
        self.canvas.pack(pady=10)

        self.compression_level_label = tk.Label(root, text="Compression Level", font=("Arial", 12))
        self.compression_level_label.pack(pady=5)

        self.compression_slider = tk.Scale(root, from_=10, to=90, orient=tk.HORIZONTAL)
        self.compression_slider.set(50)
        self.compression_slider.pack(pady=5)

        self.download_button = tk.Button(root, text="Download Compressed Images", command=self.download_images)
        self.download_button.pack(pady=20)

        self.image_paths = []
        self.images = []

    def upload_image(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_paths:
            self.image_paths = file_paths
            self.display_images()

    def display_images(self):
        self.canvas.delete("all")
        self.images = []

        for idx, image_path in enumerate(self.image_paths):
            try:
                img = Image.open(image_path)
                img.thumbnail((200, 200))
                img = ImageTk.PhotoImage(img)
                self.images.append(img)
                self.canvas.create_image(200 * idx + 100, 100, image=img)
            except Exception as e:
                print(f"Failed to load image {image_path}: {e}")

    def compress_image(self, image_path, compression_level):
        try:
            img = Image.open(image_path)

            # Apply orientation correction if EXIF data is available
            try:
                exif = img._getexif()
                if exif is not None:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    orientation = exif.get(orientation, None)
                    if orientation is not None:
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                print(f"EXIF data issue with {image_path}")

            # Convert 'RGBA' to 'RGB' if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Create compressed directory if it doesn't exist
            directory = os.path.dirname(image_path)
            compressed_dir = os.path.join(directory, 'compressed')
            if not os.path.exists(compressed_dir):
                os.makedirs(compressed_dir)

            compressed_path = os.path.join(compressed_dir, os.path.splitext(os.path.basename(image_path))[0] + "_compressed.jpg")
            img.save(compressed_path, quality=compression_level)
            return compressed_path

        except (OSError, IOError) as e:
            print(f"Failed to compress {image_path}: Unsupported format or corrupted file.")
            messagebox.showerror("Error", f"Failed to compress {image_path}: Unsupported format or corrupted file.")
        except MemoryError as e:
            print(f"Failed to compress {image_path}: Size or memory issue.")
            messagebox.showerror("Error", f"Failed to compress {image_path}: Size or memory issue.")
        except Exception as e:
            print(f"Failed to compress {image_path}: {e}")
            messagebox.showerror("Error", f"Failed to compress {image_path}: {e}")
            print(traceback.format_exc())
        return None

    def download_images(self):
        compression_level = self.compression_slider.get()
        compressed_paths = []
        failed_images = []

        for image_path in self.image_paths:
            compressed_path = self.compress_image(image_path, compression_level)
            if compressed_path:
                compressed_paths.append(compressed_path)
            else:
                failed_images.append(image_path)

        if failed_images:
            messagebox.showerror("Error", f"Failed to compress {len(failed_images)} images.")
            print("Failed images:")
            for img in failed_images:
                print(img)
        
        messagebox.showinfo("Compression Complete", f"Successfully compressed {len(compressed_paths)} images.")
        print("Successfully compressed images:")
        for compressed_path in compressed_paths:
            print(f"Compressed image saved to: {compressed_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressor(root)
    root.mainloop()
