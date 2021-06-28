import schedule

from selenium import webdriver
from bs4 import BeautifulSoup

import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(stock_name, updw):

    me = "wkd9146@gmail.com"
    my_password = "suwhtoixfpdgkwnj"
    you = "wkd9146@naver.com"
    msg = MIMEMultipart('alternative')
    if(updw > 0):
        msg['Subject'] = "[주식알림]주가상승"
        msg['From'] = me
        msg['To'] = you
        html = stock_name + " " + str(updw) + "% 상승"
    elif(updw < 0):
        msg['Subject'] = "[주식알림]주가하락"
        msg['From'] = me
        msg['To'] = you
        html = stock_name + " " + str(updw) + "% 하락"
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(me, my_password)
    s.sendmail(me, you, msg.as_string())
    s.quit()


def get_my_stock():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('chromedriver', options=options)

    codes = ['269620', '258790', '001470', '161390', '005930']

    for code in codes:

        url = 'https://m.stock.naver.com/item/main.nhn#/stocks/' + code + '/total'

        driver.get(url)

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        name = soup.select_one(
            '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.item_wrp > div > h2').text

        current_price = soup.select_one(
            '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > strong').text

        rate = soup.select_one(
        '#header > div.end_header_topinfo > div.flick-container.major_info_wrp > div > div:nth-child(2) > div > div.stock_wrp > div.price_wrp > div > span.gap_rate > span.rate').text

        print(name, current_price, rate)
        inrate = float(rate)
        if (float(rate) > 4):
            print('send', name)
            send_mail(name, inrate)
        if (float(rate) < -3):
            print('send', name)
            send_mail(name, inrate)

    print('-------')

    driver.quit()


def job():
    get_my_stock()


def run():
    schedule.every(10).seconds.do(job)  # Second
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    run()
