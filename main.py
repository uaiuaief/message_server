import os
import smtplib
from flask import Flask, jsonify, request, Response

app = Flask(__name__)


def send_email(name, email, message):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        sender = os.environ.get('SENDER_EMAIL')
        password = os.environ.get('EMAIL_PASSWORD')
        receiver = sender 

        smtp.login(sender, password)

        subject = f'Nome: {name} - Email: {email}'
        body = message

        msg = f'subject: {subject}\n\n{body}'

        smtp.sendmail(sender, receiver, msg) 


@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    body = request.form.get("body")

    try:
        send_email(name, email, body)
        return Response(status=204)
    except Exception as e:
        print(e)
        return Response(status=500)
        



@app.after_request
def add_cors_headers(response):
    white = [
            'http://localhost:3000',
            'localhost:3000',
            '127.0.0.1:3000',
            'http://127.0.0.1:3000',
            ]

    if not request.referrer:
        return response

    r = request.referrer[:-1]
    if r in white:
        response.headers.add('Access-Control-Allow-Origin', r)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response



if __name__ == '__main__':
    app.run(debug=False, port='5001', host='0.0.0.0')
    #app.run(debug=True)



