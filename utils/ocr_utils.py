import os
import easyocr
import streamlit as st
from pdf2image import convert_from_bytes

def extract_images_from_pdf(file_bytes):
    images = convert_from_bytes(file_bytes, fmt='jpeg')
    st.success(f"Converted {len(images)} pages to images.")
    return images

def extract_texts_from_pdf(pdf_bytes):
    dir_name = os.path.dirname(__file__)
    UPLOAD_FOLDER = os.path.join(dir_name, "temp_images")
    
    try:
        reader = easyocr.Reader(['en', 'hi'], gpu=False)
        images = extract_images_from_pdf(pdf_bytes)
        all_text = []

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        for i, img in enumerate(images):
            img_path = os.path.join(UPLOAD_FOLDER, f"page_{i}.jpg")
            img.save(img_path)

            st.image(img_path, caption=f"Page {i + 1}", use_column_width=True)
            with st.spinner(f"🔍 OCR on Page {i + 1}..."):
                result = reader.readtext(img_path, detail=0)
                devanagari_texts = [text for text in result if any('\u0900' <= c <= '\u097F' for c in text)]
                all_text.extend(devanagari_texts)

        return all_text
    finally:
        # Clean up temporary images
        if os.path.exists(UPLOAD_FOLDER):
            for img in os.listdir(UPLOAD_FOLDER):
                os.remove(os.path.join(UPLOAD_FOLDER, img))
            os.rmdir(UPLOAD_FOLDER)
