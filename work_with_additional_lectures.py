import json
from datetime import datetime
import pandas as pd


def convert_json_to_excel(start_date, end_date):
# pamatfunkcija lai nofiltret lekcijas pec parejiem kriterijiem un saglabat Excel faila

    def duration_in_minutes(lecture_time):
# parbaudit lekcijas ilgumu minutes
        try:
            start_str, end_str = lecture_time.split(" - ")  # piemeram "08:15 - 09:50" --> "8:15" un "09:50"
            start = datetime.strptime(start_str, "%H:%M")
            end = datetime.strptime(end_str, "%H:%M")
            delta = end - start
            return delta.total_seconds() / 60  # atgriezt lekcijas ilgumu minutes
        except Exception as e:
            print(f"Warning: could not parse time slot '{lecture_time}': {e}")
            return None

# izgut datus no json faila
    with open("all_possible_additional_lectures.json", "r", encoding="utf-8") as f:
        additional_lectures = json.load(f)

# definet "dictionary" strukturu datu glabasanai
    combined_data = {
        "Pirmā nedeļa": {},
        "Otrā nedeļa": {},
    }

# lai izvairities no vakara un nestandarta lekcijam
    allowed_lecture_start_times = {"08:15", "10:15", "12:30", "14:30", "16:30"}

# panemt un apstradat katru lekciju
    for date_str, schedule_for_one_day in additional_lectures.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # parveidot no str uz obj veidu lai vieglak operet ar datumiem

        if date_obj.weekday() >= 5:  # ja nav darba diena
            continue

        if not (start_date <= date_obj.day <= end_date):  # ja diena nav ieklauta parbaudes diapazona
            continue

# parbaudit kurai nedeļai atbilst lekcija
        reference_date = date_obj.replace(day=start_date)
        days_difference = (date_obj - reference_date).days
        week_type = "Pirmā nedeļa" if (days_difference // 7) % 2 == 0 else "Otrā nedeļa"
        weekday = date_obj.weekday()

        if weekday not in combined_data[week_type]: # izveidot jaunu sadalijumu pec dienam
            combined_data[week_type][weekday] = {}

# parbaudit katru lekciju kopas laiku vienas dienas ietvaros
        for lecture_time, lectures in schedule_for_one_day.items():
            try:
                lecture_start_time = lecture_time.split(" - ")[0]  # dabut lekcijas sakuma laiku
            except Exception as e:
                print(f"Warning: skipping invalid time slot '{lecture_time}': {e}")
                continue

            if lecture_start_time not in allowed_lecture_start_times:  # ja sakuma laiks neatbilst derigiem
                continue

            duration = duration_in_minutes(lecture_time)  # dabut lekcijas ilgumu
            if duration is None or duration > 120:  # ja lekcijai ir nestandarta ilgums
                continue

            if lecture_time not in combined_data[week_type][weekday]: # izveidot jaunu sadalijumu pec laika
                combined_data[week_type][weekday][lecture_time] = {}

# parbaudit katru lekciju no viena laika lekciju kopas
            for lecture in lectures:
                try:
# sadalit lekcijas informaciju iz atseviskiem mainigiem mosaukumam un lekcijai
                    group_info, lecture_name = lecture.split(" ||| ")  # piemeram bija "Datorsistēmas (RDBD0)_2_8 ||| Datu bāzu vadības sistēmas"
                except ValueError:
                    continue

                lecture_name = lecture_name.strip()
                group_info = group_info.strip()

# izveidot jaunu sadalijumu pec lekcijas nosaukumiem un definet vajadzigus parametrus
                if lecture_name not in combined_data[week_type][weekday][lecture_time]:
                    combined_data[week_type][weekday][lecture_time][lecture_name] = {
                        "group_count": 0,
                        "group": None
                    }

                lecture_result = combined_data[week_type][weekday][lecture_time][lecture_name]
                lecture_result["group_count"] += 1

# atseviski vajag ierakstit vienu grupu, lai varetu manuali parbaudit nodarbibas.rtu.lv un parliecinaties par programmas pareizibu
                if lecture_result["group"] is None:
                    lecture_result["group"] = group_info

    rows = []
    weekdays = {0: "Pirmdiena", 1: "Otrdiena", 2: "Trešdiena", 3: "Ceturtdiena", 4: "Piektdiena"}

# parmeklet abas nedelas
    for week_type in ["Pirmā nedeļa", "Otrā nedeļa"]:
# parmeklet visas darba dienas
        for weekday in range(5):
            if weekday not in combined_data[week_type]:
                continue

            weekday_name = weekdays[weekday]

# parmeklet visus laikus katrai dienai
            for lecture_time in combined_data[week_type][weekday].keys():
                lectures = combined_data[week_type][weekday][lecture_time]

# parmeklet visas lekcijas katram laikam
                for lecture_name in lectures.keys():
                    lecture_result = lectures[lecture_name]
# galu gala pievienot konkretu lekciju massivam "rows" lai pariet pie rezultata sakasrtosanas un saglabasanas
                    rows.append({
                        "Nedeļas kārta": week_type,
                        "Diena": weekday_name,
                        "Laiks": lecture_time,
                        "Nosaukums": lecture_name,
                        "Grupu skaits": lecture_result["group_count"],
                        "Grupas piemērs": lecture_result["group"]
                    })

# izveidot dataframe
    df = pd.DataFrame(rows)

# pievieno kolonnu "dienas numurs" lai sortet pec dienu numuriem nevis alfabeta
    df["Dienas numurs"] = df["Diena"].map({"Pirmdiena": 0, "Otrdiena": 1, "Trešdiena": 2, "Ceturtdiena": 3, "Piektdiena": 4})
# sorte datus pec vairakiem kriterijiem, izmanto apvienoti merge un insertion sort
    df.sort_values(by=["Nedeļas kārta", "Dienas numurs", "Laiks", "Nosaukums"], inplace=True)
# izdzes lieko kolonnu "dienas numurs"
    df.drop(columns=["Dienas numurs"], inplace=True)

# saglaba tabulu Excel faila
    df.to_excel("result.xlsx", index=False)
    print("Output written to 'result.xlsx'")