import pandas as pd
import re

# ============================
# LOAD CSV FILES
# ============================

subjects = pd.read_csv("subjects_202602241939.csv")
assessments = pd.read_csv("assessments_202602241940.csv")
questions = pd.read_csv("questions_202602241940.csv")
options = pd.read_csv("_options__202602241944.csv")

# ============================
# AGGRESSIVE MATH WRAPPER
# ============================

def wrap_math(text):
    if pd.isna(text):
        return text

    text = str(text)

    # Block equations (contains '=')
    text = re.sub(
        r'([A-Za-z0-9\^\+\-\*/\(\)\s]+=[A-Za-z0-9\^\+\-\*/\(\)\s]+)',
        r'$$ \1 $$',
        text
    )

    # Coordinates (x,y)
    text = re.sub(
        r'\(([A-Za-z0-9\^\+\-\*/\s]+,[A-Za-z0-9\^\+\-\*/\s]+)\)',
        r'$(\1)$',
        text
    )

    # Expressions with operators
    text = re.sub(
        r'(?<!\$)(\b[A-Za-z0-9]+\s*[\+\-\*/\^]\s*[A-Za-z0-9\^\+\-\*/]+\b)(?!\$)',
        r'$\1$',
        text
    )

    # Algebra terms like 2x, x^2
    text = re.sub(
        r'(?<!\$)(\b\d+[A-Za-z]+\b|\b[A-Za-z]+\^\d+\b)(?!\$)',
        r'$\1$',
        text
    )

    return text


# ============================
# APPLY WRAPPING
# ============================

for col in ["heading", "media_content"]:
    if col in questions.columns:
        questions[col] = questions[col].apply(wrap_math)

for col in ["option_text", "media_content"]:
    if col in options.columns:
        options[col] = options[col].apply(wrap_math)


# ============================
# REINDEX IDS SAFELY
# ============================

# Subjects
subjects = subjects.sort_values("id").reset_index(drop=True)
subjects["new_id"] = range(1, len(subjects) + 1)
subject_map = dict(zip(subjects["id"], subjects["new_id"]))
subjects["id"] = subjects["new_id"]
subjects.drop(columns=["new_id"], inplace=True)

# Assessments
assessments = assessments.sort_values("id").reset_index(drop=True)
assessments["new_id"] = range(1, len(assessments) + 1)
assessment_map = dict(zip(assessments["id"], assessments["new_id"]))
assessments["subject_id"] = assessments["subject_id"].map(subject_map)
assessments["id"] = assessments["new_id"]
assessments.drop(columns=["new_id"], inplace=True)

# Questions
questions = questions.sort_values("id").reset_index(drop=True)
questions["new_id"] = range(1, len(questions) + 1)
question_map = dict(zip(questions["id"], questions["new_id"]))
questions["assessment_id"] = questions["assessment_id"].map(assessment_map)
questions["id"] = questions["new_id"]
questions.drop(columns=["new_id"], inplace=True)

# Options
options = options.sort_values("id").reset_index(drop=True)
options["new_id"] = range(1, len(options) + 1)
options["question_id"] = options["question_id"].map(question_map)
options["id"] = options["new_id"]
options.drop(columns=["new_id"], inplace=True)


# ============================
# EXPORT CLEAN FILES
# ============================

subjects.to_csv("subjects_clean.csv", index=False)
assessments.to_csv("assessments_clean.csv", index=False)
questions.to_csv("questions_clean.csv", index=False)
options.to_csv("options_clean.csv", index=False)

print("CLEANING COMPLETE.")