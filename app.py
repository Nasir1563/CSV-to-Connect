import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Example settings data (you can replace this with database storage)
settings = {
    "site_name": "My Awesome Site",
    "site_description": "A simple website built with Flask and Supabase",
    "contact_email": "contact@myawesomesite.com",
    "support_phone": "+1234567890",
    "address": "1234 Main St, Anytown, USA"
}

@app.context_processor
def inject_settings():
    return dict(settings=settings)

@app.route('/')
def landing():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('landing.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/settings', methods=['GET', 'POST'])
def site_settings():
    global settings
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        site_name = request.form['site_name']
        site_description = request.form['site_description']
        contact_email = request.form['contact_email']
        support_phone = request.form['support_phone']
        address = request.form['address']
        
        settings['site_name'] = site_name
        settings['site_description'] = site_description
        settings['contact_email'] = contact_email
        settings['support_phone'] = support_phone
        settings['address'] = address
        
        flash('Settings updated successfully.')
    
    return render_template('settings.html', settings=settings)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Register with Supabase
        response = supabase.auth.sign_up({'email': email, 'password': password})
        
        if response.user:
            flash('Registration successful, please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed.')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Authenticate with Supabase
        response = supabase.auth.sign_in_with_password({'email': email, 'password': password})
        if response.user:
            session['user'] = email
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    ten_days_ago = (datetime.now() - timedelta(days=10)).date().isoformat()

    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and (rule.defaults is None or len(rule.defaults) >= len(rule.arguments)):
            pages.append([
                f"http://example.com{str(rule.rule)}",
                ten_days_ago
            ])

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response

# Placeholder routes for PDF functionalities
@app.route('/compress-pdf')
def compress_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Compress PDF")

@app.route('/convert-pdf/<conversion_type>')
def convert_pdf(conversion_type):
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name=f"Convert PDF: {conversion_type.replace('-', ' ')}")

@app.route('/merge-pdf')
def merge_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Merge PDF")

@app.route('/split-pdf')
def split_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Split PDF")

@app.route('/edit-pdf')
def edit_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Edit PDF")

@app.route('/sign-pdf')
def sign_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Sign PDF")

@app.route('/unlock-pdf')
def unlock_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Unlock PDF")

@app.route('/protect-pdf')
def protect_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Protect PDF")

@app.route('/rotate-pdf')
def rotate_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Rotate PDF")

@app.route('/delete-pdf-pages')
def delete_pdf_pages():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Delete PDF Pages")

@app.route('/organize-pdf-pages')
def organize_pdf_pages():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Organize PDF Pages")

@app.route('/pdf-reader')
def pdf_reader():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Reader")

@app.route('/pdf-form-filler')
def pdf_form_filler():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Form Filler")

@app.route('/pdf-annotator')
def pdf_annotator():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Annotator")

@app.route('/pdf-to-esign')
def pdf_to_esign():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to eSign")

@app.route('/pdf-to-webpage')
def pdf_to_webpage():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to Webpage")

@app.route('/batch-processing')
def batch_processing():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Batch Processing")

@app.route('/api-access')
def api_access():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="API Access")

@app.route('/add-page-numbers')
def add_page_numbers():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Add Page Numbers")

@app.route('/add-watermark')
def add_watermark():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Add Watermark")

@app.route('/pdf-to-text')
def pdf_to_text():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to Text")

@app.route('/pdf-to-png')
def pdf_to_png():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to PNG")

@app.route('/pdf-to-tiff')
def pdf_to_tiff():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to TIFF")

@app.route('/html-to-pdf')
def html_to_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="HTML to PDF")

@app.route('/pdf-to-rtf')
def pdf_to_rtf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to RTF")

@app.route('/pdf-to-epub')
def pdf_to_epub():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to EPUB")

@app.route('/pdf-to-bmp')
def pdf_to_bmp():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF to BMP")

@app.route('/extract-pdf-images')
def extract_pdf_images():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Extract PDF Images")

@app.route('/ocr')
def ocr():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="OCR (Optical Character Recognition)")

@app.route('/pdf-translator')
def pdf_translator():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Translator")

@app.route('/pdf-metadata-editor')
def pdf_metadata_editor():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Metadata Editor")

@app.route('/pdf-file-recovery')
def pdf_file_recovery():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF File Recovery")

@app.route('/pdf-redaction')
def pdf_redaction():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Redaction")

@app.route('/pdf-background-remover')
def pdf_background_remover():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Background Remover")

@app.route('/pdf-thumbnail-generator')
def pdf_thumbnail_generator():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF Thumbnail Generator")

@app.route('/pdf-a-conversion')
def pdf_a_conversion():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="PDF/A Conversion")

@app.route('/page-extraction')
def page_extraction():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feature.html', feature_name="Page Extraction")

if __name__ == '__main__':
    app.run(debug=True)
