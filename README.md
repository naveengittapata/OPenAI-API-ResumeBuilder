# My Resume.chat — AI-Powered Resume Builder

An intelligent resume builder web application that uses AI to generate professional, tailored resumes in Microsoft Word (.docx) format. Simply provide your job description, experience details, and client history — the AI handles the rest.

## Features

### Resume Generation
- **AI-Powered Content** — Uses Groq AI (LLaMA 3.1) to generate professional summaries, responsibilities, and skills
- **Smart Formatting** — Generates a polished Word document with proper sections, bullet points, and tables
- **Client Experience Sorting** — Automatically sorts work experience by most recent first
- **Categorized Skills Table** — Skills & tools are grouped by category (Languages, Databases, Cloud, etc.)
- **Experience-Scaled Content** — Responsibilities and summary depth adjust based on years of experience

### Authentication System
- **User Registration** — Sign up with first name, last name, email, phone, and password
- **Email OTP Verification** — 6-digit verification code sent to the user's real email via Gmail SMTP
- **Secure Login** — Password hashing with bcrypt, session management with Flask-Login
- **Remember Me** — Stay logged in for 30 days
- **Protected Routes** — Resume builder is accessible only to authenticated users
- **Social Login Buttons** — UI-ready for Google, Facebook, Apple OAuth (backend integration pending)

### UI/UX
- **Modern Design** — Gradient backgrounds, card layouts, smooth animations
- **Progress Overlay** — Animated progress bar during resume generation
- **Responsive** — Works on desktop and mobile
- **Pre-filled Forms** — User details auto-populate from their account

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask, Blueprints |
| **AI** | Groq API (LLaMA 3.1 8B Instant) |
| **Database** | SQLite with SQLAlchemy ORM |
| **Auth** | Flask-Login, Flask-Bcrypt |
| **Email** | Gmail SMTP (smtplib) |
| **Document Generation** | python-docx |
| **Frontend** | HTML, CSS, JavaScript |

## Project Structure

```
├── app/
│   ├── __init__.py          # App factory, extensions setup, blueprint registration
│   ├── main.py              # Resume builder route (protected)
│   ├── auth.py              # Authentication routes (signup, login, verify, logout)
│   ├── models.py            # User database model
│   ├── email_service.py     # Gmail SMTP email sending for OTP
│   └── utils.py             # AI generation functions & Word document creation
├── templates/
│   ├── index.html           # Resume builder form (main app)
│   ├── landing.html         # Landing page for visitors
│   ├── signup.html          # User registration page
│   ├── login.html           # Login page with remember me
│   └── verify.html          # OTP verification page
├── static/
│   └── style.css            # Additional styles
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
└── .gitignore
```

## Setup & Installation

### Prerequisites
- Python 3.10+
- A Groq API key ([get one free](https://console.groq.com))
- A Gmail account with an App Password for sending OTP emails

### 1. Clone the repository
```bash
git clone https://github.com/naveengittapata/OPenAI-API-ResumeBuilder.git
cd OPenAI-API-ResumeBuilder
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
```env
GROQ_API_KEY=your_groq_api_key_here

# Gmail SMTP (for sending OTP verification emails)
SMTP_EMAIL=your_gmail@gmail.com
SMTP_APP_PASSWORD=your_16_char_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

> **Getting a Gmail App Password:**
> 1. Enable [2-Step Verification](https://myaccount.google.com/signinoptions/two-step-verification) on your Google account
> 2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
> 3. Create a new App Password and copy the 16-character code (no spaces)

### 4. Run the application
```bash
python run.py
```

The app will be available at **http://localhost:5000**

## How It Works

1. **Visit the app** — You'll see the landing page
2. **Sign up** — Enter your details and create an account
3. **Verify email** — Enter the 6-digit OTP sent to your email
4. **Build your resume** — Fill in job description, education, client experiences
5. **Download** — AI generates content and you download a professional Word document

## API Keys & Security

- All sensitive keys are stored in `.env` (excluded from Git)
- Passwords are hashed with bcrypt (never stored in plain text)
- OTP codes expire after 10 minutes
- Sessions are managed securely with Flask-Login

## License

MIT License