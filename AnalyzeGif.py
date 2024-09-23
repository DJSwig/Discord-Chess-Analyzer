import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence, ImageChops

class GIFAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Chess GIF Analyzer")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="gray")
        self.canvas.pack(pady=10)

        self.listbox = tk.Listbox(self.root, height=10)
        self.listbox.pack(fill=tk.X, padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_move_select)

        self.load_button = tk.Button(self.root, text="Load GIF", command=self.load_gif)
        self.load_button.pack(pady=10)

        self.frames = []
        self.current_frame = None
        self.moves = []
        self.current_image_on_canvas = None

    def load_gif(self):
        gif_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
        if not gif_path:
            return

        gif = Image.open(gif_path)
        self.frames = [frame.convert("RGB") for frame in ImageSequence.Iterator(gif)]
        first_frame_size = self.frames[0].size
        self.frames = [frame.resize(first_frame_size) for frame in self.frames]

        self.detect_moves()

        self.listbox.delete(0, tk.END)
        for idx, move in enumerate(self.moves):
            self.listbox.insert(tk.END, f"Move {idx + 1}: {move}")

        self.display_frame_at_index(0)

    def detect_moves(self):
        self.moves.clear()
        for idx in range(1, len(self.frames)):
            prev_frame = self.frames[idx - 1]
            curr_frame = self.frames[idx]
            diff = ImageChops.difference(prev_frame, curr_frame)

            if diff.getbbox():
                move = self.analyze_diff(diff)
                if move:
                    self.moves.append(move)

    def analyze_diff(self, diff_frame):
        return "E2 to E4"

    def on_move_select(self, event):
        selected_idx = self.listbox.curselection()
        if selected_idx:
            self.display_frame_at_index(selected_idx[0])

    def display_frame_at_index(self, idx):
        frame = self.frames[idx]
        self.render_frame_on_canvas(frame)

    def render_frame_on_canvas(self, frame):
        canvas_width, canvas_height = 600, 400
        frame_resized = self.resize_frame_to_canvas(frame, canvas_width, canvas_height)

        self.current_frame = ImageTk.PhotoImage(frame_resized)
        self.canvas.delete(self.current_image_on_canvas)
        self.current_image_on_canvas = self.canvas.create_image(
            canvas_width // 2, canvas_height // 2, image=self.current_frame, anchor=tk.CENTER
        )

    def resize_frame_to_canvas(self, frame, canvas_width, canvas_height):
        frame_width, frame_height = frame.size
        aspect_ratio = frame_width / frame_height

        if frame_width > canvas_width or frame_height > canvas_height:
            if frame_width > frame_height:
                new_width = canvas_width
                new_height = int(canvas_width / aspect_ratio)
            else:
                new_height = canvas_height
                new_width = int(canvas_height * aspect_ratio)
        else:
            new_width, new_height = frame_width, frame_height

        return frame.resize((new_width, new_height), Image.LANCZOS)


if __name__ == "__main__":
    root = tk.Tk()
    app = GIFAnalyzer(root)
    root.mainloop()
