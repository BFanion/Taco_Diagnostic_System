# Taco Diagnostic System Menu Based Selection
# Brian Fanion
# Taco Comfort Solutions
# July 13, 2026

import tkinter as tk
from tkinter import filedialog
import subprocess
import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "menu_config.json")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"scripts": []}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def launch_script(script_path):
    subprocess.Popen([sys.executable, script_path])


def show_readme():
    readme_path = os.path.join(SCRIPT_DIR, "README.md")
    win = tk.Toplevel()
    win.title("README")
    win.geometry("600x500")
    text = tk.Text(win, wrap="word", font=("Consolas", 10))
    text.pack(fill="both", expand=True, padx=10, pady=10)
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            text.insert("1.0", f.read())
    else:
        text.insert("1.0", "README.md not found.")
    text.config(state="disabled")


def main():
    config = load_config()
    root = tk.Tk()
    root.title("Taco Diagnostic System")
    root.geometry("500x600")

    tk.Label(root, text="Taco Diagnostic System", font=("Arial", 16, "bold")).pack(pady=20)

    # Bottom button bar (packed first to guarantee visibility)
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side="bottom", fill="x", pady=15, padx=20)
    verbose_var = tk.BooleanVar()
    tk.Checkbutton(bottom_frame, text="Verbose Mode", variable=verbose_var,
                   font=("Arial", 10), command=lambda: refresh_buttons()).pack(anchor="w")
    tk.Button(bottom_frame, text="Set-up", width=12, height=1, font=("Arial", 9), command=lambda: add_scripts()).pack(anchor="w", pady=3)
    tk.Button(bottom_frame, text="Help", width=12, height=1, font=("Arial", 9), command=lambda: show_readme()).pack(anchor="w", pady=3)
    tk.Button(bottom_frame, text="Exit", width=12, height=1, font=("Arial", 9), command=root.destroy).pack(anchor="w", pady=3)

    # Scrollable frame for script buttons
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    button_frame = tk.Frame(canvas)

    button_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=button_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True, padx=20)

    def refresh_buttons():
        for widget in button_frame.winfo_children():
            widget.destroy()

        # Auto-detected scripts in same directory
        this_file = os.path.basename(__file__)
        local_scripts = sorted(
            f for f in os.listdir(SCRIPT_DIR)
            if f.endswith(".py") and f != this_file
        )

        if local_scripts:
            tk.Label(button_frame, text="Local Scripts", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
            for script in local_scripts:
                script_path = os.path.join(SCRIPT_DIR, script)
                display_name = script.replace("_", " ").replace(".py", "")
                tk.Button(
                    button_frame, text=display_name, width=50, height=2,
                    command=lambda p=script_path: launch_script(p)
                ).pack(pady=3)

        # Manually added scripts from config
        if config["scripts"]:
            tk.Label(button_frame, text="Available Tools", font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 5))
            for script_path in config["scripts"]:
                display_name = os.path.basename(script_path).replace("_", " ").replace(".py", "")
                btn_frame = tk.Frame(button_frame)
                btn_frame.pack(pady=3, fill="x")
                tk.Button(
                    btn_frame, text=display_name, width=45, height=2,
                    command=lambda p=script_path: launch_script(p)
                ).pack(side="left")
                if verbose_var.get():
                    tk.Label(btn_frame, text=script_path, font=("Arial", 8)).pack(side="left", padx=5)
                    tk.Button(
                        btn_frame, text="X", width=3, height=2, fg="red",
                        command=lambda p=script_path: remove_script(p)
                    ).pack(side="left", padx=2)

    def add_scripts():
        files = filedialog.askopenfilenames(
            title="Select Python Scripts",
            filetypes=[("Python Files", "*.py")],
            initialdir=os.path.expanduser("~")
        )
        if files:
            for f in files:
                if f not in config["scripts"]:
                    config["scripts"].append(f)
            save_config(config)
            refresh_buttons()

    def remove_script(script_path):
        config["scripts"].remove(script_path)
        save_config(config)
        refresh_buttons()

    refresh_buttons()

    root.mainloop()


if __name__ == "__main__":
    main()
