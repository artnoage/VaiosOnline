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

def convert_with_selenium(html_path, pdf_path=None):
    """Convert HTML to PDF using Selenium with Chrome"""
    try:
        # Import here to avoid dependency if not used
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        import json
        
        # If no output path specified, use the same name with .pdf extension
        if pdf_path is None:
            pdf_path = os.path.splitext(html_path)[0] + '_selenium.pdf'
        
        # Get the absolute path to the HTML file
        abs_html_path = os.path.abspath(html_path)
        file_url = f"file:///{abs_html_path}"
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')  # Set a large window size
        
        # Set print preferences
        app_state = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": ""
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2,
            "isLandscapeEnabled": False,
            "isHeaderFooterEnabled": False,
            "isCssBackgroundEnabled": True,  # Enable background colors/images
            "mediaSize": {
                "height_microns": 297000,
                "width_microns": 210000,
                "name": "ISO_A4"
            },
            "marginsType": 1,  # Minimum margins
            "scalingType": 3,  # Custom scaling
            "scaling": 100,  # 100%
        }
        
        prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(app_state),
            'download.default_directory': os.path.dirname(os.path.abspath(pdf_path)),
            'savefile.default_directory': os.path.dirname(os.path.abspath(pdf_path))
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        print(f"Converting {html_path} to PDF using Chrome/Selenium...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the HTML file
        driver.get(file_url)
        
        # Wait for page to fully load
        time.sleep(2)
        
        # Print to PDF
        print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
            'pageSize': 'A4',
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
            'scale': 1.0
        }
        
        result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
        
        # Save the PDF
        with open(pdf_path, 'wb') as file:
            file.write(bytes(result['data'], 'utf-8'))
        
        driver.quit()
        print(f"PDF created successfully at: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error converting HTML to PDF with Selenium: {e}")
        return None

def convert_html_to_pdf(html_path, pdf_path=None, method=None):
    """
    Convert an HTML file to PDF using available methods
    
    Args:
        html_path (str): Path to the HTML file
        pdf_path (str, optional): Path for the output PDF file
        method (str, optional): Conversion method ('pdfkit', 'weasyprint', or 'selenium')
    
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
    selenium_available = check_module_installed('selenium')
    
    if method == 'pdfkit' and pdfkit_available:
        return convert_with_pdfkit(html_path, pdf_path)
    elif method == 'weasyprint' and weasyprint_available:
        return convert_with_weasyprint(html_path, pdf_path)
    elif method == 'selenium' and selenium_available:
        return convert_with_selenium(html_path, pdf_path)
    elif method is None:
        # Try available methods in order of preference
        if selenium_available:
            result = convert_with_selenium(html_path, pdf_path)
            if result:
                return result
                
        if pdfkit_available:
            result = convert_with_pdfkit(html_path, pdf_path)
            if result:
                return result
        
        if weasyprint_available:
            return convert_with_weasyprint(html_path, pdf_path)
        
        print("Error: No PDF conversion libraries available. Please install selenium, pdfkit, or weasyprint.")
        return None
    else:
        print(f"Error: Requested method '{method}' is not available.")
        available_methods = []
        if selenium_available:
            available_methods.append('selenium')
        if pdfkit_available:
            available_methods.append('pdfkit')
        if weasyprint_available:
            available_methods.append('weasyprint')
        print(f"Available methods: {' '.join(available_methods)}")
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
