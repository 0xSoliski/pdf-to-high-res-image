#!/usr/bin/env python3
"""
PDF to High-Resolution Image Converter
Extracts pages from PDF files as high-resolution images (300 or 600 DPI)
Supports PNG, JPEG, and TIFF output formats
"""

__version__ = "1.0.0"

import os
import sys
import fitz  # PyMuPDF
from pathlib import Path

# Optional tab-completion support on Windows via pyreadline3
try:
    import readline  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    readline = None


def print_header():
    """Display application header"""
    print("=" * 60)
    print("PDF to High-Resolution Image Converter")
    print("=" * 60)
    print()


def enable_filename_completion():
    """Enable tab completion for filenames if readline is available"""
    if readline is None:
        return

    def complete(text, state):
        # Suggest files in current directory that start with the typed text
        candidates = []
        prefix = text.lower()
        for name in os.listdir('.'):
            if name.lower().startswith(prefix) and os.path.isfile(name):
                candidates.append(name)
        candidates.sort()
        return candidates[state] if state < len(candidates) else None

    try:
        readline.set_completer_delims(' \t\n')
        readline.set_completer(complete)
        readline.parse_and_bind('tab: complete')
    except Exception:
        pass


def get_pdf_filename():
    """Prompt for PDF filename with validation"""
    enable_filename_completion()
    while True:
        print("Enter the PDF filename (must be in the same directory):")
        filename = input("> ").strip()
        
        if not filename:
            print("Error: Filename cannot be empty. Please try again.\n")
            continue
        
        # Check if file exists in current directory
        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' not found in current directory.")
            print("Please make sure the file exists and try again.\n")
            continue
        
        # Check if it's a PDF (require explicit extension to avoid ambiguity)
        if not filename.lower().endswith('.pdf'):
            print("Error: Please include the .pdf extension (example: file.pdf).\n")
            continue
        
        # Try to open the PDF to validate it
        try:
            doc = fitz.open(filename)
            page_count = len(doc)
            doc.close()
            print(f"✓ PDF loaded successfully ({page_count} pages)\n")
            return filename, page_count
        except Exception as e:
            print(f"Error: Could not open PDF file. {str(e)}")
            print("Please try again.\n")
            continue


def get_dpi():
    """Prompt for DPI selection with validation"""
    while True:
        print("Select DPI (resolution):")
        print("  300 - Standard high resolution (default)")
        print("  600 - Ultra high resolution")
        print("Press Enter for default (300 DPI)")
        dpi_input = input("> ").strip()
        
        if dpi_input == "":
            print("✓ Using default: 300 DPI\n")
            return 300
        
        if dpi_input in ["300", "600"]:
            print(f"✓ Selected: {dpi_input} DPI\n")
            return int(dpi_input)
        
        print("Error: Invalid DPI. Please enter 300 or 600 (or press Enter for default).\n")


def get_output_format():
    """Prompt for output format with validation"""
    while True:
        print("Select output format:")
        print("  png  - PNG format (default, lossless)")
        print("  jpeg - JPEG format (compressed, smaller files)")
        print("Press Enter for default (png)")
        format_input = input("> ").strip().lower()
        
        if format_input == "":
            print("✓ Using default: PNG\n")
            return "png"
        
        if format_input in ["png", "jpeg"]:
            print(f"✓ Selected: {format_input.upper()}\n")
            return format_input
        
        print("Error: Invalid format. Please enter png or jpeg (or press Enter for default).\n")


def parse_page_input(page_input, max_pages):
    """
    Parse user page input into a list of 0-based page indices
    Supports: 'all', '1-5', '1,3,5', '3'
    Returns list of 0-based indices or None if invalid
    """
    page_input = page_input.strip().lower()

    if page_input == "all":
        return list(range(max_pages))

    pages = set()  # deduplicate efficiently

    try:
        parts = page_input.split(',')

        for part in parts:
            part = part.strip()
            if not part:
                continue

            if '-' in part:
                range_parts = part.split('-', 1)
                if len(range_parts) != 2:
                    return None

                start = int(range_parts[0].strip())
                end = int(range_parts[1].strip())

                if start < 1 or end < 1 or start > end or start > max_pages or end > max_pages:
                    return None

                pages.update(range(start - 1, end))
            else:
                page_num = int(part)
                if page_num < 1 or page_num > max_pages:
                    return None
                pages.add(page_num - 1)

        return sorted(pages) if pages else None

    except ValueError:
        return None


