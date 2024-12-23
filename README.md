PiMediaServer
This uses FastAPI and Nodejs to host a web application. The raspberry pi camera is being captured and streamed.

Email Script sends an email every hour of system info.

Start Pi Webcam:

Start FastAPI

CD to camera-app
Start virtual env - source venv/bin/activate
start fastAPI dev server - fastapi dev --host 0.0.0.0 main.py
Start Nodejs

cd my-app
npm run dev
visit [raspi.](https://raspi.jonahtech.org/) This is hosted by cloudflare with a secure HTTPS connection

Manaully run email script to view specs

run /home/jimp/system_email/email_script (Change email to your own to get emails sent.)
