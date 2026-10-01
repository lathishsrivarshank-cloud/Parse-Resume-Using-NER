from ner_parser import parse_resume

sample = """
RAHUL KUMAR
rahul.kumar@example.com
+91 98765 43210
Chennai, Tamil Nadu

EDUCATION
B.E. Computer Science and Engineering, ABC College of Engineering, 2024-2028

SKILLS
Python, SQL, Java, Machine Learning, Computer Vision, OpenCV, Pandas, NumPy

EXPERIENCE
Software Engineering Intern at Tech Solutions Pvt Ltd, Chennai, June 2026 - August 2026

PROJECTS
Resume Parser using NER
Traffic Analytics using Computer Vision
"""

result = parse_resume(sample)

print("\n--- PARSED RESUME ---")
for key, value in result.items():
    if key != "entities":
        print(f"{key}: {value}")

print("\n--- NER ENTITIES ---")
for ent in result["entities"]:
    print(ent["text"], "=>", ent["label"])
