# amazon-product-price-tracking
Amazon Price Tracker
Amazon Price Tracker is a Python script to monitor product prices on Amazon and send email notifications when the price drops below a specified target. It uses the requests library to scrape the website, BeautifulSoup for parsing HTML, and smtplib for sending email alerts.

Features
Automatically tracks the price of a product on Amazon.
Sends an email notification if the price drops below the target price.
Stops tracking if a specified time limit is reached.
Provides real-time status updates in the console.
Requirements
Python 3.7 or later
requests library
BeautifulSoup4 library
An active Gmail account (with app-specific password for sending emails)
Internet connection
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-username/amazon-price-tracker.git
cd amazon-price-tracker
2. Install Required Libraries
Install the necessary Python libraries:

bash
Copy code
pip install requests beautifulsoup4
3. Configure Your Email
Replace the following placeholders in the script:

Sender Email (gmail_user): Replace with your Gmail address.
Sender Password (gmail_password): Generate an App-Specific Password if you have 2FA enabled.
Recipient Email (user_email): Set the email to receive notifications.
4. Modify URL and Target Price
Replace the url, target_price, and max_time_minutes variables with your desired product details and preferences.

How to Use
Run the Script:
Execute the script with:

bash
Copy code
python amazon_price_tracker.py
Real-Time Updates:
The console will display tracking updates, including the current price and elapsed time.

Notification:
If the price drops below the target price, an email will be sent to the recipient's address.

Example Configuration
python
Copy code
url = "https://www.amazon.in/dp/B07WMS7TWB"
target_price = 1000.0
max_time_minutes = 60
user_email = "your-email@example.com"
Known Limitations
Amazon's Anti-Scraping Measures:
Frequent requests may result in a captcha or IP block. Use headers to simulate a browser request.

Price Element Changes:
If Amazon updates its HTML structure, the price selector (.a-price-whole) may need updating.

Single Product Tracking:
Currently, the script tracks one product at a time.
