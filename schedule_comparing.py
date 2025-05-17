import json

def parse_lecture(lecture):
# attirit lekciju nosaukumus no liekiem parametriem
    lecture = lecture.replace("Lekc. ", "").replace("Lab.d. ", "").replace("Pr.d. ", "").replace("Lekc, Pr.d.", "").replace("Lekc,", "")
    lecture = lecture.split(",")[0].strip()
    return lecture        

def get_main_lectures(main_schedule):
# bija ---> main_schedule = {date: {time: {lecture_name}} jeb kalendars
# bus ---> main_lectures = {lecture: {date: [time, time], date: [time]}/False (validity)} jeb sadalijums pec lekcijam

    main_lectures = {}

# cikls ar katru dienu (visas lekcijas - lectures) pec datumiem
    for date, lectures in main_schedule.items():
        if not lectures: # ja tai dienai nav lekciju
            continue

# cikls ar lekciju (viena lekcija - lecture) pec laikiem
        for time, lecture in lectures.items():
            if not lecture: # ja tam laikam nav lekcijas
                continue

# izdzest liekus lekcijas nosaukuma elementus
            lecture = parse_lecture(lecture)

            if lecture not in main_lectures: # ja lekcijas ar tadu nosaukumu vel nav in main_lectures
                main_lectures[lecture] = {}
            if date not in main_lectures[lecture]: # ja lekcijas datums vel nav pievienots
                main_lectures[lecture][date] = []
            if time not in main_lectures[lecture][date]: # ja lekcijas laiks taja datuma vel nav pievienots
                main_lectures[lecture][date].append(time)
# atgriezt sarakstu ar lekcijam ka galveno parametri
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
