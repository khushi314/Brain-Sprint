import os                           #built-i library of python,used to intract with system environmental variable
import json                         #to parse(decode) and stringify(encode) json data
from google import genai            #new google genai SDK to access gemini models
from google.genai import types      #used to define and configure different different data types of API

#initialise the gemini client
#it automatically picks up the GEMINI_API_KEY from environment variables
client = genai.Client()

def generate_quiz(topic_name: str, num_questions: int, subject: str = "General"):
    #docstring which shows the purpose of function
    """
    Asks Gemini 3.0 Flash to generate a 3-question quiz in a strict JSON format.

    """
    #define the instruction for the AI MASTER Agent
    prompt= f"""
    you are an expert Quiz Master Agent.
    Generate {num_questions} multiple choice question about the topic: '{topic_name}'under the subject:'{subject}'.
    The questions should test conceptual understanding and logic.
    provide the output in a strict JSON array format. Do not include markdown formatting like json.
    Each object in the array must follow this exact structure:
    [
    {{
       
        "question":"the question text here",
        "options":["Option A","Option B","Option C","Option D"],
        "correct_answer":"The exact correct option text"
        "explanation":"A short 1-2 line conceptual theory description about why this option is correct"

        
    }}
    ]

"""
    try:
        #send the request to Gemini Server using ner SDK syntex
        response= client.models.generate_content(model='gemini-2.5-flash', contents=prompt,) #main API call

        #convert the row text string from Gemini into a Python list/dictionary
        #the response from gemini is just a raw text string.json.loads()parses this string and converts it into a python list or dictionary ,making it easy to loop throgh and extract the data
        quiz_data=json.loads(response.text)
        return quiz_data
    
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return None
    

if __name__=="__main__":
    #test if the file loads correctly without syntex errors
    print("Agent file loaded perfectly")

#if __name__=="__main__":
    #print("testing gemini AI agent")
    #test_quiz = generate_quiz("function","python")
    #print(json.dumps(test_quiz, indent=4))    


    
