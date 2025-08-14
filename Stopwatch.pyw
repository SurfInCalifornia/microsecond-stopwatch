import os
import sys
import tkinter as tk
from datetime import datetime, timedelta

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("380x140")

        icon_path = resource_path("logo.ico")
        try:
            self.root.iconbitmap(default=icon_path)
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")

        self.running = False
        self.start_time = None
        self.elapsed = timedelta(0)

        self.time_label = tk.Label(root, text="0:00:00.000000", font=("Courier", 24))
        self.time_label.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.start_btn = tk.Button(btn_frame, text="Start", width=10, command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="Stop", width=10, command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.restart_btn = tk.Button(btn_frame, text="Restart", width=10, command=self.restart, state=tk.DISABLED)
        self.restart_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reset", width=10, command=self.reset)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.update_buttons()

    def update(self):
        if self.running:
            now = datetime.now()
            diff = now - self.start_time + self.elapsed
        else:
            diff = self.elapsed

        total_seconds = diff.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        microseconds = diff.microseconds

        time_str = f"{hours}:{minutes:02d}:{seconds:02d}.{microseconds:06d}"
        self.time_label.config(text=time_str)

        if self.running:
            self.root.after(1, self.update)

        self.update_buttons()

    def update_buttons(self):
        self.start_btn.config(state=tk.DISABLED if self.running else tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL if self.running else tk.DISABLED)
        self.restart_btn.config(state=tk.NORMAL if self.running else tk.DISABLED)
        zero_time = (self.elapsed.total_seconds() == 0) and (not self.running)
        self.reset_btn.config(state=tk.DISABLED if zero_time else tk.NORMAL)

    def start(self):
        self.elapsed = timedelta(0)
        self.start_time = datetime.now()
        self.running = True
        self.update()
        self.update_buttons()

    def stop(self):
        if self.running:
            now = datetime.now()
            self.elapsed += now - self.start_time
            self.running = False
            self.update_buttons()

    def restart(self):
        if self.running:
            self.elapsed = timedelta(0)
            self.start_time = datetime.now()
            self.update_buttons()

    def reset(self):
        if self.running:
            now = datetime.now()
            self.elapsed += now - self.start_time
            self.running = False
        self.elapsed = timedelta(0)
        self.start_time = None
        self.update()
        self.update_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    app = Stopwatch(root)
    root.mainloop()
