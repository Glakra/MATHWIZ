import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

def run():
    """
    Main function to run the Convert Time Units activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/S.Time/convert_time_units.py
    """
    # Initialize session state
    if "time_difficulty" not in st.session_state:
        st.session_state.time_difficulty = 1
    
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
    st.title("⏰ Convert Time Units")
    st.markdown("*Convert between different units of time*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.time_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Conversions",
            2: "Mixed Units",
            3: "Complex Conversions",
            4: "Multi-Step Problems",
            5: "Real-World Applications"
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
    with st.expander("📚 **Time Conversion Reference**", expanded=False):
        st.markdown("""
        ### ⏰ Time Unit Conversions
        
        **Basic Units:**
        - 1 minute = **60 seconds**
        - 1 hour = **60 minutes**
        - 1 day = **24 hours**
        - 1 week = **7 days**
        - 1 month = **30 days** (approximate)
        - 1 year = **12 months**
        - 1 year = **365 days** (366 in leap year)
        - 1 decade = **10 years**
        - 1 century = **100 years**
        - 1 millennium = **1000 years**
        
        ### 📝 Common Conversions:
        
        **Hours to Minutes:**
        - 2 hours = 2 × 60 = 120 minutes
        - 3.5 hours = 3.5 × 60 = 210 minutes
        
        **Days to Hours:**
        - 3 days = 3 × 24 = 72 hours
        - 5 days = 5 × 24 = 120 hours
        
        **Weeks to Days:**
        - 4 weeks = 4 × 7 = 28 days
        - 8 weeks = 8 × 7 = 56 days
        
        **Years to Months:**
        - 2 years = 2 × 12 = 24 months
        - 5 years = 5 × 12 = 60 months
        
        ### 💡 Mixed Units:
        
        **Example 1:** 3 hours 45 minutes to minutes
        - 3 hours = 3 × 60 = 180 minutes
        - Total = 180 + 45 = 225 minutes
        
        **Example 2:** 150 minutes to hours and minutes
        - 150 ÷ 60 = 2 remainder 30
        - Answer: 2 hours 30 minutes
        
        ### 🔑 Tips:
        - Draw a conversion chart
        - Work step by step
        - Check your answer makes sense
        - Remember: multiply when converting to smaller units
        - Remember: divide when converting to larger units
        """)

def generate_new_problem():
    """Generate a new time conversion problem based on difficulty"""
    difficulty = st.session_state.time_difficulty
    
    if difficulty == 1:
        # Level 1: Basic single-unit conversions
        problem_data = generate_basic_conversion()
    elif difficulty == 2:
        # Level 2: Mixed units (e.g., hours and minutes)
        problem_data = generate_mixed_units_conversion()
    elif difficulty == 3:
        # Level 3: Complex conversions
        problem_data = generate_complex_conversion()
    elif difficulty == 4:
        # Level 4: Multi-step problems
        problem_data = generate_multi_step_conversion()
    else:
        # Level 5: Real-world applications
        problem_data = generate_real_world_conversion()
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_basic_conversion():
    """Generate Level 1 problems - basic single conversions"""
    problem_types = [
        "minutes_to_seconds",
        "hours_to_minutes",
        "days_to_hours",
        "weeks_to_days",
        "years_to_months",
        "decades_to_years",
        "seconds_to_minutes",
        "minutes_to_hours",
        "hours_to_days",
        "days_to_weeks",
        "months_to_years",
        "facts"
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == "minutes_to_seconds":
        minutes = random.randint(2, 15)
        answer = minutes * 60
        return {
            "question": f"Convert:\n{minutes} minutes = ___ seconds",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "seconds",
            "explanation": f"{minutes} minutes × 60 seconds/minute = {answer} seconds",
            "problem_type": problem_type
        }
    
    elif problem_type == "hours_to_minutes":
        hours = random.randint(2, 12)
        answer = hours * 60
        return {
            "question": f"Convert:\n{hours} hours = ___ minutes",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "minutes",
            "explanation": f"{hours} hours × 60 minutes/hour = {answer} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "days_to_hours":
        days = random.randint(2, 10)
        answer = days * 24
        return {
            "question": f"Convert:\n{days} days = ___ hours",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "hours",
            "explanation": f"{days} days × 24 hours/day = {answer} hours",
            "problem_type": problem_type
        }
    
    elif problem_type == "weeks_to_days":
        weeks = random.randint(2, 8)
        answer = weeks * 7
        return {
            "question": f"How many days are in {weeks} weeks?",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "days",
            "explanation": f"{weeks} weeks × 7 days/week = {answer} days",
            "problem_type": problem_type
        }
    
    elif problem_type == "years_to_months":
        years = random.randint(2, 10)
        answer = years * 12
        return {
            "question": f"How many months are in {years} years?",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "months",
            "explanation": f"{years} years × 12 months/year = {answer} months",
            "problem_type": problem_type
        }
    
    elif problem_type == "decades_to_years":
        decades = random.randint(2, 5)
        answer = decades * 10
        return {
            "question": f"How many years are in {decades} decades?",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "years",
            "explanation": f"{decades} decades × 10 years/decade = {answer} years",
            "problem_type": problem_type
        }
    
    elif problem_type == "seconds_to_minutes":
        seconds = random.choice([60, 120, 180, 240, 300, 360, 420, 480, 540, 600])
        answer = seconds // 60
        return {
            "question": f"Convert:\n{seconds} seconds = ___ minutes",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "minutes",
            "explanation": f"{seconds} seconds ÷ 60 seconds/minute = {answer} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "minutes_to_hours":
        minutes = random.choice([60, 120, 180, 240, 300, 360, 420, 480])
        answer = minutes // 60
        return {
            "question": f"Convert:\n{minutes} minutes = ___ hours",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "hours",
            "explanation": f"{minutes} minutes ÷ 60 minutes/hour = {answer} hours",
            "problem_type": problem_type
        }
    
    elif problem_type == "hours_to_days":
        hours = random.choice([24, 48, 72, 96, 120, 144, 168])
        answer = hours // 24
        return {
            "question": f"Convert:\n{hours} hours = ___ days",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "days",
            "explanation": f"{hours} hours ÷ 24 hours/day = {answer} days",
            "problem_type": problem_type
        }
    
    elif problem_type == "days_to_weeks":
        days = random.choice([7, 14, 21, 28, 35, 42, 49, 56, 63, 70])
        answer = days // 7
        return {
            "question": f"Convert:\n{days} days = ___ weeks",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "weeks",
            "explanation": f"{days} days ÷ 7 days/week = {answer} weeks",
            "problem_type": problem_type
        }
    
    elif problem_type == "months_to_years":
        months = random.choice([12, 24, 36, 48, 60, 72, 84, 96])
        answer = months // 12
        return {
            "question": f"Convert:\n{months} months = ___ years",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "years",
            "explanation": f"{months} months ÷ 12 months/year = {answer} years",
            "problem_type": problem_type
        }
    
    else:  # facts
        facts = [
            {
                "question": "How many days are in a normal year (not a leap year)?",
                "answer": "365",
                "unit": "days",
                "explanation": "A normal year has 365 days (leap years have 366)"
            },
            {
                "question": "How many hours are in a day?",
                "answer": "24",
                "unit": "hours",
                "explanation": "There are 24 hours in one day"
            },
            {
                "question": "How many minutes are in an hour?",
                "answer": "60",
                "unit": "minutes",
                "explanation": "There are 60 minutes in one hour"
            },
            {
                "question": "How many seconds are in a minute?",
                "answer": "60",
                "unit": "seconds",
                "explanation": "There are 60 seconds in one minute"
            }
        ]
        
        fact = random.choice(facts)
        return {
            "question": fact["question"],
            "input_type": "single",
            "correct_answer": fact["answer"],
            "unit": fact["unit"],
            "explanation": fact["explanation"],
            "problem_type": "facts"
        }

def generate_mixed_units_conversion():
    """Generate Level 2 problems - mixed units"""
    problem_types = [
        "hours_minutes_to_minutes",
        "minutes_seconds_to_seconds",
        "years_months_to_months",
        "weeks_days_to_days",
        "minutes_to_hours_minutes",
        "seconds_to_minutes_seconds",
        "hours_to_days_hours",
        "days_to_weeks_days",
        "months_to_years_months"
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == "hours_minutes_to_minutes":
        hours = random.randint(1, 5)
        minutes = random.randint(10, 59)
        answer = hours * 60 + minutes
        return {
            "question": f"Convert:\n{hours} hours {minutes} minutes = ___ minutes",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "minutes",
            "explanation": f"{hours} hours = {hours * 60} minutes\n{hours * 60} + {minutes} = {answer} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "minutes_seconds_to_seconds":
        minutes = random.randint(2, 10)
        seconds = random.randint(10, 59)
        answer = minutes * 60 + seconds
        return {
            "question": f"Convert:\n{minutes} minutes {seconds} seconds = ___ seconds",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "seconds",
            "explanation": f"{minutes} minutes = {minutes * 60} seconds\n{minutes * 60} + {seconds} = {answer} seconds",
            "problem_type": problem_type
        }
    
    elif problem_type == "years_months_to_months":
        years = random.randint(2, 8)
        months = random.randint(1, 11)
        answer = years * 12 + months
        return {
            "question": f"Convert:\n{years} years {months} months = ___ months",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "months",
            "explanation": f"{years} years = {years * 12} months\n{years * 12} + {months} = {answer} months",
            "problem_type": problem_type
        }
    
    elif problem_type == "weeks_days_to_days":
        weeks = random.randint(2, 8)
        days = random.randint(1, 6)
        answer = weeks * 7 + days
        return {
            "question": f"Convert:\n{weeks} weeks {days} days = ___ days",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": "days",
            "explanation": f"{weeks} weeks = {weeks * 7} days\n{weeks * 7} + {days} = {answer} days",
            "problem_type": problem_type
        }
    
    elif problem_type == "minutes_to_hours_minutes":
        total_minutes = random.randint(70, 500)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return {
            "question": f"Convert:\n{total_minutes} minutes = ___ hours ___ minutes",
            "input_type": "double",
            "correct_answer": f"{hours}|{minutes}",
            "units": ["hours", "minutes"],
            "explanation": f"{total_minutes} ÷ 60 = {hours} remainder {minutes}\nAnswer: {hours} hours {minutes} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "seconds_to_minutes_seconds":
        total_seconds = random.randint(70, 600)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return {
            "question": f"Convert:\n{total_seconds} seconds = ___ minutes ___ seconds",
            "input_type": "double",
            "correct_answer": f"{minutes}|{seconds}",
            "units": ["minutes", "seconds"],
            "explanation": f"{total_seconds} ÷ 60 = {minutes} remainder {seconds}\nAnswer: {minutes} minutes {seconds} seconds",
            "problem_type": problem_type
        }
    
    elif problem_type == "hours_to_days_hours":
        total_hours = random.randint(30, 200)
        days = total_hours // 24
        hours = total_hours % 24
        return {
            "question": f"Convert:\n{total_hours} hours = ___ days ___ hours",
            "input_type": "double",
            "correct_answer": f"{days}|{hours}",
            "units": ["days", "hours"],
            "explanation": f"{total_hours} ÷ 24 = {days} remainder {hours}\nAnswer: {days} days {hours} hours",
            "problem_type": problem_type
        }
    
    elif problem_type == "days_to_weeks_days":
        total_days = random.randint(10, 100)
        weeks = total_days // 7
        days = total_days % 7
        return {
            "question": f"Convert:\n{total_days} days = ___ weeks ___ days",
            "input_type": "double",
            "correct_answer": f"{weeks}|{days}",
            "units": ["weeks", "days"],
            "explanation": f"{total_days} ÷ 7 = {weeks} remainder {days}\nAnswer: {weeks} weeks {days} days",
            "problem_type": problem_type
        }
    
    else:  # months_to_years_months
        total_months = random.randint(15, 100)
        years = total_months // 12
        months = total_months % 12
        return {
            "question": f"Convert:\n{total_months} months = ___ years ___ months",
            "input_type": "double",
            "correct_answer": f"{years}|{months}",
            "units": ["years", "months"],
            "explanation": f"{total_months} ÷ 12 = {years} remainder {months}\nAnswer: {years} years {months} months",
            "problem_type": problem_type
        }

def generate_complex_conversion():
    """Generate Level 3 problems - complex conversions"""
    problem_types = [
        "cross_unit_conversion",
        "decimal_hours",
        "fractional_time",
        "large_numbers",
        "compound_time"
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == "cross_unit_conversion":
        scenarios = [
            {
                "question": "Convert 2.5 hours to seconds",
                "answer": "9000",
                "unit": "seconds",
                "explanation": "2.5 hours = 2.5 × 60 = 150 minutes\n150 minutes = 150 × 60 = 9000 seconds"
            },
            {
                "question": "Convert 180 seconds to minutes",
                "answer": "3",
                "unit": "minutes",
                "explanation": "180 seconds ÷ 60 = 3 minutes"
            },
            {
                "question": "Convert 72 hours to days",
                "answer": "3",
                "unit": "days",
                "explanation": "72 hours ÷ 24 = 3 days"
            },
            {
                "question": "Convert 3 weeks to hours",
                "answer": "504",
                "unit": "hours",
                "explanation": "3 weeks = 3 × 7 = 21 days\n21 days = 21 × 24 = 504 hours"
            }
        ]
        
        scenario = random.choice(scenarios)
        return {
            "question": scenario["question"],
            "input_type": "single",
            "correct_answer": scenario["answer"],
            "unit": scenario["unit"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "decimal_hours":
        decimal_hours = random.choice([1.5, 2.5, 3.5, 4.5, 1.25, 2.25, 3.75])
        total_minutes = int(decimal_hours * 60)
        hours = int(decimal_hours)
        minutes = total_minutes - (hours * 60)
        
        return {
            "question": f"Convert:\n{decimal_hours} hours = ___ hours ___ minutes",
            "input_type": "double",
            "correct_answer": f"{hours}|{minutes}",
            "units": ["hours", "minutes"],
            "explanation": f"{decimal_hours} hours = {hours} hours + {decimal_hours - hours} hours\n{decimal_hours - hours} hours = {decimal_hours - hours} × 60 = {minutes} minutes\nAnswer: {hours} hours {minutes} minutes",
            "problem_type": problem_type
        }
    
    elif problem_type == "fractional_time":
        fractions = [
            {"fraction": "1/2", "value": 0.5, "text": "half"},
            {"fraction": "1/4", "value": 0.25, "text": "quarter"},
            {"fraction": "3/4", "value": 0.75, "text": "three quarters"}
        ]
        
        fraction_data = random.choice(fractions)
        unit_conversions = [
            {
                "from": "hour",
                "to": "minutes",
                "multiplier": 60,
                "base": 1
            },
            {
                "from": "day",
                "to": "hours",
                "multiplier": 24,
                "base": 1
            },
            {
                "from": "week",
                "to": "days",
                "multiplier": 7,
                "base": 1
            }
        ]
        
        conversion = random.choice(unit_conversions)
        answer = int(conversion["base"] * fraction_data["value"] * conversion["multiplier"])
        
        return {
            "question": f"How many {conversion['to']} are in {fraction_data['fraction']} of a {conversion['from']}?",
            "input_type": "single",
            "correct_answer": str(answer),
            "unit": conversion["to"],
            "explanation": f"{fraction_data['fraction']} of {conversion['base']} {conversion['from']} = {fraction_data['value']} {conversion['from']}\n{fraction_data['value']} × {conversion['multiplier']} = {answer} {conversion['to']}",
            "problem_type": problem_type
        }
    
    elif problem_type == "large_numbers":
        scenarios = [
            {
                "question": "How many seconds are in 1 day?",
                "answer": "86400",
                "unit": "seconds",
                "explanation": "1 day = 24 hours = 24 × 60 = 1440 minutes\n1440 minutes = 1440 × 60 = 86400 seconds"
            },
            {
                "question": "How many minutes are in 1 week?",
                "answer": "10080",
                "unit": "minutes",
                "explanation": "1 week = 7 days = 7 × 24 = 168 hours\n168 hours = 168 × 60 = 10080 minutes"
            },
            {
                "question": "How many hours are in 1 month (30 days)?",
                "answer": "720",
                "unit": "hours",
                "explanation": "1 month (30 days) = 30 × 24 = 720 hours"
            }
        ]
        
        scenario = random.choice(scenarios)
        return {
            "question": scenario["question"],
            "input_type": "single",
            "correct_answer": scenario["answer"],
            "unit": scenario["unit"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    else:  # compound_time
        days = random.randint(2, 5)
        hours = random.randint(2, 20)
        total_hours = days * 24 + hours
        
        return {
            "question": f"Convert:\n{days} days {hours} hours = ___ hours",
            "input_type": "single",
            "correct_answer": str(total_hours),
            "unit": "hours",
            "explanation": f"{days} days = {days} × 24 = {days * 24} hours\n{days * 24} + {hours} = {total_hours} hours",
            "problem_type": problem_type
        }

def generate_multi_step_conversion():
    """Generate Level 4 problems - multi-step conversions"""
    scenarios = [
        {
            "context": "A movie marathon lasted 3 days, 5 hours, and 30 minutes",
            "question": "How many total minutes was the movie marathon?",
            "calculation": lambda: (3 * 24 * 60) + (5 * 60) + 30,
            "answer_calc": lambda: str((3 * 24 * 60) + (5 * 60) + 30),
            "unit": "minutes",
            "explanation": "3 days = 3 × 24 × 60 = 4320 minutes\n5 hours = 5 × 60 = 300 minutes\nTotal = 4320 + 300 + 30 = 4650 minutes"
        },
        {
            "context": "A project took 2 weeks, 3 days, and 8 hours to complete",
            "question": "How many total hours did the project take?",
            "calculation": lambda: (2 * 7 * 24) + (3 * 24) + 8,
            "answer_calc": lambda: str((2 * 7 * 24) + (3 * 24) + 8),
            "unit": "hours",
            "explanation": "2 weeks = 2 × 7 × 24 = 336 hours\n3 days = 3 × 24 = 72 hours\nTotal = 336 + 72 + 8 = 416 hours"
        },
        {
            "context": "A plant has been growing for 3 years and 4 months",
            "question": "How many total months has the plant been growing?",
            "calculation": lambda: (3 * 12) + 4,
            "answer_calc": lambda: str((3 * 12) + 4),
            "unit": "months",
            "explanation": "3 years = 3 × 12 = 36 months\nTotal = 36 + 4 = 40 months"
        },
        {
            "context": "A flight was delayed by 195 minutes",
            "question": "Express this delay in hours and minutes",
            "calculation": lambda: (195 // 60, 195 % 60),
            "answer_calc": lambda: f"{195 // 60}|{195 % 60}",
            "units": ["hours", "minutes"],
            "explanation": "195 minutes ÷ 60 = 3 hours 15 minutes",
            "input_type": "double"
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if "units" in scenario:
        return {
            "question": f"{scenario['context']}.\n{scenario['question']}",
            "input_type": scenario.get("input_type", "double"),
            "correct_answer": scenario["answer_calc"](),
            "units": scenario["units"],
            "explanation": scenario["explanation"],
            "problem_type": "multi_step"
        }
    else:
        return {
            "question": f"{scenario['context']}.\n{scenario['question']}",
            "input_type": "single",
            "correct_answer": scenario["answer_calc"](),
            "unit": scenario["unit"],
            "explanation": scenario["explanation"],
            "problem_type": "multi_step"
        }

def generate_real_world_conversion():
    """Generate Level 5 problems - real-world applications"""
    scenarios = [
        {
            "context": "Sarah practices piano for 45 minutes every day",
            "question": "How many hours does she practice in a 30-day month?",
            "calculation": lambda: (45 * 30) // 60,
            "remainder": lambda: (45 * 30) % 60,
            "answer_calc": lambda: f"{(45 * 30) // 60}|{(45 * 30) % 60}",
            "units": ["hours", "minutes"],
            "explanation": "45 minutes × 30 days = 1350 minutes\n1350 ÷ 60 = 22 hours 30 minutes"
        },
        {
            "context": "A bakery is open 10 hours per day, 6 days a week",
            "question": "How many hours is the bakery open in 4 weeks?",
            "answer": str(10 * 6 * 4),
            "unit": "hours",
            "explanation": "10 hours/day × 6 days/week = 60 hours/week\n60 hours/week × 4 weeks = 240 hours"
        },
        {
            "context": "A TV series has 5 seasons with 12 episodes each. Each episode is 45 minutes",
            "question": "What is the total viewing time in hours?",
            "answer": str((5 * 12 * 45) // 60),
            "unit": "hours",
            "explanation": "5 seasons × 12 episodes = 60 episodes\n60 episodes × 45 minutes = 2700 minutes\n2700 ÷ 60 = 45 hours"
        },
        {
            "context": "A student studies 2 hours on weekdays and 3 hours on weekends",
            "question": "How many hours does the student study in a week?",
            "answer": str((2 * 5) + (3 * 2)),
            "unit": "hours",
            "explanation": "Weekdays: 2 hours × 5 days = 10 hours\nWeekends: 3 hours × 2 days = 6 hours\nTotal = 10 + 6 = 16 hours"
        },
        {
            "context": "A marathon runner trains for 90 minutes, 4 times per week",
            "question": "How many hours does the runner train in 3 weeks?",
            "answer": str((90 * 4 * 3) // 60),
            "unit": "hours",
            "explanation": "90 minutes × 4 times/week = 360 minutes/week\n360 minutes/week × 3 weeks = 1080 minutes\n1080 ÷ 60 = 18 hours"
        },
        {
            "context": "A factory operates 16 hours per day, 25 days per month",
            "question": "How many days (24-hour periods) does the factory operate in a month?",
            "answer": f"{(16 * 25) // 24}|{(16 * 25) % 24}",
            "units": ["days", "hours"],
            "explanation": "16 hours/day × 25 days = 400 hours\n400 ÷ 24 = 16 days 16 hours"
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if "units" in scenario:
        if "answer_calc" in scenario:
            answer = scenario["answer_calc"]()
        else:
            answer = scenario["answer"]
        
        return {
            "question": f"{scenario['context']}.\n{scenario['question']}",
            "input_type": "double",
            "correct_answer": answer,
            "units": scenario["units"],
            "explanation": scenario["explanation"],
            "problem_type": "real_world"
        }
    else:
        return {
            "question": f"{scenario['context']}.\n{scenario['question']}",
            "input_type": "single",
            "correct_answer": scenario["answer"],
            "unit": scenario["unit"],
            "explanation": scenario["explanation"],
            "problem_type": "real_world"
        }

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Problem {st.session_state.total_attempted + 1}")
    
    # Check if question contains context (multiline)
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
    
    # Display visual aid if applicable
    display_visual_aid(data)
    
    # Input form based on type
    if data["input_type"] == "single":
        display_single_input(data)
    else:  # double
        display_double_input(data)
    
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
    """Display visual aids for the problem"""
    problem_type = data.get("problem_type", "")
    
    # Create a simple visual timeline or conversion chart if helpful
    if problem_type in ["hours_to_days_hours", "days_to_weeks_days", "minutes_to_hours_minutes"]:
        with st.expander("💡 Visual Aid", expanded=False):
            if "hours" in problem_type and "days" in problem_type:
                st.markdown("""
                ```
                1 day = 24 hours
                2 days = 48 hours
                3 days = 72 hours
                ...
                ```
                """)
            elif "days" in problem_type and "weeks" in problem_type:
                st.markdown("""
                ```
                1 week = 7 days
                2 weeks = 14 days
                3 weeks = 21 days
                ...
                ```
                """)
            elif "minutes" in problem_type and "hours" in problem_type:
                st.markdown("""
                ```
                1 hour = 60 minutes
                2 hours = 120 minutes
                3 hours = 180 minutes
                ...
                ```
                """)

def display_single_input(data):
    """Display single input field"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Your answer:",
            placeholder=f"Enter {data.get('unit', 'answer')}",
            disabled=st.session_state.answer_submitted,
            key="time_input"
        )
        if "unit" in data:
            st.caption(data["unit"])
    
    with col2:
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            if user_input:
                st.session_state.user_answer = user_input.strip()
                check_answer()
            else:
                st.warning("Please enter your answer.")
    
    with col3:
        if st.button("Skip", type="secondary", disabled=st.session_state.answer_submitted):
            st.session_state.user_answer = None
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.rerun()

def display_double_input(data):
    """Display double input fields for mixed units"""
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1, 1])
    
    with col1:
        input1 = st.text_input(
            f"{data['units'][0]}:",
            placeholder="",
            disabled=st.session_state.answer_submitted,
            key="time_input1"
        )
        st.caption(data["units"][0])
    
    with col2:
        input2 = st.text_input(
            f"{data['units'][1]}:",
            placeholder="",
            disabled=st.session_state.answer_submitted,
            key="time_input2"
        )
        st.caption(data["units"][1])
    
    with col3:
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            if input1 and input2:
                st.session_state.user_answer = f"{input1.strip()}|{input2.strip()}"
                check_answer()
            else:
                st.warning("Please fill both fields.")
    
    with col4:
        if st.button("Skip", type="secondary", disabled=st.session_state.answer_submitted):
            st.session_state.user_answer = None
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.rerun()

def check_answer():
    """Check the user's answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # For double inputs, check both parts
    if "|" in str(correct_answer):
        is_correct = user_answer == correct_answer
    else:
        # For single inputs, compare as strings (after stripping)
        is_correct = str(user_answer).strip() == str(correct_answer).strip()
    
    st.session_state.answer_correct = is_correct
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if is_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.problem_data
    
    if st.session_state.user_answer is None:
        # Format answer for display
        if "|" in str(data['correct_answer']):
            parts = data['correct_answer'].split("|")
            display_answer = f"{parts[0]} {data['units'][0]} {parts[1]} {data['units'][1]}"
        else:
            display_answer = f"{data['correct_answer']} {data.get('unit', '')}"
        
        st.info(f"⏭️ **Skipped.** The correct answer was: **{display_answer}**")
        st.markdown(f"📚 {data['explanation']}")
    
    elif st.session_state.answer_correct:
        # Format answer for display
        if "|" in str(data['correct_answer']):
            parts = data['correct_answer'].split("|")
            display_answer = f"{parts[0]} {data['units'][0]} {parts[1]} {data['units'][1]}"
        else:
            display_answer = f"{data['correct_answer']} {data.get('unit', '')}"
        
        st.success(f"✅ **Correct! {display_answer}**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.time_difficulty
            st.session_state.time_difficulty = min(
                st.session_state.time_difficulty + 1, 5
            )
            
            if st.session_state.time_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Excellent! Moving to Level {st.session_state.time_difficulty}**")
                st.session_state.consecutive_correct = 0
    
    else:
        # Format answers for display
        if "|" in str(data['correct_answer']):
            parts = data['correct_answer'].split("|")
            display_answer = f"{parts[0]} {data['units'][0]} {parts[1]} {data['units'][1]}"
            
            user_parts = st.session_state.user_answer.split("|") if "|" in st.session_state.user_answer else ["?", "?"]
            user_display = f"{user_parts[0]} {data['units'][0]} {user_parts[1] if len(user_parts) > 1 else '?'} {data['units'][1]}"
        else:
            display_answer = f"{data['correct_answer']} {data.get('unit', '')}"
            user_display = f"{st.session_state.user_answer} {data.get('unit', '')}"
        
        st.error(f"❌ **Not quite. You said {user_display}, but the correct answer is {display_answer}**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.time_difficulty
            st.session_state.time_difficulty = max(
                st.session_state.time_difficulty - 1, 1
            )
            
            if st.session_state.time_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.time_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_solution():
    """Show detailed solution"""
    with st.expander("📚 **Step-by-Step Solution**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown("### 🔢 Solution:")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        
        # Show conversion chart
        st.markdown("### 📊 Quick Reference:")
        st.markdown("""
        | From | To | Multiply by |
        |------|-----|------------|
        | Minutes | Seconds | 60 |
        | Hours | Minutes | 60 |
        | Days | Hours | 24 |
        | Weeks | Days | 7 |
        | Years | Months | 12 |
        | Decades | Years | 10 |
        """)
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Remember:
        - **Smaller to Larger:** Divide
        - **Larger to Smaller:** Multiply
        - Always check if your answer makes sense!
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