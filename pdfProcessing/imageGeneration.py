import os
import logging
from pdf2image import convert_from_path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_page_count(pdf_path):
    try:
        from PyPDF2 import PdfReader
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            return len(pdf.pages)
    except Exception as e:
        logging.error(f"Error getting page count for {pdf_path}: {e}")
        return 0

def convert_pdf_to_images(pdf_path, output_folder, first_page=1, last_page=None, dpi=150, poppler_path=None):
    try:
        logging.info(f"Converting PDF to images: {pdf_path}")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        images = convert_from_path(pdf_path, dpi=dpi, first_page=first_page, last_page=last_page, output_folder=output_folder, fmt='png', poppler_path=poppler_path)
        logging.info(f"Converted pages {first_page} to {last_page if last_page else 'end'} to images for {pdf_path}")
        return images
    except Exception as e:
        logging.error(f"Error converting PDF to images for {pdf_path}: {e}")

def process_pdf_folder(pdf_folder, images_output_folder, poppler_path=None):
    try:
        if not os.path.exists(images_output_folder):
            os.makedirs(images_output_folder)
        pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_folder, pdf_file)
            total_pages = get_page_count(pdf_path)
            
            if total_pages <= 4:
                logging.info(f"Skipping {pdf_file}: not enough pages to process.")
                continue
            
            first_page = 3  
            last_page = total_pages - 2 
            
            pdf_name = os.path.splitext(pdf_file)[0]
            pdf_image_folder = os.path.join(images_output_folder, pdf_name)
            if not os.path.exists(pdf_image_folder):
                os.makedirs(pdf_image_folder)
            
            convert_pdf_to_images(pdf_path, pdf_image_folder, first_page=first_page, last_page=last_page, poppler_path=poppler_path)
    except Exception as e:
        logging.error(f"Error processing PDF folder {pdf_folder}: {e}")

if __name__ == "__main__":
    pdf_folder = '/home/shiva/Documents/OCR/utils'
    images_output_folder = '/home/shiva/Documents/OCR/pdfImgaes'
    poppler_path = None

    process_pdf_folder(pdf_folder, images_output_folder, poppler_path)
