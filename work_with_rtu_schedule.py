from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def get_programs_courses_groups(driver, program):
# dabut visus kursus un grupas

# uzspiezt pogu lai redzet programmu izvelni
    program_button_selector = '[data-id="program-id"]'
    print("Finding and clicking the Program dropdown button...")
    program_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, program_button_selector))
    )
    program_button.click()
    print("Program button clicked.")

# meklet un atvert programmu pec id ar prefiksu
    text_span_selector = "span.text" 
    program_id = f"bs-select-1-{program["id"]}"
    text_span_selector = "span.text" 
    option_element = WebDriverWait(driver, 5).until( 
                EC.presence_of_element_located((By.ID, program_id))
    )
    text_span_element = option_element.find_element(By.CSS_SELECTOR, text_span_selector)
    text_span_element.click()
    print("Program option clicked.")
    
    time.sleep(1)

# meklet un saglabat visus kursus jeb macibu gadus
    course_select_locator = (By.ID, "course-id")
    print("Waiting for the Course select element to be present...")
    course_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(course_select_locator)
    )
    select = Select(course_select_element)
    all_course_options = select.options
    courses_data = []

# ar ciklu parbaudit un saglabat visus kursus
    for i, option_element in enumerate(all_course_options):
        option_value = option_element.get_attribute("value") # pats kursa nr (option_value)
        if int(option_value) == 0: # "Izveleties..." atzimejas ar nr 0
            continue
        option_text = option_element.text.strip()
        courses_data.append({
            'index': i,
            'value': option_value,
            'text': option_text
        })
        print(f"  Option {i}: Value='{option_value}', Text='{option_text}'")
        
    groups_in_courses = {}

# iziet cauri jau saglabatiem kursiem un atrast grupas
    for i in range(len(courses_data)):
        time.sleep(1)
        course_id = courses_data[i]['value'] # course_id == option_value
        
# izveleties kursu pec ID
        course_select_locator = (By.ID, "course-id")
        print("Waiting for the Course select element to be present...")
        course_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(course_select_locator)
        )
        select = Select(course_select_element)
        select.select_by_value(course_id)
        print(f"Course selected: {course_id}")
    
# parbaudit un saglabat visas grupas vienam kursam
        group_select_locator = (By.ID, "group-id")
        print("Waiting for the Group select element to be present...")
        group_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(group_select_locator)
        )
        select = Select(group_select_element)
        all_group_options = select.options
        groups_data = []

# iziet cauri jau saglabatam grupam un izveidot finala dictionary
        for i, option_element in enumerate(all_group_options):
            option_value = option_element.get_attribute("value")
            if int(option_value) == 0: # "Izveleties..." atzimejas ar nr 0 ka ari pastav dazas grupas ar nr 0
                continue
            option_text = option_element.text.strip()
            groups_data.append({
                'index': i,
                'value': option_value,
                'text': option_text
            })
            groups_in_courses[course_id] = groups_data
    print(groups_in_courses)

# atgriezt grupas apvienotas pec kursiem vienai vajadzigai programmai
    return groups_in_courses

def get_needed_programs(driver, start_id_number, end_id_number):
# dabut programmu nosaukumus (no 11 lidz 94 pec ID)

# uzspiezt pogu lai redzet programmu izvelni
    program_button_selector = '[data-id="program-id"]'
    print("Finding and clicking the Program dropdown button...")
    program_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, program_button_selector))
    )
    program_button.click()
    time.sleep(1)
    
    extracted_programs = []
    id_prefix = "bs-select-1-"
    text_span_selector = "span.text" 

    print(f"Attempting to extract text from elements with IDs from {id_prefix}{start_id_number} to {id_prefix}{end_id_number}")

# ar ciklu iziet cauri visam diapazonam un atrast visu programmu nosaukumus
    for i in range(start_id_number, end_id_number + 1):
        current_id = f"{id_prefix}{i}"
# nevar izmantot select, jo cita klase, tapec ir jaizmanto by.ID ar prefiksiem
        try:
            option_element = WebDriverWait(driver, 5).until( 
                EC.presence_of_element_located((By.ID, current_id))
            )
# pats nosaukums ir vienkarsi teksts bez precizas "name" vai lidzigas tam klases
            text_span_element = option_element.find_element(By.CSS_SELECTOR, text_span_selector)
            element_text = text_span_element.text.strip()
            
