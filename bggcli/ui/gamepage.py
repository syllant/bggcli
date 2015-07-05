"""
bgg.gamepage
~~~~~~~~~~~~

Selenium Page Object to bind the game details page

"""

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bggcli import BGG_BASE_URL, BGG_SUPPORTED_FIELDS
from bggcli.ui import BasePage
from bggcli.util.logger import Logger


def in_private_info_popup(func):
    """
    Ensure the Private Info popup is displayed when updating its attributes
    """

    def _wrapper(self, *args, **kwargs):
        try:
            self.itemEl \
                .find_element_by_xpath(".//td[@class='collection_ownershipmod editfield']") \
                .click()
        except NoSuchElementException:
            pass
        else:
            self.privateInfoPopupEl = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='select-free'][contains(@id, 'editownership')]")))

        return func(self, *args, **kwargs)

    return _wrapper


def in_version_popup(func):
    """
    Ensure the Version popup is displayed when updating its attributes
    """

    def _wrapper(self, *args, **kwargs):
        try:
            self.itemEl \
                .find_element_by_xpath(".//td[@class='collection_versionmod editfield']") \
                .click()
        except NoSuchElementException:
            pass
        else:
            self.versionPopupEl = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='select-free'][contains(@id, 'editversion')]")))
            self.versionPopupEl \
                .find_element_by_xpath("//a[contains(@onclick, 'oldversion_version')]").click()
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@id, 'oldversion_version')]")))

        return func(self, *args, **kwargs)

    return _wrapper


