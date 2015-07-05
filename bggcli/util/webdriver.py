"""
bgg.webdriver
~~~~~~~~~~~~

Utility in charge of wrapping Selenium web driver

"""
import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
from bggcli.util.logger import Logger


class WebDriver:
    # noinspection PyUnusedLocal,PyDefaultArgument
    def __init__(self, name, args=[], options={}):
        self.name = name
        self.browser_keep = (options.get('browser-keep') == "true")

        # When used with Travis+SauceLabs or directly with SauceLabs
        if os.environ.get('CI') == 'true':
            self.driver = self.create_ci_driver()
        else:
            self.driver = self.create_local_firefox_driver(options.get('browser-profile-dir'))

    def __enter__(self):
        return self

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __exit__(self, type, value, traceback):
        if not self.browser_keep:
            try:
                self.driver.quit()
                Logger.verbose("Close webdriver '%s'" % self.name)
            except WebDriverException as e:
                Logger.info("Encountered error when closing webdriver '%s' (will be skipped): %s"
                            % (self.name, repr(e)))
        return type is None

    # noinspection PyMethodMayBeStatic
    def create_local_firefox_driver(self, profile_path):
        if profile_path is None:
            profile = webdriver.FirefoxProfile()
        else:
            profile = webdriver.FirefoxProfile(profile_path)

        return webdriver.Firefox(firefox_profile=profile)

    # noinspection PyMethodMayBeStatic
    def create_ci_driver(self):
        # See http://docs.travis-ci.com/user/gui-and-headless-browsers/
        capabilities = DesiredCapabilities.FIREFOX.copy()
        if os.environ.get('TRAVIS') == 'true':
            Logger.info("Configure Travis for Sauce Labs")
            capabilities.update(
                {
                    'tunnel-identifier': os.environ["TRAVIS_JOB_NUMBER"],
                    'build': os.environ["TRAVIS_JOB_NUMBER"],
                    'tags': [os.environ["TRAVIS_PYTHON_VERSION"], "CI"]
                }
            )
            sauce_url = "http://%s:%s@localhost:4445/wd/hub" %\
                        ((os.environ["SAUCE_USERNAME"]), (os.environ["SAUCE_ACCESS_KEY"]))
        else:
            Logger.info("Configure direct usage of Sauce Labs")
            sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" %\
                        ((os.environ["SAUCE_USERNAME"]), (os.environ["SAUCE_ACCESS_KEY"]))

        capabilities.update(
            {
                'name': 'bggcli-%s' % self.name
            }
        )

        result = webdriver.Remote(desired_capabilities=capabilities, command_executor=sauce_url)
        result.implicitly_wait(20)

        return result
