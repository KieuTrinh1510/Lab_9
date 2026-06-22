"""
Test Case 2: Kiểm thử chức năng Sản phẩm (Product Listing & Sorting)
Website: https://www.saucedemo.com
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.saucedemo.com"


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

    # Đăng nhập
    drv.get(BASE_URL)
    drv.find_element(By.ID, "user-name").send_keys("standard_user")
    drv.find_element(By.ID, "password").send_keys("secret_sauce")
    drv.find_element(By.ID, "login-button").click()
    WebDriverWait(drv, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    yield drv
    drv.quit()


class TestProduct:
    """TC-05: Trang sản phẩm hiển thị đủ 6 sản phẩm"""

    def test_product_count(self, logged_in_driver):
        driver = logged_in_driver
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) == 6, f"Expected 6 products, got {len(items)}"
        print(f"\n[PASS] TC-05: Hiển thị đúng {len(items)} sản phẩm")

    """TC-06: Sắp xếp sản phẩm theo giá tăng dần (Price: Low to High)"""

    def test_sort_price_low_to_high(self, logged_in_driver):
        driver = logged_in_driver

        sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_dropdown.select_by_value("lohi")

        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        price_values = [float(p.text.replace("$", "")) for p in prices]

        assert price_values == sorted(price_values), (
            f"Prices are not sorted low-to-high: {price_values}"
        )
        print(f"\n[PASS] TC-06: Giá tăng dần: {price_values}")

    """TC-07: Sắp xếp sản phẩm theo tên Z-A"""

    def test_sort_name_z_to_a(self, logged_in_driver):
        driver = logged_in_driver

        sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_dropdown.select_by_value("za")

        names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        name_values = [n.text for n in names]

        assert name_values == sorted(name_values, reverse=True), (
            f"Names are not sorted Z-A: {name_values}"
        )
        print(f"\n[PASS] TC-07: Tên Z-A: {name_values}")

    """TC-08: Click vào sản phẩm và xem chi tiết"""

    def test_product_detail(self, logged_in_driver):
        driver = logged_in_driver

        first_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        item_name = first_item.text
        first_item.click()

        detail_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_details_name"))
        )
        assert detail_name.text == item_name, (
            f"Product name mismatch: '{detail_name.text}' != '{item_name}'"
        )
        assert "inventory-item" in driver.current_url, (
            f"Should be on detail page, got: {driver.current_url}"
        )
        print(f"\n[PASS] TC-08: Xem chi tiết sản phẩm '{item_name}'")