# saglabat id bez prefiksiem un nosaukumu programmai
            program = {
                "id": current_id.replace("bs-select-1-", ""),
                "name": element_text
            }
# katras cikla iteracijas nobeiguma pievienot programmu sarakstam
            extracted_programs.append(program)
            print(f"Found and extracted text: '{program}'")
        except Exception as e:
            print(f"An error occurred while processing element ID {current_id}: {e}")

# atgriezt sarakstu ar programmu nosaukumiem
    return extracted_programs

def get_rtu_schedule_lectures(driver, program_id, course_id, group_id):
# dabut vienai programmai visas lekcijas veselam menesim

    all_lectures_by_month = {}

# uzspiezt pogu lai redzet programmu izvelni 
    program_button_selector = '[data-id="program-id"]'
    print("Finding and clicking the Program dropdown button...")
    program_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, program_button_selector))
    )
    program_button.click()
    print("Program button clicked.")

# meklet un atvert programmu pec id ar prefiksu
    current_id = f"bs-select-1-{program_id}"
    text_span_selector = "span.text" 
    option_element = WebDriverWait(driver, 5).until( 
                EC.presence_of_element_located((By.ID, current_id))
    )
    text_span_element = option_element.find_element(By.CSS_SELECTOR, text_span_selector)
    text_span_element.click()
    print("Program option clicked.")
    
    time.sleep(1)

# meklet un atvert ieksa programmai vajadzigo kursu
    course_select_locator = (By.ID, "course-id")
    print("Waiting for the Course select element to be present...")
    course_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(course_select_locator)
    )
    select = Select(course_select_element)
    select.select_by_value(course_id)
    print(f"Course selected: {course_id}")
    
    time.sleep(1)

# meklet un atvert ieksa vajadzigam kursam vajadzigo grupu
    group_select_locator = (By.ID, "group-id")
    print("Waiting for the Group select element to be present...")
    group_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(group_select_locator)
    )
    select = Select(group_select_element)
    select.select_by_visible_text(group_id)
    print(f"Group selected: {group_id}")
    
    time.sleep(1)
# programmas kursa un grupas ietvaros ir atverts lekciju kalendars

# meklet kalendara katru dienu
    day_container_selector = "td.fc-daygrid-day"
    print(f"Waiting for schedule day containers matching '{day_container_selector}' to load...")
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, day_container_selector))
        )
# ja grupai nav ievietots saraksts
    except TimeoutException:
        return all_lectures_by_month
    
    print("Schedule content appears to be loaded.")

    day_container_selector = "td.fc-daygrid-day"
    event_selector_within_day = "a.fc-daygrid-event.fc-event"
    event_title_selector = ".fc-event-title"

    print(f"\nFinding all day container elements matching '{day_container_selector}'...")
    day_elements = driver.find_elements(By.CSS_SELECTOR, day_container_selector)

    print(f"Found {len(day_elements)} day containers in the visible schedule.")

    print("\n--- Extracting Lectures from All Days ---")
# pec kartas cikla ietvaros parmeklet katru dienu lai dabut lekcijas
    for i, day_element in enumerate(day_elements):
        day_date = None

# izveidot pirmo sadalijumu ar datumiem
        try:
            day_date = day_element.get_attribute("data-date")
            if day_date:
                print(f"\nProcessing Day: {day_date}")
                all_lectures_by_month[day_date] = {}
            else:
                 day_date = f"Day Index {i}"
                 print(f"\nProcessing Day (no data-date): {day_date}")
                 all_lectures_by_month[day_date] = {}

        except Exception as e:
            print(f"Error extracting date from day element {i}: {e}")
            day_date = f"Day Index {i}"
            all_lectures_by_month[day_date] = {}

        events_in_day = day_element.find_elements(By.CSS_SELECTOR, event_selector_within_day)

# ja ir elementi (lekcijas) tad parmeklet visas lai pierakstit
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
# pierakstit lekciju nosaukumus katrai dienai ar sadalijumu pec laikiem
                    all_lectures_by_month[day_date][event_time] = event_title

                except NoSuchElementException:
                     print(f"  Event {j+1} ({day_date}): Could not find title element, skipping event.")
                except Exception as e:
                    print(f"Error processing event {j+1} ({day_date}): {e}")
        else:
            print("  No events found in this day container.")

# atgriezt sarakstu visam menesim sadalitu pec dienam un laikiem kas satur lekciju nosaukumus
    return all_lectures_by_month
