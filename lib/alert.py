import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SENDER = os.environ.get('SENDER_MAIL')
PASSWORD = os.environ.get('SENDER_PASS')
RECEIVER = os.environ.get('RECEIVER_MAIL')

def send_email(subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER, PASSWORD)
        
        # Send the email
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        
        # Close the connection
        server.quit()
        print('Email send successfully.')

    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')


def send_order_alert(action, coin, price, quantity, balance):
    message = f"""        
    Details:
    - Order : {action}
    - Asset : {coin}
    - Price : {price} INR
    - Quantity : {quantity}
    - Investment : {balance} INR
    """
    send_email('Order placed', message)

def send_alert(message):
    send_email('Error occurred!', message)

def send_action_alert(action, coin, price, signal_1d, signal_1w, s1, s2, s3, s4, h1_1d, h2_1d, h1_1w, h2_1w):
    if action == 'Buy':
        message = f"""
        Crypto Bot :
        - Order Action : {action}
        - Coin Name : {coin}
        - Current Price : {price}

        Details :
        - Daily Chart Signal : {signal_1d}
                 - All Indicators : [ Buy: {s1}, Hold: {h1_1d} ] / 44
                 - Imp Indicators : [ Buy: {s2}, Hold: {h2_1d} ] / 21
        - Weekly Chart Signal : {signal_1w}
                 - All Indicators : [ Buy: {s3}, Hold: {h1_1w}] / 44
                 - Imp Indicators : [ Buy: {s4}, Hold: {h2_1w}] / 21
        """
    else:
        message = f"""
        Crypto Bot :
        - Order Action : {action}
        - Coin Name : {coin}
        - Current Price : {price}

        Details :
         - Daily Chart Signal : {signal_1d}, 
                 - All Indicators : [ Sell: {s1}, Hold: {h1_1d} ] / 44
                 - Imp Indicators : [ Sell: {s2}, Hold: {h2_1d} ] / 21
        - Weekly Chart Signal : {signal_1w},
<<<<<<< HEAD
                 - All Indicators : [ Sell: {s3}, Hold: {h1_1w} ] 
                 - Imp Indicators : [ Sell: {s4}, Hold: {h2_1w} ]
        """      
    send_email('Alert!', message)
=======
                 - All Indicators : [ Sell: {s3}, Hold: {h1_1w} ] / 44
                 - Imp Indicators : [ Sell: {s4}, Hold: {h2_1w} ] / 21
        """


    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = f'{coin} {action} Alert'

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER, PASSWORD)
        
        # Send the email
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        
        # Close the connection
        server.quit()
        print(f'{coin} {action} Alert Send Successfully.')

    except Exception as e:
        print(f'Failed to send Alert. Error: {str(e)}')
>>>>>>> 5cfedbc6129d5679a86870905b0250f649dc8dfa
