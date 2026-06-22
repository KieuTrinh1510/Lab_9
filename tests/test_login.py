"""
Test Case 1: Kiểm thử chức năng Đăng nhập (Login)
Website: https://www.saucedemo.com
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.saucedemo.com"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


class TestLogin:
    """TC-01: Đăng nhập thành công với tài khoản hợp lệ"""

    def test_login_success(self, driver):
        driver.get(BASE_URL)

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait = WebDriverWait(driver, 10)
        inventory_title = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert inventory_title.text == "Products", (
            f"Expected 'Products' but got '{inventory_title.text}'"
        )
        assert "inventory" in driver.current_url, (
            f"URL should contain 'inventory', got: {driver.current_url}"
        )
        print("\n[PASS] TC-01: Đăng nhập thành công")

    """TC-02: Đăng nhập thất bại với mật khẩu sai"""

    def test_login_wrong_password(self, driver):
        driver.get(BASE_URL)

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("wrong_password")
        driver.find_element(By.ID, "login-button").click()

        error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error_msg.is_displayed(), "Error message should be displayed"
        assert "Username and password do not match" in error_msg.text, (
            f"Unexpected error message: {error_msg.text}"
        )
        print("\n[PASS] TC-02: Hiển thị lỗi khi mật khẩu sai")

    """TC-03: Đăng nhập thất bại với tài khoản bị khóa"""

    def test_login_locked_user(self, driver):
        driver.get(BASE_URL)

        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error_msg.is_displayed(), "Error message should be displayed"
        assert "Sorry, this user has been locked out" in error_msg.text, (
            f"Unexpected error message: {error_msg.text}"
        )
        print("\n[PASS] TC-03: Hiển thị lỗi khi tài khoản bị khóa")

    """TC-04: Đăng nhập thất bại khi để trống username"""

    def test_login_empty_username(self, driver):
        driver.get(BASE_URL)

        driver.find_element(By.ID, "login-button").click()

        error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error_msg.is_displayed(), "Error message should be displayed"
        assert "Username is required" in error_msg.text, (
            f"Unexpected error message: {error_msg.text}"
        )
        print("\n[PASS] TC-04: Hiển thị lỗi khi để trống username")
