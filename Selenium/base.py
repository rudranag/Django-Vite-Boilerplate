from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
class BaseTest:
    LOGIN_URL = 'http://127.0.0.1:8000/r/todo/'  # Replace with your actual login page URL
    USERNAME = 'admin'  # Replace with your actual username
    PASSWORD = 'admin'  # Replace with your actual password
    TIMEOUT = 10  # Timeout for waiting for elements to appear

    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        if os.environ.get("RUN_HEADLESS"):
            cls.driver = webdriver.Chrome(options=chrome_options)
        else:
            cls.driver = webdriver.Chrome()
            
        cls.driver.maximize_window()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def login(self):
        self.driver.get(self.LOGIN_URL)
        
        username_input = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(self.USERNAME)
        password_input.send_keys(self.PASSWORD)

        login_button = self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input')
        login_button.click()

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Add Todo')]"))
        )
