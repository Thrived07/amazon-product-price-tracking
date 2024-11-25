import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import re
from datetime import datetime, timedelta

user_email = ""
tracking_status = {}  # Track status and start time

def get_price(url):
    """Retrieve the current price of a product from Amazon"""
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Cache-Control': 'max-age=0'
        })
        soup = BeautifulSoup(response.content, 'html.parser')
        price_element = soup.select_one('.a-price-whole')  # Adjust if necessary
        if price_element:
            price_text = price_element.text.strip()
            price_number = re.findall(r'[\d,]+', price_text)
            if price_number:
                return float(price_number[0].replace(',', ''))
        return None
    except Exception as e:
        print(f"Error retrieving price: {e}")
        return None

def send_email(subject, body):
    """Send an email notification to the user"""
    gmail_user = 'nani3ved@gmail.com'
    gmail_password = 'ovsr fifd fpjw ievg'  # Use app-specific password if 2FA is enabled
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = user_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, user_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def track_price(url, target_price, max_time_minutes):
    """Track the price until it drops below the target price or max time is reached"""
    global tracking_status
    start_time = datetime.now()
    max_time = timedelta(minutes=max_time_minutes)
    tracking_status[url] = {"start_time": start_time, "message": "Tracking started", "max_time": max_time}

    while True:
        current_time = datetime.now()
        elapsed_time = current_time - start_time
        if elapsed_time >= max_time:
            tracking_status[url]["message"] = f"Tracking time limit reached. ({max_time_minutes} minutes passed). No price drop."
            send_email("Tracking Time Limit Reached", f"The tracking time limit of {max_time_minutes} minutes has passed without a price drop. The product was not on sale.")
            break

        current_price = get_price(url)
        if current_price is not None:
            # Calculate elapsed time in minutes and seconds
            elapsed_minutes = int(elapsed_time.total_seconds() / 60)
            elapsed_seconds = int(elapsed_time.total_seconds() % 60)

            if current_price <= target_price:
                subject = "Product Price Dropped!"
                body = f"The price dropped to ₹{current_price}!\nCheck the product here: {url}"
                send_email(subject, body)
                tracking_status[url]["message"] = f"Price dropped to ₹{current_price}. Email sent to {user_email}."
                break
            else:
                tracking_status[url]["message"] = f"Tracking for {elapsed_minutes}m {elapsed_seconds}s - Current price: ₹{current_price}. Waiting for a drop."
                print(tracking_status[url]["message"])
        else:
            tracking_status[url]["message"] = f"Could not retrieve price. Retrying in 60 seconds."

        time.sleep(60)  # Check every 60 seconds

# Example usage
url = "https://www.amazon.in/dp/B07WMS7TWB?ref_=cm_sw_r_cp_ud_dp_X934R26YTFMGE5W66PM9_1"
target_price = 1000.0
max_time_minutes = 60
user_email = "ethrivedgoud@gmail.com"

track_price(url, target_price, max_time_minutes)
