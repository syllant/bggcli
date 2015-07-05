"""
bgg.collectionpage
~~~~~~~~~~~~

Selenium Page Object to bind the collection page

"""

from selenium.common.exceptions import NoSuchElementException

from bggcli import BGG_BASE_URL
from bggcli.ui import BasePage


class CollectionPage(BasePage):
    def is_empty(self, login):
        """
        Returns True if the collection is empty, False otherwise

        :param login: User login
        """
        self.driver.get("%s/collection/user/%s" % (BGG_BASE_URL, login))
        try:
            self.driver.find_element_by_xpath("//td[contains(@class, 'collection_objectname')]")
        except NoSuchElementException:
            return True
