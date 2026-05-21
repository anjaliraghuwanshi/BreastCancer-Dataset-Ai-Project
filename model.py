import os
import json
import numpy as np
import tkinter as tk
import joblib
import time
from threading import Thread
from tkinter import messagebox

from report import save_pdf_report
from history import save_history

# ================= LOAD MODEL =================
try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")

except Exception as e:
    messagebox.showerror(
        "MODEL ERROR",
        f"Model loading failed:\n{e}"
    )
    exit()

# ================= WINDOW =================
root = tk.Tk()

root.title("🏥 AI Hospital System - Breast Cancer Detection")
root.geometry("1200x700")
root.config(bg="#0b1220")

# ================= HEADER =================
header = tk.Frame(
    root,
    bg="#111827",
    height=70
)

header.pack(fill="x")

tk.Label(
    header,
    text="🏥 BREAST CANCER AI DIAGNOSTIC SYSTEM",
    bg="#111827",
    fg="#38bdf8",
    font=("Arial", 18, "bold")
).pack(pady=18)

# ================= MAIN WRAPPER =================
wrapper = tk.Frame(
    root,
    bg="#0b1220"
)

wrapper.pack(fill="both", expand=True)

# ================= SIDEBAR =================
sidebar = tk.Frame(
    wrapper,
    bg="#0f172a",
    width=260
)

sidebar.pack(side="left", fill="y")

tk.Label(
    sidebar,
    text="DOCTOR PANEL",
    bg="#0f172a",
    fg="white",
    font=("Arial", 14, "bold")
).pack(pady=20)

tk.Label(
    sidebar,
    text="AI MEDICAL SYSTEM",
    bg="#0f172a",
    fg="gray",
    font=("Arial", 10)
).pack()

# ================= RIGHT AREA =================
right = tk.Frame(
    wrapper,
    bg="#0b1220"
)

right.pack(side="left", fill="both", expand=True)

# ================= FRAMES =================
dashboard_frame = tk.Frame(right, bg="#0b1220")
report_frame = tk.Frame(right, bg="#0b1220")
history_frame = tk.Frame(right, bg="#0b1220")
settings_frame = tk.Frame(right, bg="#0b1220")

# ================= SHOW FUNCTION =================
def show(frame):

    for f in [
        dashboard_frame,
        report_frame,
        history_frame,
        settings_frame
    ]:
        f.pack_forget()

    frame.pack(fill="both", expand=True)

# =========================================================
# ================= DASHBOARD =============================
# =========================================================

# ================= INPUT CARD =================
card = tk.Frame(
    dashboard_frame,
    bg="#111827",
    bd=2,
    relief="ridge"
)

card.pack(pady=25)

tk.Label(
    card,
    text="PATIENT MEDICAL INPUT (8 FEATURES)",
    bg="#111827",
    fg="white",
    font=("Arial", 14, "bold")
).grid(
    row=0,
    column=0,
    columnspan=2,
    pady=15
)

entries = []

for i in range(8):

    tk.Label(
        card,
        text=f"Feature {i+1}",
        bg="#111827",
        fg="#d1d5db",
        font=("Arial", 11)
    ).grid(
        row=i+1,
        column=0,
        padx=20,
        pady=8,
        sticky="w"
    )

    e = tk.Entry(
        card,
        width=30,
        font=("Arial", 11),
        bg="#1f2937",
        fg="white",
        insertbackground="white"
    )

    e.grid(
        row=i+1,
        column=1,
        padx=20,
        pady=8
    )

    entries.append(e)

# ================= RESULT =================
result = tk.Label(
    dashboard_frame,
    text="SYSTEM READY",
    fg="white",
    bg="#0b1220",
    font=("Arial", 16, "bold")
)

result.pack(pady=10)

loading = tk.Label(
    dashboard_frame,
    text="",
    fg="#facc15",
    bg="#0b1220",
    font=("Arial", 11)
)

loading.pack()

# ================= SAFE INPUT =================
def get_inputs():

    values = []

    for e in entries:

        val = str(e.get()).strip()

        if val == "":
            raise ValueError("Empty input field")

        val = val.replace(",", ".")

        try:
            num = float(val)
            values.append(num)

        except:
            raise ValueError(f"Invalid input: {val}")

    if len(values) != 8:
        raise ValueError("Exactly 8 values required")

    return np.array(values).reshape(1, -1)

# ================= PREDICTION =================
def predict_thread():

    try:

        loading.config(
            text="🔄 Analyzing Patient Data..."
        )

        result.config(
            text="PROCESSING...",
            fg="yellow"
        )

        time.sleep(1)

        values = get_inputs()

        scaled = scaler.transform(values)

        pred = model.predict(scaled)

        if int(pred[0]) == 0:

            text = "MALIGNANT (CANCER DETECTED)"
            color = "red"

        else:

            text = "BENIGN (NO CANCER)"
            color = "#22c55e"

        result.config(
            text=text,
            fg=color
        )

        # ================= FINAL FIX =================
        safe_values = values.flatten().tolist()

        save_pdf_report(
            safe_values,
            str(text)
        )

        save_history(
            [safe_values],
            str(text)
        )

    except Exception as e:

        result.config(
            text=f"⚠ ERROR: {str(e)}",
            fg="orange"
        )

    loading.config(text="")

