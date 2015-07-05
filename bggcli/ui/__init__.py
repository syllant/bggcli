import os

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # To wait for dynamic content (e.g. a popup), Sauce labs being much slower
        if os.environ.get('CI') == 'true':
            timeout = 60
        else:
            timeout = 5
        self.wait = WebDriverWait(driver, timeout)

    @staticmethod
    def update_text(el, value):
        el.clear()
        el.send_keys(value)

    @staticmethod
    def update_checkbox(root_el, xpath, value):
        elem = root_el.find_element_by_xpath(xpath)
        if (elem.is_selected() and (value == '0')) or (not elem.is_selected() and (value == '1')):
            elem.click()

    @staticmethod
    def update_select(el, value, by_text=False):
        select = Select(el)
        if value == '':
            select.select_by_index(0)
        elif by_text:
            select.select_by_visible_text(value)
        else:
            select.select_by_value(value)

    def update_textarea(self, root_el, fieldname, value):
        root_el.find_element_by_xpath(".//td[@class='collection_%smod editfield']" % fieldname) \
            .click()
        form = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, ".//form[contains(@id, '%s')]" % fieldname)))
        self.update_text(form.find_element_by_xpath(".//textarea"), value)
        form.find_element_by_xpath(".//input[contains(@onclick, 'CE_SaveData')]").click()

    def wait_and_accept_alert(self):
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
