import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

my_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

my_email = os.environ["MY_EMAIL"]
my_pass = os.environ["MY_PASSWORD"]
smtp_email_provider = os.environ["SMTP_EMAIL_PROVIDER"]

amazon_product_url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

response = requests.get(url=amazon_product_url, headers=my_header)
amazon_web = response.text

soup = BeautifulSoup(amazon_web, "html.parser")

product_price_whole = soup.find(name="span", class_="a-price-whole").getText()
product_price_fraction = soup.find(name="span", class_="a-price-fraction").getText()
product_title = soup.find(name="span", id="productTitle").getText().strip()
fixed_product_title = " ".join(product_title.split())

product_price = float(f"{product_price_whole}{product_price_fraction}")

if product_price <= 100:
    message = f"{fixed_product_title} is on sale for ${product_price}"
    with smtplib.SMTP(smtp_email_provider, port=587) as connection:
        connection.starttls()
        result = connection.login(user=my_email, password=my_pass)
        connection.sendmail(from_addr=my_email,
                            msg="Subject:Amazon Price Alert!\n\n"
                                f"{message}\n"
                                f"{amazon_product_url}".encode("utf-8"),
                            to_addrs="nikshiqinikolas@gmail.com")

print(soup.prettify())
