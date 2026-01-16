from flask import Flask, request, render_template, send_file
from weasyprint import HTML
import os
import io

# Import custom formatters
from utils.formatters import format_inr

# Tell Flask to look for templates in the 'views' folder
app = Flask(__name__, template_folder="views")

# Register custom Jinja filters
app.jinja_env.filters['format_inr'] = format_inr

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

@app.route('/generateCable-pdf/cable', methods=['POST'])
def generateCable_pdf():
    data = request.json

    rendered_html = render_template("cable/cable.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/generateMulti-pdf/Multi', methods=['POST'])
def generateMulti_pdf():
    data = request.json

    rendered_html = render_template("multi-interface/multi-interface.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/compliancePDF/compliance', methods=['POST'])
def generateCompliance_pdf():
    data = request.json

    rendered_html = render_template("compliance/compliance.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/quotes/quotes', methods=['POST'])
def generateQuotes_pdf():
    data = request.json

    rendered_html = render_template("quotes/quotes.html", data=data)
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/coverLetter/coverLetters', methods=['POST'])
def generateCoverLetter_pdf():
    data = request.json
    if not data:
        return "Invalid JSON payload", 400
    if "quotationRef" not in data or "customerName" not in data:
        return "Missing required fields", 400
    if not isinstance(data.get("items"), list):
        return "Invalid 'items' field. It must be a list.", 400
    print(data)  # Debugging: Print the incoming JSON data

    # Render the Jinja template for the cover letter
    rendered_html = render_template("coverLetter/coverLetters.html", data=data)

    # Convert HTML to PDF
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/packingList/generate', methods=['POST'])
def generatePackingList_pdf():
    """Generate Packing List PDF from JSON data"""
    data = request.json
    if not data:
        return "Invalid JSON payload", 400

    # Validate required fields
    required_fields = ["customerName"]
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}", 400

    print("Packing List PDF Data:", data)  # Debugging: Print the incoming JSON data

    # Render the Jinja template for the packing list
    rendered_html = render_template("packingList/packingList.html", data=data)

    # Convert HTML to PDF
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

@app.route('/addressSheet/generate', methods=['POST'])
def generateAddressSheet_pdf():
    """Generate Address Sheet PDF from JSON data"""
    data = request.json
    if not data:
        return "Invalid JSON payload", 400

    # Validate required fields
    required_fields = ["poNumber", "toAddress", "fromAddress"]
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}", 400

    print("Address Sheet PDF Data:", data)  # Debugging: Print the incoming JSON data

    # Render the Jinja template for the address sheet
    rendered_html = render_template("addressSheet/addressSheet.html",
                                 poNumber=data.get("poNumber", ""),
                                 toAddress=data.get("toAddress", {}),
                                 fromAddress=data.get("fromAddress", {}))

    # Convert HTML to PDF
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)