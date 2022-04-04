from flask import Flask, request, jsonify, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!!!"
