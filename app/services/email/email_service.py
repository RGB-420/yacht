import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

def send_feedback_email(feedback: dict):
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "73raul7373@gmail.com",
            "subject": f"""[FEEDBACK] {feedback.get('type')} - {feedback.get('entity_type')}""",
            "html": f"""
                <div style="font-family: Arial, sans-serif; background-color: #f4f4f5; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">

                        <h2 style="margin-bottom: 10px;">New Feedback Received</h2>

                        <p style="color: #555; margin-bottom: 20px;">
                            A user has reported an issue in your app.
                        </p>

                        <div style="margin-bottom: 10px;">
                            <strong>ID:</strong> {feedback.get("id")}
                        </div>

                        <div style="margin-bottom: 10px;">
                            <strong>Entity:</strong> {feedback.get("entity_type")}
                        </div>

                        <div style="margin-bottom: 10px;">
                            <strong>Type:</strong> 
                            <span style="color: #ef4444; font-weight: bold;">
                                {feedback.get("type")}
                            </span>
                        </div>

                        <div style="margin-bottom: 20px;">
                            <strong>Message:</strong>
                            <div style="background: #f9fafb; padding: 10px; border-radius: 6px; margin-top: 5px;">
                                {feedback.get("message") or "No message provided"}
                            </div>
                        </div>

                        <div style="margin-bottom: 20px;">
                            <strong>Page:</strong><br/>
                            <a href="{feedback.get("page")}" style="color: #2563eb;">
                                {feedback.get("page")}
                            </a>
                        </div>

                        <hr style="margin: 20px 0;" />

                        <p style="font-size: 12px; color: #888;">
                            This email was generated automatically from your feedback system.
                        </p>

                    </div>
                </div>
            """
        })
    
    except Exception as e:
        print("Email failed:", e)