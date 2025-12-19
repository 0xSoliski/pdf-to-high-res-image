# PDF to High-Resolution Image Converter

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/0xSoliski/pdf-to-high-res-image/releases/tag/v1.0.0) [![License: AGPL v3](https://img.shields.io/badge/license-AGPLv3-blue.svg)](LICENSE)

Command-line utility for extracting PDF pages as raster images using PyMuPDF. Supports PNG/JPEG output at 300 or 600 DPI.

## Features

- DPI options: 300 or 600
- Output formats: PNG (lossless), JPEG (quality=95)
- Page selection: single pages, ranges, or all
- Interactive CLI with input validation
- Batch extraction with progress tracking
- Overwrite confirmation
- Partial failure handling

## Requirements

- Python 3.7 or higher
- PyMuPDF (fitz)
- PyInstaller (for building executable)

## Installation

### For Development

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Building the Executable

Run the build script:
```bash
build_exe.bat
```

The executable will be created in the `dist` folder as `pdf_to_image.exe`.

## Usage

### Running the Python Script

```bash
python pdf_to_image.py
```

### Running the Executable

1. Place `pdf_to_image.exe` in the same directory as your PDF files
2. Double-click the executable or run from command line:
   ```bash
   pdf_to_image.exe
   ```

### Interactive Prompts

The program will guide you through the following steps:

1. **PDF Filename**: Enter the name of the PDF file (must be in the same directory)
   - Example: `document.pdf`

2. **DPI Selection**: Choose resolution (press Enter for default 300 DPI)
   - `300` - Standard high resolution
   - `600` - Ultra high resolution

3. **Output Format**: Choose image format (press Enter for default PNG)
   - `png` - PNG format (lossless)
   - `jpeg` - JPEG format (compressed, smaller files)

4. **Page Selection**: Specify which pages to extract
   - `all` - Extract all pages
   - `3` - Extract page 3
   - `1,3,5` - Extract pages 1, 3, and 5
   - `1-5` - Extract pages 1 through 5
   - `1-3,7,9-11` - Combination of ranges and individual pages

5. **Overwrite Confirmation**: If files already exist, confirm whether to overwrite

### Output Files

Output files are named using the pattern:
```
{original_pdf_name}_page_{page_number}.{format}
```

Examples:
- `document_page_1.png`
- `document_page_5.jpeg`

## Examples

### Extract All Pages as PNG at 300 DPI (defaults)
```
Enter the PDF filename: document.pdf
Select DPI: [Press Enter]
Select output format: [Press Enter]
Select pages to extract: all
```

### Extract Specific Pages as JPEG at 600 DPI
```
Enter the PDF filename: report.pdf
Select DPI: 600
Select output format: jpeg
Select pages to extract: 1,5,10-15
```

## Error Handling

- Input validation with retry loops
- File existence check before processing
- Per-page error isolation (failures don't abort batch)
- Summary report with success/failure counts
- Exit prompt to prevent terminal auto-close

## Technical Details

- **DPI Conversion**: Uses PyMuPDF's matrix scaling (`zoom = dpi / 72.0`)
- **Memory Management**: Explicitly clears pixmaps after saving to optimize memory usage
- **JPEG Quality**: Fixed at 95 for optimal quality
- **Page Numbering**: User-facing prompts use 1-based numbering (page 1 = first page)

## License

Licensed under the GNU Affero General Public License v3.0. See [LICENSE](LICENSE) for details.

## Troubleshooting

**Problem**: "PyMuPDF not found" error  
**Solution**: Install dependencies: `pip install PyMuPDF`

**Problem**: Executable doesn't run  
**Solution**: Ensure the PDF file is in the same directory as the executable

**Problem**: Out of memory errors  
**Solution**: Use 300 DPI instead of 600 DPI, or process fewer pages at once

