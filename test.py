import work_with_rtu_schedule 

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
   
    all_programs = work_with_rtu_schedule.get_needed_programs(driver, input_data["programs_range"][0], input_data["programs_range"][1])
    print("All programs:\n", all_programs)
    driver.refresh()
    
    # main_schedule = work_with_rtu_schedule.get_rtu_schedule_lectures(driver, input_data["program-id"], input_data["course-id"], input_data["group-id"])
    # print("Main schedule data:\n", json.dumps(main_schedule, indent=4))
    # driver.refresh()
    
    for program in all_programs:
        if program["name"] == input_data["program-name"]:
            continue
        print(f"Processing program: {program['name']}")
        groups_in_courses = work_with_rtu_schedule.get_programs_courses_groups(driver, program)

        for course_id, groups in groups_in_courses.items():
            print(f"  Course ID: {course_id}")
            print(groups)
            for group in groups:
                print(f"{group=}")
                schedule = work_with_rtu_schedule.get_rtu_schedule_lectures(driver, program["id"], course_id, group["text"])
                print("    Schedule data:\n", json.dumps(schedule, indent=4))
                driver.refresh()
                    
if __name__ == "__main__":
    input_data = {
        "program-name": "Finanšu inženierija (RDCM0)",
        "program-id": "21",
        "course-id": "1",
        "group-id": "15",
        "programs_range": [11, 94]
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