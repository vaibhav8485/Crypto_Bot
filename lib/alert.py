# STD Modules
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SENDER = os.environ.get('SENDER_MAIL')
PASSWORD = os.environ.get('SENDER_PASS')
RECEIVER = os.environ.get('RECEIVER_MAIL')

# Validate environment variables
if not SENDER or not PASSWORD or not RECEIVER:
    raise ValueError("Please set the environment variables for email configuration.")

# Main Function
def send_email(subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to gmail's SMTP server using SSL
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER, PASSWORD)
        
        # Send the email
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        
        # Close the connection
        server.quit()
        print('Gmail send.')

    except Exception as e:
        error_message = f'Failed to send email. Error: {str(e)}'
        print(error_message)
        
        # Optionally, send an email to the sender about the error
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, SENDER, f"Subject: Gmail Sending Failed\n\n{error_message}")
            server.quit()
        except Exception as inner_e:
            print(f'Failed to notify sender about the gmail error. Error: {str(inner_e)}')

# Order Notification Function
def send_order_alert(response):
    message = f"*Message : {response}"
    send_email('Crypto Order Placed', message)

# Alert Notification Function
def send_notification_alert(action, coin, price, signal_1d, signal_1w, signal_1m, d_momentum_buy, d_trend_buy, d_volatility_buy, d_volume_buy, d_momentum_sell, d_trend_sell, d_volatility_sell, d_volume_sell, w_momentum_buy, w_momentum_sell, w_trend_buy, w_trend_sell, w_volatility_buy, w_volatility_sell, w_volume_buy, w_volume_sell, m_momentum_buy, m_momentum_sell, m_trend_buy, m_trend_sell, m_volatility_buy, m_volatility_sell, m_volume_buy, m_volume_sell, error):
    if action == 'Buy':
        message = f"""
        Order Action: {action}
        Coin Name: {coin}
        Current Price: {price}

        
        [DETAILS]
        Daily Signal: {signal_1d}
        Weekly Signal: {signal_1w}
        Monthly Signal: {signal_1m}

        [Daily]
        Momentum: {d_momentum_buy}/11
        Trend: {d_trend_buy}/6
        Volatility: {d_volatility_buy}/8
        Volume: {d_volume_buy}/6

        [Weekly]
        Momentum: {w_momentum_buy}/11
        Trend: {w_trend_buy}/6
        Volatility: {w_volatility_buy}/8
        Volume: {w_volume_buy}/6

        [Monthly]
        Momentum: {m_momentum_buy}/11
        Trend: {m_trend_buy}/6
        Volatility: {m_volatility_buy}/8
        Volume: {m_volume_buy}/6

        *MESSAGE: [{error}]     
        """
    else:
        message = f"""
        Order Action: {action}
        Coin Name: {coin}
        Current Price: {price}

        
        [DETAILS]
        Daily Signal: {signal_1d}
        Weekly Signal: {signal_1w}
        Monthly Signal: {signal_1m}

        [Daily]
        Momentum: {d_momentum_sell}/11
        Trend: {d_trend_sell}/6
        Volatility: {d_volatility_sell}/8
        Volume: {d_volume_sell}/6

        [Weekly]
        Momentum: {w_momentum_sell}/11
        Trend: {w_trend_sell}/6
        Volatility: {w_volatility_sell}/8
        Volume: {w_volume_sell}/6

        [Monthly]
        Momentum: {m_momentum_sell}/11
        Trend: {m_trend_sell}/6
        Volatility: {m_volatility_sell}/8
        Volume: {m_volume_sell}/6
        
        *MESSAGE: [{error}]  
        """
    send_email('Crypto Alert', message)
