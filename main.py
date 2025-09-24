from flask import Flask, request, Response, jsonify, render_template, send_file
from weasyprint import HTML
import os
import io

# Tell Flask to look for templates in the 'views' folder
from cable_assembly_part_description_generator import (
    singl_if_generate_part_description,
    generate_assembly_pn_length,
    generate_assembly_type,
    generate_phase_matched_string,
)
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

@app.route('/generate-description', methods=['POST'])
def generate_description():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing input data'}), 400

        end_a = data.get("connectorA", {})
        end_b = data.get("connectorB", {})
        cable = data.get("cable", {})
        assembly = data.get("assembly", {})

        # import functions at top:
        # from cable_assembly_part_description_generator import (
        #     singl_if_generate_part_description,
        #     generate_assembly_pn_length,
        #     generate_assembly_type,
        #     generate_phase_matched_string,
        # )

        end_a_description = singl_if_generate_part_description(end_a)
        end_b_description = singl_if_generate_part_description(end_b)
        assembly_pn_length = generate_assembly_pn_length(assembly)
        assembly_type = generate_assembly_type(cable)
        phase_matched_string = generate_phase_matched_string(assembly)

        final_string = (
            f"{assembly_pn_length}, {assembly_type}. "
            f"{end_a_description} on End A and {end_b_description} on End B. "
            f"{phase_matched_string}"
        )

        return jsonify({"description": final_string})
    except Exception as e:
        app.logger.exception("Error generating description")
        return jsonify({'error': str(e)}), 500


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
    
@app.route('/workOrder/generate', methods=['POST'])
def generateWorkOrder_pdf():
    """Generate Work Order PDF from JSON data"""
    data = request.json
    if not data:
        return "Invalid JSON payload", 400

    print("Work Order PDF Data:", data)  # Debugging

    # Render the Jinja template for Work Order (uses partials inside workOrder.html)
    rendered_html = render_template("workOrder/workOrder.html", **data)

    # Convert HTML to PDF
    pdf_buffer = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)