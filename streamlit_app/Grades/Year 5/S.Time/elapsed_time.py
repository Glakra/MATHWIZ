import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, timedelta

def run():
    """
    Main function to run the Elapsed Time activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/S.Time/elapsed_time.py
    """
    # Initialize session state
    if "elapsed_difficulty" not in st.session_state:
        st.session_state.elapsed_difficulty = 1
    
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
    st.title("⏱️ Elapsed Time")
    st.markdown("*Calculate start times, end times, and time intervals*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.elapsed_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Hour Changes",
            2: "Hours and Minutes",
            3: "Complex Time Calculations",
            4: "Multi-Day Elapsed Time",
            5: "Real-World Scenarios"
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
    with st.expander("📚 **How to Calculate Elapsed Time**", expanded=False):
        st.markdown("""
        ### ⏰ Time Vocabulary
        
        **Reading the Clock:**
        - **o'clock** = :00 (e.g., 3:00 = three o'clock)
        - **quarter past** = :15 (e.g., 3:15 = quarter past three)
        - **half past** = :30 (e.g., 3:30 = half past three)
        - **quarter to** = :45 (e.g., 3:45 = quarter to four)
        - **__ minutes past** = after the hour
        - **__ minutes to** = before the next hour
        
        ### 📝 Calculating End Time
        
        **Example 1: It is 2:30. What time will it be in 3 hours?**
        - Start: 2:30
        - Add: 3 hours
        - End: 5:30
        
        **Example 2: It is 10:45. What time will it be in 2 hours 30 minutes?**
        - Start: 10:45
        - Add hours: 10:45 + 2 hours = 12:45
        - Add minutes: 12:45 + 30 minutes = 1:15
        
        ### 🎯 Methods for Complex Problems
        
        **Method 1: Count Up**
        - Start at the given time
        - Add hours first
        - Then add minutes
        - Adjust if you pass 12:00
        
        **Method 2: Use a Timeline**
        - Draw a number line
        - Mark the start time
        - Jump forward by the elapsed time
        - Find the end time
        
        **Method 3: Convert to Minutes**
        - Convert everything to minutes
        - Add the minutes
        - Convert back to hours and minutes
        
        ### 💡 Tips:
        - Remember: AM changes to PM at noon
        - Remember: PM changes to AM at midnight
        - 60 minutes = 1 hour
        - When minutes exceed 60, convert to hours
        - Practice reading analog and digital clocks
        """)

def generate_new_problem():
    """Generate a new elapsed time problem based on difficulty"""
    difficulty = st.session_state.elapsed_difficulty
    
    if difficulty == 1:
        # Level 1: Simple hour changes
        problem_data = generate_simple_hour_problem()
    elif difficulty == 2:
        # Level 2: Hours and minutes
        problem_data = generate_hours_minutes_problem()
    elif difficulty == 3:
        # Level 3: Complex calculations
        problem_data = generate_complex_time_problem()
    elif difficulty == 4:
        # Level 4: Multi-day problems
        problem_data = generate_multi_day_problem()
    else:
        # Level 5: Real-world scenarios
        problem_data = generate_real_world_problem()
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def time_to_words(hour, minute):
    """Convert time to word format"""
    # Handle special cases
    if minute == 0:
        if hour == 12:
            return "twelve o'clock"
        elif hour == 0 or hour == 24:
            return "midnight"
        else:
            hour_words = ["", "one", "two", "three", "four", "five", "six", 
                         "seven", "eight", "nine", "ten", "eleven", "twelve"]
            h = hour % 12
            if h == 0:
                h = 12
            return f"{hour_words[h]} o'clock"
    
    elif minute == 15:
        hour_words = ["", "one", "two", "three", "four", "five", "six", 
                     "seven", "eight", "nine", "ten", "eleven", "twelve"]
        h = hour % 12
        if h == 0:
            h = 12
        return f"quarter past {hour_words[h]}"
    
    elif minute == 30:
        hour_words = ["", "one", "two", "three", "four", "five", "six", 
                     "seven", "eight", "nine", "ten", "eleven", "twelve"]
        h = hour % 12
        if h == 0:
            h = 12
        return f"half past {hour_words[h]}"
    
    elif minute == 45:
        hour_words = ["", "one", "two", "three", "four", "five", "six", 
                     "seven", "eight", "nine", "ten", "eleven", "twelve", "one"]
        h = (hour % 12) + 1
        if h == 0:
            h = 12
        return f"quarter to {hour_words[h]}"
    
    elif minute < 30:
        hour_words = ["", "one", "two", "three", "four", "five", "six", 
                     "seven", "eight", "nine", "ten", "eleven", "twelve"]
        h = hour % 12
        if h == 0:
            h = 12
        
        if minute == 1:
            return f"one minute past {hour_words[h]}"
        else:
            minute_words = convert_number_to_words(minute)
            return f"{minute_words} minutes past {hour_words[h]}"
    
    else:  # minute > 30 and != 45
        minutes_to = 60 - minute
        hour_words = ["", "one", "two", "three", "four", "five", "six", 
                     "seven", "eight", "nine", "ten", "eleven", "twelve", "one"]
        h = (hour % 12) + 1
        if h == 0:
            h = 12
        
        if minutes_to == 1:
            return f"one minute to {hour_words[h]}"
        else:
            minute_words = convert_number_to_words(minutes_to)
            return f"{minute_words} minutes to {hour_words[h]}"

def convert_number_to_words(n):
    """Convert number to words (for minutes)"""
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", 
             "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty"]
    
    if n < 10:
        return ones[n]
    elif n < 20:
        return teens[n - 10]
    elif n < 60:
        t = n // 10
        o = n % 10
        if o == 0:
            return tens[t]
        else:
            return f"{tens[t]}-{ones[o]}"
    else:
        return str(n)

