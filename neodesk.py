import tkinter as tk
import time
import platform
import os

APP_BG = "#0b0f14"
ACCENT = "#00ff66"
TEXT = "white"

# ---------------- MAIN APP ----------------
root = tk.Tk()
root.title("NeoDesk")
root.geometry("800x500")
root.config(bg=APP_BG)

# ---------------- SIDEBAR ----------------
sidebar = tk.Frame(root, width=180, bg="black")
sidebar.pack(side="left", fill="y")

content = tk.Frame(root, bg=APP_BG)
content.pack(side="right", fill="both", expand=True)

# ---------------- CLEAR CONTENT ----------------
def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

# ---------------- CLOCK ----------------
def open_clock():
    clear_content()

    label = tk.Label(
        content,
        font=("Consolas", 40),
        fg=ACCENT,
        bg=APP_BG
    )
    label.pack(expand=True)

    def update():
        label.config(text=time.strftime("%H:%M:%S"))
        label.after(1000, update)

    update()

# ---------------- CALCULATOR (FIXED) ----------------
def open_calculator():
    clear_content()

    entry = tk.Entry(content, font=("Arial", 20), justify="right")
    entry.pack(fill="x", padx=10, pady=10)

    def press(val):
        entry.insert("end", val)

    def calc():
        try:
            expression = entry.get()              # FIX: get first
            result = eval(expression)             # evaluate
            entry.delete(0, "end")                # then clear
            entry.insert("end", result)           # show result
        except:
            entry.delete(0, "end")
            entry.insert("end", "Error")

    def clear():
        entry.delete(0, "end")

    buttons = [
        "7","8","9","/",
        "4","5","6","*",
        "1","2","3","-",
        "0",".","=","+"
    ]

    grid = tk.Frame(content, bg=APP_BG)
    grid.pack()

    for i, btn in enumerate(buttons):
        if btn == "=":
            cmd = calc
        else:
            cmd = lambda x=btn: press(x)

        tk.Button(
            grid,
            text=btn,
            width=5,
            height=2,
            command=cmd,
            bg="black",
            fg=ACCENT
        ).grid(row=i//4, column=i%4, padx=5, pady=5)

    tk.Button(
        content,
        text="Clear",
        command=clear,
        bg="red",
        fg="white"
    ).pack(pady=5)

# ---------------- NOTES ----------------
def open_notes():
    clear_content()

    os.makedirs("data", exist_ok=True)
    file_path = "data/notes.txt"

    text = tk.Text(content, font=("Arial", 12))
    text.pack(fill="both", expand=True)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            text.insert("1.0", f.read())

    def save():
        with open(file_path, "w") as f:
            f.write(text.get("1.0", "end"))

    tk.Button(
        content,
        text="Save Notes",
        command=save,
        bg=ACCENT,
        fg="black"
    ).pack(pady=5)

# ---------------- SYSTEM INFO ----------------
def open_system():
    clear_content()

    info = f"""
System: {platform.system()}
Node: {platform.node()}
Release: {platform.release()}
Version: {platform.version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
"""

    tk.Label(
        content,
        text=info,
        justify="left",
        fg=TEXT,
        bg=APP_BG,
        font=("Consolas", 12)
    ).pack(padx=10, pady=10, anchor="w")

# ---------------- SIDEBAR BUTTONS ----------------
def side_button(text, cmd):
    return tk.Button(
        sidebar,
        text=text,
        command=cmd,
        width=18,
        pady=10,
        bg="black",
        fg=ACCENT,
        font=("Arial", 10, "bold")
    )

tk.Label(
    sidebar,
    text="NeoDesk",
    fg=ACCENT,
    bg="black",
    font=("Arial", 18, "bold")
).pack(pady=15)

side_button("Clock", open_clock).pack(pady=5)
side_button("Calculator", open_calculator).pack(pady=5)
side_button("Notes", open_notes).pack(pady=5)
side_button("System Info", open_system).pack(pady=5)

open_clock()
root.mainloop()
