import streamlit as st
from datetime import datetime

def calculate_age(birthdate):
    """Calculates age from birthdate (MM-DD-YYYY)."""
    try:
        today = datetime.today()
        birth_date = datetime.strptime(birthdate, "%m-%d-%Y")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        return None

def get_label(age, score, gender, criteria):
    """
    Takes an age, gender, and a score (0-40) and returns the corresponding label from criteria.
    """
    if score <= 5:
        return "Probable Malingering"
    elif score <= 18:
        return "Anosmia"
    
    if gender in criteria:
        for age_range, score_ranges in criteria[gender].items():
            min_age, max_age = age_range
            if min_age <= age <= max_age:
                for score_range, label in score_ranges.items():
                    min_score, max_score = score_range
                    if min_score <= score <= max_score:
                        return label
    
    return "No matching label found."

# Updated predefined criteria
criteria = {
    "M": {
        (5, 9): {
            (19, 40): "Normosmia"
        },
        (10, 14): {
            (19, 22): "Severe Microsmia",
            (23, 27): "Moderate Microsmia",
            (28, 31): "Mild Microsmia",
            (32, 40): "Normosmia"
        },
        (15, 100): {
            (19, 25): "Severe Microsmia",
            (26, 29): "Moderate Microsmia",
            (30, 33): "Mild Microsmia",
            (34, 40): "Normosmia"
        }
    },
    "F": {
        (5, 9): {
            (19, 40): "Normosmia"
        },
        (10, 14): {
            (19, 22): "Severe Microsmia",
            (23, 27): "Moderate Microsmia",
            (28, 31): "Mild Microsmia",
            (32, 40): "Normosmia"
        },
        (15, 100): {
            (19, 25): "Severe Microsmia",
            (26, 30): "Moderate Microsmia",
            (31, 34): "Mild Microsmia",
            (35, 40): "Normosmia"
        }
    }
}

# Streamlit UI
def main():
    st.title("UPSIT Smell Classification Calculator")
    birthdate = st.text_input("Enter Birthdate (MM-DD-YYYY)")
    gender = st.selectbox("Select Gender", ["M", "F"])
    score = st.slider("Select Score", 0, 40, 20)
    
    if st.button("Calculate"):
        age = calculate_age(birthdate)
        if age is None:
            st.error("Invalid date format. Please enter MM-DD-YYYY.")
        else:
            label = get_label(age, score, gender, criteria)
            st.success(f"Age: {age}, Gender: {gender}, Score: {score}, Result: {label}")

if __name__ == "__main__":
    main()
