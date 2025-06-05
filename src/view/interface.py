import os
import sys
import tkinter as tk
from tkinter import filedialog
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../controller/')))
from controller import main


file_path = ""

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select a BMP File", filetypes=[("BMP files", "*.bmp")])
    print(file_path)

def compress():
    F = F_var.get()
    d = d_var.get()
    if file_path != "" and d < 2*F - 1:
        error_label.config(text="")
        main(file_path, F, d)
    else:
        error_msg = ""
        if file_path == "":
            error_msg = "Error: the specified file does not exist.\n"
        if d >= 2*F - 1:
            error_msg = error_msg + "Error: d must be less than 2*F - 1.\n"
        error_label.config(text=error_msg)
     
r = tk.Tk()
r.geometry("400x400")
r.title('.BMP pic Compressor')
F_var = tk.IntVar()
F_var.set(8)
d_var = tk.IntVar()
d_var.set(10)

F_label = tk.Label(r, text = 'F:', font=('calibre',10, 'bold'))
F_label.pack()

F_entry = tk.Entry(r, textvariable = F_var, font=('calibre',10,'normal'))
F_entry.pack()

d_label = tk.Label(r, text = 'd:', font=('calibre',10, 'bold'))
d_label.pack()
d_entry = tk.Entry(r, textvariable = d_var, font=('calibre',10,'normal'))
d_entry.pack()

open_button = tk.Button(r, text="Open File", command=open_file)
open_button.pack(pady=10)

button = tk.Button(r, text='Compress', width=25, command = compress)
button.pack()

error_label = tk.Label(r, text="", fg="red")
error_label.pack()

r.mainloop()