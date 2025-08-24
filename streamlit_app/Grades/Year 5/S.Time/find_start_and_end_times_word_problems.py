import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, timedelta

def run():
    """
    Main function to run the Find Start and End Times: Word Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/S.Time/find_start_and_end_times_word_problems.py
    """
    # Initialize session state
    if "time_problem_difficulty" not in st.session_state:
        st.session_state.time_problem_difficulty = 1
    
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
    st.title("🕐 Find Start and End Times: Word Problems")
    st.markdown("*Solve real-world time problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.time_problem_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Time Addition",
            2: "Complex Time Calculations",
            3: "Working Backwards",
            4: "Long Duration Problems",
            5: "Multi-Step Scenarios"
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
    with st.expander("📚 **How to Solve Time Word Problems**", expanded=False):
        st.markdown("""
        ### 📝 Steps to Solve Time Problems
        
        **1. Read Carefully:**
        - Identify the start time or end time given
        - Note the duration (how long something takes)
        - Determine what you need to find
        
        **2. Choose Your Method:**
        
        **Method A: Timeline**
        ```
        Start Time ----[Duration]----> End Time
        ```
        
        **Method B: Step by Step**
        - Add/subtract hours first
        - Then add/subtract minutes
        - Adjust for 60 minutes = 1 hour
        
        **Method C: Convert to Minutes**
        - Convert everything to minutes
        - Do the calculation
        - Convert back to hours and minutes
        
        ### ⏰ Common Scenarios
        
        **School Activities:**
        - Classes typically last 30-90 minutes
        - School days often run 8:00 AM - 3:00 PM
        - Lunch breaks are usually 30-60 minutes
        
        **Daily Activities:**
        - Short tasks: 5-30 minutes
        - Medium tasks: 30 minutes - 2 hours
        - Long activities: 2+ hours
        
        **Travel:**
        - Local trips: minutes to 1 hour
        - Longer journeys: several hours
        - Cross-country: many hours or days
        
        ### 💡 Tips:
        - Draw a clock or timeline
        - Check if you cross noon (AM→PM)
        - Check if you cross midnight (PM→AM)
        - For long durations, break into parts
        - Always check if your answer makes sense!
        """)

def generate_new_problem():
    """Generate a new time word problem based on difficulty"""
    difficulty = st.session_state.time_problem_difficulty
    
    if difficulty == 1:
        # Level 1: Simple time addition (under 2 hours)
        problem_data = generate_simple_problem()
    elif difficulty == 2:
        # Level 2: Complex calculations (2-5 hours)
        problem_data = generate_complex_problem()
    elif difficulty == 3:
        # Level 3: Working backwards
        problem_data = generate_backwards_problem()
    elif difficulty == 4:
        # Level 4: Long duration (5+ hours)
        problem_data = generate_long_duration_problem()
    else:
        # Level 5: Multi-step scenarios
        problem_data = generate_multi_step_problem()
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_simple_problem():
    """Generate Level 1: Simple time addition problems"""
    scenarios = [
        {
            "context": "Natalie decided to take a pottery class. The class started at {start_time}, and lasted for {duration}.",
            "question": "What time did the class end?",
            "start_times": ["2:40", "3:15", "4:30", "1:45", "2:20"],
            "durations": ["1 hour and 35 minutes", "45 minutes", "1 hour and 20 minutes", "55 minutes", "1 hour and 10 minutes"]
        },
        {
            "context": "Tom began climbing the stairs to his apartment at {start_time}. It took him {duration} to climb all the stairs.",
            "question": "What time was it when Tom reached his floor?",
            "start_times": ["10:10", "9:45", "3:20", "7:55", "8:30"],
            "durations": ["5 minutes", "7 minutes", "3 minutes", "8 minutes", "4 minutes"]
        },
        {
            "context": "Liz took a spelling quiz at school. The quiz started at {start_time}, and was {duration} long.",
            "question": "What time was it when Liz's quiz ended?",
            "start_times": ["11:50", "10:45", "2:40", "9:35", "1:25"],
            "durations": ["10 minutes", "15 minutes", "20 minutes", "25 minutes", "12 minutes"]
        },
        {
            "context": "Sarah started her homework at {start_time}. She worked for {duration}.",
            "question": "What time did she finish?",
            "start_times": ["3:30", "4:15", "5:20", "2:45", "6:10"],
            "durations": ["45 minutes", "1 hour", "30 minutes", "1 hour and 15 minutes", "50 minutes"]
        },
        {
            "context": "The morning assembly began at {start_time} and lasted {duration}.",
            "question": "What time did it end?",
            "start_times": ["8:15", "8:30", "8:45", "9:00", "8:20"],
            "durations": ["15 minutes", "20 minutes", "25 minutes", "10 minutes", "30 minutes"]
        }
    ]
    
    scenario = random.choice(scenarios)
    idx = random.randint(0, len(scenario["start_times"]) - 1)
    
    start_time = scenario["start_times"][idx]
    duration_text = scenario["durations"][idx]
    
    # Parse duration
    duration_parts = parse_duration(duration_text)
    
    # Calculate end time
    start_h, start_m = map(int, start_time.split(":"))
    end_h, end_m = calculate_end_time(start_h, start_m, duration_parts["hours"], duration_parts["minutes"])
    
    # Generate multiple choice options
    correct_time = f"{end_h}:{end_m:02d}"
    options = generate_time_options(end_h, end_m, 4)
    
    return {
        "question": scenario["context"].format(start_time=start_time, duration=duration_text) + " " + scenario["question"],
        "problem_type": "simple",
        "options": options,
        "correct_answer": correct_time,
        "explanation": f"Start: {start_time}\nDuration: {duration_text}\nEnd: {correct_time}",
        "show_clocks": False,
        "use_multiple_choice": True
    }

def generate_complex_problem():
    """Generate Level 2: Complex time calculation problems"""
    scenarios = [
        {
            "context": "Edwin began raking the yard at {start_time}. He raked all the leaves into piles and stuffed them into bags. It took Edwin {duration} to collect all the leaves.",
            "question": "What time was it when Edwin finished raking the yard?",
            "start_times": ["10:20", "9:15", "11:30", "8:45", "2:10"],
            "durations": ["2 hours and 35 minutes", "3 hours and 15 minutes", "2 hours and 45 minutes", "1 hour and 50 minutes", "3 hours and 20 minutes"]
        },
        {
            "context": "Vince works as a nurse. Each shift, he starts at {start_time} and works for {duration}.",
            "question": "What time does Vince's shift end?",
            "start_times": ["5:40", "6:30", "7:00", "11:45", "2:15"],
            "durations": ["8 hours and 50 minutes", "7 hours and 30 minutes", "9 hours", "8 hours and 15 minutes", "6 hours and 45 minutes"]
        },
        {
            "context": "{name} started a movie marathon at {start_time}. The movies lasted a total of {duration}.",
            "question": "What time did the marathon end?",
            "name": ["Alex", "Jamie", "Sam", "Morgan", "Casey"],
            "start_times": ["7:30", "8:15", "6:45", "9:00", "7:45"],
            "durations": ["4 hours and 20 minutes", "3 hours and 45 minutes", "5 hours and 10 minutes", "4 hours and 30 minutes", "3 hours and 55 minutes"]
        },
        {
            "context": "The school play started at {start_time} and ran for {duration}.",
            "question": "What time did the play finish?",
            "start_times": ["7:00", "7:30", "6:45", "8:00", "6:30"],
            "durations": ["2 hours and 45 minutes", "3 hours", "2 hours and 30 minutes", "2 hours and 15 minutes", "3 hours and 20 minutes"]
        }
    ]
    
    scenario = random.choice(scenarios)
    
    # Handle scenarios with name field
    if "name" in scenario:
        name = random.choice(scenario["name"])
        context = scenario["context"].format(name=name, start_time="{start_time}", duration="{duration}")
    else:
        context = scenario["context"]
    
    idx = random.randint(0, len(scenario["start_times"]) - 1)
    start_time = scenario["start_times"][idx]
    duration_text = scenario["durations"][idx]
    
    # Parse and calculate
    duration_parts = parse_duration(duration_text)
    start_h, start_m = map(int, start_time.split(":"))
    end_h, end_m = calculate_end_time(start_h, start_m, duration_parts["hours"], duration_parts["minutes"])
    
    # Generate options with clocks for some problems
    correct_time = f"{end_h}:{end_m:02d}"
    options = generate_time_options(end_h, end_m, 4)
    
    show_clocks = random.choice([True, False])
    
    return {
        "question": context.format(start_time=start_time, duration=duration_text) + " " + scenario["question"],
        "problem_type": "complex",
        "options": options,
        "correct_answer": correct_time,
        "explanation": f"Start: {start_time}\nDuration: {duration_text}\n\nCalculation:\n{start_time} + {duration_parts['hours']} hours = {(start_h + duration_parts['hours']) % 12 if (start_h + duration_parts['hours']) % 12 != 0 else 12}:{start_m:02d}\n{(start_h + duration_parts['hours']) % 12 if (start_h + duration_parts['hours']) % 12 != 0 else 12}:{start_m:02d} + {duration_parts['minutes']} minutes = {end_h}:{end_m:02d}",
        "show_clocks": show_clocks,
        "use_multiple_choice": True
    }

def generate_backwards_problem():
    """Generate Level 3: Working backwards problems"""
    scenarios = [
        {
            "context": "Daniel left a telephone message at his doctor's office at {start_time}. The doctor returned the call {duration} later.",
            "question": "What time was it when Daniel's doctor called back?",
            "start_times": ["7:35", "9:20", "10:45", "2:15", "3:50"],
            "durations": ["15 hours and 5 minutes", "12 hours and 30 minutes", "10 hours and 45 minutes", "8 hours and 20 minutes", "14 hours"]
        },
        {
            "context": "{name} finished a project at {end_time}. The project took {duration} to complete.",
            "question": "What time did {name} start the project?",
            "name": ["Emma", "Oliver", "Sophia", "Liam", "Ava"],
            "end_times": ["4:30", "5:15", "3:45", "6:00", "2:20"],
            "durations": ["3 hours and 45 minutes", "2 hours and 30 minutes", "4 hours and 15 minutes", "1 hour and 50 minutes", "3 hours and 10 minutes"]
        },
        {
            "context": "The cake needs to be ready by {end_time}. It takes {duration} to bake and cool.",
            "question": "What time should you start baking?",
            "end_times": ["6:00", "7:30", "5:45", "8:00", "4:15"],
            "durations": ["2 hours and 30 minutes", "3 hours", "2 hours and 15 minutes", "1 hour and 45 minutes", "2 hours and 45 minutes"]
        },
        {
            "context": "The train arrived at {end_time}. The journey took {duration}.",
            "question": "What time did the train depart?",
            "end_times": ["11:20", "2:45", "4:10", "9:30", "12:15"],
            "durations": ["5 hours and 40 minutes", "3 hours and 25 minutes", "6 hours and 15 minutes", "4 hours and 50 minutes", "7 hours and 30 minutes"]
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if "name" in scenario:
        name = random.choice(scenario["name"])
        context = scenario["context"].format(name=name, end_time="{end_time}", duration="{duration}")
        question = scenario["question"].format(name=name)
    else:
        context = scenario["context"]
        question = scenario["question"]
    
    # Choose whether to work forwards or backwards
    if "start_times" in scenario:
        # Forward calculation (like Daniel's doctor problem)
        idx = random.randint(0, len(scenario["start_times"]) - 1)
        start_time = scenario["start_times"][idx]
        duration_text = scenario["durations"][idx]
        
        duration_parts = parse_duration(duration_text)
        start_h, start_m = map(int, start_time.split(":"))
        
        # For very long durations, handle day transitions
        total_minutes = start_h * 60 + start_m + duration_parts["hours"] * 60 + duration_parts["minutes"]
        end_h = (total_minutes // 60) % 24
        end_m = total_minutes % 60
        
        # Convert to 12-hour format
        if end_h == 0:
            display_h = 12
        elif end_h > 12:
            display_h = end_h - 12
        else:
            display_h = end_h
        
        correct_time = f"{display_h}:{end_m:02d}"
        options = generate_time_options(display_h, end_m, 4)
        
        problem_text = context.format(start_time=start_time, duration=duration_text) + " " + question
        explanation = f"Start: {start_time}\nAdd: {duration_text}\nEnd: {correct_time}"
        
    else:
        # Backward calculation
        idx = random.randint(0, len(scenario["end_times"]) - 1)
        end_time = scenario["end_times"][idx]
        duration_text = scenario["durations"][idx]
        
        duration_parts = parse_duration(duration_text)
        end_h, end_m = map(int, end_time.split(":"))
        
        # Calculate start time by subtracting
        total_end_minutes = end_h * 60 + end_m
        total_duration_minutes = duration_parts["hours"] * 60 + duration_parts["minutes"]
        
        if total_end_minutes >= total_duration_minutes:
            total_start_minutes = total_end_minutes - total_duration_minutes
        else:
            # Need to go back past midnight/noon
            total_start_minutes = total_end_minutes + (12 * 60) - total_duration_minutes
        
        start_h = (total_start_minutes // 60) % 12
        if start_h == 0:
            start_h = 12
        start_m = total_start_minutes % 60
        
        correct_time = f"{start_h}:{start_m:02d}"
        options = generate_time_options(start_h, start_m, 4)
        
        problem_text = context.format(end_time=end_time, duration=duration_text) + " " + question
        explanation = f"End: {end_time}\nSubtract: {duration_text}\nStart: {correct_time}"
    
    return {
        "question": problem_text,
        "problem_type": "backwards",
        "options": options,
        "correct_answer": correct_time,
        "explanation": explanation,
        "show_clocks": False,
        "use_multiple_choice": True
    }

def generate_long_duration_problem():
    """Generate Level 4: Long duration problems"""
    scenarios = [
        {
            "context": "Max dropped off his clothes at the dry cleaners at {start_time}. He came back to pick up his clothes {duration} later.",
            "question": "What time was it when Max picked up his clothes from the dry cleaners?",
            "start_times": ["7:20", "8:45", "10:30", "2:15", "4:40"],
            "durations": ["14 hours", "18 hours", "20 hours", "16 hours and 30 minutes", "22 hours and 15 minutes"]
        },
        {
            "context": "Caleb rode the train from Atlanta to New York City. The train left Atlanta at {start_time}. It took {duration} to get to New York City.",
            "question": "What time was it when Caleb got off the train in New York?",
            "start_times": ["10:05", "8:30", "11:45", "6:20", "9:15"],
            "durations": ["17 hours and 15 minutes", "15 hours and 45 minutes", "19 hours and 30 minutes", "14 hours and 20 minutes", "16 hours and 10 minutes"]
        },
        {
            "context": "Jack's school held a walk-a-thon. The teams started walking at {start_time}. They walked for {duration}.",
            "question": "What time was it when the teams finished walking?",
            "start_times": ["9:55", "8:30", "7:45", "10:20", "6:40"],
            "durations": ["13 hours and 50 minutes", "11 hours and 30 minutes", "12 hours and 45 minutes", "10 hours and 20 minutes", "14 hours and 15 minutes"]
        },
        {
            "context": "A science experiment started at {start_time} and needs to run for exactly {duration}.",
            "question": "At what time should the experiment be stopped?",
            "start_times": ["3:15", "5:30", "11:00", "8:45", "1:20"],
            "durations": ["24 hours", "36 hours", "48 hours", "30 hours", "42 hours"]
        },
        {
            "context": "The marathon began at {start_time}. The last runner finished {duration} later.",
            "question": "What time did the last runner finish?",
            "start_times": ["6:00", "7:00", "5:30", "8:00", "6:30"],
            "durations": ["8 hours and 45 minutes", "9 hours and 20 minutes", "7 hours and 55 minutes", "10 hours and 10 minutes", "11 hours and 30 minutes"]
        }
    ]
    
    scenario = random.choice(scenarios)
    idx = random.randint(0, len(scenario["start_times"]) - 1)
    
    start_time = scenario["start_times"][idx]
    duration_text = scenario["durations"][idx]
    
    # Parse duration
    duration_parts = parse_duration(duration_text)
    start_h, start_m = map(int, start_time.split(":"))
    
    # For very long durations
    total_hours = duration_parts["hours"]
    total_minutes = duration_parts["minutes"]
    
    # Calculate end time considering AM/PM transitions
    end_total_minutes = start_h * 60 + start_m + total_hours * 60 + total_minutes
    
    # Handle multi-day scenarios
    days_passed = end_total_minutes // (24 * 60)
    remaining_minutes = end_total_minutes % (24 * 60)
    
    # For 12-hour clock display
    display_h = (remaining_minutes // 60) % 12
    if display_h == 0:
        display_h = 12
    display_m = remaining_minutes % 60
    
    # Determine AM/PM
    hour_24 = remaining_minutes // 60
    period = "AM" if hour_24 < 12 else "PM"
    
    correct_time = f"{display_h}:{display_m:02d}"
    
    # For very long durations, also indicate if next day
    if days_passed > 0:
        day_text = f" ({days_passed} day{'s' if days_passed > 1 else ''} later)"
    else:
        day_text = ""
    
    options = generate_time_options(display_h, display_m, 4)
    
    return {
        "question": scenario["context"].format(start_time=start_time, duration=duration_text) + " " + scenario["question"],
        "problem_type": "long_duration",
        "options": options,
        "correct_answer": correct_time,
        "explanation": f"Start: {start_time}\nDuration: {duration_text}\n{day_text}\nEnd: {correct_time} {period}",
        "show_clocks": True,
        "use_multiple_choice": True
    }

def generate_multi_step_problem():
    """Generate Level 5: Multi-step time problems"""
    scenarios = [
        {
            "context": "Colleen went over to a friend's house to play. She arrived at her friend's house at {start_time} and stayed for {duration}.",
            "question": "What time was it when Colleen went home?",
            "start_times": ["12:50", "1:30", "2:15", "11:45", "3:20"],
            "durations": ["7 hours and 40 minutes", "5 hours and 25 minutes", "6 hours and 15 minutes", "4 hours and 50 minutes", "8 hours and 10 minutes"]
        },
        {
            "context": "A bakery starts preparing bread at {time1}. Mixing takes {duration1}, rising takes {duration2}, and baking takes {duration3}.",
            "question": "What time is the bread ready?",
            "time1": ["4:30", "5:00", "3:45", "4:15", "5:30"],
            "duration1": ["30 minutes", "45 minutes", "35 minutes", "40 minutes", "25 minutes"],
            "duration2": ["2 hours", "1 hour 30 minutes", "2 hours 15 minutes", "1 hour 45 minutes", "2 hours 30 minutes"],
            "duration3": ["45 minutes", "50 minutes", "40 minutes", "55 minutes", "35 minutes"]
        },
        {
            "context": "Tom's workday: Arrives at {time1}, morning meeting for {duration1}, lunch break at noon for {duration2}, works until closing at {time2}.",
            "question": "How many total hours did Tom work (excluding lunch)?",
            "time1": ["8:30", "8:00", "9:00", "8:15", "7:45"],
            "duration1": ["1 hour", "45 minutes", "1 hour 15 minutes", "30 minutes", "1 hour 30 minutes"],
            "duration2": ["1 hour", "45 minutes", "30 minutes", "1 hour", "45 minutes"],
            "time2": ["5:30", "6:00", "5:00", "6:30", "5:45"]
        },
        {
            "context": "A flight departs at {time1}, flies for {duration1} to a layover, waits {duration2}, then flies {duration3} more.",
            "question": "What time does the flight arrive at the final destination?",
            "time1": ["7:45", "9:20", "10:15", "6:30", "8:50"],
            "duration1": ["2 hours 30 minutes", "3 hours 15 minutes", "2 hours 45 minutes", "4 hours", "3 hours 40 minutes"],
            "duration2": ["1 hour 15 minutes", "2 hours", "1 hour 30 minutes", "45 minutes", "1 hour 45 minutes"],
            "duration3": ["3 hours 20 minutes", "2 hours 55 minutes", "4 hours 10 minutes", "3 hours 35 minutes", "2 hours 40 minutes"]
        }
    ]
    
    scenario = random.choice(scenarios)
    
    if "duration1" in scenario:
        # Multi-duration problem
        idx = random.randint(0, len(scenario.get("time1", scenario.get("start_times", []))) - 1)
        
        if scenario["question"].startswith("How many"):
            # Calculate total work hours
            start = scenario["time1"][idx]
            meeting = scenario["duration1"][idx]
            lunch = scenario["duration2"][idx]
            end = scenario["time2"][idx]
            
            # Calculate total time at work
            start_h, start_m = map(int, start.split(":"))
            end_h, end_m = map(int, end.split(":"))
            
            if end_h < start_h:
                end_h += 12
            
            total_minutes = (end_h * 60 + end_m) - (start_h * 60 + start_m)
            
            # Subtract lunch
            lunch_parts = parse_duration(lunch)
            total_minutes -= (lunch_parts["hours"] * 60 + lunch_parts["minutes"])
            
            work_hours = total_minutes // 60
            work_minutes = total_minutes % 60
            
            correct_time = f"{work_hours}h {work_minutes}m"
            options = [correct_time,
                      f"{work_hours-1}h {work_minutes+30}m",
                      f"{work_hours+1}h {work_minutes-15}m",
                      f"{work_hours}h {work_minutes+15}m"]
            random.shuffle(options)
            
            problem_text = scenario["context"].format(
                time1=start, duration1=meeting, duration2=lunch, time2=end
            ) + " " + scenario["question"]
            
            explanation = f"Work day: {start} to {end}\nTotal time at work: {(end_h * 60 + end_m) - (start_h * 60 + start_m)} minutes\nMinus lunch ({lunch}): {total_minutes} minutes\nTotal work: {correct_time}"
            
        else:
            # Calculate end time through multiple steps
            if "time1" in scenario:
                start_time = scenario["time1"][idx]
                key_prefix = ""
            else:
                start_time = scenario["start_times"][idx]
                key_prefix = ""
            
            durations = []
            for i in range(1, 4):
                key = f"duration{i}"
                if key in scenario:
                    durations.append(scenario[key][idx])
            
            # Calculate cumulative time
            start_h, start_m = map(int, start_time.split(":"))
            total_minutes = start_h * 60 + start_m
            
            for duration_text in durations:
                duration_parts = parse_duration(duration_text)
                total_minutes += duration_parts["hours"] * 60 + duration_parts["minutes"]
            
            end_h = (total_minutes // 60) % 24
            end_m = total_minutes % 60
            
            # Convert to 12-hour format
            if end_h == 0:
                display_h = 12
            elif end_h > 12:
                display_h = end_h - 12
            else:
                display_h = end_h
            
            correct_time = f"{display_h}:{end_m:02d}"
            options = generate_time_options(display_h, end_m, 4)
            
            # Format problem text
            format_dict = {"time1": start_time}
            for i, dur in enumerate(durations, 1):
                format_dict[f"duration{i}"] = dur
            
            problem_text = scenario["context"].format(**format_dict) + " " + scenario["question"]
            explanation = f"Start: {start_time}\n" + "\n".join([f"Add: {dur}" for dur in durations]) + f"\nEnd: {correct_time}"
    
    else:
        # Simple multi-step (Colleen type)
        idx = random.randint(0, len(scenario["start_times"]) - 1)
        start_time = scenario["start_times"][idx]
        duration_text = scenario["durations"][idx]
        
        duration_parts = parse_duration(duration_text)
        start_h, start_m = map(int, start_time.split(":"))
        end_h, end_m = calculate_end_time(start_h, start_m, duration_parts["hours"], duration_parts["minutes"])
        
        correct_time = f"{end_h}:{end_m:02d}"
        options = generate_time_options(end_h, end_m, 4)
        
        problem_text = scenario["context"].format(start_time=start_time, duration=duration_text) + " " + scenario["question"]
        explanation = f"Arrived: {start_time}\nStayed: {duration_text}\nLeft: {correct_time}"
    
    return {
        "question": problem_text,
        "problem_type": "multi_step",
        "options": options,
        "correct_answer": correct_time,
        "explanation": explanation,
        "show_clocks": True,
        "use_multiple_choice": True
    }

def parse_duration(duration_text):
    """Parse duration text into hours and minutes"""
    hours = 0
    minutes = 0
    
    # Handle various formats
    if "hour" in duration_text:
        parts = duration_text.split("and")
        for part in parts:
            part = part.strip()
            if "hour" in part:
                hours = int(part.split()[0])
            elif "minute" in part:
                minutes = int(part.split()[0])
    elif "minute" in duration_text:
        minutes = int(duration_text.split()[0])
    
    return {"hours": hours, "minutes": minutes}

def calculate_end_time(start_h, start_m, elapsed_h, elapsed_m):
    """Calculate end time given start and elapsed time"""
    total_minutes = start_h * 60 + start_m + elapsed_h * 60 + elapsed_m
    
    end_h = (total_minutes // 60) % 12
    if end_h == 0:
        end_h = 12
    end_m = total_minutes % 60
    
    return end_h, end_m

def generate_time_options(correct_h, correct_m, num_options):
    """Generate multiple choice time options"""
    options = [f"{correct_h}:{correct_m:02d}"]
    
    # Generate plausible wrong answers
    variations = [
        (-1, 0), (1, 0),  # Hour off
        (0, -15), (0, 15),  # 15 minutes off
        (0, -30), (0, 30),  # 30 minutes off
        (-1, 30), (1, -30),  # Complex variations
        (0, -5), (0, 5),  # 5 minutes off
        (-2, 0), (2, 0)  # 2 hours off
    ]
    
    random.shuffle(variations)
    
    for h_diff, m_diff in variations:
        if len(options) >= num_options:
            break
            
        new_h = correct_h + h_diff
        new_m = correct_m + m_diff
        
        # Handle minute overflow/underflow
        if new_m >= 60:
            new_h += 1
            new_m -= 60
        elif new_m < 0:
            new_h -= 1
            new_m += 60
        
        # Handle hour wrapping
        if new_h > 12:
            new_h -= 12
        elif new_h < 1:
            new_h += 12
        
        option = f"{new_h}:{new_m:02d}"
        if option not in options:
            options.append(option)
    
    # Ensure we have exactly num_options
    while len(options) < num_options:
        rand_h = random.randint(1, 12)
        rand_m = random.randint(0, 59)
        option = f"{rand_h}:{rand_m:02d}"
        if option not in options:
            options.append(option)
    
    random.shuffle(options)
    return options[:num_options]

def display_problem():
    """Display the current problem with options"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Problem {st.session_state.total_attempted + 1}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    st.markdown("---")
    
    # Display options
    if data.get("show_clocks", False):
        display_clock_options(data)
    else:
        display_text_options(data)
    
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

def display_text_options(data):
    """Display text-based multiple choice options"""
    options = data["options"]
    
    cols = st.columns(len(options))
    
    for i, (col, option) in enumerate(zip(cols, options)):
        with col:
            if st.button(option, key=f"option_{i}", disabled=st.session_state.answer_submitted,
                        use_container_width=True):
                st.session_state.user_answer = option
                check_answer()

def display_clock_options(data):
    """Display clock face options"""
    options = data["options"]
    
    # Create clock faces
    cols = st.columns(len(options))
    
    for i, (col, time_str) in enumerate(zip(cols, options)):
        with col:
            # Parse time
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1])
            
            # Create clock visualization
            fig, ax = plt.subplots(figsize=(2, 2))
            
            # Draw clock circle
            circle = plt.Circle((0, 0), 1, fill=False, linewidth=2, color='black')
            ax.add_patch(circle)
            
            # Clock face color (alternating)
            colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink']
            face = plt.Circle((0, 0), 0.98, fill=True, color=colors[i % 4], alpha=0.3)
            ax.add_patch(face)
            
            # Draw hour markers
            for j in range(12):
                angle = np.pi/2 - (j * np.pi/6)
                x = 0.85 * np.cos(angle)
                y = 0.85 * np.sin(angle)
                ax.text(x, y, str(12 if j == 0 else j), ha='center', va='center', fontsize=8, fontweight='bold')
            
            # Draw hour hand
            hour_angle = np.pi/2 - ((hour % 12 + minute/60) * np.pi/6)
            ax.arrow(0, 0, 0.5 * np.cos(hour_angle), 0.5 * np.sin(hour_angle),
                    head_width=0.05, head_length=0.05, fc='black', ec='black', linewidth=2)
            
            # Draw minute hand
            minute_angle = np.pi/2 - (minute * np.pi/30)
            ax.arrow(0, 0, 0.75 * np.cos(minute_angle), 0.75 * np.sin(minute_angle),
                    head_width=0.03, head_length=0.03, fc='blue', ec='blue', linewidth=1.5)
            
            # Center dot
            ax.plot(0, 0, 'ko', markersize=5)
            
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)
            ax.set_aspect('equal')
            ax.axis('off')
            
            st.pyplot(fig)
            plt.close()
            
            # Button below clock
            if st.button(f"Select {time_str}", key=f"clock_{i}", 
                        disabled=st.session_state.answer_submitted,
                        use_container_width=True):
                st.session_state.user_answer = time_str
                check_answer()

def check_answer():
    """Check the user's answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    # Normalize answers for comparison
    user_normalized = user_answer.replace(" ", "").lower()
    correct_normalized = correct_answer.replace(" ", "").lower()
    
    is_correct = user_normalized == correct_normalized
    
    st.session_state.answer_correct = is_correct
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if is_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.problem_data
    
    if st.session_state.answer_correct:
        st.success(f"✅ **Correct! The answer is {data['correct_answer']}**")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.time_problem_difficulty
            st.session_state.time_problem_difficulty = min(
                st.session_state.time_problem_difficulty + 1, 5
            )
            
            if st.session_state.time_problem_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Great job! Moving to Level {st.session_state.time_problem_difficulty}**")
                st.session_state.consecutive_correct = 0
    
    else:
        st.error(f"❌ **Not quite. You selected {st.session_state.user_answer}, but the correct answer is {data['correct_answer']}**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.time_problem_difficulty
            st.session_state.time_problem_difficulty = max(
                st.session_state.time_problem_difficulty - 1, 1
            )
            
            if st.session_state.time_problem_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.time_problem_difficulty}**")
                st.session_state.consecutive_wrong = 0
    
    # Show explanation
    st.markdown(f"📚 **Explanation:** {data['explanation']}")

def show_solution():
    """Show detailed solution steps"""
    with st.expander("📚 **Step-by-Step Solution**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown("### 🔢 Solution:")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        
        # Show method based on problem type
        if data["problem_type"] == "backwards":
            st.markdown("""
            ### 🔄 Working Backwards Method:
            1. Start with the end time
            2. Subtract the duration
            3. Handle borrowing if needed
            4. Check AM/PM transitions
            """)
        elif data["problem_type"] == "long_duration":
            st.markdown("""
            ### ⏰ Long Duration Method:
            1. Note if duration crosses days
            2. Calculate total hours and minutes
            3. Add to start time
            4. Convert to standard time format
            """)
        else:
            st.markdown("""
            ### ➕ Time Addition Method:
            1. Start with the given time
            2. Add hours first
            3. Then add minutes
            4. Adjust if minutes ≥ 60
            5. Convert to 12-hour format if needed
            """)
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Quick Tips:
        - Draw a timeline to visualize
        - Break complex problems into steps
        - Check if you cross noon (AM→PM)
        - Check if you cross midnight (PM→AM)
        - Always verify your answer makes sense!
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