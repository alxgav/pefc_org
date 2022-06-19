from selenium import webdriver


def browser(headless=True) -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/101.0.4951.54 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("window-size=1920,1080")
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    return webdriver.Chrome(executable_path='/home/alxgav/chromedrive/chromedriver', options=options)
