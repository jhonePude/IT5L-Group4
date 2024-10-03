import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Loadingsplash:
    def setup(self, gif_path):
        # Create Tkinter window
        self.root = tk.Tk()
        self.root.title("GIF and Progress Bar Example")

        # Set window transparency color (choose a color that will be transparent)
        self.transparent_color = 'grey'  # Use a color that won't be in the GIF
        self.root.attributes('-transparentcolor', self.transparent_color)  
        self.root.overrideredirect(True)

        # Load the GIF file
        self.gif = Image.open(gif_path)

        # Get GIF frame count
        self.frames = []
        self.frame_count = 0
        self.resize_factor = 0.5  # Set this to change the size (0.5 means half the original size)

        try:
            while True:
                # Resize each frame
                resized_frame = self.gif.copy().resize(
                    (int(self.gif.width * self.resize_factor), int(self.gif.height * self.resize_factor)),
                    Image.LANCZOS  # Use LANCZOS for high-quality downsampling
                )
                self.frames.append(ImageTk.PhotoImage(resized_frame))
                self.gif.seek(len(self.frames))  # Move to the next frame
                self.frame_count += 1
        except EOFError:
            pass  # End of GIF, stop loading frames

        if not self.frames:
            raise ValueError("No frames could be loaded from the GIF!")

        # Create a Label to display GIF
        self.label = tk.Label(self.root, bg=self.transparent_color)  # Set the background to the transparent color
        self.label.pack(pady=(0, 50))  # Add padding to create space around the label

        # Create a label to display progress percentage
        self.progress_label = tk.Label(self.root, text="0%", bg=self.transparent_color, font=("Helvetica", 16))
        self.progress_label.place(x=200, y=460)  # Position the label (adjust as needed)

        # Set a more flexible style
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.style.configure("TProgressbar", thickness=58, troughcolor='lightgrey', foreground='blue', background='green')
        
        # Create a Progressbar widget
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=426, mode="determinate", style="TProgressbar")
        self.progress_bar.pack()
        self.progress_bar.place(x=2, y=438)
        self.progress_bar['value'] = 0  # Start with 0% progress

        # Center the window on the screen
        self.root.geometry(f"{430}x{500}+{500}+{100}")

        # Start the GIF animation and progress bar updates separately
        self.root.after(0, self.update_frame, 0)
        self.root.after(0, self.update_progress)

        # Start the fade-in effect from below
        self.root.attributes('-alpha', 0)  # Start fully transparent
        self.root.geometry(f"{430}x{500}+{500}+{600}")  # Start below the screen
        self.fade_in()

        # Start Tkinter main loop
        self.root.mainloop()

    # Function to update frames
    def update_frame(self, ind):
        frame = self.frames[ind]
        ind += 1
        if ind == self.frame_count:  # Loop back to the first frame
            ind = 0
        self.label.config(image=frame)
        self.root.after(100, self.update_frame, ind)

    # Function to update progress bar independently
    def update_progress(self):
        progress = self.progress_bar['value'] + 1  # Increment progress by 1
        if progress <= 100:
            self.progress_bar['value'] = progress
            self.progress_label.config(text=f"{progress}%")  # Update the label with the current progress
            self.root.after(40, self.update_progress)  # Update every 40 ms
        else:
            self.fade_out()  # Start fade-out when progress completes

    # Function for fade-in effect from below
    def fade_in(self):
        for i in range(0, 101, 2):  # Increase alpha from 0 to 100
            # Move the window up while fading in
            self.root.attributes('-alpha', i / 100)  # Set window transparency
            self.root.geometry(f"{430}x{500}+{500}+{600 - (i * 5)}")  # Adjust Y position
            self.root.update()
            self.root.after(10)  # Adjust speed of fade-in

    # Function for fade-out effect
    def fade_out(self):
        for i in range(100, -1, -2):  # Decrease alpha from 100 to 0
            self.root.attributes('-alpha', i / 100)  # Set window transparency
            self.root.update()
            self.root.after(10)  # Adjust speed of fade-out
        self.root.quit()  # Exit the application after fade-out


# Usage
loading_splash = Loadingsplash()
gif_path = "catdance.gif"  # Replace with your GIF file path
loading_splash.setup(gif_path)
