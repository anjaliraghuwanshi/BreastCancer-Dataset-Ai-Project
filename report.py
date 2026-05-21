from fpdf import FPDF
import random

def save_pdf_report(values, result):

    pid = f"PAT_{random.randint(1000,9999)}"

    # REMOVE EMOJIS
    result = str(result)
    result = result.replace("❌", "")
    result = result.replace("✅", "")

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="BREAST CANCER REPORT", ln=True)
    pdf.cell(200, 10, txt=f"Patient ID: {pid}", ln=True)
    pdf.cell(200, 10, txt=f"Result: {result}", ln=True)

    pdf.cell(200, 10, txt="Features:", ln=True)

    # ✅ FINAL FIX
    for i, v in enumerate(values[0]):

        pdf.cell(
            200,
            10,
            txt=f"Feature {i+1}: {v}",
            ln=True
        )

    filename = f"{pid}_report.pdf"

    pdf.output(filename)

    print("REPORT SAVED:", filename)