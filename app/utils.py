import openai

def generate_summary(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Generate a summary for the following job description:\n{user_input}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_skills_and_tools(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"List the skills and tools associated with the following job description:\n{user_input}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_professional_experience(client_names, start_dates, end_dates, user_input):
    professional_experience = ""
    for i in range(len(client_names)):
        responsibilities = generate_responsibilities(user_input)
        professional_experience += f"Client: {client_names[i]}\nStart Date: {start_dates[i]}\nEnd Date: {end_dates[i]}\nResponsibilities:\n{responsibilities}\n\n"
    return professional_experience

def generate_responsibilities(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Generate responsibilities for the following job description:\n{user_input}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_resume(user_input, client_names, start_dates, end_dates, education_details):
    summary = generate_summary(user_input)
    skills_tools = generate_skills_and_tools(user_input)
    professional_experience = generate_professional_experience(client_names, start_dates, end_dates, user_input)
    education = f"Education: {education_details}"

    resume_content = {
        'summary': summary,
        'skills_tools': skills_tools,
        'professional_experience': professional_experience,
        'education': education
    }

    return resume_content
