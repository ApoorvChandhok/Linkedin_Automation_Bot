'''





License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            




version:    26.01.20.5.08
'''


###################################################### APPLICATION INPUTS ######################################################


# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

# Give an relative path of your default resume to be uploaded. If file in not found, will continue using your previously uploaded resume in LinkedIn.
default_resume_path = "all resumes/default/resume.pdf"      # Resume path relative to project root

# What do you want to answer for questions that ask about years of experience you have, this is different from current_experience? 
years_of_experience = '3'          # A number in quotes Eg: "0","1","2","3","4", etc.

# Per-skill experience in years. Keys are matched (partial, case-insensitive) against the question label.
# Add any skill you know here with how many years of experience you have.
# Questions about skills NOT listed here will receive min_experience_for_unknown_skills as the answer.
skill_experience = {
    "# --- Cloud & DevOps ---
    "aws": 1,
    "# --- Core Skills ---
    "python": 3,
    "# --- Data & Big Data ---
    "pyspark": 2,
    "# --- Databases ---
    "mysql": 3,
    "# --- ML / AI (add only if you have some exposure) ---
    "machine learning": 1,
    "# --- Web / Other Frameworks (minimal exposure) ---
    "flask": 1,
    "CI/CD": 3,
    "api": 2,
    "automation": 3,
    "azure": 1,
    "big data": 2,
    "data analysis": 3,
    "data analytics": 3,
    "data pipeline": 2,
    "deep learning": 1,
    "django": 1,
    "docker": 1,
    "etl": 2,
    "excel": 3,
    "fastapi": 1,
    "gcp": 1,
    "git": 2,
    "linux": 2,
    "mongodb": 1,
    "nosql": 1,
    "numpy": 2,
    "pandas": 3,
    "postgresql": 2,
    "power bi": 2,
    "rest api": 2,
    "scikit": 1,
    "spark": 2,
    "sql": 3,
    "tableau": 1,
    "tensorflow": 1
}

# For skills NOT found in skill_experience above, answer with this number (avoids 0-year rejection)
min_experience_for_unknown_skills = "1"

# Do you need visa sponsorship now or in future?
require_visa = "No"               # "Yes" or "No"

# What is the link to your portfolio website, leave it empty as "", if you want to leave this question unanswered
website = "https://github.com/ApoorvChandhok"                   # "www.example.bio" or "" and so on....

# Please provide the link to your LinkedIn profile.
linkedIn = 'https://www.linkedin.com/in/apoorvchandhok/'        # "https://www.linkedin.com/in/example" or "" and so on...

# What is the status of your citizenship? # If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
# Valid options are: "U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident" or "Other"
us_citizenship = "Other"

# Dict mapping question keywords to standardized answers for Dropdowns and Radios.
# Extend these phrases or mappings to accurately handle binary/categorical questions.
categorical_answers = {
    ("sponsorship", "visa"): require_visa,
    ("citizenship", "employment eligibility"): us_citizenship,
    # Standard responses for general questions
    ("agree to the terms", "consent", "terms and conditions", "privacy policy"): "Yes",
    ("felony", "criminal", "misdemeanor"): "No"
}

## SOME ANNOYING QUESTIONS BY COMPANIES 🫠 ##

# What to enter in your desired salary question (American and European), What is your expected CTC (South Asian and others)?, only enter in numbers as some companies only allow numbers,
desired_salary = 1000000          # 10 LPA = 1000000. Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your expected CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 1000000 will be answered as "10.00"
* 500000 will be answered as "5.00"
And if asked in months, then it will divide by 12 and answer. Examples:
* 1000000 will be answered as "83333"
* 500000 will be answered as "41666"
'''

# What is your current CTC? Some companies make it compulsory to be answered in numbers...
current_ctc = 500000            # 5 LPA = 500000. Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your current CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
# And if asked in months, then it will divide by 12 and answer. Examples:
# * 2400000 will be answered as "200000"
# * 850000 will be answered as "70833"
'''

# (In Development) # Currency of salaries you mentioned. Companies that allow string inputs will add this tag to the end of numbers. Eg: 
# currency = "INR"                 # "USD", "INR", "EUR", etc.