def predict():

    Thread(
        target=predict_thread
    ).start()

# ================= SAMPLE DATA =================
def fill_benign():

    data = [
        12,15,78,450,
        0.09,0.06,0.04,0.02
    ]

    for i in range(8):

        entries[i].delete(0, tk.END)

        entries[i].insert(
            0,
            str(data[i])
        )

def fill_malignant():

    data = [
        20,30,130,1200,
        0.15,0.25,0.30,0.15
    ]

    for i in range(8):

        entries[i].delete(0, tk.END)

        entries[i].insert(
            0,
            str(data[i])
        )

# ================= BUTTONS =================
btn = tk.Frame(
    dashboard_frame,
    bg="#0b1220"
)

btn.pack(pady=20)

tk.Button(
    btn,
    text="🔍 PREDICT",
    command=predict,
    bg="#22c55e",
    fg="white",
    width=18,
    height=2,
    bd=0,
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=10
)

tk.Button(
    btn,
    text="🟢 BENIGN",
    command=fill_benign,
    bg="#3b82f6",
    fg="white",
    width=18,
    height=2,
    bd=0,
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=1,
    padx=10
)

tk.Button(
    btn,
    text="🔴 MALIGNANT",
    command=fill_malignant,
    bg="#ef4444",
    fg="white",
    width=18,
    height=2,
    bd=0,
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=2,
    padx=10
)

# =========================================================
# ================= REPORT PAGE ===========================
# =========================================================

def load_reports():

    for w in report_frame.winfo_children():
        w.destroy()

    tk.Label(
        report_frame,
        text="📄 GENERATED REPORTS",
        bg="#0b1220",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    listbox = tk.Listbox(
        report_frame,
        width=70,
        height=20,
        bg="#111827",
        fg="white",
        font=("Arial", 10)
    )

    listbox.pack(pady=10)

    found = False

    for file in os.listdir():

        if file.endswith(".pdf"):

            listbox.insert(
                tk.END,
                file
            )

            found = True

    if not found:

        listbox.insert(
            tk.END,
            "No reports available"
        )

    def open_report():

        try:

            selected = listbox.get(tk.ACTIVE)

            os.startfile(selected)

        except:

            messagebox.showerror(
                "ERROR",
                "Cannot open report"
            )

    tk.Button(
        report_frame,
        text="OPEN REPORT",
        command=open_report,
        bg="#22c55e",
        fg="white",
        width=20,
        height=2,
        bd=0
    ).pack(pady=15)

# =========================================================
# ================= HISTORY PAGE ==========================
# =========================================================

def load_history():

    for w in history_frame.winfo_children():
        w.destroy()

    tk.Label(
        history_frame,
        text="📊 PATIENT HISTORY",
        bg="#0b1220",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    history_box = tk.Text(
        history_frame,
        width=95,
        height=28,
        bg="#111827",
        fg="white",
        font=("Arial", 10)
    )

    history_box.pack(pady=10)

    try:

        with open(
            "history.json",
            "r"
        ) as f:

            data = json.load(f)

            for item in data:

                history_box.insert(
                    tk.END,
                    f"\nTIME: {item['time']}\n"
                )

                history_box.insert(
                    tk.END,
                    f"VALUES: {item['values']}\n"
                )

                history_box.insert(
                    tk.END,
                    f"RESULT: {item['result']}\n"
                )

                history_box.insert(
                    tk.END,
                    "--------------------------------------\n"
                )

    except:

        history_box.insert(
            tk.END,
            "No history available"
        )

# =========================================================
# ================= SETTINGS PAGE =========================
# =========================================================

def load_settings():

    for w in settings_frame.winfo_children():
        w.destroy()

    tk.Label(
        settings_frame,
        text="⚙ SYSTEM SETTINGS",
        bg="#0b1220",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        settings_frame,
        text="AI MODEL : Breast Cancer Prediction",
        bg="#0b1220",
        fg="#d1d5db",
        font=("Arial", 12)
    ).pack(pady=10)

    tk.Label(
        settings_frame,
        text="MODEL STATUS : ACTIVE",
        bg="#0b1220",
        fg="#22c55e",
        font=("Arial", 12)
    ).pack(pady=10)

    tk.Label(
        settings_frame,
        text="DEVELOPER : AI Hospital System",
        bg="#0b1220",
        fg="#d1d5db",
        font=("Arial", 12)
    ).pack(pady=10)

# =========================================================
# ================= SIDEBAR MENU ==========================
# =========================================================

def menu(name, frame, loader=None):

    def open_page():

        if loader:
            loader()

        show(frame)

    tk.Button(
        sidebar,
        text=name,
        command=open_page,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        activeforeground="white",
        bd=0,
        width=25,
        pady=10,
        font=("Arial", 10, "bold")
    ).pack(pady=8)

menu(
    "🏠 Dashboard",
    dashboard_frame
)

menu(
    "📄 Reports",
    report_frame,
    load_reports
)

menu(
    "📊 History",
    history_frame,
    load_history
)

menu(
    "⚙ Settings",
    settings_frame,
    load_settings
)

# ================= DEFAULT PAGE =================
show(dashboard_frame)

# ================= START =================
root.mainloop()