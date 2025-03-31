import tkinter as tk
from tkinter import messagebox
import subprocess
import cv2
import sys
import sys
print("Using Python:", sys.executable)

def run_add_member():
    root.destroy()
    subprocess.run([sys.executable, "gui.py"])


def mark_attendance():
    root.destroy()
    subprocess.run([sys.executable, "main.py"])


# Create main window
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Title label
title_label = tk.Label(root, text="Welcome", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

# Buttons
btn_add = tk.Button(root, text="Add New Member", command=run_add_member, font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5)
btn_add.pack(pady=20)

btn_attend = tk.Button(root, text="Mark Attendance", font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=10, command=mark_attendance)
btn_attend.pack(pady=10)

# Run the UI
root.mainloop()
