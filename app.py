from flask import Flask, render_template, url_for, send_file, request
from socket import gethostname
import re
import random
import io
import tempfile
import os
import subprocess


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')




def randomize_numbers_in_expression(expr):
    def repl(match):
        return str(random.randint(0, 10))
    return re.sub(r'\d+(\.\d+)?', repl, expr)

@app.route('/generate', methods=['GET', 'POST'])
def serve_pdf():
    ## if the user uploads a file 
    if request.method == 'POST':
      if 'file' not in request.files:
        return 'No file part'
      file = request.files['file']
      if file.filename == '':
        return 'No selected file'
      if file.mimetype != "application/octet-stream":
         return 'Please upload a LaTeX (.tex) file'
      if file:
        tex_content = file.read().decode('utf-8')
    

    else:
      filename = 'static/HomeworkSample.tex'
      with app.open_resource(filename, 'r', encoding='utf-8') as f:
          tex_content = f.read()

    print(tex_content)

    pattern = r'(\${1,2})(.*?)(\1)'
    def replacer(match):
        delimiter = match.group(1)
        expr = match.group(2)
        randomized_expr = randomize_numbers_in_expression(expr)
        return f"{delimiter}{randomized_expr}{delimiter}"

    randomized_tex_content = re.sub(pattern, replacer, tex_content, flags=re.DOTALL)

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "doc.tex")
        pdf_path = os.path.join(tmpdir, "doc.pdf")
        # Write the randomized tex to a file
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(randomized_tex_content)
        # Run pdflatex
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
            check=True
        )
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
    
    buf = io.BytesIO(pdf_bytes)
    buf.seek(0)

    return send_file(
        buf,
        download_name="randomized_output.pdf",
        as_attachment=False,
        mimetype="application/pdf"
    )











if __name__ == '__main__':
    ## db.create_all()
    if 'liveconsole' not in gethostname():
        app.run()