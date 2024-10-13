import sys
import os
import re
from pypdf import PdfReader

def sanitize_filename(filename):
    # Remove or replace invalid characters for filenames
    # For Windows, the following characters are not allowed:
    # \ / : * ? " < > |
    invalid_chars = r'[\\\/\:*?"<>|]'
    return re.sub(invalid_chars, '', filename)

def extract_title(pdf_path):
    reader = PdfReader(pdf_path)
    # First, try to get the title from metadata
    if reader.metadata and '/Title' in reader.metadata:
        title = reader.metadata['/Title']
        if title:
            return [title.strip()]  # Return as a list
    # If no title in metadata, try to extract text from first page
    first_page = reader.pages[0]
    text = first_page.extract_text()
    if text:
        # Heuristic to get the first non-empty lines as titles
        lines = text.strip().split('\n')
        return [line.strip() for line in lines if line.strip()]
    return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python rename_pdfs.py <directory_path> [-m]")
        sys.exit(1)

    directory = sys.argv[1]
    manual_mode = '-m' in sys.argv

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            titles = extract_title(pdf_path)
            if not titles:
                print(f"Could not extract title from '{filename}'. Skipping.")
                continue

            if manual_mode:
                for i, title in enumerate(titles):
                    sanitized_title = sanitize_filename(title)
                    response = input(f"Rename '{filename}' to '{sanitized_title}.pdf'? (y/n): ").strip().lower()
                    if response == 'y':
                        new_pdf_path = os.path.join(directory, sanitized_title + '.pdf')
                        break
                    elif i == len(titles) - 1:
                        print(f"Skipping '{filename}'.")
                        new_pdf_path = None
                else:
                    new_pdf_path = None
            else:
                sanitized_title = sanitize_filename(titles[0])
                new_pdf_path = os.path.join(directory, sanitized_title + '.pdf')

            if new_pdf_path:
                try:
                    os.rename(pdf_path, new_pdf_path)
                    print(f"Renamed '{filename}' to '{os.path.basename(new_pdf_path)}'")
                except Exception as e:
                    print(f"Failed to rename '{filename}': {e}")

if __name__ == '__main__':
    main()
