"""
merge.py

This script merges all PDF files in the current folder into a single PDF file. 
If a PDF has an odd number of pages, it adds a blank page to ensure an even page count.
Additionally, the merged PDF includes bookmarks for each file, named after the original filenames.

Created: 2024-12-06
Author: Generated with the assistance of ChatGPT

Dependencies:
- PyPDF2: For merging PDFs and adding bookmarks
- ReportLab: For creating blank pages

Usage:
1. Place this script in the folder containing the PDFs you want to merge.
2. Run the script using Python:
   python merge.py
3. The output file `merged_output_with_bookmarks.pdf` will be created in the current folder.

"""
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from tempfile import NamedTemporaryFile

def add_blank_page(pdf_writer):
    """Adds a blank page to the PDF writer."""
    # Create a temporary PDF with a blank page
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        c = canvas.Canvas(temp_pdf.name, pagesize=letter)
        c.showPage()
        c.save()
        temp_pdf.close()
        # Read the blank page PDF and add its page to the writer
        reader = PdfReader(temp_pdf.name)
        pdf_writer.add_page(reader.pages[0])
        os.unlink(temp_pdf.name)  # Delete the temporary file

def merge_pdfs_with_bookmarks(output_file):
    """Merges all PDFs in the current folder with bookmarks for each merged file."""
    pdf_writer = PdfWriter()

    current_folder = os.getcwd()
    current_page = 0  # Track the current page number for bookmarks

    for filename in sorted(os.listdir(current_folder)):
        if filename.endswith('.pdf'):
            file_path = os.path.join(current_folder, filename)
            reader = PdfReader(file_path)

            # Add a bookmark for the current file
            pdf_writer.add_outline_item(filename, current_page)

            # Add all pages of the current PDF to the writer
            for page in reader.pages:
                pdf_writer.add_page(page)
                current_page += 1
            
            # Add a blank page if the PDF has an odd number of pages
            if len(reader.pages) % 2 != 0:
                add_blank_page(pdf_writer)
                current_page += 1

    # Write the merged PDF to the output file
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

if __name__ == "__main__":
    # Output merged PDF file
    output_file = "merged_pdf.pdf"
    
    merge_pdfs_with_bookmarks(output_file)
    print(f"Merged PDF with bookmarks saved to {output_file}")
