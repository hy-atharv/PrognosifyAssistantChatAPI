from flask import Flask, request
import Practo_Scrap
import GeminiAI

app = Flask(__name__)


@app.route('/')
def home():
    return "Chat API Server Running"


@app.route("/chat", methods=['GET', 'POST'])
def Chat():
    if request.method == "POST":
        data = request.get_json()
        location = data.get("location", "")
        chat = data.get("chat", "")
        location = location.lower()
        chat = chat.lower()

        if chat.__contains__('how to book appointment'):
            appointment_info = "To book an appointment with the registered doctors on Prognosify,\nFollow these simple steps:\n- Click on the Consult tab in the Tab Bar\n- Search for different Specialities and according to the fees thats affordable for you, consult with the respective Doctor by clicking on Consult.\n- Then fill the additional notes field and click on Submit."
            return appointment_info

        elif chat.__contains__('find doctors'):
            scraped_data = Practo_Scrap.Scrap(location, 'general')
            return scraped_data

        else:
            answer = GeminiAI.Ask_Gemini(chat)
            return answer


if __name__ == '__main__':
    app.run(debug=True)
