import os.path
import pickle
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

email = 'steamkaiduev@gmail.com'
password = 'Mlb123!123!'

mlb_login_url = 'https://www.mlbshop.com/login'
# mlb_login_url = 'https://www.nbastore.eu/login'


def save_cookies(browser):
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))


def manually_login(browser):
    try:
        email_input = browser.find_element(By.ID, 'emailInput')
        password_input = browser.find_element(By.ID, 'passwordInput')
        email_input.send_keys(email)
        password_input.send_keys(password)
        time.sleep(2)
        login_button = browser.find_element(By.CSS_SELECTOR, 'button[data-trk-id=login-form-submit]')
        login_button.click()
        time.sleep(30)
        try:
            browser.find_element(By.CSS_SELECTOR, 'button[data-trk-id=login-form-submit]').click()
            time.sleep(10)
            save_cookies(browser)
            print("Success Login")
        except Exception as e:
            print("Success Login")
    except Exception as e:
        print(e)
        print("Authorization error")


def authenticate(browser):
    cookie_file = os.path.isfile('cookies.pkl')
    logged_in = bool()
    if cookie_file:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.refresh()
        time.sleep(3)
        try:
            browser.find_element(By.CSS_SELECTOR, 'header[data-talos=labelAccountHome]')
            logged_in = True
        except Exception as e:
            logged_in = False
        if not logged_in:
            manually_login(browser)
    else:
        manually_login(browser)
    browser.save_screenshot('auth.png')
    print(logged_in)


def buy(browser, selected_size, product_url):
    browser.get(product_url)
    time.sleep(3)
    sizes = browser.find_elements(By.CSS_SELECTOR, 'a[data-talos="buttonSize"]')
    for size in sizes:
        if size.text == selected_size:
            size.click()
    time.sleep(3)
    add_to_cart_button = browser.find_element(By.CSS_SELECTOR, 'button[data-trk-id="add-to-cart"]')
    add_to_cart_button.click()
    time.sleep(15)
    checkout_button = browser.find_element(By.CSS_SELECTOR, 'button[data-trk-id="checkout-button-cart-vertical"]')
    browser.save_screenshot('checkout.png')
    checkout_button.click()
    pass


def main(selected_size, product_url):
    display = Display(visible=False, size=(1400, 800))
    display.start()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    browser = webdriver.Chrome(
        options=options,
    )
    browser.set_window_size(1400, 800)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdcadoQpoasnfa76pfcZLmcfl_Symbol;
            '''
    })
    browser.get(mlb_login_url)
    time.sleep(3)
    authenticate(browser)
    time.sleep(3)
    buy(browser, selected_size, product_url)
    time.sleep(10)
    browser.quit()
    pass


if __name__ == "__main__":
    product_url = 'https://www.mlbshop.com/baltimore-orioles/mens-baltimore-orioles-nike-black-local-team-skyline-t-shirt/t-14888540+p-35223326781441+z-8-4256428533?_ref=p-GALP:m-GRID:i-r0c0:po-0'
    selected_size = 'M'
    main(selected_size, product_url)
