from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json


def get_rtu_schedule_lectures(driver, input_data):
    all_lectures_by_day = {}

    print("!!! ACTION REQUIRED: Add code to select the Faculty here. !!!")

    program_button_selector = '[data-id="program-id"]'
    print("Finding and clicking the Program dropdown button...")
    program_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, program_button_selector))
    )
    program_button.click()
    print("Program button clicked.")

    program_option_xpath = "/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div/div[2]/ul/li[22]/a/span"
    print(f"Attempting to click program option at XPath: {program_option_xpath}")
    program_option_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, program_option_xpath))
    )
    program_option_element.click()
    print("Program option clicked.")
    time.sleep(1)

    course_select_locator = (By.ID, "course-id")
    print("Waiting for the Course select element to be present...")
    course_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(course_select_locator)
    )
    course_select = Select(course_select_element)
    select = Select(course_select_element)
    select.select_by_value(input_data["course-id"])
    print(f"Course selected: {input_data['course-id']}")
    time.sleep(1)

    group_select_locator = (By.ID, "group-id")
    print("Waiting for the Group select element to be present...")
    group_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(group_select_locator)
    )
    group_select = Select(group_select_element)
    select = Select(group_select_element)
    select.select_by_visible_text(input_data["group-id"])
    print(f"Group selected: {input_data['group-id']}")

    time.sleep(2)
    day_container_selector = "td.fc-daygrid-day"
    print(f"Waiting for schedule day containers matching '{day_container_selector}' to load...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, day_container_selector))
    )
    print("Schedule content appears to be loaded.")

    day_container_selector = "td.fc-daygrid-day"

    event_selector_within_day = "a.fc-daygrid-event.fc-event"

    event_title_selector = ".fc-event-title"

    print(f"\nFinding all day container elements matching '{day_container_selector}'...")
    day_elements = driver.find_elements(By.CSS_SELECTOR, day_container_selector)

    print(f"Found {len(day_elements)} day containers in the visible schedule.")

    print("\n--- Extracting Lectures from All Days ---")
    for i, day_element in enumerate(day_elements):
        day_date = None

        try:
            day_date = day_element.get_attribute("data-date")
            if day_date:
                print(f"\nProcessing Day: {day_date}")
                all_lectures_by_day[day_date] = []
            else:
                 day_date = f"Day Index {i}"
                 print(f"\nProcessing Day (no data-date): {day_date}")
                 all_lectures_by_day[day_date] = []


        except Exception as e:
            print(f"Error extracting date from day element {i}: {e}")
            day_date = f"Day Index {i}"
            all_lectures_by_day[day_date] = []


        events_in_day = day_element.find_elements(By.CSS_SELECTOR, event_selector_within_day)

        if events_in_day:
            print(f"  Found {len(events_in_day)} total events for {day_date}.")
            for j, event_element in enumerate(events_in_day):
                try:
                    title_element = event_element.find_element(By.CSS_SELECTOR, event_title_selector)
                    event_title = title_element.text.strip()

                    event_time = ""
                    try:
                        time_element = event_element.find_element(By.CLASS_NAME, "fc-event-time")
                        event_time = time_element.text.strip()
                    except NoSuchElementException:
                        pass

                    lecture_details = {
                        'Time': event_time,
                        'Title': event_title,
                    }
                    all_lectures_by_day[day_date].append(lecture_details)
                    print(f"    Found Lecture: {lecture_details}")

                except NoSuchElementException:
                     print(f"  Event {j+1} ({day_date}): Could not find title element, skipping event.")
                except Exception as e:
                    print(f"Error processing event {j+1} ({day_date}): {e}")
        else:
            print("  No events found in this day container.")


    print("\n--- Finished Extracting Lectures from All Days ---")

    return all_lectures_by_day

if __name__ == "__main__":
    input_data = {
        "program": "Finanšu inženierija (RDCM0)",
        "course-id": "1",
        "group-id": "15"
    }

    url = "https://nodarbibas.rtu.lv/?lang=lv"
    driver = webdriver.Chrome()
    print(f"Opening page: {url}")
    driver.get(url)

    try:
        schedule_data = get_rtu_schedule_lectures(driver, input_data)

        print("\n--- Final Extracted Schedule Data (Lectures Only) ---")
        if schedule_data:
            print(json.dumps(schedule_data, indent=2, ensure_ascii=False))
        else:
            print("No lecture data was extracted.")
        print("----------------------------------------------------")


    except TimeoutException:
        print(f"Error: Timed out waiting for elements to load or become clickable.")
        print("This could be due to slowness or if the element never becomes available.")
        print("Check if previous steps (Faculty, Program, Course, Group selection) populated correctly or increase wait times.")
    except NoSuchElementException:
        print("Error: Could not find an element on the page using the specified locators or XPATH.")
        print("This usually means the element wasn't loaded or the selector is wrong.")
        print("Verify that the Faculty and Program selections correctly populate the subsequent dropdowns and the schedule structure.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        print("Closing browser.")
        input("Press Enter to close the browser...")
        if driver:
            driver.quit()
