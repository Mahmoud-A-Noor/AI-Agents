import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
AUTH = 'brd-customer-hl_fc3d34c3-zone-ai_scraper:6ae8s1xy07kd'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'



def scrape_website(website):
    print("Launching chrome browser...")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Solving Captcha...')
        solve_res = driver.execute('executeCdpCommand', {'cmd': 'Captcha.waitForSolve', 'params': {"detectTimeout": 10000}})
        print("Captcha Solve Status : ", solve_res["value"]["status"])
        html = driver.page_source
        print("html :" , html)

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content) 
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length=7000):
    return [
        dom_content[i:i+max_length]
        for i in range(0, len(dom_content), max_length)
    ]