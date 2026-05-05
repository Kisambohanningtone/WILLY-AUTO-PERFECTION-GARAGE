from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)   # templates/ and static/ are auto-discovered
app.secret_key = "willy_auto_perfection_2026"

SENDER_EMAIL = "kisamboningtone41@gmail.com"
SENDER_PASS  = "eppe rker xzsl ycou"   # Gmail App Password
GARAGE_EMAIL = "kisamboningtone41@gmail.com"

# ── Page routes ────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ── Email helper ───────────────────────────────────────────────────────────────

def send_email(subject, body_text, to_address):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = to_address
    msg.attach(MIMEText(body_text, "plain"))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.sendmail(SENDER_EMAIL, to_address, msg.as_string())
        return True, ""
    except Exception as e:
        return False, str(e)

# ── Booking form  POST /submit-booking ────────────────────────────────────────

@app.route("/submit-booking", methods=["POST"])
def submit_booking():
    name         = request.form.get("name", "").strip()
    phone        = request.form.get("phone", "").strip()
    service      = request.form.get("service", "").strip()
    date         = request.form.get("date", "").strip()
    time         = request.form.get("time", "").strip()
    client_email = request.form.get("email", "").strip()

    if not all([name, phone, service, date, time, client_email]):
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for("service") + "#booking")

    # Notify garage
    send_email(
        f"New Booking: {service}",
        f"New Booking Received:\n\nName: {name}\nPhone: {phone}\nEmail: {client_email}\nService: {service}\nDate: {date}\nTime: {time}",
        GARAGE_EMAIL
    )

    # Confirm to client
    ok, err = send_email(
        "Booking Confirmation – Willy Auto Perfection Garage",
        f"Dear {name},\n\nThank you for booking with Willy Auto Perfection Garage.\n\nService : {service}\nDate    : {date}\nTime    : {time}\n\nOur team will contact you shortly to confirm details.\n\nRegards,\nWilly Auto Perfection Garage\nTel: 0782 817 395 | 0710 817 390",
        client_email
    )

    if ok:
        flash("Booking submitted! A confirmation email has been sent to you.", "success")
    else:
        flash(f"Booking received, but confirmation email failed: {err}", "warning")

    return redirect(url_for("service") + "#booking")

# ── Contact form  POST /submit-contact ────────────────────────────────────────

@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    name         = request.form.get("name", "").strip()
    phone        = request.form.get("phone", "").strip()
    client_email = request.form.get("email", "").strip()
    service      = request.form.get("service", "").strip()
    message      = request.form.get("message", "").strip()

    if not all([name, client_email, message]):
        flash("Please fill in your name, email, and message.", "danger")
        return redirect(url_for("contact"))

    send_email(
        f"New Message from {name}",
        f"Name: {name}\nPhone: {phone}\nEmail: {client_email}\nService: {service}\n\nMessage:\n{message}",
        GARAGE_EMAIL
    )
    send_email(
        "We received your message – Willy Auto Perfection Garage",
        f"Dear {name},\n\nThank you for reaching out. We'll reply within 24 hours.\n\nYour message:\n\"{message}\"\n\nRegards,\nWilly Auto Perfection Garage\nTel: 0782 817 395 | 0710 817 390",
        client_email
    )

    flash("Your message has been sent! We'll get back to you shortly.", "success")
    return redirect(url_for("contact"))

# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
