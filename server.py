from flask import Flask, request, Response, jsonify
from weasyprint import HTML
import logging

app = Flask(__name__)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        # Expect JSON data with an "html" field containing your HTML string
        data = request.get_json()
        html_content = data.get('html')
        if not html_content:
            return jsonify({'error': 'Missing HTML content'}), 400
        
        # Optional: Provide a base URL if your HTML contains relative URLs
        base_url = data.get('base_url', None)

        # Generate PDF using WeasyPrint
        pdf = HTML(string=html_content, base_url=base_url).write_pdf()

        # Return the PDF with proper headers
        response = Response(pdf, mimetype='application/pdf')
        response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response
    except Exception as e:
        logging.exception("Error generating PDF")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
