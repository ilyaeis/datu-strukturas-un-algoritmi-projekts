from work_with_rtu_schedule import get_rtu_schedule_lectures, get_needed_programms

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
    
    all_programms = get_needed_programms(driver, input_data["programs_range"][0], input_data["programs_range"][1])
    all_programms.remove(input_data["program"])
    print("All programms:\n", all_programms)
    
if __name__ == "__main__":
    input_data = {
        "program": "21",
        "course-id": "1",
        "group-id": "15"
    }

    url = "https://nodarbibas.rtu.lv/?lang=lv"
    driver = webdriver.Chrome()
    try:
        main(driver, input_data, url)
    except Exception as e:
        print(e)
    finally:
        input("Press Enter to close the driver...")
        driver.quit()
        print("Driver closed.")