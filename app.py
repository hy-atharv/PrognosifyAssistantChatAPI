from flask import Flask, request, jsonify
from langchain.chains import LLMChain
import Practo_Scrap
import GeminiAI
from tempfile import NamedTemporaryFile
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyDzgWoLfkzBQjvfDmIPLsP7DfnIAEqHnnE'

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                               temperature=0.3, google_api_key=GOOGLE_API_KEY)


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


@app.route("/reportAI", methods=['GET', 'POST'])
def summariser():
    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file is not None:
            # Save the uploaded file to a temporary location
            with NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            loader = PyPDFLoader(temp_file_path)
            pages = loader.load()
            context = "\n".join(str(p.page_content) for p in pages[:30])

            template = '''Analyse and summarize the given context which is a medical report, in simple and easy to understand language, and generate medical insights/advices from it that the patient should follow:\n\n
            Context:\n{context}\n\n
            
            
             "Summary" : a paragraph for summary,
             "Insights" : a paragraph for insights
            
            Output should be exactly in the above JSON format
            
            Answer:
            '''

            prompt_template = PromptTemplate(input_variables=["context"], template=template)
            # chain = LLMChain(model=model, prompt=prompt_template)
            stuff_chain = load_qa_chain(model, chain_type="stuff", prompt=prompt_template)

            answer = stuff_chain(
                {"input_documents": pages[1:]}, return_only_outputs=True
            )

            return jsonify(answer['output_text'])

        else:

            return "No File Received at Backend"


@app.route("/LifestyleAI", methods=['GET', 'POST'])
def lifestyle():
    if request.method == 'POST':
        data = request.get_json()
        bmi = data.get("bmi", "")
        avg_sleep = data.get("sleep", "")
        steps = data.get("steps", "")
        cal = data.get("calories", "")
        gender = data.get("gender", "")
        age = data.get("age", "")

        context = "Age: " + age + "\nGender: " + gender + "\nBody Measure Index: " + bmi + "\nCalories(kcal) burnt by walking in last week: " + cal + "\nTotal steps walked in last week: " + steps + "\nAverage sleep duration in last week: " + avg_sleep

        template = '''Given below is the Lifestyle Data of a user in the last week. Analyze it thoroughly and medically and calculate an appropriate Lifestyle Score out of 100 based on the data given, give valuable health insights from this data and advise some personalized steps for this user to follow daily to live a better Lifestyle:\n\n
        {context}\n\n
        
        "Lifestyle_Score" : a numerical score out of 100,
        "Health_Insights" : a paragraph for health insights,
        "Steps" : a paragraph for personalized steps
        
        Output should be exactly in the above JSON format
            
        Answer:
        '''

        prompt_template = PromptTemplate(input_variables=["context"], template=template)
        chain = LLMChain(llm=model, prompt=prompt_template)
        #stuff_chain = load_qa_chain(model, chain_type="stuff", prompt=prompt_template)

        answer = chain.run(context)

        return jsonify(answer)




if __name__ == '__main__':
    app.run(debug=True)
