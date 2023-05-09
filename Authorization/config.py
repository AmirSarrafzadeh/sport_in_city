import json
import random
import smtplib
import logging
import configparser
from flask import Flask, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def check_email(email, domains):
    try:
        while True:
            if email.find("@") != -1:
                domain = email.split("@")[1]
                if domain in domains:
                    return email
                    break
                else:
                    print("Please give an institutional email located in Rome")
            else:
                print("please provide a valid email address")
    except Exception as ex:
        print("There is an error {} in getting email".format(ex))
