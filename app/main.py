from flask import Flask, render_template, request, send_file
import os
import openai
from io import BytesIO
from docx import Document
from utils import generate_resume, save_resume_as_docx_in_memory

app = Flask(__name__)

# Load your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get form input
        user_input = request.form["user_input"]
        education_details = request.form["education_details"]
        client_names = request.form.getlist("client_name[]")
        start_dates = request.form.getlist("start_date[]")
        end_dates = request.form.getlist("end_date[]")

        # Generate resume using utils function
        resume_content = generate_resume(user_input, client_names, start_dates, end_dates, education_details)

        # Save resume as Word document in memory
        file_stream = save_resume_as_docx_in_memory(resume_content)

        # Send the generated document as a downloadable file
        return send_file(file_stream, as_attachment=True, download_name="creative_resume.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
