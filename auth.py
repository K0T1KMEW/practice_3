from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import logging

def check_login_success(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "ddCredit"))
        )
        return True
    except:
        return False

def perform_login(email, password):
    driver = None
    try:
        logging.info("Запуск браузера...")
        firefox_options = Options()
        firefox_options.page_load_strategy = 'eager'

        driver = webdriver.Firefox(options=firefox_options)
        url = "https://secure.veesp.com/clientarea"
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        email_form = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        email_form.send_keys(email)
        logging.info("Введена почта")

        passwd_form = driver.find_element(By.NAME, "password")
        passwd_form.send_keys(password)
        logging.info("Введен пароль")

        enter_button = driver.find_element(By.XPATH, '//button[text()="Вход"]')
        enter_button.click()
        logging.info("Кнопка входа нажата")

        success = check_login_success(driver)
        logging.info(f"Результат входа: {'Успешно' if success else 'Неудачно'}")

        return success
    except Exception as e:
        logging.error(f"Ошибка при выполнении входа: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            logging.info("Браузер закрыт")