# What is your notice period in days?
notice_period = 0                    # Immediate joiner. Any number >= 0 without quotes. Eg: 0, 7, 15, 30, 45, etc.
'''
Note: If question has 'month' or 'week' in it (Example: What is your notice period in months), 
then it will divide by 30 or 7 and answer respectively. Examples:
* For notice_period = 66:
  - "66" OR "2" if asked in months OR "9" if asked in weeks
* For notice_period = 15:"
  - "15" OR "0" if asked in months OR "2" if asked in weeks
* For notice_period = 0:
  - "0" OR "0" if asked in months OR "0" if asked in weeks
'''

# Your LinkedIn headline in quotes Eg: "Software Engineer @ Google, Masters in Computer Science", "Recent Grad Student @ MIT, Computer Science"
linkedin_headline = "Associate Data Analyst @ Wipro | Data Analysis, Automation, Python" # "Headline" or "" to leave this question unanswered

# Your summary in quotes, use \n to add line breaks if using single quotes "Summary".You can skip \n if using triple quotes """Summary"""
linkedin_summary = """
I'm Apoorv Chandhok, an Associate Data Analyst at Wipro with 3.5 years of experience in Python, data analysis, SQL, and automation. I specialize in building data pipelines, automation scripts, and delivering actionable insights from large datasets.
"""

'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Your cover letter in quotes, use \n to add line breaks if using single quotes "Cover Letter".You can skip \n if using triple quotes """Cover Letter""" (This question makes sense though)
cover_letter = """
Dear Hiring Manager,

I am Apoorv Chandhok, an Associate Data Analyst at Wipro with 3.5 years of hands-on experience in Python, data analysis, SQL, and automation. I am an immediate joiner, eager to bring my analytical and technical skills to your team.

During my time at Wipro, I have built automated data pipelines, performed large-scale data analysis, and delivered insights that directly impacted business decisions. I am proficient in Python, Pandas, PySpark, SQL, and big data tools.

I am excited about this opportunity and confident I can make an immediate contribution. Thank you for your consideration.

Best regards,
Apoorv Chandhok
"""
##> ------ Dheeraj Deshwal : dheeraj9811 Email:dheeraj20194@iiitd.ac.in/dheerajdeshwal9811@gmail.com - Feature ------

# Your user_information_all letter in quotes, use \n to add line breaks if using single quotes "user_information_all".You can skip \n if using triple quotes """user_information_all""" (This question makes sense though)
# We use this to pass to AI to generate answer from information , Assuing Information contians eg: resume  all the information like name, experience, skills, Country, any illness etc. 
user_information_all ="""
Name: Apoorv Chandhok
Current Role: Associate Data Analyst at Wipro
Experience: 3.5 years
Skills: Python, SQL, Data Analysis, Automation, PySpark, Big Data, Pandas, NumPy, Power BI, Excel, Data Pipelines
Education: Bachelor's Degree (No Masters)
Location: Gurgaon, Haryana, India
Phone: 9999424997
Email: apoorv.chandhok1999@gmail.com
LinkedIn: https://www.linkedin.com/in/apoorvchandhok/
GitHub: https://github.com/ApoorvChandhok
Expected Salary: 10 LPA
Current Salary: 5 LPA
Notice Period: Immediate joiner
Visa: Not required (Indian citizen)
"""
##<
'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Name of your most recent employer
recent_employer = "Wipro"          # "", "Lala Company", "Google", "Snowflake", "Databricks"

# Example question: "On a scale of 1-10 how much experience do you have building web or mobile applications? 1 being very little or only in school, 10 being that you have built and launched applications to real users"
confidence_level = "7"             # Any number between "1" to "10" including 1 and 10, put it in quotes ""
##



# >>>>>>>>>>> RELATED SETTINGS <<<<<<<<<<<

## Allow Manual Inputs
# Should the tool pause before every submit application during easy apply to let you check the information?
pause_before_submit = True         # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''

# Should the tool pause if it needs help in answering questions during easy apply?
# Note: If set as False will answer randomly...
pause_at_failed_question = True    # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''
##

# Do you want to overwrite previous answers?
overwrite_previous_answers = False # True or False, Note: True or False are case-sensitive







############################################################################################################
'''
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,

'''
############################################################################################################