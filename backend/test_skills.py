from skills import extract_skills

text = """
I know Python, Django, FastAPI, GitHub, SQL and Machine Learning.
"""

skills = extract_skills(text)

print(skills)