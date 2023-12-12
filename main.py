from random import *
from flask import *
from flask_session import Session
from flask_mail import Mail, Message
import secrets
import string
import onetimepad

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'AltwayawiN@gmail.com'
app.config['MAIL_PASSWORD'] ='fgat tstm rplp lnos'
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/home', methods=['GET', 'POST'])

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

def otp():
    characters = string.digits + string.ascii_uppercase
    otp = ""
    for i in range(6):
        otp += secrets.choice(characters)
    return otp

@app.route('/send_email', methods=['POST'])
def send_email():
    
    text_email = request.form['text_email']
    
    OTP1 = otp()
    session['passOTP'] = OTP1

    msg = Message(subject="Hello from Nada", sender='noreply@demo.com', recipients=[text_email])
    msg.body = "Your OTP Number is: " + OTP1
    mail.send(msg)
    return render_template('verify.html')

@app.route('/validate',methods=["POST"])   
def validate():

    user_otp = request.form['otp_Enter'] 
    OTP2 = session.get('passOTP')

    if OTP2 == user_otp:  
        return render_template('OTPencryption.html')
    else:
        return render_template('index.html')
    
def generate_key(message):
    random_string = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(message))
    return random_string

@app.route('/optencryption', methods=['GET', 'POST'])
def OTPecnryption():
    message = request.form['message']
    key = generate_key(len(message))
    cipher = onetimepad.encrypt(message, key)
    msg = onetimepad.decrypt(cipher, key)
    return render_template('OTPencryption.html', cipher=cipher, OTPKEY= key, MESS=message)
    
if __name__ == '__main__':
    app.run(debug=True)
