import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

def send_feedback_email(feedback: dict):
    try:
        resend.Emails.send({
            "from": "onboarding@resned.dev",
            "to": "73raul7373@gmail.com",
            "subject": "New feedback received",
            "html": f"""
                <h3>New feedback</h3>
                <p><strong>Entity:>/strong> {feedback.get("entity_type")}</p>
                <p><strong>Type:</strong> {feedback.get("type")}</p>
                <p><strong>Message:</strong> {feedback.get("message")}</p>
                <p><strong>Page:</strong> {feedback.get("page")}</p>                
            """
        })
    
    except Exception as e:
        print("Email failed:", e)