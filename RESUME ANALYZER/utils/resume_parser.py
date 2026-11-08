import io
import pdfplumber

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from an uploaded PDF file or file-like object using pdfplumber.
    Returns cleaned text.
    """
    extracted_text = []
    try:
        # If pdf_file is UploadedFile from streamlit, wrap or pass directly to pdfplumber
        if hasattr(pdf_file, "read"):
            pdf_bytes = io.BytesIO(pdf_file.read())
            # reset pointer so it can be re-read if needed
            pdf_file.seek(0)
            with pdfplumber.open(pdf_bytes) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text)
        else:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text)
                        
        full_text = "\n".join(extracted_text).strip()
        return full_text
    except Exception as e:
        raise RuntimeError(f"Error reading PDF file: {str(e)}") from e