def get_pages_to_extract(page_count):
    """Prompt for pages to extract with validation"""
    while True:
        print(f"Select pages to extract (1-{page_count}):")
        print("  Examples:")
        print("    all       - Extract all pages")
        print("    3         - Extract page 3")
        print("    1,3,5     - Extract pages 1, 3, and 5")
        print("    1-5       - Extract pages 1 through 5")
        print("    1-3,7,9-11 - Combination of ranges and individual pages")
        page_input = input("> ").strip()
        
        if not page_input:
            print("Error: Please enter page selection.\n")
            continue
        
        pages = parse_page_input(page_input, page_count)
        
        if pages is None:
            print(f"Error: Invalid page selection. Please use valid page numbers (1-{page_count}).\n")
            continue
        
        if not pages:
            print("Error: No pages selected.\n")
            continue
        
        # Convert back to 1-based for display
        display_pages = [p + 1 for p in pages]
        if len(display_pages) <= 10:
            print(f"✓ Selected pages: {', '.join(map(str, display_pages))}\n")
        else:
            print(f"✓ Selected {len(display_pages)} pages: {display_pages[0]}-{display_pages[-1]} and others\n")
        
        return pages


def check_existing_files(pdf_basename, pages, output_format):
    """Check for existing output files and prompt for overwrite confirmation"""
    existing_files = []
    
    for page_idx in pages:
        page_num = page_idx + 1  # Convert to 1-based
        output_filename = f"{pdf_basename}_page_{page_num}.{output_format}"
        
        if os.path.isfile(output_filename):
            existing_files.append(output_filename)
    
    if not existing_files:
        return True  # No conflicts, proceed
    
    print("⚠ Warning: The following files already exist:")
    for filename in existing_files:
        print(f"  - {filename}")
    print()
    
    while True:
        response = input("Overwrite existing files? (y/n): ").strip().lower()
        if response == 'y':
            print("✓ Will overwrite existing files\n")
            return True
        elif response == 'n':
            print("Operation cancelled by user.\n")
            return False
        else:
            print("Error: Please enter 'y' or 'n'.\n")


def extract_pages(pdf_filename, pages, dpi, output_format):
    """Extract pages from PDF as high-resolution images"""
    pdf_basename = Path(pdf_filename).stem
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    save_jpeg = output_format == "jpeg"

    success_count = 0
    errors = []
    total_pages = len(pages)

    try:
        doc = fitz.open(pdf_filename)

        for idx, page_idx in enumerate(pages):
            page_num = page_idx + 1  # Convert to 1-based for display
            print(f"Processing page {page_num} ({idx + 1} of {total_pages})...", end=" ", flush=True)

            try:
                page = doc.load_page(page_idx)
                pix = page.get_pixmap(matrix=mat, alpha=False)

                output_filename = f"{pdf_basename}_page_{page_num}.{output_format}"

                if save_jpeg:
                    pix.save(output_filename, output="jpeg", jpg_quality=95)
                else:
                    pix.save(output_filename)

                pix = None
                del page

                print(f"✓ Saved as {output_filename}")
                success_count += 1

            except Exception as e:
                error_msg = f"Page {page_num}: {str(e)}"
                errors.append(error_msg)
                print(f"✗ Error: {str(e)}")

        doc.close()

    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        errors.append(f"Fatal error: {str(e)}")

    return success_count, errors


def main():
    """Main application flow"""
    print_header()
    
    # Get PDF filename
    pdf_filename, page_count = get_pdf_filename()
    
    # Get DPI setting
    dpi = get_dpi()
    
    # Get output format
    output_format = get_output_format()
    
    # Get pages to extract
    pages = get_pages_to_extract(page_count)
    
    # Check for existing files
    pdf_basename = Path(pdf_filename).stem
    if not check_existing_files(pdf_basename, pages, output_format):
        input("Press Enter to exit...")
        return
    
    # Extract pages
    print("=" * 60)
    print("Starting extraction...")
    print("=" * 60)
    print()
    
    success_count, errors = extract_pages(pdf_filename, pages, dpi, output_format)
    
    # Display summary
    print()
    print("=" * 60)
    print("Extraction Complete")
    print("=" * 60)
    print(f"Successfully extracted: {success_count} page(s)")
    
    if errors:
        print(f"Errors encountered: {len(errors)}")
        print("\nError details:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors encountered!")
    
    print("=" * 60)
    print()
    
    # Wait for user input before exiting
    input("Press Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        input("Press Enter to exit...")
