from weasyprint import HTML
import os
import sys

def convert_html_to_pdf(html_path, pdf_path=None):
    """
    Convert an HTML file to PDF using WeasyPrint
    
    Args:
        html_path (str): Path to the HTML file
        pdf_path (str, optional): Path for the output PDF file. If not provided,
                                 uses the same name as the HTML file with .pdf extension
    
    Returns:
        str: Path to the generated PDF file
    """
    # Validate input file exists
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        return None
    
    # If no output path specified, use the same name with .pdf extension
    if pdf_path is None:
        pdf_path = os.path.splitext(html_path)[0] + '.pdf'
    
    try:
        # Get the absolute path to the HTML file for proper resource loading
        abs_html_path = os.path.abspath(html_path)
        base_url = os.path.dirname(abs_html_path)
        
        # Convert HTML to PDF
        print(f"Converting {html_path} to PDF...")
        HTML(filename=abs_html_path, base_url=base_url).write_pdf(pdf_path)
        print(f"PDF created successfully at: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")
        return None

if __name__ == "__main__":
    # If run as a script, process command line arguments
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
        pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_html_to_pdf(html_file, pdf_file)
    else:
        # Default to index.html if no arguments provided
        convert_html_to_pdf('index.html')
