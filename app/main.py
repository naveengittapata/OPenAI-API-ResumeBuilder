from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from app.utils import generate_resume, save_resume_as_docx_in_memory

main = Blueprint('main', __name__)

@main.route("/builder", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        # Get form input
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        user_input = request.form["user_input"]
        education_details = request.form["education_details"]
        years_of_experience = request.form["years_of_experience"]
        client_names = request.form.getlist("client_name[]")
        start_dates = request.form.getlist("start_date[]")
        end_dates = request.form.getlist("end_date[]")

        user_details = {
            'name': f"{first_name} {last_name}",
            'email': email,
            'phone': phone
        }

        # Generate resume using utils function
        resume_content = generate_resume(user_input, client_names, start_dates, end_dates, education_details, years_of_experience, user_details)

        # Save resume as Word document in memory
        file_stream = save_resume_as_docx_in_memory(resume_content)

        # Send the generated document as a downloadable file
        return send_file(file_stream, as_attachment=True, download_name="creative_resume.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    return render_template("index.html", user=current_user)

