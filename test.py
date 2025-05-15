from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://nodarbibas.rtu.lv/?lang=lv"
driver = webdriver.Chrome() 
driver.get(url)

try:
    date_to_find = "2025-05-07" 
    specific_day_selector = f'[data-date="{date_to_find}"]' 
    print(f"Waiting for the specific day element matching '{specific_day_selector}'...")
    day_element = WebDriverWait(driver, 20).until( 
        EC.presence_of_element_located((By.CSS_SELECTOR, specific_day_selector))
    )
    print(f"Specific day element found for date: {day_element.get_attribute('data-date')}")

    event_selector_within_day = "a.fc-daygrid-event.fc-event" 

    event_title_selector = ".fc-event-title" 

    print(f"Finding all event elements within the day '{date_to_find}'...")
    events_in_day = day_element.find_elements(By.CSS_SELECTOR, event_selector_within_day)

    print(f"Found {len(events_in_day)} total events for {date_to_find}.")

    lectures_in_day = []

    print("\n--- Identifying Lectures for this day ---")
    if events_in_day:
        for j, event_element in enumerate(events_in_day):
            try:
                title_element = event_element.find_element(By.CSS_SELECTOR, event_title_selector)
                event_title = title_element.text.strip()

                if "Lekc." in event_title:
                    event_time = ""
                    try:
                        time_element = event_element.find_element(By.CLASS_NAME, "fc-event-time") # Class is visible in your snippet
                        event_time = time_element.text.strip()
                    except NoSuchElementException:
                        pass 

                    lecture_details = {
                        'Time': event_time,
                        'Title': event_title,
                    }
                    lectures_in_day.append(lecture_details)
                    print(f"  Found Lecture: {lecture_details}")

            except NoSuchElementException:
                 print(f"  Event {j+1} ({date_to_find}): Could not find title element, skipping event.")
            except Exception as e:
                print(f"Error processing event {j+1} ({date_to_find}): {e}")

    else:
        print("No events found in this specific day element.")

    print(f"\n--- Finished finding Lectures on {date_to_find}: Found {len(lectures_in_day)} ---")

except TimeoutException:
    print(f"Error: Timed out waiting for the specific day element '{specific_day_selector}' to appear.")
    print("Check if the schedule loaded correctly and the date is visible in the current view.")
except NoSuchElementException:
    print(f"Error: Could not find the specific day element using the initial selector '{specific_day_selector}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")