import work_with_rtu_schedule 
import schedule_comparing
import work_with_additional_lectures

from selenium import webdriver
import json

# manuali ierakstit visus parametrus (1_solis)
# uzsakt programmu un gaidit kamer tiks izpilditas sekojosas darbibas: (2_solis)
    # dabut visu vajadzigu salidzinasanai programmu nosaukumus (3_solis)
    # dabut pamata lekciju sarakstu visam menesim (4_solis)
    # parveidot pamatsaraksta lekciju glabasanas strukturu (5_solis)
    # dabut visas grupas visiem kursiem visam programmam ar cikliem (6_solis)
    # dabut lekciju sarakstu vienai (katrai pec kartas ar ciklu) konkretai grupai vajadzigaja kursa vajadzigaja programma veselam menesim (7_solis)
    # pievienot tas grupas lekcijas musu papildus lekciju sarakstam pec dalas no atbilstosiem kriterijiem (8_solis)
    # ierakstit visas atbilstosas papildus lekcijas, kuras izgaja pamatfiltresanu, json failam, lai vienkarsak stradat talak (9_solis)
    # velreiz nofiltret lekcijas un ierakstit Excel faila visas, kuras tika lidz galam cauri visiem parejiem kriterijiem (10_solis)
# programma ir pabeigta

def main(driver, input_data, url):
    driver.get(url)

# (3_solis) dabut visu vajadzigu salidzinasanai programmu nosaukumus
    all_programs = work_with_rtu_schedule.get_needed_programs(driver, input_data["programs_range"][0], input_data["programs_range"][1])
    print("All programs:\n", all_programs)
    driver.refresh()
    
# (4_solis) dabut pamata lekciju sarakstu visam menesim
    main_schedule = work_with_rtu_schedule.get_rtu_schedule_lectures(driver, input_data["program-id"], input_data["course-id"], input_data["group-id"])
    print("Main schedule data:\n", json.dumps(main_schedule, indent=4))
    # with open("main_schedule.json", 'w', encoding='utf-8') as f:
    #     json.dump(main_schedule, f, indent=4, ensure_ascii=False)
    
# (5_solis) izveidot no kalendara lekciju dictionary
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

# (6_solis) dabut grupas apvienotas pec kursiem vienai vajadzigai programmai
        groups_in_courses = work_with_rtu_schedule.get_programs_courses_groups(driver, program)
        print("Courses and groups:\n", json.dumps(groups_in_courses, indent=4))

        for course_id, groups in groups_in_courses.items():
            print(f"  Course ID: {course_id}")
            print(groups)

# iziet cauri visam grupam viena kursa ietvaros
            for group in groups:
                print(f"{group=}")

# (7_solis) dabut lekciju sarakstu vienai konkretai grupai vajadzigaja kursa vajadzigaja programma veselam menesim
                schedule = work_with_rtu_schedule.get_rtu_schedule_lectures(driver, program["id"], course_id, group["text"])
                print("    Schedule data:\n", json.dumps(schedule, indent=4))
                # with open(f"{program["name"]}_{course_id}_{group["text"]}_schedule.json", 'w', encoding='utf-8') as f:
                #     json.dump(schedule, f, indent=4, ensure_ascii=False)
                program_title = f"{program['name']}_{course_id}_{group['text']}"

# (8_solis) pievienot tas grupas lekcijas musu papildus lekciju sarakstam pec atbilstosiem kriterijiem
                additional_lectures = schedule_comparing.update_additional_lectures(program_title, additional_lectures, main_schedule, main_lectures, schedule)
                driver.refresh()
                print("    Additional lectures:\n", json.dumps(additional_lectures, indent=4))
    print("Final additional lectures:\n", json.dumps(additional_lectures, indent=4))

# (9_solis) ierakstit loti daudz iespejamas lekcijas, kuras izgaja pamatfiltresanu, json failam, lai vienkarsak stradat talak
    with open("all_possible_additional_lectures.json", 'w', encoding='utf-8') as f:
        json.dump(additional_lectures, f, indent=4, ensure_ascii=False)
    print("All possible additional lectures saved to all_possible_additional_lectures.json")

# (10_solis) velreiz nofiltret lekcijas un ierakstit excel faila visas, kuras tika lidz galam cauri visiem kriterijiem
    work_with_additional_lectures.convert_json_to_excel(input_data["dates_range"][0], input_data["dates_range"][1])


# (1_solis)
if __name__ == "__main__":
    input_data = {
        "program-name": "Finanšu inženierija (RDCM0)",
        "program-id": "21", # var dabut ja izmantot "inspect" nodarbibas.rtu.lv majaslapas izvelne ar programmam
        "course-id": "1",
        "group-id": "15",
        "programs_range": [11, 94], # var dabut ja izmantot "inspect" nodarbibas.rtu.lv majaslapas izvelne ar programmam
        "dates_range": [12, 25] # ir jaizvelas 2 veselas nedelas bez svetkiem un arkartas saraksta izmainam
    }

    url = "https://nodarbibas.rtu.lv/?lang=lv"
    driver = webdriver.Chrome()
    
    main(driver, input_data, url)
    input()
