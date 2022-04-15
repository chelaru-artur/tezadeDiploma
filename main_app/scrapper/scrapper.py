from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..models import Scenario, Action, Record
from .action_types import ActionTypes
import time
import datetime
globalCount = 0
commands = []
status = {}


def init():
    global globalCount
    globalCount = globalCount + 1


class Scraper:
    count = 0
    def __init__(self):
        self.driver = None
        print("inited?")

    def exec(self):
        global commands
        driver = webdriver.Chrome()
        SEARCH_FILTERS_SELECTOR = "[data-marker=search-filters]"
        driver.get("https://www.avito.ru/rossiya/avtomobili")
        try:
            try:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_FILTERS_SELECTOR)))
            except:
                print("entered")
                driver.close()

            searchFilters = driver.find_element(By.CSS_SELECTOR, SEARCH_FILTERS_SELECTOR)
            priceFrom = driver.find_element(By.CSS_SELECTOR, "[data-marker='price/from']")
            priceFrom.send_keys(1000000)
            submitBtn = driver.find_element(By.CSS_SELECTOR, "[data-marker='search-filters/submit-button']")
            driver.implicitly_wait(100)
            submitBtn.click()
            items = driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
            for i in items[:10]:
                i.click()
            availableTabs = driver.window_handles
            print("window handles %d", len(availableTabs))
            for tab in availableTabs[1:]:
                driver.switch_to.window(tab)
                btn = driver.find_element(By.CSS_SELECTOR, "[data-marker='item-phone-button/card']")
                btn.click()
                print(driver.find_element(By.CSS_SELECTOR, "[data-marker='seller-info/name']").text)
                img = btn.find_element(By.TAG_NAME, 'img').get_attribute('src')
                # img_text = get_image_text(img.replace('data:image/png;base64,', ''))
                # print(img_text)
                driver.implicitly_wait(1000)
                if len(commands) > 0:
                    driver.quit()
                    print('stopped')
                    break
            time.sleep(30)
            # print(elem.text)
            # assert "Python" in driver.title
            # elem = driver.find_element(By.NAME, "q")
            # elem.clear()
            # elem.send_keys("pycon")
            # elem.send_keys(Keys.RETURN)
            # assert "No results found." not in driver.page_source
        finally:
            driver.close()

    def start(self, scenarioId):
        global status
        self.currentScenario = Scenario.objects.get(pk=scenarioId)
        status["scenario"] = self.currentScenario.name

        # TODO: think how to implement nested actions
        # Get only root actions
        actions = Action.objects.filter(scenario=scenarioId, parentId=None)
        print (datetime.datetime.now(), "started: ", self.currentScenario.name)
        self.driver = webdriver.Chrome()
        try:
            for action in actions:
                print(datetime.datetime.now(), "action: ", ActionTypes(action.actionType).name)
                status["action"] = ActionTypes(action.actionType).name
                self.do(action)
        finally:
            time.sleep(30)
            self.driver.__exit__()
            status={}
            status["running"]=False

    def do(self, action, element=None):
        if action.actionType == ActionTypes.OPEN.value:
            self.driver.get(action.params["url"])
        elif action.actionType == ActionTypes.CLICK.value:
            if element:
                element.click()
                return
            el = self.driver.find_element(By.CSS_SELECTOR, action.params["selector"])
            el.click()
        elif action.actionType == ActionTypes.WAIT.value:
            self.driver.implicitly_wait(action.params["time"])
        elif action.actionType == ActionTypes.SET_DATA.value:
            # self.driver.save_screenshot('screenie.png')
            data = {}
            for key in action.params:
                el = self.driver.find_element(By.CSS_SELECTOR, action.params[key])
                print(el)
                data[key] = el.text
            print(data)
            rec = Record(data=data, scenario=self.currentScenario)
            rec.save()
            time.sleep(0.5)
        elif action.actionType == ActionTypes.FOR_EACH_ELEMENT.value:
            self.do_for_each_element(action)
        elif action.actionType == ActionTypes.CLOSE_TAB.value:
            self.driver.close()
        elif action.actionType == ActionTypes.MOVE_TO_NEXT_TAB.value:
            self.driver.switch_to.window(self.driver.window_handles[1])

    def do_for_each_element(self, action):
        elements = self.driver.find_elements(By.CSS_SELECTOR, action.params["selector"])
        actions = Action.objects.filter(parentId=action.pk)
        main_tab = self.driver.current_window_handle
        for el in elements:
            self.driver.switch_to.window(main_tab)
            for a in actions:
                print ("child action", a)
                self.do(a, el)




scraper = Scraper()
