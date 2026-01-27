from flask import Flask, request, Response, jsonify, render_template, send_file
from weasyprint import HTML
import logging
import io

# ✅ Import description generator functions from client script
from cable_assembly_part_description_generator import (
    singl_if_generate_part_description,
    generate_assembly_pn_length,
    generate_assembly_type,
    generate_phase_matched_string,
)

app = Flask(__name__)

# ========================
# PDF GENERATION ROUTES
# ========================

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        template_data = data.get('data')
        if not template_data:
            return jsonify({'error': 'Missing data for template'}), 400

        html_content = render_template("template.html", **template_data)
        pdf = HTML(string=html_content).write_pdf()

        response = Response(pdf, mimetype='application/pdf')
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response
    except Exception as e:
        logging.exception("Error generating PDF")
        return jsonify({'error': str(e)}), 500


@app.route('/compliancePDF/compliance', methods=['POST'])
def generateCompliance_pdf():
    try:
        data = request.json
        rendered_html = render_template("compliance/compliance.html", data=data)
        pdf_buffer = io.BytesIO()
        HTML(string=rendered_html).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, mimetype='application/pdf')
    except Exception as e:
        logging.exception("Error generating compliance PDF")
        return jsonify({'error': str(e)}), 500

# ========================
# DESCRIPTION GENERATION ROUTE
# ========================

@app.route('/generate-description', methods=['POST'])
def generate_description():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing input data'}), 400

        # Expecting structured input with connectorA, connectorB, cable, and assembly
        end_a = data.get("connectorA", {})
        end_b = data.get("connectorB", {})
        cable = data.get("cable", {})
        assembly = data.get("assembly", {})

        # Call client-provided functions
        end_a_description = singl_if_generate_part_description(end_a)
        end_b_description = singl_if_generate_part_description(end_b)
        assembly_pn_length = generate_assembly_pn_length(assembly)
        assembly_type = generate_assembly_type(cable)
        phase_matched_string = generate_phase_matched_string(assembly)

        # Build final description string
        final_string = (
            f"{assembly_pn_length}, {assembly_type}. "
            f"{end_a_description} on End A and {end_b_description} on End B. "
            f"{phase_matched_string}"
        )

        return jsonify({"description": final_string})
    except Exception as e:
        logging.exception("Error generating description")
        return jsonify({'error': str(e)}), 500

# ========================
# WARMUP (optional)
# ========================

@app.before_first_request
def warmup_pdf():
    try:
        HTML(string="<p>warm up weasyprint pdf</p>").write_pdf()
        app.logger.info("weasyprint warmed up successfully")
    except Exception as e:
        app.logger.exception("Error during warm up: %s", e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
