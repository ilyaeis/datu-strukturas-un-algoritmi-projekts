from read_the_schedule import get_rtu_schedule_lectures

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json

def main(driver, input_data, url):
    driver.get(url)
    main_schedule = get_rtu_schedule_lectures(driver, input_data)
    print("Main schedule data:\n", json.dumps(main_schedule, indent=4))
    
    
if __name__ == "__main__":
    input_data = {
        "program": "Finanšu inženierija (RDCM0)",
        "course-id": "1",
        "group-id": "15"
    }

    url = "https://nodarbibas.rtu.lv/?lang=lv"
    driver = webdriver.Chrome()
    main(driver, input_data, url)