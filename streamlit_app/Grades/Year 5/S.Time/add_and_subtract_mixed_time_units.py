import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

def run():
    """
    Main function to run the Add and Subtract Mixed Time Units activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/S.Time/add_and_subtract_mixed_time_units.py
    """
    # Initialize session state
    if "mixed_time_difficulty" not in st.session_state:
        st.session_state.mixed_time_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header
    st.markdown("**📚 Year 5 > S. Time**")
    st.title("➕➖ Add and Subtract Mixed Time Units")
    st.markdown("*Add and subtract time with mixed units (like hours and minutes)*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.mixed_time_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Addition (no regrouping)",
            2: "Simple Subtraction (no borrowing)",
            3: "Addition with Regrouping",
            4: "Subtraction with Borrowing",
            5: "Complex Mixed Operations"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic')}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 3:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level == 4:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("📚 **How to Add and Subtract Mixed Time Units**", expanded=False):
        st.markdown("""
        ### ➕ Adding Mixed Time Units
        
        **Example: 3 hours 45 minutes + 2 hours 30 minutes**
        
        **Method 1: Add separately**
        1. Add hours: 3 + 2 = 5 hours
        2. Add minutes: 45 + 30 = 75 minutes
        3. Convert if needed: 75 minutes = 1 hour 15 minutes
        4. Final answer: 5 hours + 1 hour 15 minutes = 6 hours 15 minutes
        
        **Method 2: Convert to single unit**
        1. Convert to minutes: (3 × 60) + 45 = 225 minutes
        2. Convert second: (2 × 60) + 30 = 150 minutes
        3. Add: 225 + 150 = 375 minutes
        4. Convert back: 375 ÷ 60 = 6 hours 15 minutes
        
        ### ➖ Subtracting Mixed Time Units
        
        **Example: 5 hours 20 minutes - 2 hours 45 minutes**
        
        **With Borrowing:**
        1. Can't subtract 45 from 20 minutes
        2. Borrow 1 hour = 60 minutes
        3. 5 hours 20 minutes = 4 hours 80 minutes
        4. Now subtract: 4 hours 80 minutes - 2 hours 45 minutes
        5. Answer: 2 hours 35 minutes
        
        ### 📊 Key Conversions:
        - 1 minute = 60 seconds
        - 1 hour = 60 minutes
        - 1 day = 24 hours
        - 1 week = 7 days
        - 1 year = 12 months
        
        ### 💡 Tips:
        - Line up units vertically
        - Start with the smallest unit
        - Regroup/borrow when needed
        - Check your answer makes sense
        """)

def generate_new_problem():
    """Generate a new mixed time units problem based on difficulty"""
    difficulty = st.session_state.mixed_time_difficulty
    
    if difficulty == 1:
        # Level 1: Simple addition without regrouping
        problem_data = generate_simple_addition()
    elif difficulty == 2:
        # Level 2: Simple subtraction without borrowing
        problem_data = generate_simple_subtraction()
    elif difficulty == 3:
        # Level 3: Addition with regrouping
        problem_data = generate_addition_with_regrouping()
    elif difficulty == 4:
        # Level 4: Subtraction with borrowing
        problem_data = generate_subtraction_with_borrowing()
    else:
        # Level 5: Complex mixed operations
        problem_data = generate_complex_mixed_operation()
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_simple_addition():
    """Generate Level 1: Simple addition without regrouping"""
    problem_types = [
        "hours_minutes",
        "minutes_seconds",
        "days_hours",
        "weeks_days",
        "years_months"
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == "hours_minutes":
        # Ensure no regrouping (sum of minutes < 60)
        h1 = random.randint(1, 5)
        m1 = random.randint(10, 30)
        h2 = random.randint(1, 4)
        m2 = random.randint(10, 29)
        
        # Make sure sum of minutes < 60
        if m1 + m2 >= 60:
            m2 = 59 - m1
        
        result_h = h1 + h2
        result_m = m1 + m2
        
        return {
            "question": f"Add:\n{h1} hours {m1} minutes + {h2} hours {m2} minutes = ",
            "operation": "add",
            "units": ["hours", "minutes"],
            "correct_answer": f"{result_h}|{result_m}",
            "explanation": f"Add hours: {h1} + {h2} = {result_h} hours\nAdd minutes: {m1} + {m2} = {result_m} minutes\nAnswer: {result_h} hours {result_m} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "minutes_seconds":
        m1 = random.randint(2, 8)
        s1 = random.randint(10, 25)
        m2 = random.randint(1, 5)
        s2 = random.randint(10, 25)
        
        # Ensure no regrouping
        if s1 + s2 >= 60:
            s2 = 59 - s1
        
        result_m = m1 + m2
        result_s = s1 + s2
        
        return {
            "question": f"Add:\n{m1} minutes {s1} seconds + {m2} minutes {s2} seconds = ",
            "operation": "add",
            "units": ["minutes", "seconds"],
            "correct_answer": f"{result_m}|{result_s}",
            "explanation": f"Add minutes: {m1} + {m2} = {result_m} minutes\nAdd seconds: {s1} + {s2} = {result_s} seconds\nAnswer: {result_m} minutes {result_s} seconds",
            "problem_type": problem_type
        }
    
    elif problem_type == "days_hours":
        d1 = random.randint(1, 3)
        h1 = random.randint(2, 10)
        d2 = random.randint(1, 2)
        h2 = random.randint(2, 10)
        
        # Ensure no regrouping
        if h1 + h2 >= 24:
            h2 = 23 - h1
        
        result_d = d1 + d2
        result_h = h1 + h2
        
        return {
            "question": f"Add:\n{d1} days {h1} hours + {d2} days {h2} hours = ",
            "operation": "add",
            "units": ["days", "hours"],
            "correct_answer": f"{result_d}|{result_h}",
            "explanation": f"Add days: {d1} + {d2} = {result_d} days\nAdd hours: {h1} + {h2} = {result_h} hours\nAnswer: {result_d} days {result_h} hours",
            "problem_type": problem_type
        }
    
    elif problem_type == "weeks_days":
        w1 = random.randint(1, 3)
        d1 = random.randint(1, 3)
        w2 = random.randint(1, 2)
        d2 = random.randint(1, 3)
        
        # Ensure no regrouping
        if d1 + d2 >= 7:
            d2 = 6 - d1
        
        result_w = w1 + w2
        result_d = d1 + d2
        
        return {
            "question": f"Add:\n{w1} weeks {d1} days + {w2} weeks {d2} days = ",
            "operation": "add",
            "units": ["weeks", "days"],
            "correct_answer": f"{result_w}|{result_d}",
            "explanation": f"Add weeks: {w1} + {w2} = {result_w} weeks\nAdd days: {d1} + {d2} = {result_d} days\nAnswer: {result_w} weeks {result_d} days",
            "problem_type": problem_type
        }
    
    else:  # years_months
        y1 = random.randint(1, 3)
        m1 = random.randint(2, 5)
        y2 = random.randint(1, 2)
        m2 = random.randint(2, 5)
        
        # Ensure no regrouping
        if m1 + m2 >= 12:
            m2 = 11 - m1
        
        result_y = y1 + y2
        result_m = m1 + m2
        
        return {
            "question": f"Add:\n{y1} years {m1} months + {y2} years {m2} months = ",
            "operation": "add",
            "units": ["years", "months"],
            "correct_answer": f"{result_y}|{result_m}",
            "explanation": f"Add years: {y1} + {y2} = {result_y} years\nAdd months: {m1} + {m2} = {result_m} months\nAnswer: {result_y} years {result_m} months",
            "problem_type": problem_type
        }

def generate_simple_subtraction():
    """Generate Level 2: Simple subtraction without borrowing"""
    problem_types = [
        "hours_minutes",
        "minutes_seconds",
        "days_hours",
        "weeks_days",
        "years_months"
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == "hours_minutes":
        # Ensure no borrowing needed
        h1 = random.randint(4, 8)
        m1 = random.randint(30, 50)
        h2 = random.randint(1, 3)
        m2 = random.randint(10, 29)
        
        # Make sure m1 > m2
        if m2 >= m1:
            m2 = m1 - random.randint(1, 10)
        
        result_h = h1 - h2
        result_m = m1 - m2
        
        return {
            "question": f"Subtract:\n{h1} hours {m1} minutes - {h2} hours {m2} minutes = ",
            "operation": "subtract",
            "units": ["hours", "minutes"],
            "correct_answer": f"{result_h}|{result_m}",
            "explanation": f"Subtract hours: {h1} - {h2} = {result_h} hours\nSubtract minutes: {m1} - {m2} = {result_m} minutes\nAnswer: {result_h} hours {result_m} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "minutes_seconds":
        m1 = random.randint(5, 10)
        s1 = random.randint(30, 50)
        m2 = random.randint(2, 4)
        s2 = random.randint(10, 29)
        
        # Make sure s1 > s2
        if s2 >= s1:
            s2 = s1 - random.randint(1, 10)
        
        result_m = m1 - m2
        result_s = s1 - s2
        
        return {
            "question": f"Subtract:\n{m1} minutes {s1} seconds - {m2} minutes {s2} seconds = ",
            "operation": "subtract",
            "units": ["minutes", "seconds"],
            "correct_answer": f"{result_m}|{result_s}",
            "explanation": f"Subtract minutes: {m1} - {m2} = {result_m} minutes\nSubtract seconds: {s1} - {s2} = {result_s} seconds\nAnswer: {result_m} minutes {result_s} seconds",
            "problem_type": problem_type
        }
    
    elif problem_type == "days_hours":
        d1 = random.randint(4, 7)
        h1 = random.randint(12, 20)
        d2 = random.randint(1, 3)
        h2 = random.randint(5, 11)
        
        # Make sure h1 > h2
        if h2 >= h1:
            h2 = h1 - random.randint(1, 5)
        
        result_d = d1 - d2
        result_h = h1 - h2
        
        return {
            "question": f"Subtract:\n{d1} days {h1} hours - {d2} days {h2} hours = ",
            "operation": "subtract",
            "units": ["days", "hours"],
            "correct_answer": f"{result_d}|{result_h}",
            "explanation": f"Subtract days: {d1} - {d2} = {result_d} days\nSubtract hours: {h1} - {h2} = {result_h} hours\nAnswer: {result_d} days {result_h} hours",
            "problem_type": problem_type
        }
    
    elif problem_type == "weeks_days":
        w1 = random.randint(4, 7)
        d1 = random.randint(4, 6)
        w2 = random.randint(1, 3)
        d2 = random.randint(1, 3)
        
        # Make sure d1 > d2
        if d2 >= d1:
            d2 = d1 - 1
        
        result_w = w1 - w2
        result_d = d1 - d2
        
        return {
            "question": f"Subtract:\n{w1} weeks {d1} days - {w2} weeks {d2} days = ",
            "operation": "subtract",
            "units": ["weeks", "days"],
            "correct_answer": f"{result_w}|{result_d}",
            "explanation": f"Subtract weeks: {w1} - {w2} = {result_w} weeks\nSubtract days: {d1} - {d2} = {result_d} days\nAnswer: {result_w} weeks {result_d} days",
            "problem_type": problem_type
        }
    
    else:  # years_months
        y1 = random.randint(4, 8)
        m1 = random.randint(7, 11)
        y2 = random.randint(1, 3)
        m2 = random.randint(2, 6)
        
        # Make sure m1 > m2
        if m2 >= m1:
            m2 = m1 - random.randint(1, 3)
        
        result_y = y1 - y2
        result_m = m1 - m2
        
        return {
            "question": f"Subtract:\n{y1} years {m1} months - {y2} years {m2} months = ",
            "operation": "subtract",
            "units": ["years", "months"],
            "correct_answer": f"{result_y}|{result_m}",
            "explanation": f"Subtract years: {y1} - {y2} = {result_y} years\nSubtract months: {m1} - {m2} = {result_m} months\nAnswer: {result_y} years {result_m} months",
            "problem_type": problem_type
        }

def generate_addition_with_regrouping():
    """Generate Level 3: Addition with regrouping"""
    problem_types = [
        "hours_minutes",
        "minutes_seconds",
        "days_hours",
        "weeks_days",
        "years_months"
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == "hours_minutes":
        h1 = random.randint(2, 6)
        m1 = random.randint(35, 55)
        h2 = random.randint(1, 4)
        m2 = random.randint(25, 45)
        
        # Ensure regrouping is needed
        if m1 + m2 < 60:
            m2 = 60 - m1 + random.randint(5, 20)
        
        total_minutes = m1 + m2
        extra_hours = total_minutes // 60
        result_m = total_minutes % 60
        result_h = h1 + h2 + extra_hours
        
        return {
            "question": f"Add:\n{h1} hours {m1} minutes + {h2} hours {m2} minutes = ",
            "operation": "add",
            "units": ["hours", "minutes"],
            "correct_answer": f"{result_h}|{result_m}",
            "explanation": f"Add hours: {h1} + {h2} = {h1 + h2} hours\nAdd minutes: {m1} + {m2} = {total_minutes} minutes\n{total_minutes} minutes = {extra_hours} hour {result_m} minutes\nTotal: {h1 + h2} hours + {extra_hours} hour = {result_h} hours\nAnswer: {result_h} hours {result_m} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "minutes_seconds":
        m1 = random.randint(3, 8)
        s1 = random.randint(35, 55)
        m2 = random.randint(2, 6)
        s2 = random.randint(25, 45)
        
        # Ensure regrouping is needed
        if s1 + s2 < 60:
            s2 = 60 - s1 + random.randint(5, 20)
        
        total_seconds = s1 + s2
        extra_minutes = total_seconds // 60
        result_s = total_seconds % 60
        result_m = m1 + m2 + extra_minutes
        
        return {
            "question": f"Add:\n{m1} minutes {s1} seconds + {m2} minutes {s2} seconds = ",
            "operation": "add",
            "units": ["minutes", "seconds"],
            "correct_answer": f"{result_m}|{result_s}",
            "explanation": f"Add minutes: {m1} + {m2} = {m1 + m2} minutes\nAdd seconds: {s1} + {s2} = {total_seconds} seconds\n{total_seconds} seconds = {extra_minutes} minute {result_s} seconds\nTotal: {m1 + m2} minutes + {extra_minutes} minute = {result_m} minutes\nAnswer: {result_m} minutes {result_s} seconds",
            "problem_type": problem_type
        }
    
    elif problem_type == "days_hours":
        d1 = random.randint(1, 3)
        h1 = random.randint(15, 22)
        d2 = random.randint(1, 2)
        h2 = random.randint(10, 20)
        
        # Ensure regrouping
        if h1 + h2 < 24:
            h2 = 24 - h1 + random.randint(2, 8)
        
        total_hours = h1 + h2
        extra_days = total_hours // 24
        result_h = total_hours % 24
        result_d = d1 + d2 + extra_days
        
        return {
            "question": f"Add:\n{d1} days {h1} hours + {d2} days {h2} hours = ",
            "operation": "add",
            "units": ["days", "hours"],
            "correct_answer": f"{result_d}|{result_h}",
            "explanation": f"Add days: {d1} + {d2} = {d1 + d2} days\nAdd hours: {h1} + {h2} = {total_hours} hours\n{total_hours} hours = {extra_days} day {result_h} hours\nTotal: {d1 + d2} days + {extra_days} day = {result_d} days\nAnswer: {result_d} days {result_h} hours",
            "problem_type": problem_type
        }
    
    elif problem_type == "weeks_days":
        w1 = random.randint(2, 4)
        d1 = random.randint(4, 6)
        w2 = random.randint(1, 3)
        d2 = random.randint(3, 6)
        
        # Ensure regrouping
        if d1 + d2 < 7:
            d2 = 7 - d1 + random.randint(1, 3)
        
        total_days = d1 + d2
        extra_weeks = total_days // 7
        result_d = total_days % 7
        result_w = w1 + w2 + extra_weeks
        
        return {
            "question": f"Add:\n{w1} weeks {d1} days + {w2} weeks {d2} days = ",
            "operation": "add",
            "units": ["weeks", "days"],
            "correct_answer": f"{result_w}|{result_d}",
            "explanation": f"Add weeks: {w1} + {w2} = {w1 + w2} weeks\nAdd days: {d1} + {d2} = {total_days} days\n{total_days} days = {extra_weeks} week {result_d} days\nTotal: {w1 + w2} weeks + {extra_weeks} week = {result_w} weeks\nAnswer: {result_w} weeks {result_d} days",
            "problem_type": problem_type
        }
    
    else:  # years_months
        y1 = random.randint(2, 5)
        m1 = random.randint(7, 11)
        y2 = random.randint(1, 3)
        m2 = random.randint(5, 10)
        
        # Ensure regrouping
        if m1 + m2 < 12:
            m2 = 12 - m1 + random.randint(1, 5)
        
        total_months = m1 + m2
        extra_years = total_months // 12
        result_m = total_months % 12
        result_y = y1 + y2 + extra_years
        
        return {
            "question": f"Add:\n{y1} years {m1} months + {y2} years {m2} months = ",
            "operation": "add",
            "units": ["years", "months"],
            "correct_answer": f"{result_y}|{result_m}",
            "explanation": f"Add years: {y1} + {y2} = {y1 + y2} years\nAdd months: {m1} + {m2} = {total_months} months\n{total_months} months = {extra_years} year {result_m} months\nTotal: {y1 + y2} years + {extra_years} year = {result_y} years\nAnswer: {result_y} years {result_m} months",
            "problem_type": problem_type
        }

def generate_subtraction_with_borrowing():
    """Generate Level 4: Subtraction with borrowing"""
    problem_types = [
        "hours_minutes",
        "minutes_seconds",
        "days_hours",
        "weeks_days",
        "years_months"
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == "hours_minutes":
        h1 = random.randint(4, 8)
        m1 = random.randint(10, 30)
        h2 = random.randint(1, 3)
        m2 = random.randint(35, 55)
        
        # Ensure borrowing is needed (m1 < m2)
        if m1 >= m2:
            m1 = random.randint(10, 25)
            m2 = random.randint(30, 55)
        
        # Perform subtraction with borrowing
        if m1 < m2:
            h1_borrowed = h1 - 1
            m1_borrowed = m1 + 60
            result_h = h1_borrowed - h2
            result_m = m1_borrowed - m2
        else:
            result_h = h1 - h2
            result_m = m1 - m2
        
        return {
            "question": f"Subtract:\n{h1} hours {m1} minutes - {h2} hours {m2} minutes = ",
            "operation": "subtract",
            "units": ["hours", "minutes"],
            "correct_answer": f"{result_h}|{result_m}",
            "explanation": f"Can't subtract {m2} minutes from {m1} minutes\nBorrow 1 hour = 60 minutes\n{h1} hours {m1} minutes = {h1-1} hours {m1+60} minutes\nSubtract: {h1-1} hours {m1+60} minutes - {h2} hours {m2} minutes\nAnswer: {result_h} hours {result_m} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "minutes_seconds":
        m1 = random.randint(5, 10)
        s1 = random.randint(10, 25)
        m2 = random.randint(2, 4)
        s2 = random.randint(30, 55)
        
        # Ensure borrowing is needed
        if s1 >= s2:
            s1 = random.randint(10, 25)
            s2 = random.randint(30, 55)
        
        # Perform subtraction with borrowing
        if s1 < s2:
            m1_borrowed = m1 - 1
            s1_borrowed = s1 + 60
            result_m = m1_borrowed - m2
            result_s = s1_borrowed - s2
        else:
            result_m = m1 - m2
            result_s = s1 - s2
        
        return {
            "question": f"Subtract:\n{m1} minutes {s1} seconds - {m2} minutes {s2} seconds = ",
            "operation": "subtract",
            "units": ["minutes", "seconds"],
            "correct_answer": f"{result_m}|{result_s}",
            "explanation": f"Can't subtract {s2} seconds from {s1} seconds\nBorrow 1 minute = 60 seconds\n{m1} minutes {s1} seconds = {m1-1} minutes {s1+60} seconds\nSubtract: {m1-1} minutes {s1+60} seconds - {m2} minutes {s2} seconds\nAnswer: {result_m} minutes {result_s} seconds",
            "problem_type": problem_type
        }
    
    elif problem_type == "days_hours":
        d1 = random.randint(4, 7)
        h1 = random.randint(5, 15)
        d2 = random.randint(1, 3)
        h2 = random.randint(16, 23)
        
        # Ensure borrowing is needed
        if h1 >= h2:
            h1 = random.randint(5, 15)
            h2 = random.randint(16, 23)
        
        # Perform subtraction with borrowing
        if h1 < h2:
            d1_borrowed = d1 - 1
            h1_borrowed = h1 + 24
            result_d = d1_borrowed - d2
            result_h = h1_borrowed - h2
        else:
            result_d = d1 - d2
            result_h = h1 - h2
        
        return {
            "question": f"Subtract:\n{d1} days {h1} hours - {d2} days {h2} hours = ",
            "operation": "subtract",
            "units": ["days", "hours"],
            "correct_answer": f"{result_d}|{result_h}",
            "explanation": f"Can't subtract {h2} hours from {h1} hours\nBorrow 1 day = 24 hours\n{d1} days {h1} hours = {d1-1} days {h1+24} hours\nSubtract: {d1-1} days {h1+24} hours - {d2} days {h2} hours\nAnswer: {result_d} days {result_h} hours",
            "problem_type": problem_type
        }
    
    elif problem_type == "weeks_days":
        w1 = random.randint(4, 8)
        d1 = random.randint(1, 3)
        w2 = random.randint(1, 3)
        d2 = random.randint(4, 6)
        
        # Ensure borrowing is needed
        if d1 >= d2:
            d1 = random.randint(1, 3)
            d2 = random.randint(4, 6)
        
        # Perform subtraction with borrowing
        if d1 < d2:
            w1_borrowed = w1 - 1
            d1_borrowed = d1 + 7
            result_w = w1_borrowed - w2
            result_d = d1_borrowed - d2
        else:
            result_w = w1 - w2
            result_d = d1 - d2
        
        return {
            "question": f"Subtract:\n{w1} weeks {d1} days - {w2} weeks {d2} days = ",
            "operation": "subtract",
            "units": ["weeks", "days"],
            "correct_answer": f"{result_w}|{result_d}",
            "explanation": f"Can't subtract {d2} days from {d1} days\nBorrow 1 week = 7 days\n{w1} weeks {d1} days = {w1-1} weeks {d1+7} days\nSubtract: {w1-1} weeks {d1+7} days - {w2} weeks {d2} days\nAnswer: {result_w} weeks {result_d} days",
            "problem_type": problem_type
        }
    
    else:  # years_months
        y1 = random.randint(4, 8)
        m1 = random.randint(2, 6)
        y2 = random.randint(1, 3)
        m2 = random.randint(7, 11)
        
        # Ensure borrowing is needed
        if m1 >= m2:
            m1 = random.randint(2, 6)
            m2 = random.randint(7, 11)
        
        # Perform subtraction with borrowing
        if m1 < m2:
            y1_borrowed = y1 - 1
            m1_borrowed = m1 + 12
            result_y = y1_borrowed - y2
            result_m = m1_borrowed - m2
        else:
            result_y = y1 - y2
            result_m = m1 - m2
        
        return {
            "question": f"Subtract:\n{y1} years {m1} months - {y2} years {m2} months = ",
            "operation": "subtract",
            "units": ["years", "months"],
            "correct_answer": f"{result_y}|{result_m}",
            "explanation": f"Can't subtract {m2} months from {m1} months\nBorrow 1 year = 12 months\n{y1} years {m1} months = {y1-1} years {m1+12} months\nSubtract: {y1-1} years {m1+12} months - {y2} years {m2} months\nAnswer: {result_y} years {result_m} months",
            "problem_type": problem_type
        }

def generate_complex_mixed_operation():
    """Generate Level 5: Complex mixed operations"""
    scenarios = [
        {
            "context": "Sarah practiced piano for 2 hours 45 minutes on Monday and 1 hour 50 minutes on Tuesday",
            "question": "How long did she practice in total?",
            "values": [(2, 45), (1, 50)],
            "operation": "add",
            "units": ["hours", "minutes"],
            "calculation": lambda v: calculate_time_sum(v, 60)
        },
        {
            "context": "A movie is 3 hours 15 minutes long. Tom watched 1 hour 40 minutes",
            "question": "How much is left to watch?",
            "values": [(3, 15), (1, 40)],
            "operation": "subtract",
            "units": ["hours", "minutes"],
            "calculation": lambda v: calculate_time_difference(v, 60)
        },
        {
            "context": "A project took 5 weeks 6 days. Another took 3 weeks 5 days",
            "question": "What's the total time for both projects?",
            "values": [(5, 6), (3, 5)],
            "operation": "add",
            "units": ["weeks", "days"],
            "calculation": lambda v: calculate_time_sum(v, 7)
        },
        {
            "context": "A flight was scheduled for 8 hours 30 minutes but arrived 2 hours 45 minutes early",
            "question": "What was the actual flight time?",
            "values": [(8, 30), (2, 45)],
            "operation": "subtract",
            "units": ["hours", "minutes"],
            "calculation": lambda v: calculate_time_difference(v, 60)
        },
        {
            "context": "Three tasks took: 45 minutes, 1 hour 20 minutes, and 35 minutes",
            "question": "What's the total time? (Express as hours and minutes)",
            "values": [(0, 45), (1, 20), (0, 35)],
            "operation": "add",
            "units": ["hours", "minutes"],
            "calculation": lambda v: calculate_multiple_time_sum(v, 60)
        }
    ]
    
    scenario = random.choice(scenarios)
    result = scenario["calculation"](scenario["values"])
    
    return {
        "question": f"{scenario['context']}.\n{scenario['question']}",
        "operation": scenario["operation"],
        "units": scenario["units"],
        "correct_answer": f"{result[0]}|{result[1]}",
        "explanation": generate_complex_explanation(scenario, result),
        "problem_type": "complex"
    }

def calculate_time_sum(values, conversion_factor):
    """Calculate sum of time values with regrouping"""
    total_smaller = sum(v[1] for v in values)
    total_larger = sum(v[0] for v in values)
    
    extra_larger = total_smaller // conversion_factor
    remaining_smaller = total_smaller % conversion_factor
    
    total_larger += extra_larger
    
    return (total_larger, remaining_smaller)

def calculate_time_difference(values, conversion_factor):
    """Calculate difference of time values with borrowing"""
    larger1, smaller1 = values[0]
    larger2, smaller2 = values[1]
    
    if smaller1 < smaller2:
        larger1 -= 1
        smaller1 += conversion_factor
    
    result_larger = larger1 - larger2
    result_smaller = smaller1 - smaller2
    
    return (result_larger, result_smaller)

def calculate_multiple_time_sum(values, conversion_factor):
    """Calculate sum of multiple time values"""
    total_smaller = sum(v[1] for v in values)
    total_larger = sum(v[0] for v in values)
    
    extra_larger = total_smaller // conversion_factor
    remaining_smaller = total_smaller % conversion_factor
    
    total_larger += extra_larger
    
    return (total_larger, remaining_smaller)

def generate_complex_explanation(scenario, result):
    """Generate explanation for complex problems"""
    if scenario["operation"] == "add":
        if len(scenario["values"]) == 2:
            v1, v2 = scenario["values"]
            return f"Add {scenario['units'][0]}: {v1[0]} + {v2[0]} = {v1[0] + v2[0]}\nAdd {scenario['units'][1]}: {v1[1]} + {v2[1]} = {v1[1] + v2[1]}\nConvert and combine for final answer: {result[0]} {scenario['units'][0]} {result[1]} {scenario['units'][1]}"
        else:
            return f"Add all values and convert as needed\nFinal answer: {result[0]} {scenario['units'][0]} {result[1]} {scenario['units'][1]}"
    else:
        v1, v2 = scenario["values"]
        return f"Subtract with borrowing if needed\n{v1[0]} {scenario['units'][0]} {v1[1]} {scenario['units'][1]} - {v2[0]} {scenario['units'][0]} {v2[1]} {scenario['units'][1]}\nAnswer: {result[0]} {scenario['units'][0]} {result[1]} {scenario['units'][1]}"

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Problem {st.session_state.total_attempted + 1}")
    
    # Check if question contains context
    if "\n" in st.session_state.current_problem:
        parts = st.session_state.current_problem.split("\n")
        if len(parts) > 1:
            st.info(parts[0])  # Context
            st.markdown(f"**{parts[1]}**")  # Question
        else:
            st.markdown(f"**{st.session_state.current_problem}**")
    else:
        st.markdown(f"**{st.session_state.current_problem}**")
    
    st.markdown("---")
    
    # Display visual aid
    display_visual_aid(data)
    
    # Input fields
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1, 1])
    
    with col1:
        input1 = st.text_input(
            "",
            placeholder=data["units"][0],
            disabled=st.session_state.answer_submitted,
            key="time_input1"
        )
        st.caption(data["units"][0])
    
    with col2:
        input2 = st.text_input(
            "",
            placeholder=data["units"][1],
            disabled=st.session_state.answer_submitted,
            key="time_input2"
        )
        st.caption(data["units"][1])
    
    with col3:
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            if input1 and input2:
                try:
                    val1 = int(input1.strip())
                    val2 = int(input2.strip())
                    st.session_state.user_answer = f"{val1}|{val2}"
                    check_answer()
                except ValueError:
                    st.error("Please enter valid numbers.")
            else:
                st.warning("Please fill both fields.")
    
    with col4:
        if st.button("Skip", type="secondary", disabled=st.session_state.answer_submitted):
            st.session_state.user_answer = None
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.rerun()
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Navigation
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📖 Show Solution", type="secondary", use_container_width=True):
                show_solution()
            
            if st.button("Next Problem →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%")

def display_visual_aid(data):
    """Display visual representation of the problem"""
    operation = data.get("operation", "")
    
    # Show operation symbol
    if operation == "add":
        symbol = "➕"
        symbol_text = "Addition"
    else:
        symbol = "➖"
        symbol_text = "Subtraction"
    
    with st.expander(f"{symbol} {symbol_text} Tips", expanded=False):
        if operation == "add":
            st.markdown("""
            **Adding Mixed Time Units:**
            1. Add larger units (hours, days, years)
            2. Add smaller units (minutes, days, months)
            3. If smaller units ≥ conversion factor, carry over
            4. Add carried amount to larger units
            
            **Example:** 3h 45m + 2h 30m
            - Hours: 3 + 2 = 5
            - Minutes: 45 + 30 = 75
            - 75 minutes = 1h 15m
            - Total: 5h + 1h 15m = 6h 15m
            """)
        else:
            st.markdown("""
            **Subtracting Mixed Time Units:**
            1. Check if you can subtract smaller units
            2. If not, borrow from larger units
            3. Subtract both units
            
            **Example:** 5h 20m - 2h 45m
            - Can't subtract 45 from 20
            - Borrow: 5h 20m = 4h 80m
            - Now: 4h 80m - 2h 45m = 2h 35m
            """)

def check_answer():
    """Check the user's answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    is_correct = user_answer == correct_answer
    
    st.session_state.answer_correct = is_correct
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if is_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.problem_data
    
    # Format answers for display
    correct_parts = data['correct_answer'].split("|")
    display_answer = f"{correct_parts[0]} {data['units'][0]} {correct_parts[1]} {data['units'][1]}"
    
    if st.session_state.user_answer is None:
        st.info(f"⏭️ **Skipped.** The correct answer was: **{display_answer}**")
        st.markdown(f"📚 {data['explanation']}")
    
    elif st.session_state.answer_correct:
        st.success(f"✅ **Correct! {display_answer}**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.mixed_time_difficulty
            st.session_state.mixed_time_difficulty = min(
                st.session_state.mixed_time_difficulty + 1, 5
            )
            
            if st.session_state.mixed_time_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Great work! Moving to Level {st.session_state.mixed_time_difficulty}**")
                st.session_state.consecutive_correct = 0
    
    else:
        user_parts = st.session_state.user_answer.split("|") if "|" in st.session_state.user_answer else ["?", "?"]
        user_display = f"{user_parts[0]} {data['units'][0]} {user_parts[1] if len(user_parts) > 1 else '?'} {data['units'][1]}"
        
        st.error(f"❌ **Not quite. You answered {user_display}, but the correct answer is {display_answer}**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.mixed_time_difficulty
            st.session_state.mixed_time_difficulty = max(
                st.session_state.mixed_time_difficulty - 1, 1
            )
            
            if st.session_state.mixed_time_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.mixed_time_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_solution():
    """Show detailed solution with steps"""
    with st.expander("📚 **Step-by-Step Solution**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown("### 🔢 Detailed Solution:")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        
        # Show method based on operation
        if data["operation"] == "add":
            st.markdown("""
            ### ➕ Addition Method:
            1. Add the larger units first
            2. Add the smaller units
            3. Check if regrouping is needed
            4. If smaller units ≥ conversion factor:
               - Divide by conversion factor
               - Add quotient to larger units
               - Keep remainder as smaller units
            """)
        else:
            st.markdown("""
            ### ➖ Subtraction Method:
            1. Check if you can subtract smaller units
            2. If not, borrow from larger units:
               - Subtract 1 from larger units
               - Add conversion factor to smaller units
            3. Now subtract both units
            """)
        
        st.markdown("---")
        st.markdown("""
        ### 📊 Quick Conversion Reference:
        - 1 minute = 60 seconds
        - 1 hour = 60 minutes
        - 1 day = 24 hours
        - 1 week = 7 days
        - 1 year = 12 months
        """)

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.problem_data = {}
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None
    if 'answer_correct' in st.session_state:
        del st.session_state.answer_correct