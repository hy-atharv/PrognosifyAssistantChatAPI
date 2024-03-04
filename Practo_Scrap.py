import requests
import re
from bs4 import BeautifulSoup

proxy = {
    "https": "https://91.25.93.174:3128"
}


# the location and the keywords has to be sent by the app
# the keywords should include the gynao,dermi,ent,general,dentist,homeo,ayurveda
# we have to take Dermatologist , Ear-nose-throat , Genral Physicain , Dentist , Gynecologist , Homoeopath , Ayurveda
# location=["Chennai","Mumbai","Banglore","Delhi","Agra","Gurgaon"]
# location = str(input("Enter Location: "))
# location = location.lower()
# category = str(input("Enter Category: "))
# category = category.lower()


def Scrap(location, category):
    result = []
    doc = ""
    gynao = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22Gynecologist"
             "%2Fobstetrician%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city"
             "=") + location
    dermi = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22dermatologist%22%2C"
             "%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") + location
    ent = (("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22Ear-nose-throat%20("
            "ent)%20Specialist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") +
           location)
    general = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22General%20Physician"
               "%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") + location
    dentist = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22dentist%22%2C"
               "%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") + location
    homeo = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22Homoeopath%22%2C"
             "%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") + location
    ayurveda = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22Ayurveda%22%2C"
                "%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") + location
    cardio = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22cardiologist%22%2C"
              "%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") + location
    neuro = ("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22neurologist%22%2C"
             "%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") + location
    immune = (("https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22allergist"
               "%2Fimmunologist%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=") +
              location)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
    # change the category from here
    if str(category) == "gynao":
        category = gynao
    elif category == "dermi":
        category = dermi
    elif category == "ent":
        category = ent
        doc = "Ear-Nose-Throat (ENT) Specialist"
    elif category == "general":
        category = general
    elif category == "dentist":
        category = dentist
    elif category == "homeo":
        doc = "Homeopath"
        category = homeo
    elif category == "ayurveda":
        category = ayurveda
    elif category == "cardio":
        category = cardio
    elif category == "neuro":
        category = neuro
    elif category == "immune":
        category = immune
    else:
        category = general
    r = requests.get(category).text
    soup = BeautifulSoup(r, 'lxml')
    name = soup.find_all('h2', class_="doctor-name")
    clinic = soup.find_all('div', class_="u-d-inlineblock u-valign--middle")
    add1 = soup.find_all('span', {'data-qa-id': "doctor_clinic_name"})
    add2 = soup.find_all('span', {'data-qa-id': "practice_locality"})
    fees = soup.find_all('span', {'data-qa-id': "consultation_fee"})
    rating = soup.find_all('span', {'data-qa-id': "doctor_recommendation"})
    for (n, a1, a2, f, r) in zip(name, add1, add2, fees, rating):
        entry = [
            "Doctor Name: " + n.text,
            "Clinic/Hospital: " + a1.text + " " + a2.text + " " + location,  # Combine address lines
            "Consultation Fees: " + f.text,
            "Doctor Recommendation: " + r.text
        ]
        result.append(entry)
    res = ""
    for lst in result:
        for item in lst:
            res += item + "\n"
        res += "\n"

    print(res)
    return res

# Scrap(location, category)
