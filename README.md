# Symptom Explorer: A Python-Based Medical Diagnosis Analysis Tool 
## Project Title 
Symptom Explorer, a command-line application for exploring symptoms and diagnoses using synthetic medical data. 
## Motivation and Problem Statement 
In medical education, one of the biggest challenges is understanding how different symptoms relate to specific illnesses. Real medical data is usually restricted because of privacy issues, which makes it difficult for students and researchers to practice analysis on real cases. Synthetic datasets offer a safe and accessible alternative. 
The Synthetic Medical Symptoms and Diagnosis Dataset from Kaggle provides realistic symptom diagnosis combinations without containing any private information. With this dataset, it becomes possible to build a small analysis tool that allows users to explore patterns, view simple visual summaries, compute statistics, and experiment with a basic rule-based diagnosis suggestion feature. This feature is not meant for real medical use but serves as an educational way to understand how symptoms cluster around diagnoses. 
The overall goal is to create an interactive learning tool that helps users engage with the data and practice analytical thinking. This project meets the course requirements by including data loading, data cleaning, user authentication, a text-based interface, statistical functionality and visualizations. 
## Project Description 
Symptom Explorer is a terminal based application. After logging in, users can explore the dataset, run simple analyses, create charts, and try a symptom-matching tool that suggests likely diagnoses based on frequency patterns in the data. 
### User login system 
The program includes at least four user accounts stored in an SQLite database, including an admin user. Passwords are hashed for security. Users can log in and log out, and the admin can add or remove accounts from inside the application. 
### Data loading and cleaning 
The dataset is loaded from CSV. Missing values are handled, and symptom columns are prepared in a consistent format for analysis. 
### Interactive CLI menu 
All program functions are accessible through a simple text menu. 
### Statistical analysis 
The tool can calculate the most frequent symptoms and diagnoses, the average number of symptoms per patient, and simple co-occurrence patterns. Users can also save results to a text file. 
### Visualization tools 
The program generates bar charts showing how often different symptoms or diagnoses appear, and may include a simple heatmap describing relationships between symptoms and conditions. Charts can be displayed or saved as PNG files. 
### Optional rule-based symptom checker 
This optional feature lets users type in a list of symptoms and receive a suggestion of a likely diagnosis based on how frequently similar patterns appear in the dataset. It uses no machine learning, only transparent, rule-based logic that making it suitable for classroom or training use. 
## Target Users and Use Cases 
The primary users of this tool are medical students or trainees who want to explore patterns in symptom data in a safe and controlled environment. It can also be helpful for educators who need quick charts or summaries for teaching, demonstrations, or workshops. 
Typical use cases include checking which symptoms are most common, studying how symptoms appear together, examining how symptoms relate to specific diagnoses, and creating simple visualizations for learning or presentations. 
## Technical Architecture 
The program is implemented in Python. User accounts are stored in an SQLite database. Data analysis uses pandas, and visualization uses matplotlib or seaborn. Passwords are secured using hashlib or Werkzeug’s security utilities. 
### The code is organized into modules such as: 
•	auth.py for authentication and admin functions 
•	data_handler.py for loading and preparing the dataset 
•	statistics.py for analysis functions 
•	visuals.py for generating plots 
•	diagnosis.py for the optional rule-based feature 
•	cli.py for menu navigation 
•	main.py as the entry point 
### Application flow is straightforward: 
the user logs in, navigates through the menu, selects a function, receives results or charts, and logs out when finished. 
## Expected Outcomes 
At the end of the project, the result will be a functional command-line application that loads and analyzes the synthetic dataset, displays results, saves summaries, generates visualizations, and allows secure user login and administrative control. The program will be well-structured, documented, and suitable for educational use. 
### Dataset Source
https://www.kaggle.com/datasets/khushikyad001/synthetic-medical-symptoms-and-diagnosis-dataset

