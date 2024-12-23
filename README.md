# PiMediaServer
This uses FastAPI and Nodejs to host a web application. The raspberry pi camera is being captured and streamed.

Email Script sends an email every hour of system info.


Start Pi Webcam:


Start FastAPI

1. CD to camera-app
2. Start virtual env - source venv/bin/activate
3. start fastAPI dev server - fastapi dev --host 0.0.0.0 main.py

Start Nodejs

1. cd my-app
2. npm run dev


visit [r[aspi.](https://raspi.jonahtech.org/)](https://raspi.jonahtech.org/)
This is hosted by cloudflare with a secure HTTPS connection


Manaully run email script to view specs
1. run /home/jimp/system_email/email_script  (Change email to your own to get emails sent.)