def generate_simple_hour_problem():
    """Generate Level 1: Simple hour changes only"""
    # Random start time (round hours)
    start_hour = random.randint(1, 11)
    start_minute = 0
    
    # Random elapsed hours (1-6 hours)
    elapsed_hours = random.randint(1, 6)
    elapsed_minutes = 0
    
    # Calculate end time
    end_hour = start_hour + elapsed_hours
    end_minute = start_minute
    
    # Handle 12-hour format
    if end_hour > 12:
        end_hour = end_hour - 12
    
    # Format the problem
    start_words = time_to_words(start_hour, start_minute)
    
    return {
        "question": f"It is now {start_words}. What time will it be in {elapsed_hours} {'hour' if elapsed_hours == 1 else 'hours'}? Write your answer using numbers and a colon (for example, 11:58).",
        "problem_type": "find_end_time",
        "start_time": f"{start_hour}:{start_minute:02d}",
        "elapsed_time": f"{elapsed_hours} hours",
        "correct_answer": f"{end_hour}:{end_minute:02d}",
        "explanation": f"Start: {start_hour}:{start_minute:02d}\nAdd {elapsed_hours} hours: {start_hour} + {elapsed_hours} = {start_hour + elapsed_hours}\nSince {start_hour + elapsed_hours} {'>' if start_hour + elapsed_hours > 12 else '<='} 12, the time is {end_hour}:{end_minute:02d}",
        "show_clock": True
    }

