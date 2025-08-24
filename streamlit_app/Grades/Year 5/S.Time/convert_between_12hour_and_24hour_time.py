import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def run():
    """
    Main function to run the Convert between 12-hour and 24-hour time activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/S.Time/convert_between_12_hour_and_24_hour_time.py
    """
    # Initialize session state
    if "time_conversion_difficulty" not in st.session_state:
        st.session_state.time_conversion_difficulty = 1
    
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
    st.title("🕐 Convert Between 12-hour and 24-hour Time")
    st.markdown("*Master time conversion between 12-hour (AM/PM) and 24-hour formats*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.time_conversion_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Morning Times (AM)",
            2: "Afternoon Times (PM)",
            3: "Tricky Times (Noon/Midnight)",
            4: "All Times Mixed",
            5: "Real-World Schedules"
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
    with st.expander("📚 **Time Conversion Guide**", expanded=False):
        st.markdown("""
        ### 🕐 12-Hour vs 24-Hour Time
        
        **12-Hour Time (AM/PM):**
        - Uses AM (morning) and PM (afternoon/evening)
        - 12:00 AM = Midnight (start of day)
        - 12:00 PM = Noon (midday)
        - Hours go: 12, 1, 2, 3...11 (then repeat with AM/PM change)
        
        **24-Hour Time (Military Time):**
        - No AM/PM needed
        - 00:00 = Midnight (start of day)
        - 12:00 = Noon (midday)
        - Hours go: 00, 01, 02...23 (then back to 00)
        
        ### 🔄 Conversion Rules
        
        **12-Hour → 24-Hour:**
        
        **Morning (AM):**
        - 12:00 AM - 12:59 AM → 00:00 - 00:59
        - 1:00 AM - 11:59 AM → 01:00 - 11:59
        - *(Keep same numbers, but 12 AM becomes 00)*
        
        **Afternoon/Evening (PM):**
        - 12:00 PM - 12:59 PM → 12:00 - 12:59
        - 1:00 PM - 11:59 PM → 13:00 - 23:59
        - *(Add 12 to hours, except for 12 PM)*
        
        **24-Hour → 12-Hour:**
        
        **00:00 - 11:59 → 12:00 AM - 11:59 AM**
        - 00:00 - 00:59 → 12:00 AM - 12:59 AM
        - 01:00 - 11:59 → 1:00 AM - 11:59 AM
        
        **12:00 - 23:59 → 12:00 PM - 11:59 PM**
        - 12:00 - 12:59 → 12:00 PM - 12:59 PM
        - 13:00 - 23:59 → 1:00 PM - 11:59 PM
        - *(Subtract 12 from hours 13-23)*
        
        ### 📊 Quick Reference Table
        
        | 12-Hour | 24-Hour | 12-Hour | 24-Hour |
        |---------|---------|---------|---------|
        | 12:00 AM | 00:00 | 12:00 PM | 12:00 |
        | 1:00 AM | 01:00 | 1:00 PM | 13:00 |
        | 2:00 AM | 02:00 | 2:00 PM | 14:00 |
        | 3:00 AM | 03:00 | 3:00 PM | 15:00 |
        | 6:00 AM | 06:00 | 6:00 PM | 18:00 |
        | 9:00 AM | 09:00 | 9:00 PM | 21:00 |
        | 11:00 AM | 11:00 | 11:00 PM | 23:00 |
        | 11:59 AM | 11:59 | 11:59 PM | 23:59 |
        
        ### 💡 Tips:
        - Remember: 12 AM = Midnight = 00:00
        - Remember: 12 PM = Noon = 12:00
        - AM times (except 12 AM) stay the same
        - PM times (except 12 PM) add 12
        - Always use leading zeros in 24-hour time (05:00, not 5:00)
        """)

def generate_new_problem():
    """Generate a new time conversion problem based on difficulty"""
    difficulty = st.session_state.time_conversion_difficulty
    
    if difficulty == 1:
        # Level 1: Morning times (AM) - simple conversions
        problem_data = generate_morning_problem()
    elif difficulty == 2:
        # Level 2: Afternoon/Evening times (PM)
        problem_data = generate_afternoon_problem()
    elif difficulty == 3:
        # Level 3: Tricky times (noon, midnight, edge cases)
        problem_data = generate_tricky_problem()
    elif difficulty == 4:
        # Level 4: Mixed times - all types
        problem_data = generate_mixed_problem()
    else:
        # Level 5: Real-world schedule conversions
        problem_data = generate_real_world_problem()
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_morning_problem():
    """Generate Level 1: Morning time conversions"""
    # Decide conversion direction
    direction = random.choice(["24_to_12", "12_to_24"])
    
    if direction == "24_to_12":
        # Generate 24-hour morning time
        hour = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        minute = random.choice([0, 15, 30, 45] + list(range(0, 60, 5)))
        
        time_24 = f"{hour:02d}:{minute:02d}"
        
        # Convert to 12-hour
        if hour == 0:
            time_12 = f"12:{minute:02d} A.M."
        else:
            time_12 = f"{hour}:{minute:02d} A.M."
        
        return {
            "question": f"Write {time_24} as a 12-hour time.\n\nWrite your answer using only numbers, a colon, and A.M. or P.M. (for example, 3:15 A.M.).",
            "problem_type": "24_to_12",
            "given_time": time_24,
            "correct_answer": time_12,
            "explanation": generate_24_to_12_explanation(hour, minute, time_24, time_12),
            "show_visual": False
        }
    
    else:  # 12_to_24
        # Generate 12-hour morning time
        hour = random.choice([12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        minute = random.choice([0, 15, 30, 45] + list(range(0, 60, 5)))
        
        if hour == 12:
            time_12 = f"{hour}:{minute:02d} A.M."
            time_24 = f"00:{minute:02d}"
        else:
            time_12 = f"{hour}:{minute:02d} A.M."
            time_24 = f"{hour:02d}:{minute:02d}"
        
        return {
            "question": f"Write {time_12} as a 24-hour time.\n\nWrite your answer using only numbers and a colon (for example, 03:15).",
            "problem_type": "12_to_24",
            "given_time": time_12,
            "correct_answer": time_24,
            "explanation": generate_12_to_24_explanation(hour, minute, "A.M.", time_12, time_24),
            "show_visual": False
        }

def generate_afternoon_problem():
    """Generate Level 2: Afternoon/Evening time conversions"""
    direction = random.choice(["24_to_12", "12_to_24"])
    
    if direction == "24_to_12":
        # Generate 24-hour afternoon/evening time
        hour = random.choice([12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
        minute = random.choice([0, 15, 30, 45] + list(range(0, 60, 5)))
        
        time_24 = f"{hour:02d}:{minute:02d}"
        
        # Convert to 12-hour
        if hour == 12:
            time_12 = f"12:{minute:02d} P.M."
        else:
            display_hour = hour - 12
            time_12 = f"{display_hour}:{minute:02d} P.M."
        
        return {
            "question": f"Write {time_24} as a 12-hour time.\n\nWrite your answer using only numbers, a colon, and A.M. or P.M. (for example, 3:15 A.M.).",
            "problem_type": "24_to_12",
            "given_time": time_24,
            "correct_answer": time_12,
            "explanation": generate_24_to_12_explanation(hour, minute, time_24, time_12),
            "show_visual": False
        }
    
    else:  # 12_to_24
        # Generate 12-hour afternoon/evening time
        hour = random.choice([12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        minute = random.choice([0, 15, 30, 45] + list(range(0, 60, 5)))
        
        time_12 = f"{hour}:{minute:02d} P.M."
        
        if hour == 12:
            time_24 = f"12:{minute:02d}"
        else:
            time_24 = f"{hour + 12:02d}:{minute:02d}"
        
        return {
            "question": f"Write {time_12} as a 24-hour time.\n\nWrite your answer using only numbers and a colon (for example, 03:15).",
            "problem_type": "12_to_24",
            "given_time": time_12,
            "correct_answer": time_24,
            "explanation": generate_12_to_24_explanation(hour, minute, "P.M.", time_12, time_24),
            "show_visual": False
        }

def generate_tricky_problem():
    """Generate Level 3: Tricky times (noon, midnight, transitions)"""
    tricky_times = [
        # Midnight variations
        {"24h": "00:00", "12h": "12:00 A.M.", "context": "midnight"},
        {"24h": "00:01", "12h": "12:01 A.M.", "context": "just after midnight"},
        {"24h": "00:30", "12h": "12:30 A.M.", "context": "half past midnight"},
        {"24h": "00:59", "12h": "12:59 A.M.", "context": "almost 1 AM"},
        
        # Noon variations
        {"24h": "12:00", "12h": "12:00 P.M.", "context": "noon"},
        {"24h": "12:01", "12h": "12:01 P.M.", "context": "just after noon"},
        {"24h": "12:30", "12h": "12:30 P.M.", "context": "half past noon"},
        {"24h": "12:59", "12h": "12:59 P.M.", "context": "almost 1 PM"},
        
        # Transition times
        {"24h": "11:59", "12h": "11:59 A.M.", "context": "one minute before noon"},
        {"24h": "13:00", "12h": "1:00 P.M.", "context": "one hour after noon"},
        {"24h": "23:59", "12h": "11:59 P.M.", "context": "one minute before midnight"},
        {"24h": "01:00", "12h": "1:00 A.M.", "context": "one hour after midnight"},
    ]
    
    time_data = random.choice(tricky_times)
    direction = random.choice(["24_to_12", "12_to_24"])
    
    if direction == "24_to_12":
        return {
            "question": f"Write {time_data['24h']} as a 12-hour time.\n\nWrite your answer using only numbers, a colon, and A.M. or P.M. (for example, 3:15 A.M.).",
            "problem_type": "24_to_12",
            "given_time": time_data['24h'],
            "correct_answer": time_data['12h'],
            "explanation": f"{time_data['24h']} in 24-hour time is {time_data['context']}.\nIn 12-hour format, this is {time_data['12h']}.\n\nRemember:\n- 00:00-00:59 = 12:00-12:59 A.M.\n- 12:00-12:59 = 12:00-12:59 P.M.",
            "show_visual": True
        }
    else:
        return {
            "question": f"Write {time_data['12h']} as a 24-hour time.\n\nWrite your answer using only numbers and a colon (for example, 03:15).",
            "problem_type": "12_to_24",
            "given_time": time_data['12h'],
            "correct_answer": time_data['24h'],
            "explanation": f"{time_data['12h']} is {time_data['context']}.\nIn 24-hour format, this is {time_data['24h']}.\n\nRemember:\n- 12:00-12:59 A.M. = 00:00-00:59\n- 12:00-12:59 P.M. = 12:00-12:59",
            "show_visual": True
        }

def generate_mixed_problem():
    """Generate Level 4: Mixed time conversions"""
    # Generate any time of day
    hour_24 = random.randint(0, 23)
    minute = random.randint(0, 59)
    
    time_24 = f"{hour_24:02d}:{minute:02d}"
    
    # Convert to 12-hour
    if hour_24 == 0:
        time_12 = f"12:{minute:02d} A.M."
    elif hour_24 < 12:
        time_12 = f"{hour_24}:{minute:02d} A.M."
    elif hour_24 == 12:
        time_12 = f"12:{minute:02d} P.M."
    else:
        time_12 = f"{hour_24 - 12}:{minute:02d} P.M."
    
    # Randomly choose direction
    direction = random.choice(["24_to_12", "12_to_24"])
    
    if direction == "24_to_12":
        return {
            "question": f"Write {time_24} as a 12-hour time.\n\nWrite your answer using only numbers, a colon, and A.M. or P.M. (for example, 3:15 A.M.).",
            "problem_type": "24_to_12",
            "given_time": time_24,
            "correct_answer": time_12,
            "explanation": generate_24_to_12_explanation(hour_24, minute, time_24, time_12),
            "show_visual": False
        }
    else:
        return {
            "question": f"Write {time_12} as a 24-hour time.\n\nWrite your answer using only numbers and a colon (for example, 03:15).",
            "problem_type": "12_to_24",
            "given_time": time_12,
            "correct_answer": time_24,
            "explanation": generate_12_to_24_explanation_from_full(time_12, time_24),
            "show_visual": False
        }

def generate_real_world_problem():
    """Generate Level 5: Real-world schedule conversions"""
    scenarios = [
        {
            "context": "A train schedule shows departure at 14:35",
            "question": "What time is this in 12-hour format?",
            "given": "14:35",
            "answer": "2:35 P.M.",
            "type": "24_to_12"
        },
        {
            "context": "The doctor's appointment is at 3:45 P.M.",
            "question": "How would this appear on a 24-hour digital clock?",
            "given": "3:45 P.M.",
            "answer": "15:45",
            "type": "12_to_24"
        },
        {
            "context": "An international flight departs at 23:50",
            "question": "What time is this in 12-hour format?",
            "given": "23:50",
            "answer": "11:50 P.M.",
            "type": "24_to_12"
        },
        {
            "context": "The museum opens at 9:00 A.M.",
            "question": "How would this be shown in military time?",
            "given": "9:00 A.M.",
            "answer": "09:00",
            "type": "12_to_24"
        },
        {
            "context": "A TV show airs at 20:00",
            "question": "What time should you tune in using AM/PM format?",
            "given": "20:00",
            "answer": "8:00 P.M.",
            "type": "24_to_12"
        },
        {
            "context": "The restaurant closes at 10:30 P.M.",
            "question": "What is this in 24-hour time?",
            "given": "10:30 P.M.",
            "answer": "22:30",
            "type": "12_to_24"
        },
        {
            "context": "Your flight boards at 06:45",
            "question": "What time is this in 12-hour format?",
            "given": "06:45",
            "answer": "6:45 A.M.",
            "type": "24_to_12"
        },
        {
            "context": "School starts at 8:30 A.M.",
            "question": "How is this written in 24-hour time?",
            "given": "8:30 A.M.",
            "answer": "08:30",
            "type": "12_to_24"
        },
        {
            "context": "The night shift begins at 00:00",
            "question": "What time is this in 12-hour format?",
            "given": "00:00",
            "answer": "12:00 A.M.",
            "type": "24_to_12"
        },
        {
            "context": "Lunch is served at 12:15 P.M.",
            "question": "Express this in 24-hour time.",
            "given": "12:15 P.M.",
            "answer": "12:15",
            "type": "12_to_24"
        }
    ]
    
    scenario = random.choice(scenarios)
    
    # Create multiple choice options including some with schedule context
    schedule_contexts = [
        "Bus Schedule:",
        "Train Timetable:",
        "Flight Schedule:",
        "TV Guide:",
        "Work Schedule:",
        "School Timetable:",
        "Hospital Hours:",
        "Store Hours:"
    ]
    
    schedule_context = random.choice(schedule_contexts)
    
    if scenario["type"] == "24_to_12":
        instruction = "Write your answer using only numbers, a colon, and A.M. or P.M. (for example, 3:15 A.M.)."
    else:
        instruction = "Write your answer using only numbers and a colon (for example, 03:15)."
    
    return {
        "question": f"{schedule_context}\n{scenario['context']}.\n{scenario['question']}\n\n{instruction}",
        "problem_type": scenario["type"],
        "given_time": scenario["given"],
        "correct_answer": scenario["answer"],
        "explanation": f"Given: {scenario['given']}\nAnswer: {scenario['answer']}\n\n{generate_context_explanation(scenario['type'], scenario['given'], scenario['answer'])}",
        "show_visual": True,
        "context": schedule_context
    }

def generate_24_to_12_explanation(hour_24, minute, time_24, time_12):
    """Generate explanation for 24-hour to 12-hour conversion"""
    if hour_24 == 0:
        return f"{time_24} is midnight (start of the day).\n00:XX becomes 12:XX A.M.\nAnswer: {time_12}"
    elif hour_24 < 12:
        return f"{time_24} is in the morning.\nHours 01-11 stay the same, just add A.M.\nAnswer: {time_12}"
    elif hour_24 == 12:
        return f"{time_24} is noon (midday).\n12:XX stays as 12:XX but with P.M.\nAnswer: {time_12}"
    else:
        return f"{time_24} is in the afternoon/evening.\nSubtract 12 from the hour: {hour_24} - 12 = {hour_24 - 12}\nAdd P.M.\nAnswer: {time_12}"

def generate_12_to_24_explanation(hour_12, minute, period, time_12, time_24):
    """Generate explanation for 12-hour to 24-hour conversion"""
    if period == "A.M.":
        if hour_12 == 12:
            return f"{time_12} is midnight.\n12:XX A.M. becomes 00:XX\nAnswer: {time_24}"
        else:
            return f"{time_12} is in the morning.\nA.M. times (except 12 A.M.) stay the same.\nAdd leading zero if needed.\nAnswer: {time_24}"
    else:  # P.M.
        if hour_12 == 12:
            return f"{time_12} is noon.\n12:XX P.M. stays as 12:XX\nAnswer: {time_24}"
        else:
            return f"{time_12} is in the afternoon/evening.\nAdd 12 to the hour: {hour_12} + 12 = {hour_12 + 12}\nAnswer: {time_24}"

def generate_12_to_24_explanation_from_full(time_12, time_24):
    """Generate explanation from full time strings"""
    parts = time_12.split()
    time_part = parts[0]
    period = parts[1]
    
    hour_12 = int(time_part.split(":")[0])
    
    if period == "A.M.":
        if hour_12 == 12:
            return f"{time_12} is just after midnight.\n12:XX A.M. becomes 00:XX\nAnswer: {time_24}"
        else:
            return f"{time_12} is in the morning.\nA.M. times stay the same, add leading zero if needed.\nAnswer: {time_24}"
    else:
        if hour_12 == 12:
            return f"{time_12} is in the afternoon.\n12:XX P.M. stays as 12:XX\nAnswer: {time_24}"
        else:
            return f"{time_12} is in the afternoon/evening.\nAdd 12: {hour_12} + 12 = {hour_12 + 12}\nAnswer: {time_24}"

def generate_context_explanation(conversion_type, given, answer):
    """Generate explanation with context"""
    if conversion_type == "24_to_12":
        hour = int(given.split(":")[0])
        if hour < 6:
            time_period = "early morning"
        elif hour < 12:
            time_period = "morning"
        elif hour == 12:
            time_period = "noon"
        elif hour < 17:
            time_period = "afternoon"
        elif hour < 21:
            time_period = "evening"
        else:
            time_period = "night"
        return f"This is {time_period}. In everyday use, we'd say {answer}."
    else:
        if "A.M." in given:
            return f"Morning times use A.M. In 24-hour format, we use {answer}."
        else:
            return f"Afternoon/evening times use P.M. In 24-hour format, we use {answer}."

def display_problem():
    """Display the current problem"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Problem {st.session_state.total_attempted + 1}")
    
    # Check if there's context
    if "context" in data:
        st.info(data.get("context", ""))
    
    # Display the main question
    lines = st.session_state.current_problem.split("\n")
    for line in lines[:-1]:  # All lines except the instruction
        if line:
            st.markdown(f"**{line}**")
    
    # Display the instruction separately
    if lines:
        st.caption(lines[-1])
    
    st.markdown("---")
    
    # Display visual aid if applicable
    if data.get("show_visual", False):
        display_time_visual(data)
    
    # Input field
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if data["problem_type"] == "24_to_12":
            placeholder = "e.g., 3:15 A.M."
        else:
            placeholder = "e.g., 03:15"
        
        user_input = st.text_input(
            "Your answer:",
            placeholder=placeholder,
            disabled=st.session_state.answer_submitted,
            key="conversion_input"
        )
    
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

def display_time_visual(data):
    """Display visual representation of time conversion"""
    with st.expander("🕐 Visual Aid", expanded=False):
        # Create two clocks side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        
        # Parse the given time
        given_time = data["given_time"]
        
        if data["problem_type"] == "24_to_12":
            # Given is 24-hour
            hour_24 = int(given_time.split(":")[0])
            minute = int(given_time.split(":")[1])
            
            # Left clock shows 24-hour
            draw_digital_clock(ax1, given_time, "24-Hour Time")
            
            # Right clock shows 12-hour (answer)
            draw_analog_clock(ax2, hour_24, minute, "12-Hour Time")
            
        else:
            # Given is 12-hour
            parts = given_time.replace(".", "").split()
            time_parts = parts[0].split(":")
            hour_12 = int(time_parts[0])
            minute = int(time_parts[1])
            period = parts[1]
            
            # Convert to 24-hour for display
            if period == "AM" and hour_12 == 12:
                hour_24 = 0
            elif period == "AM":
                hour_24 = hour_12
            elif period == "PM" and hour_12 == 12:
                hour_24 = 12
            else:
                hour_24 = hour_12 + 12
            
            # Left clock shows 12-hour
            draw_analog_clock(ax1, hour_24, minute, "12-Hour Time")
            
            # Right clock shows 24-hour (answer)
            draw_digital_clock(ax2, f"{hour_24:02d}:{minute:02d}", "24-Hour Time")
        
        st.pyplot(fig)
        plt.close()

def draw_analog_clock(ax, hour_24, minute, title):
    """Draw an analog clock"""
    # Draw clock circle
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=2)
    ax.add_patch(circle)
    
    # Draw hour markers
    for i in range(12):
        angle = np.pi/2 - (i * np.pi/6)
        x = 0.85 * np.cos(angle)
        y = 0.85 * np.sin(angle)
        ax.text(x, y, str(12 if i == 0 else i), ha='center', va='center', fontsize=10)
    
    # Draw hands
    hour_12 = hour_24 % 12
    hour_angle = np.pi/2 - ((hour_12 + minute/60) * np.pi/6)
    minute_angle = np.pi/2 - (minute * np.pi/30)
    
    # Hour hand
    ax.arrow(0, 0, 0.5 * np.cos(hour_angle), 0.5 * np.sin(hour_angle),
            head_width=0.05, head_length=0.05, fc='black', ec='black', linewidth=2)
    
    # Minute hand
    ax.arrow(0, 0, 0.75 * np.cos(minute_angle), 0.75 * np.sin(minute_angle),
            head_width=0.03, head_length=0.03, fc='blue', ec='blue', linewidth=1.5)
    
    # Center dot
    ax.plot(0, 0, 'ko', markersize=8)
    
    # Add AM/PM indicator
    period = "AM" if hour_24 < 12 else "PM"
    ax.text(0, -1.3, period, ha='center', fontsize=12, fontweight='bold')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12, fontweight='bold')

def draw_digital_clock(ax, time_str, title):
    """Draw a digital clock display"""
    # Create digital display background
    rect = patches.Rectangle((-0.8, -0.3), 1.6, 0.6, linewidth=2, 
                            edgecolor='black', facecolor='lightgreen', alpha=0.3)
    ax.add_patch(rect)
    
    # Display time
    ax.text(0, 0, time_str, ha='center', va='center', fontsize=24, 
           fontfamily='monospace', fontweight='bold')
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.5, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12, fontweight='bold')

def normalize_answer(answer):
    """Normalize answer for comparison"""
    # Remove extra spaces
    answer = answer.strip()
    
    # Handle various formats
    answer = answer.replace(" ", "")
    answer = answer.replace(".", "")
    answer = answer.upper()
    
    # Ensure AM/PM has dots
    answer = answer.replace("AM", "A.M.")
    answer = answer.replace("PM", "P.M.")
    
    # Add space before AM/PM
    if "A.M." in answer:
        answer = answer.replace("A.M.", " A.M.")
    if "P.M." in answer:
        answer = answer.replace("P.M.", " P.M.")
    
    return answer

def check_answer():
    """Check the user's answer"""
    user_answer = normalize_answer(st.session_state.user_answer)
    correct_answer = normalize_answer(st.session_state.correct_answer)
    
    # Additional flexibility for 24-hour format
    if ":" in user_answer and "M" not in user_answer:
        # Ensure leading zeros for 24-hour time
        parts = user_answer.split(":")
        if len(parts) == 2:
            try:
                h = int(parts[0])
                m = int(parts[1])
                user_answer = f"{h:02d}:{m:02d}"
            except:
                pass
    
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
    
    if st.session_state.user_answer is None:
        st.info(f"⏭️ **Skipped.** The correct answer was: **{data['correct_answer']}**")
        st.markdown(f"📚 {data['explanation']}")
    
    elif st.session_state.answer_correct:
        st.success(f"✅ **Correct! {data['correct_answer']}**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.time_conversion_difficulty
            st.session_state.time_conversion_difficulty = min(
                st.session_state.time_conversion_difficulty + 1, 5
            )
            
            if st.session_state.time_conversion_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Excellent! Moving to Level {st.session_state.time_conversion_difficulty}**")
                st.session_state.consecutive_correct = 0
    
    else:
        st.error(f"❌ **Not quite. You wrote {st.session_state.user_answer}, but the correct answer is {data['correct_answer']}**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.time_conversion_difficulty
            st.session_state.time_conversion_difficulty = max(
                st.session_state.time_conversion_difficulty - 1, 1
            )
            
            if st.session_state.time_conversion_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.time_conversion_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_solution():
    """Show detailed solution with conversion guide"""
    with st.expander("📚 **Complete Conversion Guide**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown("### 🔢 Solution:")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        
        if data["problem_type"] == "24_to_12":
            st.markdown("""
            ### 🔄 24-Hour → 12-Hour Conversion Steps:
            
            1. **Check the hour:**
               - 00:XX → 12:XX A.M. (midnight hour)
               - 01:XX to 11:XX → Same time with A.M.
               - 12:XX → 12:XX P.M. (noon hour)
               - 13:XX to 23:XX → Subtract 12, add P.M.
            
            2. **Minutes stay the same**
            
            3. **Add A.M. or P.M.**
            """)
        else:
            st.markdown("""
            ### 🔄 12-Hour → 24-Hour Conversion Steps:
            
            1. **Check A.M. or P.M.:**
               - 12:XX A.M. → 00:XX (midnight hour)
               - 1:XX to 11:XX A.M. → Same time (add leading zero if needed)
               - 12:XX P.M. → 12:XX (noon hour)
               - 1:XX to 11:XX P.M. → Add 12 to the hour
            
            2. **Minutes stay the same**
            
            3. **Use leading zeros (05:30, not 5:30)**
            """)
        
        st.markdown("---")
        
        # Quick reference table
        st.markdown("### 📊 Quick Reference:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Special Times:**
            - 12:00 A.M. = 00:00 (Midnight)
            - 12:30 A.M. = 00:30
            - 12:00 P.M. = 12:00 (Noon)
            - 12:30 P.M. = 12:30
            """)
        
        with col2:
            st.markdown("""
            **Common Times:**
            - 6:00 A.M. = 06:00
            - 9:00 A.M. = 09:00
            - 3:00 P.M. = 15:00
            - 11:00 P.M. = 23:00
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