class GamePage(BasePage):
    # CSV_SUPPORTED_COLUMNS = [
    #     'objectid', 'rating', 'weight', 'own', 'fortrade', 'want', 'wanttobuy', 'wanttoplay',
    #     'prevowned', 'preordered', 'wishlist', 'wishlistpriority', 'wishlistcomment', 'comment',
    #     'conditiontext', 'haspartslist', 'wantpartslist', 'publisherid', 'imageid',
    #     'year', 'language', 'other', 'pricepaid', 'pp_currency', 'currvalue', 'cv_currency',
    #     'acquisitiondate', 'acquiredfrom', 'quantity', 'privatecomment', '_versionid'
    # ]

    def __init__(self, driver):
        BasePage.__init__(self, driver)

        self.itemEl = None
        self.privateInfoPopupEl = None
        self.versionPopupEl = None

    def goto(self, game_attrs):
        """
        Set Web Driver on the game details page

        :param game_attrs: Game attributes as a dictionary
        """
        self.driver.get("%s/boardgame/%s" % (BGG_BASE_URL, game_attrs['objectid']))

    def update(self, game_attrs):
        """
        Update game details

        :param game_attrs: Game attributes as a dictionary
        """
        self.goto(game_attrs)

        try:
            self.itemEl = self.driver.find_element_by_xpath(
                "//table[@class='collectionmodule_table']")
            Logger.info(" (already in collection)", append=True, break_line=False)
        except NoSuchElementException:
            self.driver.find_element_by_xpath(
                "(//a[contains(@onclick, 'CE_ModuleAddItem')])[last()]").click()
            self.itemEl = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//table[@class='collectionmodule_table']")))

        # Fill all provided values using dynamic invocations 'fill_[fieldname]'
        for key in game_attrs:
            if key in BGG_SUPPORTED_FIELDS:
                value = game_attrs[key]
                if value is not None:
                    getattr(self, "fill_%s" % key)(value)

        # Save "Private Info" popup if opened
        try:
            self.privateInfoPopupEl.find_element_by_xpath(".//input[@type='submit']").click()
        except WebDriverException:
            pass
        else:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, ".//td[@class='collection_ownershipmod editfield']")))

        # Save "Version" popup if opened
        try:
            self.versionPopupEl.find_element_by_xpath(".//input[@type='submit']").click()
        except WebDriverException:
            pass
        else:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, ".//td[@class='collection_versionmod editfield']")))

    def delete(self, game_attrs):
        """
        Delete a game in the collection

        :param game_attrs: Game attributes as a dictionary. Only the id will be used
        """
        self.goto(game_attrs)
        try:
            del_button = self.driver.find_element_by_xpath("//a[contains(@onclick, "
                                                           "'CE_ModuleDeleteItem')]")
        except NoSuchElementException:
            Logger.info(" (not in collection)", append=True, break_line=False)
            return

        del_button.click()

        # Confirm alert message
        self.wait_and_accept_alert()

    ###############################################################################################
    # All following functions are invoked dynamically, for each attribute that can be updated     #
    # Functions are named 'fill_{attribute-name}'                                                 #
    ###############################################################################################

    def fill_objectid(self, value):
        pass

    def fill_objectname(self, value):
        pass

    def fill_rating(self, value):
        td = self.driver.find_element_by_xpath("//td[contains(@id, 'CEcell_rating')]")
        td.click()

        self.update_text(self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@style='editrating']"))), value)
        td.find_element_by_xpath(".//input[@type='submit']").click()

    def fill_weight(self, value):
        self.update_select(self.itemEl.find_element_by_xpath(".//select[@name='weight']"), value)

    def fill_own(self, value):
        self.update_checkbox(self.itemEl, ".//ul[@class='collectionstatus']//input[@name='own']",
                             value)

    def fill_fortrade(self, value):
        self.update_checkbox(self.itemEl,
                             ".//ul[@class='collectionstatus']//input[@name='fortrade']", value)

    def fill_want(self, value):
        self.update_checkbox(self.itemEl, ".//ul[@class='collectionstatus']//input[@name='want']",
                             value)

    def fill_wanttobuy(self, value):
        self.update_checkbox(self.itemEl,
                             ".//ul[@class='collectionstatus']//input[@name='wanttobuy']", value)

    def fill_wanttoplay(self, value):
        self.update_checkbox(self.itemEl,
                             ".//ul[@class='collectionstatus']//input[@name='wanttoplay']", value)

    def fill_prevowned(self, value):
        self.update_checkbox(self.itemEl,
                             ".//ul[@class='collectionstatus']//input[@name='prevowned']", value)

    def fill_preordered(self, value):
        self.update_checkbox(self.itemEl,
                             ".//ul[@class='collectionstatus']//input[@name='preordered']", value)

    def fill_wishlist(self, value):
        self.update_checkbox(self.itemEl, ".//input[@name='wishlist']", value)

    def fill_wishlistpriority(self, value):
        self.update_select(
            self.itemEl.find_element_by_xpath(".//select[@name='wishlistpriority']"), value)

    def fill_wishlistcomment(self, value):
        self.update_textarea(self.itemEl, 'wishlistcomment', value)

    def fill_comment(self, value):
        self.update_textarea(self.itemEl, 'comment', value)

    def fill_conditiontext(self, value):
        self.update_textarea(self.itemEl, 'conditiontext', value)

    def fill_haspartslist(self, value):
        self.update_textarea(self.itemEl, 'haspartslist', value)

    def fill_wantpartslist(self, value):
        self.update_textarea(self.itemEl, 'wantpartslist', value)

    @in_version_popup
    def fill__versionid(self, value):
        if value:
            radio_version = self.versionPopupEl.find_element_by_xpath(
                "(.//ul)[1]//input[@value='%s']" % value)
            radio_version.click()

    @in_version_popup
    def fill_publisherid(self, value):
        self.update_text(self.versionPopupEl.find_element_by_name('publisherid'), value)

    @in_version_popup
    def fill_imageid(self, value):
        self.update_text(self.versionPopupEl.find_element_by_name('imageid'), value)

    @in_version_popup
    def fill_year(self, value):
        self.update_text(self.versionPopupEl.find_element_by_name('year'), value)

    @in_version_popup
    def fill_language(self, value):
        self.update_select(self.versionPopupEl.find_element_by_name('languageid'), value,
                           by_text=True)

    @in_version_popup
    def fill_other(self, value):
        self.update_text(self.versionPopupEl.find_element_by_name('other'), value)

    @in_private_info_popup
    def fill_pricepaid(self, value):
        self.update_text(self.privateInfoPopupEl.find_element_by_name('pricepaid'), value)

    @in_private_info_popup
    def fill_pp_currency(self, value):
        self.update_select(self.privateInfoPopupEl.find_element_by_name('pp_currency'), value)

    @in_private_info_popup
    def fill_currvalue(self, value):
        self.update_text(self.privateInfoPopupEl.find_element_by_name('currvalue'), value)

    @in_private_info_popup
    def fill_cv_currency(self, value):
        self.update_select(self.privateInfoPopupEl.find_element_by_name('cv_currency'), value)

    @in_private_info_popup
    def fill_acquisitiondate(self, value):
        self.update_text(
            self.privateInfoPopupEl.find_element_by_xpath(
                "//input[contains(@id, 'acquisitiondateinput')]"), value)

    @in_private_info_popup
    def fill_acquiredfrom(self, value):
        self.update_text(self.privateInfoPopupEl.find_element_by_name('acquiredfrom'), value)

    @in_private_info_popup
    def fill_quantity(self, value):
        self.update_text(self.privateInfoPopupEl.find_element_by_name('quantity'), value)

    @in_private_info_popup
    def fill_privatecomment(self, value):
        self.update_text(self.privateInfoPopupEl.find_element_by_name('privatecomment'), value)
