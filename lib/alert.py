# STD Modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
EMAIL_ADDRESS = 'cryptobot8485@gmail.com' # Sender
PASSWORD = 'otwx mqmy tuip ffly' # Sender's Password
RECIPIENT = 'vaibhavumbarkar8485@gmail.com' # Receiver

def send_alert(action, coin_name, current_price, m1, m2, r1, r2, p1, p2, s1, s2):
    message = f"""
    Crypto Bot :

    - Action : {action}
    - Coin Name : {coin_name}
    - Price : {current_price}
    

    Advance Information :

    - MACD Signal : {m1}
    - MACD Value (+/-) : {m2}

    - RSI Signal : {r1}
    - RSI Value (60/30) : {r2}

    - Price Percentage Oscillator : {p1}
    - Price Percentage Oscillator (+/-) : {p2}

    - Stochastic Oscillator : {s1}
    - Stochastic Oscillator (80/20) : {s2}

    (NOTE : Timeframe: 1w for above information)

    """

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT
    msg['Subject'] = 'Crypto Alert!'

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_ADDRESS, PASSWORD)
        
        # Send the email
        server.sendmail(EMAIL_ADDRESS, RECIPIENT, msg.as_string())
        
        # Close the connection
        server.quit()
        print(f'Crypto Bot: {action} Alert Send Successfully.')
    except Exception as e:
        print(f'Failed to send Alert. Error: {str(e)}')
