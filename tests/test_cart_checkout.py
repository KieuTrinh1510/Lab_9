"""
Test Case 3: Kiểm thử chức năng Giỏ hàng & Checkout
Website: https://www.saucedemo.com
"""

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.saucedemo.com"


def click_until(driver, locator, condition):
    """Click tối đa 3 lần cho đến khi trang đạt trạng thái mong đợi."""
    for attempt in range(3):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locator)
        ).click()
        try:
            return WebDriverWait(driver, 5).until(condition)
        except TimeoutException:
            if attempt == 2:
                raise


@pytest.fixture
def logged_in_driver():
    """Fixture: khởi tạo driver và đăng nhập sẵn trước mỗi test."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)

    drv.get(BASE_URL)
    drv.find_element(By.ID, "user-name").send_keys("standard_user")
    drv.find_element(By.ID, "password").send_keys("secret_sauce")
    drv.find_element(By.ID, "login-button").click()
    WebDriverWait(drv, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    yield drv
    drv.quit()


class TestCart:
    """TC-09: Thêm sản phẩm vào giỏ hàng"""

    def test_add_to_cart(self, logged_in_driver):
        driver = logged_in_driver

        # Lấy tên sản phẩm đầu tiên
        item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text

        # Nhấn nút Add to cart
        badge = click_until(
            driver,
            (By.CSS_SELECTOR, ".btn_inventory"),
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")),
        )

        # Badge giỏ hàng phải hiện số 1
        assert badge.text == "1", f"Cart badge should be '1', got '{badge.text}'"

        # Vào giỏ hàng kiểm tra
        click_until(
            driver,
            (By.CLASS_NAME, "shopping_cart_link"),
            EC.url_contains("cart.html"),
        )
        cart_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        cart_name = cart_item.find_element(By.CLASS_NAME, "inventory_item_name").text
        assert cart_name == item_name, (
            f"Cart item name mismatch: '{cart_name}' != '{item_name}'"
        )
        print(f"\n[PASS] TC-09: Thêm '{item_name}' vào giỏ hàng thành công")

    """TC-10: Xóa sản phẩm khỏi giỏ hàng"""

    def test_remove_from_cart(self, logged_in_driver):
        driver = logged_in_driver

        # Thêm sản phẩm rồi xóa
        click_until(
            driver,
            (By.CSS_SELECTOR, ".btn_inventory"),
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")),
        )
        click_until(
            driver,
            (By.CLASS_NAME, "shopping_cart_link"),
            EC.url_contains("cart.html"),
        )

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        driver.find_element(By.CSS_SELECTOR, ".cart_button").click()

        # Giỏ hàng phải trống
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0, f"Cart should be empty, got {len(cart_items)} items"

        # Badge biến mất
        badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(badges) == 0, "Cart badge should disappear after removing all items"
        print("\n[PASS] TC-10: Xóa sản phẩm khỏi giỏ hàng thành công")


class TestCheckout:
    """TC-11: Hoàn tất quy trình Checkout"""

    def test_checkout_complete(self, logged_in_driver):
        driver = logged_in_driver

        # Thêm sản phẩm
        click_until(
            driver,
            (By.CSS_SELECTOR, ".btn_inventory"),
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")),
        )
        click_until(
            driver,
            (By.CLASS_NAME, "shopping_cart_link"),
            EC.url_contains("cart.html"),
        )

        # Bước 1: Checkout
        click_until(
            driver,
            (By.ID, "checkout"),
            EC.url_contains("checkout-step-one.html"),
        )

        # Bước 2: Điền thông tin
        driver.find_element(By.ID, "first-name").send_keys("Nguyen")
        driver.find_element(By.ID, "last-name").send_keys("Van A")
        driver.find_element(By.ID, "postal-code").send_keys("700000")
        click_until(
            driver,
            (By.ID, "continue"),
            EC.url_contains("checkout-step-two.html"),
        )

        # Bước 3: Xác nhận tổng tiền
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        assert "Total:" in total, f"Total label not found: {total}"

        # Bước 4: Finish
        click_until(
            driver,
            (By.ID, "finish"),
            EC.url_contains("checkout-complete.html"),
        )

        # Kiểm tra trang cảm ơn
        confirm_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert "Thank you" in confirm_header.text, (
            f"Expected 'Thank you', got '{confirm_header.text}'"
        )
        print(f"\n[PASS] TC-11: Checkout hoàn tất. Tổng: {total}")

    """TC-12: Checkout thất bại khi thiếu thông tin (First Name)"""

    def test_checkout_missing_info(self, logged_in_driver):
        driver = logged_in_driver

        click_until(
            driver,
            (By.CSS_SELECTOR, ".btn_inventory"),
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")),
        )
        click_until(
            driver,
            (By.CLASS_NAME, "shopping_cart_link"),
            EC.url_contains("cart.html"),
        )

        click_until(
            driver,
            (By.ID, "checkout"),
            EC.url_contains("checkout-step-one.html"),
        )

        # Bỏ trống First Name, chỉ điền Last Name và Zip
        driver.find_element(By.ID, "last-name").send_keys("Van A")
        driver.find_element(By.ID, "postal-code").send_keys("700000")
        driver.find_element(By.ID, "continue").click()

        error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert error_msg.is_displayed(), "Error message should be displayed"
        assert "First Name is required" in error_msg.text, (
            f"Unexpected error: {error_msg.text}"
        )
        print("\n[PASS] TC-12: Hiển thị lỗi khi thiếu First Name")
