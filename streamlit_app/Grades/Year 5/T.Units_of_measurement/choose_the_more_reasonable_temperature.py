import streamlit as st
import random

def run():
    """
    Main function to run the Choose the More Reasonable Temperature practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/T. Units of measurement/choose_the_more_reasonable_temperature.py
    """
    
    # Initialize session state
    if "temperature_difficulty" not in st.session_state:
        st.session_state.temperature_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > T. Units of measurement**")
    st.title("🌡️ Choose the More Reasonable Temperature")
    st.markdown("*Select the more reasonable temperature for each situation*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.temperature_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Common situations (obvious)",
            2: "Everyday scenarios",
            3: "Weather and environment",
            4: "Food and objects", 
            5: "Challenging comparisons"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Level ' + str(difficulty_level))}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Show stats
    if st.session_state.total_attempted > 0:
        accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
        st.markdown(f"**📊 Accuracy:** {accuracy:.0f}% ({st.session_state.total_correct}/{st.session_state.total_attempted})")
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the situation** carefully
        - **Think about** what temperature makes sense
        - **Choose** the more reasonable temperature
        - **Click Submit** to check your answer
        
        ### Temperature Reference Guide (Celsius):
        
        **❄️ Cold Temperatures:**
        - **Below 0°C:** Freezing (ice, snow, frost)
        - **0°C:** Water freezes
        - **1-10°C:** Cold day, refrigerator
        - **10-15°C:** Cool day, need a jacket
        
        **🌤️ Moderate Temperatures:**
        - **15-20°C:** Mild day, light jacket
        - **20-25°C:** Room temperature, comfortable
        - **25-30°C:** Warm day, t-shirt weather
        
        **☀️ Hot Temperatures:**
        - **30-35°C:** Hot summer day
        - **35-40°C:** Very hot day
        - **40°C+:** Extreme heat (desert, heat wave)
        
        **🔥 Object Temperatures:**
        - **37°C:** Normal body temperature
        - **40-60°C:** Hot bath water
        - **60-80°C:** Hot coffee/tea
        - **100°C:** Boiling water
        - **180-220°C:** Oven for baking
        - **-18°C:** Freezer temperature
        
        ### Tips for Success:
        - **Eliminate the silly answer** - Would tea really be 0°C?
        - **Think of similar experiences** - How hot is your bath water?
        - **Consider the context** - Desert vs ocean, summer vs winter
        - **Remember key points:**
          - Water freezes at 0°C
          - Water boils at 100°C
          - Body temperature is 37°C
          - Room temperature is about 20-22°C
        
        ### Common Mistakes to Avoid:
        - Don't confuse Celsius with Fahrenheit
        - Remember that 100°C is boiling (not 212°C)
        - Think about whether it's hot or cold first
        """)

def generate_new_question():
    """Generate a new temperature comparison question based on difficulty"""
    
    difficulty = st.session_state.temperature_difficulty
    
    if difficulty == 1:
        # Very obvious differences - common situations
        scenarios = [
            {"situation": "a glass of ice water", "correct": "2°C", "wrong": "50°C"},
            {"situation": "a hot pizza from the oven", "correct": "65°C", "wrong": "5°C"},
            {"situation": "snow on the ground", "correct": "-2°C", "wrong": "25°C"},
            {"situation": "a swimming pool in summer", "correct": "28°C", "wrong": "80°C"},
            {"situation": "inside a freezer", "correct": "-18°C", "wrong": "20°C"},
            {"situation": "a cold drink from the fridge", "correct": "4°C", "wrong": "40°C"},
            {"situation": "steam from a kettle", "correct": "100°C", "wrong": "20°C"},
            {"situation": "an ice cube", "correct": "0°C", "wrong": "30°C"},
            {"situation": "a warm blanket", "correct": "30°C", "wrong": "90°C"},
            {"situation": "cold winter air", "correct": "-5°C", "wrong": "35°C"},
        ]
    
    elif difficulty == 2:
        # Everyday scenarios (like in images)
        scenarios = [
            {"situation": "a piece of warm bread", "correct": "63°C", "wrong": "10°C"},
            {"situation": "a hot cup of tea", "correct": "85°C", "wrong": "0°C"},
            {"situation": "a warm grilled cheese sandwich", "correct": "52°C", "wrong": "10°C"},
            {"situation": "warm soup", "correct": "70°C", "wrong": "15°C"},
            {"situation": "room temperature water", "correct": "22°C", "wrong": "60°C"},
            {"situation": "a cold soda", "correct": "5°C", "wrong": "35°C"},
            {"situation": "freshly baked cookies", "correct": "45°C", "wrong": "5°C"},
            {"situation": "morning coffee", "correct": "75°C", "wrong": "20°C"},
            {"situation": "cold milk", "correct": "3°C", "wrong": "30°C"},
            {"situation": "a warm bath", "correct": "40°C", "wrong": "80°C"},
            {"situation": "melted ice cream", "correct": "10°C", "wrong": "50°C"},
            {"situation": "hot chocolate", "correct": "65°C", "wrong": "15°C"},
        ]
    
    elif difficulty == 3:
        # Weather and environment scenarios
        scenarios = [
            {"situation": "a hot day in the desert", "correct": "49°C", "wrong": "10°C"},
            {"situation": "outside on a cold, rainy day", "correct": "12°C", "wrong": "20°C"},
            {"situation": "a cool day by the ocean", "correct": "10°C", "wrong": "60°C"},
            {"situation": "outside on a frosty morning", "correct": "4°C", "wrong": "20°C"},
            {"situation": "outside on a nice, sunny day", "correct": "21°C", "wrong": "60°C"},
            {"situation": "outside on a very hot day", "correct": "46°C", "wrong": "60°C"},
            {"situation": "a spring morning", "correct": "15°C", "wrong": "35°C"},
            {"situation": "autumn afternoon", "correct": "18°C", "wrong": "38°C"},
            {"situation": "tropical beach at noon", "correct": "32°C", "wrong": "52°C"},
            {"situation": "mountain top in winter", "correct": "-10°C", "wrong": "10°C"},
            {"situation": "rainforest humidity", "correct": "35°C", "wrong": "55°C"},
            {"situation": "arctic conditions", "correct": "-30°C", "wrong": "-5°C"},
        ]
    
    elif difficulty == 4:
        # Food and objects - closer choices
        scenarios = [
            {"situation": "a boiling pot of water", "correct": "100°C", "wrong": "212°C"},  # Testing C vs F confusion
            {"situation": "normal body temperature", "correct": "37°C", "wrong": "47°C"},
            {"situation": "comfortable room temperature", "correct": "22°C", "wrong": "32°C"},
            {"situation": "a fever temperature", "correct": "39°C", "wrong": "29°C"},
            {"situation": "lukewarm water", "correct": "35°C", "wrong": "25°C"},
            {"situation": "a hot shower", "correct": "42°C", "wrong": "62°C"},
            {"situation": "refrigerator temperature", "correct": "4°C", "wrong": "14°C"},
            {"situation": "oven for baking bread", "correct": "200°C", "wrong": "100°C"},
            {"situation": "car dashboard in summer sun", "correct": "75°C", "wrong": "45°C"},
            {"situation": "sauna temperature", "correct": "80°C", "wrong": "50°C"},
            {"situation": "laptop computer surface", "correct": "45°C", "wrong": "25°C"},
            {"situation": "candle flame", "correct": "1000°C", "wrong": "100°C"},
        ]
    
    else:  # difficulty 5
        # Challenging comparisons - both plausible
        scenarios = [
            {"situation": "Death Valley in summer", "correct": "54°C", "wrong": "44°C"},
            {"situation": "Antarctica in winter", "correct": "-60°C", "wrong": "-30°C"},
            {"situation": "surface of a hot road", "correct": "65°C", "wrong": "45°C"},
            {"situation": "pizza oven temperature", "correct": "400°C", "wrong": "200°C"},
            {"situation": "slow cooker setting", "correct": "85°C", "wrong": "65°C"},
            {"situation": "dishwasher water", "correct": "70°C", "wrong": "50°C"},
            {"situation": "CPU temperature under load", "correct": "75°C", "wrong": "55°C"},
            {"situation": "greenhouse interior", "correct": "35°C", "wrong": "25°C"},
            {"situation": "underground cave", "correct": "15°C", "wrong": "5°C"},
            {"situation": "compost pile center", "correct": "65°C", "wrong": "35°C"},
            {"situation": "car engine coolant", "correct": "90°C", "wrong": "60°C"},
            {"situation": "volcanic hot spring", "correct": "45°C", "wrong": "75°C"},
            {"situation": "smartphone while charging", "correct": "38°C", "wrong": "28°C"},
            {"situation": "attic in summer", "correct": "50°C", "wrong": "35°C"},
        ]
    
    # Select a random scenario
    scenario = random.choice(scenarios)
    
    # Randomize the order of options
    options = [scenario["correct"], scenario["wrong"]]
    random.shuffle(options)
    
    # Store question data
    st.session_state.question_data = {
        "situation": scenario["situation"],
        "correct_answer": scenario["correct"],
        "wrong_answer": scenario["wrong"],
        "options": options
    }
    
    st.session_state.correct_answer = scenario["correct"]
    st.session_state.current_question = f"What is the temperature of {scenario['situation']}? Choose the more reasonable answer."

def display_question():
    """Display the current question"""
    
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Create answer options
    st.markdown("")  # Add some space
    
    if not st.session_state.answer_submitted:
        # Show clickable options - horizontal layout
        cols = st.columns(2)
        
        for i, option in enumerate(data["options"]):
            with cols[i]:
                # Style the button based on selection
                button_type = "primary" if option == st.session_state.selected_answer else "secondary"
                
                if st.button(
                    option,
                    key=f"option_{i}",
                    use_container_width=True,
                    type=button_type
                ):
                    st.session_state.selected_answer = option
                    st.rerun()
        
        # Submit button
        st.markdown("")  # Add space
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "✅ Submit",
                type="primary",
                use_container_width=True,
                disabled=(st.session_state.selected_answer is None)
            ):
                if st.session_state.selected_answer:
                    st.session_state.answer_submitted = True
                    st.session_state.total_attempted += 1
                    if st.session_state.selected_answer == st.session_state.correct_answer:
                        st.session_state.total_correct += 1
                    st.rerun()
    
    else:
        # Show results after submission
        cols = st.columns(2)
        
        for i, option in enumerate(data["options"]):
            with cols[i]:
                if option == st.session_state.correct_answer:
                    # Correct answer - show in green
                    st.success(f"✓ {option}")
                elif option == st.session_state.selected_answer and option != st.session_state.correct_answer:
                    # Wrong answer selected - show in red
                    st.error(f"✗ {option}")
                else:
                    # Other option - show disabled
                    st.button(option, disabled=True, use_container_width=True)
        
        # Show feedback
        show_feedback()
        
        # Next question button
        st.markdown("")  # Add space
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    st.markdown("---")
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.temperature_difficulty
            st.session_state.temperature_difficulty = min(
                st.session_state.temperature_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.temperature_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.temperature_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The more reasonable temperature is **{correct_answer}**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.temperature_difficulty
            st.session_state.temperature_difficulty = max(
                st.session_state.temperature_difficulty - 1, 1
            )
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.temperature_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.temperature_difficulty}. Keep practicing!**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show explanation for why one temperature is more reasonable"""
    
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Why this temperature?")
        
        st.markdown(f"**Situation:** {data['situation']}")
        st.markdown(f"**Reasonable temperature:** {data['correct_answer']}")
        st.markdown(f"**Unreasonable temperature:** {data['wrong_answer']}")
        
        # Parse temperatures
        correct_temp = int(data['correct_answer'].replace('°C', ''))
        wrong_temp = int(data['wrong_answer'].replace('°C', ''))
        
        # Provide context based on temperature ranges
        st.markdown("### Temperature Analysis:")
        
        # Analyze correct temperature
        if correct_temp < 0:
            correct_context = "below freezing (ice/snow conditions)"
        elif correct_temp <= 10:
            correct_context = "cold (refrigerator temperature)"
        elif correct_temp <= 20:
            correct_context = "cool (light jacket weather)"
        elif correct_temp <= 30:
            correct_context = "comfortable room temperature"
        elif correct_temp <= 40:
            correct_context = "warm to hot"
        elif correct_temp <= 60:
            correct_context = "very hot (hot drinks/food)"
        elif correct_temp <= 100:
            correct_context = "extremely hot (near boiling)"
        else:
            correct_context = "above boiling point (cooking temperatures)"
        
        st.markdown(f"✅ **{data['correct_answer']}** is {correct_context}")
        
        # Analyze wrong temperature
        if wrong_temp < 0:
            wrong_context = "below freezing"
        elif wrong_temp <= 10:
            wrong_context = "cold"
        elif wrong_temp <= 20:
            wrong_context = "cool"
        elif wrong_temp <= 30:
            wrong_context = "room temperature"
        elif wrong_temp <= 40:
            wrong_context = "warm"
        elif wrong_temp <= 60:
            wrong_context = "very hot"
        elif wrong_temp <= 100:
            wrong_context = "extremely hot"
        elif wrong_temp == 212:
            wrong_context = "212°F (this is Fahrenheit for boiling, not Celsius!)"
        else:
            wrong_context = "above boiling point"
        
        st.markdown(f"❌ **{data['wrong_answer']}** would be {wrong_context}")
        
        # Specific explanations based on situation keywords
        situation_lower = data['situation'].lower()
        
        if "boiling" in situation_lower or "steam" in situation_lower:
            st.markdown("""
            ### Remember:
            - Water boils at **100°C** (not 212°C - that's Fahrenheit!)
            - Steam is at or above 100°C
            """)
        elif "ice" in situation_lower or "snow" in situation_lower or "frozen" in situation_lower:
            st.markdown("""
            ### Remember:
            - Water freezes at **0°C**
            - Ice and snow are at or below 0°C
            """)
        elif "body" in situation_lower or "fever" in situation_lower:
            st.markdown("""
            ### Remember:
            - Normal body temperature: **37°C**
            - Fever: above 38°C
            - 47°C would be life-threatening!
            """)
        elif "room" in situation_lower:
            st.markdown("""
            ### Remember:
            - Comfortable room temperature: **20-22°C**
            - Too cold: below 18°C
            - Too warm: above 26°C
            """)
        elif "desert" in situation_lower:
            st.markdown("""
            ### Remember:
            - Desert temperatures can exceed **45°C**
            - Death Valley record: 54°C
            - 10°C would be a cold winter night
            """)
        elif "ocean" in situation_lower or "beach" in situation_lower:
            st.markdown("""
            ### Remember:
            - Ocean temperature: typically **10-30°C**
            - 60°C would be scalding hot!
            """)
        
        # General temperature reference
        st.markdown("""
        ### Quick Reference:
        - **0°C:** Water freezes ❄️
        - **20°C:** Room temperature 🏠
        - **37°C:** Body temperature 🌡️
        - **100°C:** Water boils 💨
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None