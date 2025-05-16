import work_with_rtu_schedule 
import schedule_comparing
import work_with_additional_lectures

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import json

# dabut visu vajadzigu salidzinasanai programmu nosaukumus (all_programs)
# dabut pamata lekciju sarakstu visam menesim (main_schedule)
# parveidot pamatsaraksta lekciju glabasanas strukturu (main_lectures)
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 


def main(driver, input_data, url):
    driver.get(url)

# dabut visu vajadzigu salidzinasanai programmu nosaukumus
    all_programs = work_with_rtu_schedule.get_needed_programs(driver, input_data["programs_range"][0], input_data["programs_range"][1])
    print("All programs:\n", all_programs)
    driver.refresh()
    
# dabut pamata lekciju sarakstu visam menesim
    main_schedule = work_with_rtu_schedule.get_rtu_schedule_lectures(driver, input_data["program-id"], input_data["course-id"], input_data["group-id"])
    print("Main schedule data:\n", json.dumps(main_schedule, indent=4))
    # with open("main_schedule.json", 'w', encoding='utf-8') as f:
    #     json.dump(main_schedule, f, indent=4, ensure_ascii=False)
    
# izveidot no kalendara lekciju dictionary
    main_lectures = schedule_comparing.get_main_lectures(main_schedule)
    print("Main lectures:\n", json.dumps(main_lectures, indent=4))
    
# sakas darbs ar papildus lekcijam
    driver.refresh()
    additional_lectures = {} # {date: {time: [lectures]}}

# cikls nem katru programmu no ieprieks dabuta programmu saraksta
    for program in all_programs:

# ja programma sakrit ar lietotaja ievadito programmu tad nevajag parbaudit
        if program["name"] == input_data["program-name"]:
            continue
        print(f"Processing program: {program['name']}")

# dabut grupas apvienotas pec kursiem vienai vajadzigai programmai
        groups_in_courses = work_with_rtu_schedule.get_programs_courses_groups(driver, program)
        print("Courses and groups:\n", json.dumps(groups_in_courses, indent=4))

        for course_id, groups in groups_in_courses.items():
            print(f"  Course ID: {course_id}")
            print(groups)

# iziet cauri visam grupam viena kursa ietvaros
            for group in groups:
                print(f"{group=}")

# dabut lekciju sarakstu vienai konkretai grupai vajadzigaja kursa vajadzigaja programma veselam menesim
                schedule = work_with_rtu_schedule.get_rtu_schedule_lectures(driver, program["id"], course_id, group["text"])
                print("    Schedule data:\n", json.dumps(schedule, indent=4))
                # with open(f"{program["name"]}_{course_id}_{group["text"]}_schedule.json", 'w', encoding='utf-8') as f:
                #     json.dump(schedule, f, indent=4, ensure_ascii=False)
                program_title = f"{program['name']}_{course_id}_{group['text']}"

# pievienot noteiktas grupas lekcijas musu papildus lekciju sarakstam pec atbilstosiem kriterijiem















                additional_lectures = schedule_comparing.update_additional_lectures(program_title, additional_lectures, main_schedule, main_lectures, schedule)
                driver.refresh()
                print("    Additional lectures:\n", json.dumps(additional_lectures, indent=4))
    print("Final additional lectures:\n", json.dumps(additional_lectures, indent=4))
    with open("all_possible_additional_lectures.json", 'w', encoding='utf-8') as f:
        json.dump(additional_lectures, f, indent=4, ensure_ascii=False)
    print("All possible additional lectures saved to all_possible_additional_lectures.json")

    work_with_additional_lectures.convert_json_to_excel(input_data["dates_range"][0], input_data["dates_range"][1])


    
if __name__ == "__main__":
    input_data = {
        "program-name": "Finanšu inženierija (RDCM0)",
        "program-id": "21",
        "course-id": "1",
        "group-id": "15",
        "programs_range": [11, 94],
        "dates_range": [12, 25]
    }

    url = "https://nodarbibas.rtu.lv/?lang=lv"
    driver = webdriver.Chrome()
    
    main(driver, input_data, url)
    input()