def generate_hours_minutes_problem():
    """Generate Level 2: Hours and minutes problems"""
    problem_types = ["find_end_time", "find_start_time", "find_elapsed"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "find_end_time":
        # Use various time expressions
        time_expressions = [
            {"hour": 2, "minute": 30, "text": "half past two"},
            {"hour": 9, "minute": 15, "text": "quarter past nine"},
            {"hour": 12, "minute": 36, "text": "twenty-four minutes to one"},
            {"hour": 3, "minute": 49, "text": "eleven minutes to four"},
            {"hour": 6, "minute": 51, "text": "nine minutes to seven"},
            {"hour": 10, "minute": 35, "text": "twenty-five to eleven"},
            {"hour": 11, "minute": 56, "text": "four minutes to twelve"},
            {"hour": 1, "minute": 1, "text": "one minute past one"},
            {"hour": 12, "minute": 0, "text": "twelve o'clock"},
            {"hour": 4, "minute": 40, "text": "twenty to five"},
            {"hour": 5, "minute": 25, "text": "twenty-five past five"},
            {"hour": 7, "minute": 45, "text": "quarter to eight"},
            {"hour": 8, "minute": 10, "text": "ten past eight"},
            {"hour": 11, "minute": 55, "text": "five to twelve"}
        ]
        
        start_time = random.choice(time_expressions)
        
        # Random elapsed time
        elapsed_hours = random.randint(1, 11)
        elapsed_minutes = random.randint(0, 59)
        
        # Calculate end time
        total_minutes = start_time["hour"] * 60 + start_time["minute"] + elapsed_hours * 60 + elapsed_minutes
        end_hour = (total_minutes // 60) % 24
        end_minute = total_minutes % 60
        
        # Convert to 12-hour format
        if end_hour == 0:
            display_hour = 12
        elif end_hour > 12:
            display_hour = end_hour - 12
        else:
            display_hour = end_hour
        
        return {
            "question": f"It is now {start_time['text']}. What time will it be in {elapsed_hours} {'hour' if elapsed_hours == 1 else 'hours'} and {elapsed_minutes} {'minute' if elapsed_minutes == 1 else 'minutes'}? Write your answer using numbers and a colon (for example, 11:58).",
            "problem_type": "find_end_time",
            "start_time": f"{start_time['hour']}:{start_time['minute']:02d}",
            "elapsed_time": f"{elapsed_hours}h {elapsed_minutes}m",
            "correct_answer": f"{display_hour}:{end_minute:02d}",
            "explanation": f"Start: {start_time['text']} = {start_time['hour']}:{start_time['minute']:02d}\nAdd {elapsed_hours} hours {elapsed_minutes} minutes\nEnd time: {display_hour}:{end_minute:02d}",
            "show_clock": True
        }
    
    elif problem_type == "find_start_time":
        # What time was it X hours ago?
        end_hour = random.randint(1, 12)
        end_minute = random.randint(0, 59)
        
        elapsed_hours = random.randint(1, 6)
        elapsed_minutes = random.randint(0, 59)
        
        # Calculate start time
        total_end_minutes = end_hour * 60 + end_minute
        total_elapsed_minutes = elapsed_hours * 60 + elapsed_minutes
        
        if total_end_minutes >= total_elapsed_minutes:
            total_start_minutes = total_end_minutes - total_elapsed_minutes
        else:
            total_start_minutes = total_end_minutes + (12 * 60) - total_elapsed_minutes
        
        start_hour = (total_start_minutes // 60) % 12
        if start_hour == 0:
            start_hour = 12
        start_minute = total_start_minutes % 60
        
        return {
            "question": f"It is now {end_hour}:{end_minute:02d}. What time was it {elapsed_hours} {'hour' if elapsed_hours == 1 else 'hours'} and {elapsed_minutes} {'minute' if elapsed_minutes == 1 else 'minutes'} ago?",
            "problem_type": "find_start_time",
            "end_time": f"{end_hour}:{end_minute:02d}",
            "elapsed_time": f"{elapsed_hours}h {elapsed_minutes}m",
            "correct_answer": f"{start_hour}:{start_minute:02d}",
            "explanation": f"Current time: {end_hour}:{end_minute:02d}\nSubtract {elapsed_hours} hours {elapsed_minutes} minutes\nStart time: {start_hour}:{start_minute:02d}",
            "show_clock": True
        }
    
    else:  # find_elapsed
        # How much time has passed?
        start_hour = random.randint(1, 11)
        start_minute = random.randint(0, 59)
        
        elapsed_hours = random.randint(1, 6)
        elapsed_minutes = random.randint(0, 59)
        
        # Calculate end time
        total_minutes = start_hour * 60 + start_minute + elapsed_hours * 60 + elapsed_minutes
        end_hour = (total_minutes // 60) % 12
        if end_hour == 0:
            end_hour = 12
        end_minute = total_minutes % 60
        
        return {
            "question": f"Sarah started reading at {start_hour}:{start_minute:02d} and finished at {end_hour}:{end_minute:02d}. How long did she read? (Answer in hours and minutes)",
            "problem_type": "find_elapsed",
            "start_time": f"{start_hour}:{start_minute:02d}",
            "end_time": f"{end_hour}:{end_minute:02d}",
            "correct_answer": f"{elapsed_hours}h {elapsed_minutes}m",
            "explanation": f"Start: {start_hour}:{start_minute:02d}\nEnd: {end_hour}:{end_minute:02d}\nElapsed: {elapsed_hours} hours {elapsed_minutes} minutes",
            "show_clock": True
        }

def generate_complex_time_problem():
    """Generate Level 3: Complex time calculations"""
    scenarios = [
        {
            "context": "A train departs at 9:45 AM",
            "elapsed": (3, 47),
            "question": "What time does it arrive?",
            "format": "time"
        },
        {
            "context": "A movie starts at 7:20 PM and is 2 hours 35 minutes long",
            "elapsed": (2, 35),
            "question": "What time does it end?",
            "format": "time"
        },
        {
            "context": "A flight leaves at 11:30 AM and arrives at 4:15 PM",
            "start": (11, 30),
            "end": (16, 15),  # 4:15 PM in 24-hour
            "question": "How long is the flight?",
            "format": "duration"
        },
        {
            "context": "School starts at 8:30 AM. Lunch is 4 hours 15 minutes later",
            "elapsed": (4, 15),
            "question": "What time is lunch?",
            "format": "time"
        },
        {
            "context": "The bakery opens at 6:00 AM. It's been open for 5 hours 45 minutes",
            "elapsed": (5, 45),
            "question": "What time is it now?",
            "format": "time"
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if scenario["format"] == "time":
        # Extract or generate start time
        if "A train departs" in scenario["context"]:
            start_h, start_m = 9, 45
        elif "movie starts" in scenario["context"]:
            start_h, start_m = 19, 20  # 7:20 PM
        elif "School starts" in scenario["context"]:
            start_h, start_m = 8, 30
        elif "bakery opens" in scenario["context"]:
            start_h, start_m = 6, 0
        else:
            start_h = random.randint(6, 11)
            start_m = random.randint(0, 59)
        
        elapsed_h, elapsed_m = scenario["elapsed"]
        
        # Calculate end time
        total_minutes = start_h * 60 + start_m + elapsed_h * 60 + elapsed_m
        end_h = (total_minutes // 60) % 24
        end_m = total_minutes % 60
        
        # Convert to 12-hour format for display
        if end_h == 0:
            display_h = 12
            period = "AM"
        elif end_h < 12:
            display_h = end_h
            period = "AM"
        elif end_h == 12:
            display_h = 12
            period = "PM"
        else:
            display_h = end_h - 12
            period = "PM"
        
        return {
            "question": f"{scenario['context']}. {scenario['question']}",
            "problem_type": "complex",
            "correct_answer": f"{display_h}:{end_m:02d}",
            "explanation": f"Start: {start_h % 12 if start_h % 12 != 0 else 12}:{start_m:02d}\nAdd: {elapsed_h} hours {elapsed_m} minutes\nEnd: {display_h}:{end_m:02d} {period}",
            "show_clock": False
        }
    
    else:  # duration
        start_h, start_m = scenario["start"]
        end_h, end_m = scenario["end"]
        
        # Calculate elapsed time
        start_total = start_h * 60 + start_m
        end_total = end_h * 60 + end_m
        
        elapsed_total = end_total - start_total
        elapsed_h = elapsed_total // 60
        elapsed_m = elapsed_total % 60
        
        return {
            "question": f"{scenario['context']}. {scenario['question']}",
            "problem_type": "complex",
            "correct_answer": f"{elapsed_h}h {elapsed_m}m",
            "explanation": f"Start: {start_h % 12 if start_h % 12 != 0 else 12}:{start_m:02d} {'AM' if start_h < 12 else 'PM'}\nEnd: {end_h % 12 if end_h % 12 != 0 else 12}:{end_m:02d} {'AM' if end_h < 12 else 'PM'}\nElapsed: {elapsed_h} hours {elapsed_m} minutes",
            "show_clock": False
        }

def generate_multi_day_problem():
    """Generate Level 4: Multi-day elapsed time problems"""
    scenarios = [
        {
            "context": "A camping trip starts Friday at 3:00 PM and ends Sunday at 11:00 AM",
            "question": "How long is the camping trip?",
            "start_day": "Friday",
            "start_time": (15, 0),
            "end_day": "Sunday",
            "end_time": (11, 0),
            "days_between": 2
        },
        {
            "context": "A science experiment begins Monday at 9:30 AM and runs for 72 hours",
            "question": "When does it end? (Give day and time)",
            "start_day": "Monday",
            "start_time": (9, 30),
            "elapsed_hours": 72
        },
        {
            "context": "A flight leaves New York Wednesday at 11:45 PM and arrives in London Thursday at 11:30 AM",
            "question": "How long is the flight?",
            "start_day": "Wednesday",
            "start_time": (23, 45),
            "end_day": "Thursday",
            "end_time": (11, 30),
            "days_between": 1
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if "elapsed_hours" in scenario:
        # Calculate end day and time
        start_h, start_m = scenario["start_time"]
        elapsed_h = scenario["elapsed_hours"]
        
        total_minutes = start_h * 60 + start_m + elapsed_h * 60
        days_passed = total_minutes // (24 * 60)
        remaining_minutes = total_minutes % (24 * 60)
        
        end_h = remaining_minutes // 60
        end_m = remaining_minutes % 60
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        start_idx = days.index(scenario["start_day"])
        end_idx = (start_idx + days_passed) % 7
        end_day = days[end_idx]
        
        # Format answer
        display_h = end_h % 12 if end_h % 12 != 0 else 12
        period = "AM" if end_h < 12 else "PM"
        
        return {
            "question": f"{scenario['context']}. {scenario['question']}",
            "problem_type": "multi_day",
            "correct_answer": f"{end_day} {display_h}:{end_m:02d} {period}",
            "explanation": f"Start: {scenario['start_day']} {start_h % 12 if start_h % 12 != 0 else 12}:{start_m:02d} AM\nAdd: {elapsed_h} hours = {days_passed} days + {remaining_minutes // 60} hours\nEnd: {end_day} {display_h}:{end_m:02d} {period}",
            "show_clock": False
        }
    
    else:
        # Calculate elapsed time
        start_h, start_m = scenario["start_time"]
        end_h, end_m = scenario["end_time"]
        days = scenario["days_between"]
        
        # Handle time calculation
        if end_h * 60 + end_m >= start_h * 60 + start_m:
            elapsed_h = end_h - start_h
            elapsed_m = end_m - start_m
        else:
            days -= 1
            total_end = (24 * 60) + end_h * 60 + end_m
            total_start = start_h * 60 + start_m
            elapsed_total = total_end - total_start
            elapsed_h = elapsed_total // 60
            elapsed_m = elapsed_total % 60
        
        if elapsed_m < 0:
            elapsed_h -= 1
            elapsed_m += 60
        
        total_hours = days * 24 + elapsed_h
        
        return {
            "question": f"{scenario['context']}. {scenario['question']}",
            "problem_type": "multi_day",
            "correct_answer": f"{total_hours}h {elapsed_m}m",
            "explanation": f"From {scenario['start_day']} to {scenario['end_day']}: {days} days\nTime difference: {elapsed_h} hours {elapsed_m} minutes\nTotal: {total_hours} hours {elapsed_m} minutes",
            "show_clock": False
        }

def generate_real_world_problem():
    """Generate Level 5: Real-world scenario problems"""
    scenarios = [
        {
            "context": "A bakery opens at 5:00 AM. They bake bread for 2 hours 15 minutes, then pastries for 1 hour 45 minutes",
            "question": "What time are all items ready?",
            "start": (5, 0),
            "steps": [(2, 15), (1, 45)]
        },
        {
            "context": "Tom's work shift is 8 hours 30 minutes. He takes a 45-minute lunch and two 15-minute breaks",
            "question": "If he starts at 7:00 AM, what time does he finish?",
            "start": (7, 0),
            "work": (8, 30),
            "breaks": [(0, 45), (0, 15), (0, 15)]
        },
        {
            "context": "A concert has three acts: 45 minutes, 1 hour 20 minutes, and 55 minutes, with 20-minute breaks between",
            "question": "If it starts at 7:30 PM, when does it end?",
            "start": (19, 30),
            "acts": [(0, 45), (1, 20), (0, 55)],
            "breaks": 2,
            "break_duration": 20
        },
        {
            "context": "Sarah studies math for 1 hour 15 minutes, takes a 20-minute break, then studies science for 1 hour 40 minutes",
            "question": "If she starts at 3:45 PM, when does she finish?",
            "start": (15, 45),
            "activities": [(1, 15), (0, 20), (1, 40)]
        },
        {
            "context": "A recipe needs 45 minutes prep, 2 hours 30 minutes cooking, and 1 hour cooling",
            "question": "If you need it ready by 6:00 PM, when should you start?",
            "end": (18, 0),
            "times": [(0, 45), (2, 30), (1, 0)],
            "reverse": True
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if "reverse" in scenario and scenario["reverse"]:
        # Work backwards from end time
        end_h, end_m = scenario["end"]
        total_elapsed = sum(h * 60 + m for h, m in scenario["times"])
        
        start_total = end_h * 60 + end_m - total_elapsed
        if start_total < 0:
            start_total += 24 * 60
        
        start_h = start_total // 60
        start_m = start_total % 60
        
        display_h = start_h % 12 if start_h % 12 != 0 else 12
        period = "AM" if start_h < 12 else "PM"
        
        return {
            "question": f"{scenario['context']}",
            "problem_type": "real_world",
            "correct_answer": f"{display_h}:{start_m:02d} {period}",
            "explanation": f"Work backwards from 6:00 PM\nTotal time needed: {total_elapsed // 60} hours {total_elapsed % 60} minutes\nStart time: {display_h}:{start_m:02d} {period}",
            "show_clock": False
        }
    
    elif "acts" in scenario:
        # Concert scenario
        start_h, start_m = scenario["start"]
        
        total_elapsed = 0
        for act in scenario["acts"]:
            total_elapsed += act[0] * 60 + act[1]
        total_elapsed += scenario["breaks"] * scenario["break_duration"]
        
        end_total = start_h * 60 + start_m + total_elapsed
        end_h = (end_total // 60) % 24
        end_m = end_total % 60
        
        display_h = end_h % 12 if end_h % 12 != 0 else 12
        period = "AM" if end_h < 12 else "PM"
        
        return {
            "question": f"{scenario['context']}",
            "problem_type": "real_world",
            "correct_answer": f"{display_h}:{end_m:02d} {period}",
            "explanation": f"Performance time: {sum(a[0] * 60 + a[1] for a in scenario['acts'])} minutes\nBreak time: {scenario['breaks'] * scenario['break_duration']} minutes\nTotal: {total_elapsed} minutes\nEnd time: {display_h}:{end_m:02d} {period}",
            "show_clock": False
        }
    
    elif "work" in scenario:
        # Work shift scenario
        start_h, start_m = scenario["start"]
        work_h, work_m = scenario["work"]
        
        # Add work time and breaks
        total_time = work_h * 60 + work_m
        for break_h, break_m in scenario["breaks"]:
            total_time += break_h * 60 + break_m
        
        end_total = start_h * 60 + start_m + total_time
        end_h = (end_total // 60) % 24
        end_m = end_total % 60
        
        display_h = end_h % 12 if end_h % 12 != 0 else 12
        period = "AM" if end_h < 12 else "PM"
        
        return {
            "question": f"{scenario['context']}",
            "problem_type": "real_world",
            "correct_answer": f"{display_h}:{end_m:02d} {period}",
            "explanation": f"Work: {work_h} hours {work_m} minutes\nBreaks: {sum(b[0] * 60 + b[1] for b in scenario['breaks'])} minutes\nEnd time: {display_h}:{end_m:02d} {period}",
            "show_clock": False
        }
    
    else:
        # General multi-step scenario
        start_h, start_m = scenario["start"]
        
        if "steps" in scenario:
            steps = scenario["steps"]
        else:
            steps = scenario.get("activities", [(1, 0)])
        
        total_elapsed = sum(h * 60 + m for h, m in steps)
        
        end_total = start_h * 60 + start_m + total_elapsed
        end_h = (end_total // 60) % 24
        end_m = end_total % 60
        
        display_h = end_h % 12 if end_h % 12 != 0 else 12
        period = "AM" if end_h < 12 else "PM"
        
        return {
            "question": f"{scenario['context']}",
            "problem_type": "real_world",
            "correct_answer": f"{display_h}:{end_m:02d}",
            "explanation": f"Start: {start_h % 12 if start_h % 12 != 0 else 12}:{start_m:02d}\nTotal time: {total_elapsed // 60} hours {total_elapsed % 60} minutes\nEnd: {display_h}:{end_m:02d} {period}",
            "show_clock": False
        }

def display_problem():
    """Display the current problem with visual aids"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Problem {st.session_state.total_attempted + 1}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    st.markdown("---")
    
    # Display clock if applicable
    if data.get("show_clock", False) and st.session_state.elapsed_difficulty <= 2:
        display_analog_clock(data)
    
    # Input field
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if "h" in data.get("correct_answer", ""):
            # Duration answer
            placeholder = "e.g., 2h 30m"
        elif "day" in data.get("correct_answer", "").lower():
            # Day and time answer
            placeholder = "e.g., Monday 3:30 PM"
        else:
            # Time answer
            placeholder = "e.g., 11:58"
        
        user_input = st.text_input(
            "Your answer:",
            placeholder=placeholder,
            disabled=st.session_state.answer_submitted,
            key="elapsed_input"
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

def display_analog_clock(data):
    """Display a simple analog clock visualization"""
    with st.expander("🕐 Visual Aid", expanded=False):
        st.markdown("### Starting Time")
        
        # Parse start time if available
        if "start_time" in data:
            time_parts = data["start_time"].split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            
            # Create clock visualization
            fig, ax = plt.subplots(figsize=(4, 4))
            
            # Draw clock circle
            circle = plt.Circle((0, 0), 1, fill=False, linewidth=2)
            ax.add_patch(circle)
            
            # Draw hour markers
            for i in range(12):
                angle = np.pi/2 - (i * np.pi/6)
                x = 0.85 * np.cos(angle)
                y = 0.85 * np.sin(angle)
                ax.text(x, y, str(12 if i == 0 else i), ha='center', va='center', fontsize=10)
            
            # Draw hour hand
            hour_angle = np.pi/2 - ((hour % 12 + minute/60) * np.pi/6)
            ax.arrow(0, 0, 0.5 * np.cos(hour_angle), 0.5 * np.sin(hour_angle),
                    head_width=0.05, head_length=0.05, fc='black', ec='black', linewidth=2)
            
            # Draw minute hand
            minute_angle = np.pi/2 - (minute * np.pi/30)
            ax.arrow(0, 0, 0.75 * np.cos(minute_angle), 0.75 * np.sin(minute_angle),
                    head_width=0.03, head_length=0.03, fc='blue', ec='blue', linewidth=1.5)
            
            # Center dot
            ax.plot(0, 0, 'ko', markersize=8)
            
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)
            ax.set_aspect('equal')
            ax.axis('off')
            
            st.pyplot(fig)
            plt.close()
            
            st.caption(f"Start: {hour}:{minute:02d}")

def normalize_answer(answer):
    """Normalize answer format for comparison"""
    # Remove extra spaces and convert to lowercase
    answer = answer.strip().lower()
    
    # Handle various time formats
    answer = answer.replace(" ", "")
    answer = answer.replace("am", "")
    answer = answer.replace("pm", "")
    answer = answer.replace("hours", "h")
    answer = answer.replace("hour", "h")
    answer = answer.replace("minutes", "m")
    answer = answer.replace("minute", "m")
    answer = answer.replace("mins", "m")
    answer = answer.replace("min", "m")
    
    return answer

def check_answer():
    """Check the user's answer with flexible formatting"""
    user_answer = normalize_answer(st.session_state.user_answer)
    correct_answer = normalize_answer(st.session_state.correct_answer)
    
    # Also check without leading zeros (e.g., 9:05 vs 9:5)
    user_alt = user_answer.replace(":0", ":")
    correct_alt = correct_answer.replace(":0", ":")
    
    is_correct = (user_answer == correct_answer) or (user_alt == correct_alt)
    
    # Additional format checks for time
    if ":" in st.session_state.correct_answer and ":" in st.session_state.user_answer:
        # Check if times are equivalent (e.g., 1:00 vs 1:0)
        try:
            user_parts = st.session_state.user_answer.split(":")
            correct_parts = st.session_state.correct_answer.split(":")
            
            user_h = int(user_parts[0])
            user_m = int(user_parts[1]) if len(user_parts) > 1 else 0
            
            correct_h = int(correct_parts[0])
            correct_m = int(correct_parts[1]) if len(correct_parts) > 1 else 0
            
            is_correct = (user_h == correct_h) and (user_m == correct_m)
        except:
            pass
    
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
            old_difficulty = st.session_state.elapsed_difficulty
            st.session_state.elapsed_difficulty = min(
                st.session_state.elapsed_difficulty + 1, 5
            )
            
            if st.session_state.elapsed_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Excellent! Moving to Level {st.session_state.elapsed_difficulty}**")
                st.session_state.consecutive_correct = 0
    
    else:
        st.error(f"❌ **Not quite. You answered {st.session_state.user_answer}, but the correct answer is {data['correct_answer']}**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.elapsed_difficulty
            st.session_state.elapsed_difficulty = max(
                st.session_state.elapsed_difficulty - 1, 1
            )
            
            if st.session_state.elapsed_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.elapsed_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_solution():
    """Show detailed solution with timeline"""
    with st.expander("📚 **Step-by-Step Solution**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown("### 🔢 Solution Steps:")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        
        # Show timeline visualization for elapsed time
        if data.get("problem_type") == "find_end_time":
            st.markdown("### 📊 Timeline Method:")
            st.markdown("""
            ```
            Start Time ----[+Elapsed Time]----> End Time
            ```
            """)
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Tips for Elapsed Time:
        
        **Finding End Time:**
        1. Start with the given time
        2. Add hours first
        3. Then add minutes
        4. Adjust if minutes ≥ 60
        5. Check AM/PM if needed
        
        **Finding Start Time:**
        1. Start with the end time
        2. Work backwards
        3. Subtract the elapsed time
        
        **Finding Duration:**
        1. Note the start time
        2. Note the end time
        3. Count the hours between
        4. Count the additional minutes
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