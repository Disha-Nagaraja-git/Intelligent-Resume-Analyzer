INPUT:

#pip install PyPDF2 python-docx scikit-learn

with open("resume.txt", "w") as f:
    f.write("""Name: Disha
Email: disha@gmail.com

Skills:
Python, SQL, Machine Learning, Data Analysis""")

with open("job_description.txt", "w") as f:
    f.write("""Looking for candidate with Python,
SQL, Machine Learning, Data Analysis skills.""")

import re
import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    import PyPDF2
    from docx import Document
except:
    pass


def read_resume(file):
    if file.endswith(".txt"):
        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    elif file.endswith(".pdf"):
        text = ""
        with open(file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text

    elif file.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return ""


def extract_email(text):
    emails = re.findall(r'\S+@\S+', text)
    return emails[0] if emails else "Not Found"


SKILLS_DB = [
    "python", "java", "sql", "machine learning",
    "data analysis", "html", "css", "javascript",
    "c++", "communication", "teamwork"
]


def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS_DB if skill in text]


def calculate_match(resume, job):
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([resume, job])
    score = cosine_similarity(vectors)[0][1]
    return round(score * 100, 2)


def main():

    resume_file = "resume.txt"          
    job_file = "job_description.txt"

    if not os.path.exists(resume_file):
        print("Resume file not found!")
        return

    if not os.path.exists(job_file):
        print("Job description file not found!")
        return

    resume_text = read_resume(resume_file)

    with open(job_file, "r", encoding="utf-8") as f:
        job_text = f.read()

    email = extract_email(resume_text)
    skills = extract_skills(resume_text)
    score = calculate_match(resume_text, job_text)

    if score > 70:
        recommendation = "Strong Candidate"
    elif score > 40:
        recommendation = "Average Match"
    else:
        recommendation = "Low Match"

    report = {
        "Email": email,
        "Skills Found": skills,
        "Match Score (%)": score,
        "Recommendation": recommendation
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\n Resume Analysis Completed\n")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()

OUTPUT:

Resume Analysis Completed

{
    "Email": "disha@gmail.com",
    "Skills Found": [
        "python",
        "sql",
        "machine learning",
        "data analysis"
    ],
    "Match Score (%)": 54.49,
    "Recommendation": "Average Match"
}
