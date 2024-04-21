import tkinter as tk
import json

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Drawing App")

        self.canvas = tk.Canvas(root, bg="white", width=1200, height=900)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.coordinates = {"strokes": {"x": [], "y": []}}
        self.current_stroke = {"x": [], "y": []}

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.finish_stroke)

    def paint(self, event):
        x, y = event.x, event.y

        self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black", width=2)
        self.current_stroke["x"].append(x)
        self.current_stroke["y"].append(y)

    def finish_stroke(self, event):
        self.coordinates["strokes"]["x"].append(self.current_stroke["x"].copy())
        self.coordinates["strokes"]["y"].append(self.current_stroke["y"].copy())
        self.current_stroke["x"].clear()
        self.current_stroke["y"].clear()

    def save_to_json(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.coordinates, json_file, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    
    def save_and_exit():
        app.save_to_json("coordinates.json")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save_and_exit)
    root.mainloop()
