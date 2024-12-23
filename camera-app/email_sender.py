import os
import socket
import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import time

# Initialize FastAPI
app = FastAPI()

# SMTP Settings (replace with your email provider)
SMTP_SERVER = "smtp.gmail.com"  # Example: Gmail SMTP
SMTP_PORT = 587  # Common port for SMTP
SENDER_EMAIL = "pottejae@gmail.com"
SENDER_PASSWORD = "Cyclonestate2"  # Use an app-specific password if 2FA is enabled
RECIPIENT_EMAIL = "pottejae@gmail.com"

# Get system details (Memory, CPU)
def get_system_info():
    # Memory info
    memory = psutil.virtual_memory()
    memory_usage = {
        "total": memory.total / (1024 ** 3),  # in GB
        "used": memory.used / (1024 ** 3),    # in GB
        "free": memory.free / (1024 ** 3),    # in GB
    }
    
    # CPU info
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage in percentage
    cpu_temp = None  # Can be retrieved for specific devices like Raspberry Pi
    
    try:
        if os.name == 'posix':  # Assuming you're on a Unix-like system (e.g., Raspberry Pi)
            cpu_temp = psutil.sensors_temperatures().get('cpu_thermal', [{}])[0].get('current')
    except Exception as e:
        cpu_temp = "N/A"

    # Get hostname
    hostname = socket.gethostname()

    # Return system stats
    return {
        "hostname": hostname,
        "cpu_usage": cpu_usage,
        "cpu_temp": cpu_temp,
        "memory": memory_usage
    }

# Function to send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Setup the SMTP server and send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

# Function to get system stats and send email periodically
def send_system_stats():
    system_info = get_system_info()
    subject = "Raspberry Pi System Stats"
    body = f"""
    Hostname: {system_info['hostname']}
    CPU Usage: {system_info['cpu_usage']}%
    CPU Temperature: {system_info['cpu_temp']}°C
    Memory Usage: {system_info['memory']['used']:.2f} GB / {system_info['memory']['total']:.2f} GB
    """

    send_email(subject, body)

# Setup APScheduler to call the send_system_stats function periodically
scheduler = BackgroundScheduler()
scheduler.add_job(send_system_stats, 'interval', hours=1)  # Send every hour
scheduler.start()

# Route to manually trigger email (for testing)
@app.get("/send_stats")
def trigger_email():
    send_system_stats()
    return {"message": "System stats email sent."}

# Example route for your camera feed (This can be another existing route in your `main.py`)
@app.get("/camera_feed")
def get_camera_feed():
    # Your existing camera streaming logic here (e.g., MJPEG stream)
    return {"message": "Camera feed route"}

# Run server (if this script is run directly)
if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
