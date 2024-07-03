import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ExifTags
import os
import traceback

class ImageSqueezer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Squeezer")

        # Set up the interface
        self.label = tk.Label(root, text="Compress Image", font=("Arial", 20))
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Select Images", command=self.select_images)
        self.upload_button.pack(pady=5)

        self.drag_drop_label = tk.Label(root, text="Or drag and drop an image here", font=("Arial", 12))
        self.drag_drop_label.pack(pady=5)

        # Create a frame for the canvas and scrollbar
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.canvas = tk.Canvas(self.frame, width=600, height=200)
        self.scrollbar = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left")

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.compression_level_label = tk.Label(root, text="Compression Level", font=("Arial", 12))
        self.compression_level_label.pack(pady=5)

        self.compression_slider = tk.Scale(root, from_=10, to=90, orient=tk.HORIZONTAL)
        self.compression_slider.set(50)
        self.compression_slider.pack(pady=5)

        self.download_button = tk.Button(root, text="Compress and Download Images", command=self.download_images)
        self.download_button.pack(pady=20)

        self.upload_progress_label = tk.Label(root, text="Upload Progress", font=("Arial", 12))
        self.upload_progress_label.pack(pady=5)

        self.upload_progress = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate', style="green.Horizontal.TProgressbar")
        self.upload_progress.pack(pady=5)

        self.compress_progress_label = tk.Label(root, text="Compression Progress", font=("Arial", 12))
        self.compress_progress_label.pack(pady=5)

        self.compress_progress = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate', style="blue.Horizontal.TProgressbar")
        self.compress_progress.pack(pady=5)

        self.status_label = tk.Label(root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.selected_images_label = tk.Label(root, text="Total images selected: 0", font=("Arial", 12))
        self.selected_images_label.pack(pady=5)

        self.uploaded_images_label = tk.Label(root, text="Total images uploaded: 0", font=("Arial", 12))
        self.uploaded_images_label.pack(pady=5)

        self.compressed_images_label = tk.Label(root, text="Total images compressed: 0", font=("Arial", 12))
        self.compressed_images_label.pack(pady=5)

        self.image_paths = []
        self.images = []

        # Configure the styles for the progress bars
        style = ttk.Style()
        style.configure("green.Horizontal.TProgressbar", troughcolor='white', background='green')
        style.configure("blue.Horizontal.TProgressbar", troughcolor='white', background='blue')

    def select_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_paths:
            self.image_paths = [path for path in file_paths if path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'))]
            print(f"Total images selected: {len(self.image_paths)}")
            self.selected_images_label.config(text=f"Total images selected: {len(self.image_paths)}")
            self.upload_progress['maximum'] = len(self.image_paths)
            self.display_images()

    def display_images(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.images = []
        failed_images = []

        for idx, image_path in enumerate(self.image_paths):
            try:
                print(f"Loading image: {image_path}")
                img = Image.open(image_path)
                img.thumbnail((200, 200))
                img = ImageTk.PhotoImage(img)
                self.images.append(img)
                label = tk.Label(self.scrollable_frame, image=img)
                label.grid(row=0, column=idx)
                self.upload_progress['value'] = idx + 1
                self.uploaded_images_label.config(text=f"Total images uploaded: {len(self.images)}")
                self.root.update_idletasks()
            except Exception as e:
                print(f"Failed to load image {image_path}: {e}")
                traceback.print_exc()
                failed_images.append(image_path)

        if failed_images:
            messagebox.showerror("Error", f"Failed to load {len(failed_images)} images.")
            print("Failed images:")
            for img in failed_images:
                print(img)

    def compress_image(self, image_path, compression_level):
        try:
            print(f"Attempting to open image: {image_path}")
            if not os.path.exists(image_path):
                print(f"File does not exist: {image_path}")
                return None

            img = Image.open(image_path)
            print(f"Opened image: {image_path}")

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
                    print(f"Applied EXIF orientation for image: {image_path}")
            except (AttributeError, KeyError, IndexError) as exif_error:
                print(f"EXIF data issue with {image_path}: {exif_error}")

            # Convert 'RGBA' to 'RGB' if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                print(f"Converted RGBA to RGB for image: {image_path}")

            # Create compressed directory if it doesn't exist
            directory = os.path.dirname(image_path)
            compressed_dir = os.path.join(directory, 'compressed')
            if not os.path.exists(compressed_dir):
                os.makedirs(compressed_dir)
                print(f"Created directory: {compressed_dir}")

            compressed_path = os.path.join(compressed_dir, os.path.splitext(os.path.basename(image_path))[0] + "_compressed.jpg")
            img.save(compressed_path, quality=compression_level)
            print(f"Compressed image saved to: {compressed_path}")
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
            traceback.print_exc()
        return None

    def download_images(self):
        compression_level = self.compression_slider.get()
        compressed_paths = []
        failed_images = []
        skipped_images = []

        self.compress_progress['maximum'] = len(self.image_paths)
        print(f"Starting compression for {len(self.image_paths)} images.")

        for idx, image_path in enumerate(self.image_paths):
            print(f"Processing image: {image_path}")
            compressed_path = self.compress_image(image_path, compression_level)
            if compressed_path:
                compressed_paths.append(compressed_path)
            else:
                skipped_images.append(image_path)
            self.compress_progress['value'] = idx + 1
            self.compressed_images_label.config(text=f"Total images compressed: {len(compressed_paths)}")
            self.root.update_idletasks()

        if skipped_images:
            messagebox.showerror("Error", f"Skipped {len(skipped_images)} images.")
            print("Skipped images:")
            for img in skipped_images:
                print(img)

        messagebox.showinfo("Compression Complete", f"Successfully compressed {len(compressed_paths)} images.")
        print("Successfully compressed images:")
        for compressed_path in compressed_paths:
            print(f"Compressed image saved to: {compressed_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSqueezer(root)
    root.mainloop()
