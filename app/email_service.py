import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(to_email, otp_code, first_name=""):
    smtp_email = os.getenv('SMTP_EMAIL')
    smtp_password = os.getenv('SMTP_APP_PASSWORD')
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))

    if not smtp_email or not smtp_password:
        print(f"\n[WARNING] SMTP not configured. OTP for {to_email}: {otp_code}\n")
        return False

    msg = MIMEMultipart('alternative')
    msg['From'] = f"My Resume.chat <{smtp_email}>"
    msg['To'] = to_email
    msg['Subject'] = f"Your verification code: {otp_code}"

    greeting = f"Hi {first_name}," if first_name else "Hi,"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 40px 30px; background: #0f172a; border-radius: 16px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <span style="font-size: 28px; font-weight: 800; color: #ffffff;">My Resume</span><span style="font-size: 28px; font-weight: 800; color: #a78bfa;">.chat</span>
        </div>
        <div style="background: #1e293b; border-radius: 14px; padding: 32px; text-align: center;">
            <p style="color: #d0cbe5; font-size: 15px; margin: 0 0 8px 0;">{greeting}</p>
            <p style="color: #9a97b0; font-size: 14px; margin: 0 0 24px 0;">Use the code below to verify your account:</p>
            <div style="background: rgba(167, 139, 250, 0.08); border: 1px solid rgba(167, 139, 250, 0.2); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
                <span style="font-size: 32px; font-weight: 800; color: #a78bfa; letter-spacing: 8px;">{otp_code}</span>
            </div>
            <p style="color: #7a7494; font-size: 12px; margin: 0;">This code expires in 10 minutes. If you didn't request this, please ignore this email.</p>
        </div>
        <p style="text-align: center; color: #5a5672; font-size: 11px; margin-top: 24px;">My Resume.chat — Powered by AI</p>
    </div>
    """

    text_body = f"{greeting}\n\nYour verification code is: {otp_code}\n\nThis code expires in 10 minutes.\n\nMy Resume.chat"

    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())
        server.quit()
        print(f"\n[EMAIL] Verification code sent to {to_email}\n")
        return True
    except Exception as e:
        print(f"\n[EMAIL ERROR] Failed to send email to {to_email}: {e}\n")
        return False
