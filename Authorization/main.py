from config import *

app = Flask(__name__)


@app.route('/check', methods=['POST'])
def check():
    if request.method == 'POST':
        print(request)
        print(request.values)
        data = request.values.get("email")
        print(data)
        logging.basicConfig(filename="file.log",
                            level=logging.INFO,
                            format='%(levelname)s   %(asctime)s   %(message)s')
        logging.info("All setting of the logging is done")

        try:
            # open the JSON file for reading
            domains = []
            with open('domains.json', 'r') as f:
                # load the contents of the file as a JSON object
                domain_data = json.load(f)
                for i in domain_data:
                    domains.append(list(i.values())[0])
        except Exception as ex:
            logging.error("There is an error {} in reading json file".format(ex))

        # Read the confing file
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            sender = config.get('config', 'sender')
            password = config.get('config', 'password')
            subject = config.get('config', 'subject')
            logging.info("All paths are defined")
        except Exception as ex:
            logging.error("There is an error {} in reading config.ini file".format(ex))

        email = check_email(data, domains)

        if email is not None:
            six_digit_number = random.randint(100000, 999999)
            body = str(six_digit_number)
            logging.info("The authorization code is ".format(body))

            # create message object
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = email
            message['Subject'] = subject
            body = '<h1 style="color: red; font-family: Arial, sans-serif;">{}</h1><p style="font-size: 14px;"></p>'.format(
                body)
            message.attach(MIMEText(body, 'html'))
            # create SMTP session
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            # login to the email account
            session.login(sender, password)
            # send the email
            text = message.as_string()
            session.sendmail(sender, email, text)
            # close the SMTP session
            session.quit()

            result = {
                "email": data,
                "code": six_digit_number,
            }
            return result

        else:
            return "error"


if __name__ == '__main__':
    app.run(debug=True)

    # if check_email(domains) is not None:

    # Generate a random six-digit number
    # six_digit_number = random.randint(100000, 999999)
    # body = str(six_digit_number)
    #
    # # create message object
    # message = MIMEMultipart()
    # message['From'] = sender
    # message['To'] = email
    # message['Subject'] = subject
    # body = '<h1 style="color: red; font-family: Arial, sans-serif;">{}</h1><p style="font-size: 14px;"></p>'.format(body)
    # message.attach(MIMEText(body, 'html'))
    #
    # # create SMTP session
    # session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.starttls()
    # # login to the email account
    # session.login(sender, password)
    # # send the email
    # text = message.as_string()
    # session.sendmail(sender, email, text)
    # # close the SMTP session
    # session.quit()

#
#
# if __name__ == "__main__":
#     app.run(debug=True)
