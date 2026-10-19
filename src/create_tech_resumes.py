"""Texniki karyera CV-ləri üçün sintetik təlim datası yaradır.

Niyə lazımdır: data/raw/resumes_real.csv demək olar ki, proqramçı / data / ML CV-si
saxlamır (məs. "Django" sözü 0 CV-də, "Docker" cəmi 3 CV-də var). Ona görə model texniki CV
yükləyəndə səhv kateqoriya (BANKING, AVIATION və s.) qaytarırdı.

Bu skript hər karyera üçün real CV formatında (başlıq, Summary, Skills, Experience, Education)
təsadüfi CV-lər yaradır. Nəticə: data/raw/tech_resumes_synthetic.csv

Qeyd: bu data SİNTETİKDİR; real CV-lər toplandıqca onunla əvəz edilməlidir.
"""
import random
from pathlib import Path

import pandas as pd

random.seed(42)

OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "tech_resumes_synthetic.csv"
PER_CLASS = 90

CAREERS = {
    "BACKEND-DEVELOPER": {
        "titles": ["Backend Developer", "Python Backend Developer", "Software Engineer", "API Developer",
                   "Senior Backend Engineer", "Django Developer", "Java Backend Developer"],
        "core": ["Python", "Django", "FastAPI", "Flask", "REST API", "PostgreSQL", "MySQL", "SQL", "Redis",
                 "Docker", "Git", "Microservices", "Celery", "SQLAlchemy", "Node.js", "Java", "Spring Boot",
                 "RabbitMQ", "Linux", "Unit Testing", "pytest", "CI/CD", "GraphQL", "MongoDB"],
        "tasks": ["Designed and implemented RESTful APIs serving thousands of requests per second",
                  "Developed backend services using Python and Django",
                  "Optimized SQL queries and database schemas to reduce response time",
                  "Built microservices and deployed them with Docker",
                  "Wrote unit tests and integration tests to improve code coverage",
                  "Integrated third-party payment and authentication services",
                  "Maintained CI/CD pipelines and participated in code reviews",
                  "Implemented caching with Redis and background jobs with Celery"],
    },
    "FRONTEND-DEVELOPER": {
        "titles": ["Frontend Developer", "React Developer", "Web Developer", "UI Developer",
                   "Senior Frontend Engineer", "JavaScript Developer", "Front-End Engineer"],
        "core": ["HTML", "CSS", "JavaScript", "React", "TypeScript", "Redux", "Vue.js", "Angular", "Sass",
                 "Tailwind CSS", "Bootstrap", "Webpack", "Vite", "Responsive Design", "Figma", "Git",
                 "Next.js", "Jest", "REST API", "Accessibility", "Flexbox", "Grid"],
        "tasks": ["Built responsive user interfaces with React and TypeScript",
                  "Converted Figma designs into pixel-perfect HTML and CSS",
                  "Implemented state management using Redux",
                  "Improved page load performance and Lighthouse scores",
                  "Developed reusable UI component libraries",
                  "Consumed REST APIs and handled asynchronous data in the browser",
                  "Ensured cross-browser compatibility and web accessibility",
                  "Wrote component tests with Jest and React Testing Library"],
    },
    "DATA-SCIENTIST": {
        "titles": ["Data Scientist", "Junior Data Scientist", "Senior Data Scientist", "Applied Scientist",
                   "Statistician and Data Scientist", "Data Science Specialist"],
        "core": ["Python", "R", "SQL", "Pandas", "NumPy", "scikit-learn", "Statistics", "Machine Learning",
                 "Data Visualization", "Matplotlib", "Seaborn", "Hypothesis Testing", "A/B Testing",
                 "Jupyter", "Regression", "Feature Engineering", "Tableau", "Time Series", "Probability",
                 "Predictive Modeling", "Clustering", "XGBoost"],
        "tasks": ["Analyzed large datasets with Pandas and NumPy to extract business insights",
                  "Built predictive models using scikit-learn and evaluated them with cross-validation",
                  "Designed and analyzed A/B tests and statistical experiments",
                  "Created dashboards and visualizations to communicate findings to stakeholders",
                  "Performed feature engineering and exploratory data analysis",
                  "Developed customer churn and demand forecasting models",
                  "Wrote SQL queries to extract and transform data from data warehouses"],
    },
    "MACHINE-LEARNING-ENGINEER": {
        "titles": ["Machine Learning Engineer", "ML Engineer", "AI Engineer", "Deep Learning Engineer",
                   "NLP Engineer", "Computer Vision Engineer", "Senior Machine Learning Engineer"],
        "core": ["Python", "TensorFlow", "PyTorch", "Keras", "Deep Learning", "Machine Learning", "NLP",
                 "Computer Vision", "scikit-learn", "NumPy", "Pandas", "Neural Networks", "Transformers",
                 "MLOps", "Docker", "Model Deployment", "CUDA", "OpenCV", "Hugging Face", "LLM",
                 "Feature Store", "MLflow", "Kubernetes"],
        "tasks": ["Trained and fine-tuned deep learning models using PyTorch and TensorFlow",
                  "Deployed machine learning models to production with Docker and REST APIs",
                  "Built NLP pipelines for text classification and named entity recognition",
                  "Developed computer vision models for image classification and object detection",
                  "Optimized model inference latency and GPU utilization",
                  "Set up MLOps pipelines for experiment tracking and model monitoring with MLflow",
                  "Researched and implemented transformer-based architectures"],
    },
    "DATA-ANALYST": {
        "titles": ["Data Analyst", "Business Data Analyst", "BI Analyst", "Junior Data Analyst",
                   "Reporting Analyst", "Business Intelligence Developer"],
        "core": ["SQL", "Excel", "Power BI", "Tableau", "Python", "Pandas", "Data Visualization", "Reporting",
                 "ETL", "Dashboards", "KPI", "Google Analytics", "Data Cleaning", "Statistics", "DAX",
                 "Looker", "Pivot Tables", "VBA", "Data Warehousing"],
        "tasks": ["Built interactive dashboards in Power BI and Tableau for management",
                  "Wrote complex SQL queries to prepare weekly and monthly reports",
                  "Cleaned and validated data from multiple sources to ensure accuracy",
                  "Tracked KPIs and identified trends to support business decisions",
                  "Automated recurring reports with Excel macros and Python scripts",
                  "Collaborated with stakeholders to define metrics and requirements"],
    },
    "DEVOPS-ENGINEER": {
        "titles": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer", "Platform Engineer",
                   "Infrastructure Engineer", "Senior DevOps Engineer"],
        "core": ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "Terraform", "Ansible", "Jenkins",
                 "GitHub Actions", "CI/CD", "Linux", "Bash", "Prometheus", "Grafana", "Nginx", "Helm",
                 "Infrastructure as Code", "Monitoring", "Python", "Git", "GitLab CI", "ELK"],
        "tasks": ["Built and maintained CI/CD pipelines with Jenkins and GitHub Actions",
                  "Provisioned cloud infrastructure using Terraform and Ansible",
                  "Managed Kubernetes clusters and containerized applications with Docker",
                  "Set up monitoring and alerting with Prometheus and Grafana",
                  "Improved system reliability and reduced deployment time",
                  "Automated operational tasks with Bash and Python scripts",
                  "Managed AWS services including EC2, S3, RDS and IAM"],
    },
    "CYBERSECURITY-ANALYST": {
        "titles": ["Cybersecurity Analyst", "Information Security Analyst", "Security Engineer",
                   "SOC Analyst", "Penetration Tester", "Network Security Engineer"],
        "core": ["Network Security", "SIEM", "Splunk", "Penetration Testing", "Vulnerability Assessment",
                 "Firewalls", "Incident Response", "Wireshark", "Nmap", "Metasploit", "OWASP", "ISO 27001",
                 "Threat Detection", "IDS/IPS", "Linux", "Python", "Encryption", "Risk Assessment",
                 "Burp Suite", "NIST"],
        "tasks": ["Monitored security events in the SIEM and investigated alerts",
                  "Performed vulnerability scans and penetration tests on web applications",
                  "Responded to security incidents and wrote post-incident reports",
                  "Configured firewalls and intrusion detection systems",
                  "Conducted risk assessments aligned with ISO 27001 and NIST frameworks",
                  "Trained employees on security awareness and phishing prevention"],
    },
}

