import spacy
#spaCy is a NLP library for advanced natural language processing in Python.
#Helps computers understand, process, and analyze  human language txt.
#Think of it like a toolbox for text: tokenization,
#named entity recognition, (Detects entities--> eg: Python:LANGUAGE, machine learning:FIELD)
# part-of-speech tagging etc.

from pypdf import PdfReader
#imports the Pdfreader classfrom pypdf library (a library to read PDF files).
#Use: To extract text from PDF files.

import io 
#Provides tools to work with streams , like files in memory. 
#Use: Here, to handle PDF files uploaded as bytes (in-memory file objects).

#Load the spaCy NLP Model.
try:
    nlp = spacy.load("en_core_web_sm")
    #Loads the small English NLP model en_core_web_sm from spaCy.
    #nlp is a variable that will now hold a ready-to-use NLP Pipeline.
except OSError: 
    print("Downloading spaCy model") 
    spacy.cli.download("en_core_web_sm")
    #In spaCy, spacy.cli is a module that contains functions.
    #You normally run from the terminal/command line. 
    #Downloads the NLP model. Happens only once on the system. 

    nlp = spacy.load("en_core_web_sm") 
    #Loads the model again after downloading. so we can use it immediately. 

#The Resume Parsing Agent Function. 
def parse_resume_pdf_agent(pdf_file):
    """Extracts text from a PDF file.""" 
    try:
        reader = PdfReader(io.BytesIO(pdf_file.read())) 
        #pdf_file.read() -> reads the whole pdf file into bytes. 
        #io.BytesIO(...) -> Concerts the bytes into an in-memory file-like object. 
        #PdfReader(...) -> creates a PDF reader object to read the PDF content. 

        text = "" 
        #Initializes an empty string to store the extracted text.

        for page in reader.pages: 
        #Loops through each page in the PDF.

            text += page.extract_text() or "" 
            #page.extract_text() -> extracts text from the current page.
            #or "" -> ensures that if no text is found, it adds an empty string instead of None.
            #text += ... -> appends the extracted text to the text variable.
        return text 
        #Returns all the extracted text from the PDF.

    except Exception as e:
        return f"Error extracting text: {e}" 
    
def parse_resume_txt_agent(txt_file):
    """Extracts text from a TXT file."""
    return txt_file.read().decode("utf-8") 
    #txt_file.getValue() -> Reads the entire content of the uploaded text file as bytes.
    #.decode("utf-8") -> Converts the bytes into a string using UTF-8 encoding.
    #Returns the decoded text content. 

#The Skill Extraction Agent Function.
def extract_skills_agent(text):
    """Extracts skills from text using a pre-defined list.""" 
    skills_list = [
        "python", "java", "c++", "javascript", "sql", "machine learning", 
        "data analysis", "project management", "communication", "leadership",
        "problem solving", "time management", "teamwork", "critical thinking",
        "cloud computing", "aws", "azure", "docker", "kubernetes",
        "agile methodologies", "scrum", "devops", "git", "html", 
        "css", "react", "node.js", "django", "flask"
    ]
    #A list of predefined skills to look for in the resume text. 

    doc = nlp(text.lower()) 
    #Converts text to lowercase -> text.lower()
    #Passes it to nlp(...) -> spaCy breaks the text into tokens, semtences, etc. 
    
    found_skills = {token.text for token in doc if token.text in skills_list} 
    #Set comprehension:
    #Loops over each token in the text. 
    #If token is in the skills_list, include it in found_skills. 
    #{...} -> Creates a set(unique skills only). 

    return found_skills 
    #Returns the set of skills found in the resume. 

#The Candidate Information Agent Function.
def get_candidate_name_agent(resume_text):
    """Extracts a simple name from the first few lines of the text.""" 
    lines = resume_text.strip().split("\n")
    #.strip() -> removes leading/trailing whitespace.
    #.split("\n") -> splits the text into lines based on newline characters.

    if lines:
        #Checks if the list is not empty.

        return lines[0].strip()
        #Returns the first line (assumed to be the name) after stripping whitespace. 

    return "Unknown Candidate"
    #If no lines found, returns a default name. 
     
#The Scoring & Ranking Agent Function. 
def calculate_score_agent(resume_skills, job_skills):
    """Calculates a match score based on shared skills."""
    if not job_skills:
        return 0.0 
        #If job_skills is empty, return a score of 0.0 to avoid division by zero.

    matched_skills = resume_skills.intersection(job_skills)
    #Finds the common skills between resume_skills and job_skills.

    score = (len(matched_skills) / len(job_skills)) * 100
    #Calculates the score as a percentage of matched skills to total job skills.
     
    return round(score, 2)
    #Rounds the score to 2 decimal places and returns it.   

#Summary:
#1) Imports -> bring in libraries for NLP and PDF handling.
#2) Load spaCy model -> sets up NLP capabilities.
#3) Define agents -> functions to parse resumes, extract skills, get names, and calculate scores.
#4) Each agent has a specific task, making the code modular and easy to maintain.
