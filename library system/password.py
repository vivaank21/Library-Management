import tkinter as tk
from tkinter import messagebox
import bcrypt

# ---------- FUNCTIONS ----------

def generate_hash():
    password = entry_password.get()

    if password == "":
        messagebox.showwarning("Warning", "Enter password first")
        return

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_str = hashed.decode()

    text_hash.delete("1.0", tk.END)
    text_hash.insert(tk.END, hashed_str)


def copy_hash():
    hash_value = text_hash.get("1.0", tk.END).strip()

    if hash_value == "":
        messagebox.showwarning("Warning", "No hash to copy")
        return

    root.clipboard_clear()
    root.clipboard_append(hash_value)

    messagebox.showinfo("Copied", "Hash copied to clipboard")


def verify_password():
    password = entry_verify_password.get()
    hash_value = entry_verify_hash.get()

    if password == "" or hash_value == "":
        messagebox.showwarning("Warning", "Enter password and hash")
        return

    try:
        if bcrypt.checkpw(password.encode(), hash_value.encode()):
            label_result.config(text="✔ Password MATCHES hash", fg="#00ff9c")
        else:
            label_result.config(text="✖ Password DOES NOT match", fg="#ff4d4d")

    except:
        messagebox.showerror("Error", "Invalid hash format")


# ---------- DARK THEME COLORS ----------

bg = "#1e1e1e"
fg = "#ffffff"
entry_bg = "#2d2d2d"
btn_green = "#00c853"
btn_blue = "#2962ff"
btn_purple = "#aa00ff"

# ---------- WINDOW ----------

root = tk.Tk()
root.title("Password Hash Generator - Dark Theme")
root.geometry("600x500")
root.configure(bg=bg)
root.resizable(False, False)

# ---------- TITLE ----------

title = tk.Label(root, text="Password Hash Generator", font=("Arial", 18, "bold"), bg=bg, fg=fg)
title.pack(pady=10)

# ---------- GENERATE HASH ----------

tk.Label(root, text="Enter Password:", bg=bg, fg=fg).pack()

entry_password = tk.Entry(root, width=40, bg=entry_bg, fg=fg, insertbackground=fg)
entry_password.pack(pady=5)

btn_generate = tk.Button(root, text="Generate Hash", command=generate_hash, bg=btn_green, fg="white", width=20)
btn_generate.pack(pady=5)

text_hash = tk.Text(root, height=3, width=60, bg=entry_bg, fg=fg, insertbackground=fg)
text_hash.pack(pady=5)

btn_copy = tk.Button(root, text="Copy Hash", command=copy_hash, bg=btn_blue, fg="white", width=20)
btn_copy.pack(pady=5)

# ---------- VERIFY SECTION ----------

tk.Label(root, text="Verify Password", font=("Arial", 14, "bold"), bg=bg, fg=fg).pack(pady=10)

tk.Label(root, text="Enter Password:", bg=bg, fg=fg).pack()
entry_verify_password = tk.Entry(root, width=40, bg=entry_bg, fg=fg, insertbackground=fg)
entry_verify_password.pack(pady=5)

tk.Label(root, text="Enter Hash:", bg=bg, fg=fg).pack()
entry_verify_hash = tk.Entry(root, width=60, bg=entry_bg, fg=fg, insertbackground=fg)
entry_verify_hash.pack(pady=5)

btn_verify = tk.Button(root, text="Verify Password", command=verify_password, bg=btn_purple, fg="white", width=20)
btn_verify.pack(pady=10)

label_result = tk.Label(root, text="", bg=bg, fg=fg, font=("Arial", 12, "bold"))
label_result.pack()

# ---------- RUN ----------

root.mainloop()
