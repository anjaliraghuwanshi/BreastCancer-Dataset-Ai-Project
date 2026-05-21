import numpy as np
import tkinter as tk
from tkinter import ttk
import joblib

# ================= LOAD MODEL =================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("🏥 AI Breast Cancer Hospital System")
root.geometry("1000x600")
root.config(bg="#f2f6ff")

# ================= HEADER =================
header = tk.Label(
    root,
    text="BREAST CANCER AI DIAGNOSIS SYSTEM",
    bg="#1f3b57",
    fg="white",
    font=("Arial", 18, "bold"),
    pady=15
)
header.pack(fill="x")

# ================= MAIN FRAME =================
main_frame = tk.Frame(root, bg="#f2f6ff")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# ================= LEFT PANEL =================
left = tk.Frame(main_frame, bg="#f2f6ff")
left.pack(side="left", fill="both", expand=True)

# ================= RIGHT PANEL =================
right = tk.Frame(main_frame, bg="#f2f6ff", width=300)
right.pack(side="right", fill="y")

# ================= TITLE =================
tk.Label(
    left,
    text="Enter Patient Medical Data (8 Features)",
    bg="#f2f6ff",
    font=("Arial", 14, "bold")
).grid(row=0, column=0, columnspan=2, pady=10)

# ================= INPUT FIELDS (8 FEATURES ONLY) =================
entries = []

for i in range(8):

    tk.Label(
        left,
        text=f"Feature {i+1}",
        bg="#f2f6ff",
        font=("Arial", 11)
    ).grid(row=i+1, column=0, padx=10, pady=8, sticky="w")

    e = tk.Entry(left, width=25, font=("Arial", 11))
    e.grid(row=i+1, column=1, padx=10, pady=8)

    entries.append(e)

# ================= RESULT LABEL =================
result_label = tk.Label(
    right,
    text="RESULT\nWAITING...",
    font=("Arial", 16, "bold"),
    bg="#f2f6ff",
    fg="#333"
)
result_label.pack(pady=40)

# ================= PREDICT FUNCTION =================
 def predict_thread():

    loading_label.config(text="🔄 Analyzing Patient Data...")

    time.sleep(1.5)

    try:
        values = np.array([float(i.get()) for i in entries]).reshape(1, -1)

        values = scaler.transform(values)
        out = model.predict(values)

        if out[0] == 0:
            result_text = "❌ MALIGNANT (CANCER DETECTED)"
            color = "red"
        else:
            result_text = "✅ BENIGN (NO CANCER)"
            color = "green"

        result.config(text=result_text, fg=color)

        # 🔥 SAVE PDF REPORT
        save_pdf_report(values, result_text)

        # 🔥 SAVE HISTORY
        save_history(values, result_text)

    except:
        result.config(text="⚠ INVALID INPUT", fg="orange")

    loading_label.config(text="")
# ================= BUTTON =================
btn = tk.Button(
    left,
    text="🔍 PREDICT DIAGNOSIS",
    command=predict,
    bg="#27ae60",
    fg="white",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=10
)
btn.grid(row=10, column=0, columnspan=2, pady=20)

# ================= FOOTER =================
tk.Label(
    right,
    text="AI Hospital System\nFinal Year Project",
    bg="#f2f6ff",
    font=("Arial", 10)
).pack(pady=20)

# ================= RUN =================
root.mainloop()