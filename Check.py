import pymupdf
import pdfplumber
import os

# Define the exact PDF path
PDF_PATH = r"F:\Python assignment\Form ADT-1-29092023_signed.pdf"


def validate_pdf(path):
    """Check if PDF exists and is readable"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF file not found at: {path}")
    if not path.lower().endswith('.pdf'):
        raise ValueError("File is not a PDF")
    return True


def extract_pdf_data(path):
    """Extract data using both libraries"""
    print(f"\n➡️ Processing PDF: {os.path.basename(path)}")

    # PyMuPDF extraction
    print("\n🔍 PyMuPDF Results:")
    with pymupdf.open(path) as doc:
        print(f"• Pages: {len(doc)}")
        print(f"• Metadata: {doc.metadata}")
        print(f"• First 200 chars: {doc[0].get_text()[:200]}...")

    # pdfplumber extraction
    print("\n🔍 pdfplumber Results:")
    with pdfplumber.open(path) as pdf:
        first_page = pdf.pages[0]
        print(f"• Page width: {first_page.width}")
        print(f"• First 200 chars:\n{first_page.extract_text()[:200]}...")


if __name__ == "__main__":
    try:
        if validate_pdf(PDF_PATH):
            extract_pdf_data(PDF_PATH)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print(f"1. Confirm the file exists at: {PDF_PATH}")
        print("2. Check file permissions")
        print("3. Verify the file is not corrupted")