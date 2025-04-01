from flask import Flask, request, render_template, send_file
from weasyprint import HTML
import os
import io

# Tell Flask to look for templates in the 'views' folder
app = Flask(__name__, template_folder="views")

@app.route('/generate-pdf/single-interface', methods=['POST'])
def generate_pdf():
     # Sample data to pass into Jinja
    data = request.json

    # Render the Jinja template as an HTML string
    rendered_html = render_template("single-interface/single-interface.html", data=data)

    # Convert HTML to PDF
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)

    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/generateCable-pdf/cable',methods=['POST'])
def generateCable_pdf():

    data=request.json

    rendered_html=render_template("cable/cable.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')


@app.route('/generateMulti-pdf/Multi',methods=['POST'])
def generateMulti_pdf():

    data=request.json

    rendered_html=render_template("multi-interface/multi-interface.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/compliancePDF/compliance',methods=['POST'])
def generateCompliance_pdf():

    data=request.json

    rendered_html=render_template("compliance/compliance.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/quotes/quotes',methods=['POST'])
def generateQuotes_pdf():

    data=request.json

    rendered_html=render_template("quotes/quotes.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')





if __name__ == '__main__':
    app.run(debug=True)
