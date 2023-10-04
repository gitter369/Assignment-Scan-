from flask import Flask, render_template, request, redirect, url_for,  send_from_directory
import fitz  # PyMuPDF library
import os

app = Flask(__name__)

# Define the directory where uploaded PDF files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to highlight text in a PDF
def highlight_text_in_pdf(pdf_path, keywords):
    pdf_document = fitz.open(pdf_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        for keyword in keywords:
            text_instances = page.search_for(keyword)
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors({"stroke": (1, 1, 0)})  # Yellow highlight color
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'highlighted_output.pdf')
    pdf_document.save(output_path)
    pdf_document.close()
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.form['keywords'].split(',')
        pdf_file = request.files['document']
        if pdf_file and pdf_file.filename.endswith(('.pdf', '.doc', '.docx')):
            # Save the uploaded PDF file
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.pdf')
            pdf_file.save(pdf_path)

            # Highlight the specified keywords in the PDF
            highlighted_pdf_path = highlight_text_in_pdf(pdf_path, keywords)

            return redirect(url_for('result'))
    return render_template('index.html')

@app.route('/result')
def result():
    highlighted_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'highlighted_output.pdf')
    print("PDF Path:", highlighted_pdf_path)  # Debugging line
    return render_template('result.html', highlighted_pdf=highlighted_pdf_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
