import streamlit as st
import pandas as pd
#Brings in pandas for working with data tables (DataFrames).
from agent_logic import (
    parse_resume_pdf_agent,
    parse_resume_txt_agent,         
    extract_skills_agent,
    calculate_score_agent,
    get_candidate_name_agent
)
#Imports specific functions from agent_logic.py for various tasks.
 
st.set_page_config(
    page_title = "Recruitment AI Agent",
    page_icon = "🔍",
    layout = "centered",
)
#Sets up the look and feel of the Streamlit app page.
#page_title -> title in browser tab.
#page_icon -> icon in browser tab (empty here).
#layout -> centers the content on the page.

st.title("Recruitment AI Agent")
st.subheader("Automate Resume Screening with AI") 
#Big title and subtitle for the app.

#------User Inputs------ 
job_description = st.text_area(
    "Paste the Job Description here:",
    height=200,
    placeholder="e.g., Looking for a skilled Python developer with experience in machine learning and data analysis.",
) 
#Creates a large text area for users to input the job description.
#job_description -> variable to hold the input text.
#height -> sets the height of the text area.
#placeholder -> example text shown when the area is empty.

uploaded_resumes = st.file_uploader(
    "Upload Resumes (.pdf or .txt):",
    type=["pdf", "txt"],
    accept_multiple_files=True,
) 
#Lets user upload resumes. 
#type -> restricts to PDF and TXT files.
#accept_multiple_files -> allows uploading more than one file. 

#------Agent Logic and Results Display------
if st.button("Screen candidates", use_container_width=True):
    if job_description and uploaded_resumes:
        with st.spinner("Screening candidates..."):
            job_skills = extract_skills_agent(job_description)
            candidate_results = []
            for resume_file in uploaded_resumes:
                file_extension = resume_file.name.split(".")[-1].lower()
                if file_extension == "pdf":
                    resume_text = parse_resume_pdf_agent(resume_file)  
                elif file_extension == "txt":
                    resume_text = parse_resume_txt_agent(resume_file)
                else:
                    st.warning(f'Skipping unsupported file type: {resume_file.name}')
                    continue 
                resume_skills = extract_skills_agent(resume_text)
                score = calculate_score_agent(resume_skills, job_skills)

                candidate_results.append({
                    "Candidate Name": get_candidate_name_agent(resume_text),
                    "Match Score": score,
                    "File name": resume_file.name, 
                    "Matching Skills": ", ".join(resume_skills.intersection(job_skills)),
                }) 

        candidate_results.sort(key=lambda x: x["Match Score"], reverse=True)

        st.success("Screening complete!")
        st.markdown("---") 
        st.header("Candidate Rankings")

        df = pd.DataFrame(candidate_results)
        st.dataframe(df, use_container_width=True)  

        st.markdown("---")
        st.header("Detailed Analysis") 

        for candidate in candidate_results:
            st.subheader(f"Analysis for {candidate['Candidate Name']}") 
            st.metric("Match Score", f"{candidate["Match Score"]}%")
            st.markdown("**Matching Skills:**")
            
            if candidate["Matching Skills"]:
                st.code(candidate["Matching Skills"]) 
            else:
                st.warning("No matching skills found.")
    else:
        st.warning("Please provide a job description and upload at least one resume.")




