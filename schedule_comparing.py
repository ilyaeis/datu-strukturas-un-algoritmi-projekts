import json
import os 
import time 

def parse_lecture(lecture):
    lecture = lecture.replace("Lekc. ", "").replace("Lab.d. ", "").replace("Pr.d. ", "").replace("Lekc, Pr.d.", "").replace("Lekc,", "")
    lecture = lecture.split(",")[0].strip()
    return lecture 

def get_before_after_lecture_times(time):
    time_to_number = [
        "8:15 - 9:50",
        "10:15 - 11:50",
        "12:30 - 14:05",
        "14:30 - 16:05",
        "16:30 - 18:05",
        "18:15 - 19:50"
    ]
    previous_time = None
    next_time = None
    if time in time_to_number:
        index = time_to_number.index(time)
        if index == 0:
            next_time = time_to_number[index + 1]
        elif index == len(time_to_number) - 1:
            previous_time = time_to_number[index - 1]
        else:
            previous_time = time_to_number[index - 1]
            next_time = time_to_number[index + 1]
            
    return previous_time, next_time        

def get_main_lectures(main_schedule):
    main_lectures = {} # {lecture: {date: [time, time], date: [time]}/False (validity)}
    for date, lectures in main_schedule.items():
        if not lectures:
            continue
        for time, lecture in lectures.items():
            if not lecture:
                continue
            lecture = parse_lecture(lecture)
            if lecture not in main_lectures:
                main_lectures[lecture] = {}
            if date not in main_lectures[lecture]:
                main_lectures[lecture][date] = []
            if time not in main_lectures[lecture][date]:
                main_lectures[lecture][date].append(time)
    return main_lectures

def algorithm_to_compare_main_schedule_to_additional_schedules(main_schedule, main_lectures, additional_schedule):
    additonal_checked_lectures = {}
    for date, lectures in additional_schedule.items():
        if not lectures:
            continue
        for time, lecture in lectures.items():
            if not lecture:
                continue
            print(lecture)
            lecture = parse_lecture(lecture)
            print(f"Lecture: {lecture} {date} {time}")
            # check if starts with Kons. or Eks\u010m remove
            if lecture.startswith("Kons.") or lecture.startswith("Eks\u0101m"):
                print(f"Lecture {lecture} is Kons. or Eks\u0101m.")
                additonal_checked_lectures[lecture] = False
                continue
            if lecture in main_lectures:
                print(f"Lecture {lecture} is already in main lectures.")
                additonal_checked_lectures[lecture] = False
                continue
            if main_schedule.get(date) and main_schedule[date].get(time):
                print(f"During {date} at {time} some lecture is already in main schedule.")
                additonal_checked_lectures[lecture] = False
                continue
            if lecture in additonal_checked_lectures and additonal_checked_lectures[lecture] != False:
                print(f"Lecture {lecture} is already in additional lectures and it is valid.")
                if date not in additonal_checked_lectures[lecture]:
                    additonal_checked_lectures[lecture][date] = []
                if time not in additonal_checked_lectures[lecture][date]:
                    additonal_checked_lectures[lecture][date].append(time)
                print(f"Added {lecture} {date} {time} to additional lectures.")
                continue
            if lecture not in additonal_checked_lectures:
                print(f"Lecture {lecture} is not in additional checked lectures.")
                additonal_checked_lectures[lecture] = {}      
                if date not in additonal_checked_lectures[lecture]:
                    additonal_checked_lectures[lecture][date] = []
                if time not in additonal_checked_lectures[lecture][date]:
                    additonal_checked_lectures[lecture][date].append(time)
                print(f"Added {lecture} {date} {time} to additional checked lectures.")
                continue
    print("Additional lecturesss:\n", json.dumps(additonal_checked_lectures, indent=4))
    return additonal_checked_lectures

def update_additional_lectures(program_title, additional_lectures, main_schedule, main_lectures, schedule):
    additonal_checked_lectures = algorithm_to_compare_main_schedule_to_additional_schedules(main_schedule, main_lectures, schedule)
    for lecture, dates in additonal_checked_lectures.items():
        if dates:
            lecture = f"{program_title} ||| {lecture}"
            for date, times in dates.items():
                if date not in additional_lectures:
                    additional_lectures[date] = {}
                for lecture_time in times:
                    if lecture_time not in additional_lectures[date]:
                        additional_lectures[date][lecture_time] = []
                    if lecture not in additional_lectures[date][lecture_time]:
                        additional_lectures[date][lecture_time].append(lecture)
    return additional_lectures        
                        
if __name__ == "__main__":
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    schedules = {}
    for json_file in json_files:
        if json_file != "main_schedule.json":
            with open(json_file, 'r', encoding='utf-8') as f:
                schedules[json_file.replace(".json", "")] = json.load(f)

    with open("main_schedule.json", 'r', encoding='utf-8') as f:
        main_schedule = json.load(f)
        
    main_schedule = main_schedule
    print("Main schedule data:\n", json.dumps(main_schedule, indent=4))
    main_lectures = get_main_lectures(main_schedule)
    print("Main lectures:\n", json.dumps(main_lectures, indent=4))
    additional_lectures = {} # {date: {time: [lectures]}}
    for program_title, schedule in schedules.items():
        additional_lectures = update_additional_lectures(program_title, additional_lectures, main_schedule, main_lectures, schedule)
    print("Additional lectures:\n", json.dumps(additional_lectures, indent=4))