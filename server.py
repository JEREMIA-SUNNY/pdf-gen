from flask import Flask, request, Response, jsonify, render_template
from weasyprint import HTML
import logging

app = Flask(__name__)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        # Expect JSON data with a "data" field containing template variables
        data = request.get_json()
        template_data = data.get('data')
        if not template_data:
            return jsonify({'error': 'Missing data for template'}), 400
        
        # Render the HTML using a Jinja template (e.g., "template.html")
        html_content = render_template("template.html", **template_data)
        
        # Generate PDF using WeasyPrint
        pdf = HTML(string=html_content).write_pdf()

        # Return the PDF with proper headers
        response = Response(pdf, mimetype='application/pdf')
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response
    except Exception as e:
        logging.exception("Error generating PDF")
        return jsonify({'error': str(e)}), 500
    
@app.before_first_request
def warmup_pdf():
    try:
        HTML(string="<p>warm up weasyprint pdf</p>").write_pdf()
        app.logger.info("weasyprint warmed up successfully")
    except Exception as e:
        app.logger.exception("Error during warm up: %s", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
