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
# salidzinat pamata sarakstu ar parejiem sarakstiem

    additonal_checked_lectures = {}

# nem visas lekcijas vienam datumam
    for date, lectures in additional_schedule.items():
        if not lectures:
            continue

# nem vienu lekciju no visam
        for time, lecture in lectures.items():
            if not lecture: # ja nav taja diena
                continue
            print(lecture)

            lecture = parse_lecture(lecture) # attirit no liekiem elementiem nosaukumu
            print(f"Lecture: {lecture} {date} {time}")

            if lecture.startswith("Kons.") or lecture.startswith("Eks\u0101m"): # ja lekcija ir eksamens vai konsultacija
                print(f"Lecture {lecture} is Kons. or Eks\u0101m.")
                additonal_checked_lectures[lecture] = False # nedzes bet vnk apzime ka neder
                continue

            if lecture in main_lectures: # ja tads prieksmets jau ir musu pamatsaraksta
                print(f"Lecture {lecture} is already in main lectures.")
                additonal_checked_lectures[lecture] = False # nedzes bet vnk apzime ka neder
                continue

            if main_schedule.get(date) and main_schedule[date].get(time): # ja taja laika mums jau notiek lekcijas
                print(f"During {date} at {time} some lecture is already in main schedule.")
                additonal_checked_lectures[lecture] = False # nedzes bet vnk apzime ka neder
                continue

# parbauda vai lekcija notiek vairakas reizes viena nedela lai butu iespeja apmeklet visas
            if lecture in additonal_checked_lectures and additonal_checked_lectures[lecture] != False:
                print(f"Lecture {lecture} is already in additional lectures and it is valid.")

                if date not in additonal_checked_lectures[lecture]: # ja tadam datumam vel nav pierakstita
                    additonal_checked_lectures[lecture][date] = []
                if time not in additonal_checked_lectures[lecture][date]: # ja tadam laikam vel nav pierakstita
                    additonal_checked_lectures[lecture][date].append(time)
                print(f"Added {lecture} {date} {time} to additional lectures.")
                continue

# ja visi ieprieksejie kriteriji tika nokartoti, tad vienkarsi pievienot jaunu ierakstu
            if lecture not in additonal_checked_lectures:
                print(f"Lecture {lecture} is not in additional checked lectures.")
                additonal_checked_lectures[lecture] = {}      
                if date not in additonal_checked_lectures[lecture]: # ja tadam datumam vel nav pierakstita
                    additonal_checked_lectures[lecture][date] = []
                if time not in additonal_checked_lectures[lecture][date]: # ja tadam laikam vel nav pierakstita
                    additonal_checked_lectures[lecture][date].append(time)
                print(f"Added {lecture} {date} {time} to additional checked lectures.")
                continue
    print("Additional lecturesss:\n", json.dumps(additonal_checked_lectures, indent=4))

# atgriezt visas parbauditas papildus lekcijas konkretai grupai
    return additonal_checked_lectures

def update_additional_lectures(program_title, additional_lectures, main_schedule, main_lectures, schedule):
# papildinat jau ieprieks izveidotu datni ar lekcijam ar jaunam tikko parbautitam lekcijam nakamai grupai

# parbaudit konkretas grupas lekciju atbilstibu musu kriterijiem
    additonal_checked_lectures = algorithm_to_compare_main_schedule_to_additional_schedules(main_schedule, main_lectures, schedule) # {lecture: {date: {time: [string]}}}

# pierakstit katru lekciju lielai datnei ar visam derigam papildus lekcijam no vasam grupam
    for lecture, dates in additonal_checked_lectures.items():

        if dates: # papildus parbaude katram gadijumam lai nedabut liekas kludas
            lecture = f"{program_title} ||| {lecture}" # nomainit attelosanas formatu turpmakai saglabasanai
            for date, times in dates.items():
                if date not in additional_lectures: # ja tads datums vel nav pierakstits
                    additional_lectures[date] = {}
                for lecture_time in times:
                    if lecture_time not in additional_lectures[date]: # ja tads laiks vel nav pierakstits tadam datumam
                        additional_lectures[date][lecture_time] = []
                    if lecture not in additional_lectures[date][lecture_time]:  # ja tada lekcija vel nav pierakstita tadam laikam
                        additional_lectures[date][lecture_time].append(lecture)

# atgriezt atjaunotu sarakstu ar visam papildus lekcijam no visam iepreiks parbauditam grupam
    return additional_lectures        
