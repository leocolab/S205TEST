from flask import Flask, request, jsonify, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
app = Flask(__name__)

codeDict = {}
lastSignedOut = {}
laptopDict = {}
laptopList = ['TAB_Laptop_1', 'TAB_Laptop_2', 'TAB_Laptop_3', 'TAB_Laptop_4', 'TAB_Laptop_5', 'TAB_Laptop_6', 'TAB_Laptop_7', 'TAB_Laptop_8', 'TAB_Laptop_9', 'TAB_Laptop_10', 'TAB_Laptop_11', 'TAB_Laptop_12', 'TAB_Laptop_13', 'TAB_Laptop_14', 'TAB_Laptop_15', 'TAB_Laptop_16', 'TAB_Laptop_17', 'TAB_Laptop_18', 'TAB_Laptop_19', 'TAB_Laptop_20', 'TAB_Laptop_21', 'TAB_Laptop_22', 'TAB_Laptop_23', 'TAB_Laptop_24', 'TAB_Laptop_25', 'TAB_Laptop_26', 'TAB_Laptop_27', 'TAB_Laptop_28', 'TAB_Laptop_29', 'TAB_Laptop_30']

@app.route('/login',methods = ['POST', 'GET'])
def login():

   if request.method == 'POST':
      user = request.form['nm']      
   else:
      user = request.args.get('nm')

   if "@hdsb.ca" in user:
      S = 4
      codeList = random.choices(string.digits, k=S)
      code = ''.join(codeList)
      email = 's205laptops@gmail.com'
      password = 'ehtiuvauwgfftsht'
      send_to_email = str(user)
      subject = 'TAB Laptops Verification Code' # The subject line
      message = "Your Verrification Code is " + str(code)

      msg = MIMEMultipart()
      msg['From'] = email
      msg['To'] = send_to_email
      msg['Subject'] = subject

       # Attach the message to the MIMEMultipart object
      msg.attach(MIMEText(message, 'plain'))

      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(email, password)
      text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
      server.sendmail(email, send_to_email, text)
      server.quit()
      codeDict.update({user : code})
      return "Check your email for your verification code. Then return to the previous page to Login. MAKE SURE TO CHECK YOUR SPAM FOLDER IF IT IS NOT IN YOUR MAIN INBOX."
   
   else:
      return "Please use a valid HDSB email"


@app.route("/signOut", methods = ['POST', 'GET'])
def signOut():
   if request.method == 'POST':
      QR = request.form['QR']
      email2 = request.form['email']
      veri = request.form['code']
   else:
      QR = request.args.get('QRoutput')
      email2 = request.args.get('email')
      veri = request.args.get('form')
   
   if email2 in codeDict and codeDict[email2] == veri and QR in laptopList:
      if laptopDict == {}:
         laptopDict.update({email2 : QR})
         lastSignedOut.update({email2: QR}) 
      else:
         if QR in laptopDict.values():
            previousUser = list(laptopDict.keys())[list(laptopDict.values()).index(QR)]
            laptopDict.pop(previousUser)
            lastSignedOut.pop(previousUser)
            laptopDict.update({email2 : QR})
            lastSignedOut.update({email2: QR})
         else:
            laptopDict.update({email2 : QR})
            lastSignedOut.update({email2: QR})  
      return "Laptop Sign Out Success!"
   else:
      return "Error! Email, QR Code, or Verification Code does not match."

@app.route('/return', methods = ['POST', 'GET'])
def Return():
   if request.method == 'POST':
      email3 = request.form['email']
      veri2 = request.form['code']
   else:
      email3 = request.args.get('email')
      veri2 = request.args.get('code')
   if email3 in codeDict and codeDict[email3] == veri2:
      laptopDict.pop(email3)
      return "Laptop Returned"
   else:
      return "Email or code does not match out records"


@app.route('/admin', methods = ['POST', 'GET'])
def admin():
   AdminCode = '1243'
   if request.method == 'POST':
      adminCodeInput = request.form['code']
   else:
      adminCodeInput = request.args.get['code']
   if adminCodeInput == AdminCode:
      if laptopDict == {}:
         return "No one has signed out a laptop."
      else:
         string = ""
         string2 = ""
         for user in lastSignedOut:
            laptop = lastSignedOut[user]
            string = string + "<br>" + user + " signed out: " + laptop
         for user2 in laptopDict:
            laptop2 = laptopDict[user2]
            string2 = string2 + "<br>" + user2 + " signed out: " + laptop2
         tables = "Users who were the last to sign out each computer: " + "<br>" + string + "<br>" + "" + "<br>" + "Users who currently have laptops signed out: " + "<br>" + string2
         return tables


      #return "Current Laptops Signed Out: " + str(laptopDict) +" "+ "Most Recent User of Each Laptop: " + str(lastSignedOut)
   else:
      return "The code you inputed was incorrect"



if __name__ == "__main__":
	app.run(debug=True)
