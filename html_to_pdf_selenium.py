from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys
import time
import json

def convert_html_to_pdf(html_path, pdf_path=None):
    """
    Convert an HTML file to PDF using Chrome/Selenium
    
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
        pdf_path = os.path.splitext(html_path)[0] + '_selenium.pdf'
    
    try:
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
            "profile.default_content_settings.popups": 0,
            "download.default_directory": os.path.dirname(os.path.abspath(pdf_path))
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

if __name__ == "__main__":
    # If run as a script, process command line arguments
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
        pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_html_to_pdf(html_file, pdf_file)
    else:
        # Default to index.html if no arguments provided
        convert_html_to_pdf('index.html')
