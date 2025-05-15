input_data = {
    "program": "Finanšu inženierija (RDCM0)",
    "course-id": "1",
    "group-id": "15"
}
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

url = "https://nodarbibas.rtu.lv/?lang=lv"
driver = webdriver.Chrome() 

try:
    print(f"Opening page: {url}")
    driver.get(url)

    program_button = driver.find_element(By.CSS_SELECTOR, '[data-id="program-id"]')
    program_button.click()
    print("program button clicked")

    program_option_xpath = "/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div/div[2]/ul/li[22]/a/span"
    program_option_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, program_option_xpath))
    )
    program_option_element.click()
    print("program option clicked")
    
    select_element_locator = (By.ID, "course-id")
    course_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(select_element_locator)
    )
    select = Select(course_select_element)
    select.select_by_value(input_data["course-id"])
    print(f"Course selected: {input_data['course-id']}")
    
    select_element_locator = (By.ID, "group-id")
    group_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(select_element_locator)
    )
    select = Select(group_select_element)
    select.select_by_visible_text(input_data["group-id"])
    print(f"Group selected: {input_data['group-id']}")
    
    time.sleep(2)
    
except NoSuchElementException:
    print("Error: Could not find one of the elements (dropdowns, button, table) on the page.")
except TimeoutException:
    print("Error: Timed out waiting for elements to load or become clickable.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    print("Closing browser.")
    input("Press Enter to close the browser...")
    driver.quit()