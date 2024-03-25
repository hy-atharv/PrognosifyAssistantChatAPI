import google.generativeai as genai


GOOGLE_API_KEY = 'AIzaSyBKumofJExXh_kyOYCn_HSL43Qgv4QVr-w'

genai.configure(api_key=GOOGLE_API_KEY)


def Ask_Gemini(query):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    return response.text

#print(Ask_Gemini("What is Myocardial Infarction?"))
