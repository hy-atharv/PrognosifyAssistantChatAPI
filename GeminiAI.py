import google.generativeai as genai


GOOGLE_API_KEY = 'AIzaSyA13K0uJP5ti0R6eCy_ogK0UlqenbFfr_o'

genai.configure(api_key=GOOGLE_API_KEY)


def Ask_Gemini(query):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    return response.text

#print(Ask_Gemini("What is Myocardial Infarction?"))