SUMMARIES = [
    "Motivated {t} with {n} years of experience delivering reliable solutions in fast-paced teams.",
    "Results-driven {t} passionate about clean, maintainable work and continuous learning.",
    "{t} with a strong foundation in problem solving and a track record of shipping projects on time.",
    "Detail-oriented professional with {n}+ years of hands-on experience as {t}.",
]
COMPANIES = ["Tech Solutions", "Digital Labs", "DataWorks", "CloudNine", "Innovate Systems", "NextGen Software",
             "Softline", "Azercell", "Kapital Bank", "Pasha Technology", "Bright Soft", "Alpha Data"]
DEGREES = ["Bachelor of Science in Computer Science", "Bachelor of Engineering in Information Technology",
           "Master of Science in Data Science", "Bachelor of Science in Applied Mathematics",
           "Bachelor of Science in Software Engineering", "Bachelor of Science in Computer Engineering"]
SCHOOLS = ["Baku State University", "Azerbaijan Technical University", "ADA University", "Khazar University",
           "Western Caspian University", "Middle East Technical University", "State University"]
FILLER = ["Collaborated with cross-functional teams", "Participated in daily stand-ups and sprint planning",
          "Documented technical decisions and mentored junior colleagues", "Communicated results to non-technical stakeholders"]


def make_resume(career: dict) -> str:
    title = random.choice(career["titles"])
    years = random.randint(1, 9)
    skills = random.sample(career["core"], k=random.randint(6, min(14, len(career["core"]))))

    # Digər karyeralardan 1-3 təsadüfi ortaq bacarıq əlavə edirik (real CV-lərdə sərhəd bulanıqdır).
    others = [s for c in CAREERS.values() for s in c["core"] if s not in skills]
    skills += random.sample(others, k=random.randint(0, 3))
    random.shuffle(skills)

    jobs = []
    for _ in range(random.randint(1, 3)):
        role = random.choice(career["titles"])
        tasks = random.sample(career["tasks"], k=random.randint(2, 4)) + [random.choice(FILLER)]
        random.shuffle(tasks)
        start = random.randint(2012, 2022)
        jobs.append(
            f"{role} {start} to {start + random.randint(1, 4)} Company Name - {random.choice(COMPANIES)}, Baku "
            + " ".join(f"{t}." for t in tasks)
        )

    summary = random.choice(SUMMARIES).format(t=title, n=years)
    education = f"{random.choice(DEGREES)} {random.choice(SCHOOLS)}"
    # Başlıq real datasetdəki kimi böyük hərflə olur (bəzən).
    head = title.upper() if random.random() < 0.5 else title
    return f"{head} Summary {summary} Skills {', '.join(skills)} Experience {' '.join(jobs)} Education {education}"


def main():
    rows = [
        {"category": name, "text": make_resume(career)}
        for name, career in CAREERS.items()
        for _ in range(PER_CLASS)
    ]
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"{len(df)} sintetik texniki CV yaradıldı → {OUT_PATH}")
    print(df.category.value_counts().to_string())


if __name__ == "__main__":
    main()
