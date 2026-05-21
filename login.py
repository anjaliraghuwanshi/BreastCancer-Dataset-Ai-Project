import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("AI Hospital Login System")
root.geometry("520x620")
root.config(bg="#0b1220")
root.resizable(False, False)

# ================= CENTER CARD =================
card = tk.Frame(root, bg="#0f172a")
card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=540)

# ================= HEADER =================
tk.Label(
    card,
    text="🏥 AI HOSPITAL SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
).pack(pady=30)

tk.Label(
    card,
    text="Breast Cancer Diagnosis Login",
    bg="#0f172a",
    fg="gray",
    font=("Arial", 11)
).pack()

# ================= INPUT BOX =================
box = tk.Frame(card, bg="#111827")
box.pack(pady=40, padx=20, fill="both")

tk.Label(box, text="USERNAME", bg="#111827", fg="gray").pack(pady=(20,5))
username = tk.Entry(box, font=("Arial", 12), justify="center")
username.pack(ipady=8, padx=20)

tk.Label(box, text="PASSWORD", bg="#111827", fg="gray").pack(pady=(20,5))
password = tk.Entry(box, font=("Arial", 12), show="*", justify="center")
password.pack(ipady=8, padx=20)

# ================= LOGIN FUNCTION =================
def login():
    if username.get() == "doctor" and password.get() == "1234":
        root.destroy()
        subprocess.run([sys.executable, "model.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# ================= BUTTON =================
tk.Button(
    box,
    text="LOGIN TO DASHBOARD",
    command=login,
    bg="#22c55e",
    fg="white",
    font=("Arial", 12, "bold"),
    bd=0,
    pady=10
).pack(pady=40, ipadx=10)

root.mainloop()