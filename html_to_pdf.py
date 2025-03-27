import os
import sys
import importlib.util

def check_module_installed(module_name):
    """Check if a Python module is installed"""
    return importlib.util.find_spec(module_name) is not None

def convert_with_pdfkit(html_path, pdf_path=None):
    """Convert HTML to PDF using pdfkit"""
    try:
        import pdfkit
        
        # If no output path specified, use the same name with .pdf extension
        if pdf_path is None:
            pdf_path = os.path.splitext(html_path)[0] + '_pdfkit.pdf'
        
        # Get the absolute path to the HTML file for proper resource loading
        abs_html_path = os.path.abspath(html_path)
        
        # Configure options for wkhtmltopdf
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'enable-local-file-access': None  # Allow access to local files
        }
        
        # Convert HTML to PDF
        print(f"Converting {html_path} to PDF using pdfkit...")
        pdfkit.from_file(abs_html_path, pdf_path, options=options)
        print(f"PDF created successfully at: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error converting HTML to PDF with pdfkit: {e}")
        return None

def convert_with_weasyprint(html_path, pdf_path=None):
    """Convert HTML to PDF using WeasyPrint"""
    try:
        from weasyprint import HTML
        
        # If no output path specified, use the same name with .pdf extension
        if pdf_path is None:
            pdf_path = os.path.splitext(html_path)[0] + '_weasyprint.pdf'
        
        # Get the absolute path to the HTML file for proper resource loading
        abs_html_path = os.path.abspath(html_path)
        base_url = os.path.dirname(abs_html_path)
        
        # Convert HTML to PDF
        print(f"Converting {html_path} to PDF using WeasyPrint...")
        HTML(filename=abs_html_path, base_url=base_url).write_pdf(pdf_path)
        print(f"PDF created successfully at: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error converting HTML to PDF with WeasyPrint: {e}")
        return None

def convert_html_to_pdf(html_path, pdf_path=None, method=None):
    """
    Convert an HTML file to PDF using available methods
    
    Args:
        html_path (str): Path to the HTML file
        pdf_path (str, optional): Path for the output PDF file
        method (str, optional): Conversion method ('pdfkit' or 'weasyprint')
    
    Returns:
        str: Path to the generated PDF file
    """
    # Validate input file exists
    if not os.path.exists(html_path):
        print(f"Error: HTML file not found at {html_path}")
        return None
    
    # Determine which method to use
    pdfkit_available = check_module_installed('pdfkit')
    weasyprint_available = check_module_installed('weasyprint')
    
    if method == 'pdfkit' and pdfkit_available:
        return convert_with_pdfkit(html_path, pdf_path)
    elif method == 'weasyprint' and weasyprint_available:
        return convert_with_weasyprint(html_path, pdf_path)
    elif method is None:
        # Try available methods in order of preference
        if pdfkit_available:
            result = convert_with_pdfkit(html_path, pdf_path)
            if result:
                return result
        
        if weasyprint_available:
            return convert_with_weasyprint(html_path, pdf_path)
        
        print("Error: No PDF conversion libraries available. Please install pdfkit or weasyprint.")
        return None
    else:
        print(f"Error: Requested method '{method}' is not available.")
        print(f"Available methods: {'pdfkit' if pdfkit_available else ''} {'weasyprint' if weasyprint_available else ''}")
        return None

if __name__ == "__main__":
    # If run as a script, process command line arguments
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
        pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
        method = sys.argv[3] if len(sys.argv) > 3 else None
        convert_html_to_pdf(html_file, pdf_file, method)
    else:
        # Default to index.html if no arguments provided
        convert_html_to_pdf('index.html')
