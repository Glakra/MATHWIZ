import streamlit as st
import random

def run():
    """
    Main function to run the Choose Metric Units practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/T. Units of measurement/choose_the_appropriate_metric_unit_of_measure.py
    """
    
    # Initialize session state
    if "metric_units_difficulty" not in st.session_state:
        st.session_state.metric_units_difficulty = 1  # Start with simple comparisons
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
    st.title("📏 Choose the Appropriate Metric Unit")
    st.markdown("*Select the better estimate for each measurement*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.metric_units_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Common objects (obvious differences)",
            2: "Everyday items (closer values)",
            3: "Mixed measurements",
            4: "Challenging comparisons",
            5: "Expert level (tricky estimates)"
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
        - **Read the question** about what you're measuring
        - **Think about the size** of the object or distance
        - **Choose the better estimate** between two options
        - **Click Submit** to check your answer
        
        ### Metric Units to Remember:
        
        **📏 Length:**
        - **Millimetres (mm):** thickness of a coin, width of a pencil lead
        - **Centimetres (cm):** width of a finger, length of a key
        - **Metres (m):** height of a door, length of a car
        - **Kilometres (km):** distance between towns, length of a long walk
        
        **⚖️ Mass/Weight:**
        - **Grams (g):** mass of a paperclip, a coin, a spoon
        - **Kilograms (kg):** mass of a textbook, a bag of flour, a person
        
        **🥤 Volume/Capacity:**
        - **Millilitres (mL):** a spoonful, eye drops, small medicine dose
        - **Litres (L):** bottle of water, milk carton, fish bowl
        
        ### Tips for Success:
        - **Visualize the object** - How big is it really?
        - **Compare to familiar things** - Is it bigger or smaller than your hand?
        - **Eliminate the silly answer** - Would a spoon really be 14 metres long?
        - **Think about practical use** - How would you measure this in real life?
        
        ### Common Reference Points:
        - Your thumb width ≈ 2 cm
        - A door height ≈ 2 m
        - A water bottle ≈ 500 mL or 0.5 L
        - An apple ≈ 150 g
        - A textbook ≈ 1 kg
        """)

def generate_new_question():
    """Generate a new metric unit question based on difficulty"""
    
    difficulty = st.session_state.metric_units_difficulty
    
    # Question banks by difficulty
    if difficulty == 1:
        # Very obvious differences
        questions = [
            # Length
            {"item": "the height of a tree", "correct": "10 metres", "wrong": "10 millimetres", "type": "length"},
            {"item": "the width of a pencil", "correct": "7 millimetres", "wrong": "7 metres", "type": "length"},
            {"item": "the length of a bus", "correct": "12 metres", "wrong": "12 centimetres", "type": "length"},
            {"item": "the thickness of a coin", "correct": "2 millimetres", "wrong": "2 metres", "type": "length"},
            {"item": "the distance to school", "correct": "2 kilometres", "wrong": "2 centimetres", "type": "length"},
            
            # Mass
            {"item": "the mass of an elephant", "correct": "5000 kilograms", "wrong": "5000 grams", "type": "mass"},
            {"item": "the mass of a feather", "correct": "1 gram", "wrong": "1 kilogram", "type": "mass"},
            {"item": "the mass of a car", "correct": "1500 kilograms", "wrong": "1500 grams", "type": "mass"},
            {"item": "the mass of a paper clip", "correct": "1 gram", "wrong": "1 kilogram", "type": "mass"},
            
            # Volume
            {"item": "the volume of a swimming pool", "correct": "50000 litres", "wrong": "50000 millilitres", "type": "volume"},
            {"item": "the volume of an eye dropper", "correct": "1 millilitre", "wrong": "1 litre", "type": "volume"},
            {"item": "the volume of a bathtub", "correct": "200 litres", "wrong": "200 millilitres", "type": "volume"},
            {"item": "the volume of a teaspoon", "correct": "5 millilitres", "wrong": "5 litres", "type": "volume"},
        ]
    
    elif difficulty == 2:
        # Common everyday items (like in your images)
        questions = [
            # Length
            {"item": "the length of a house key", "correct": "6 centimetres", "wrong": "6 millimetres", "type": "length"},
            {"item": "the length of a spoon", "correct": "14 centimetres", "wrong": "14 millimetres", "type": "length"},
            {"item": "the length of a hairbrush", "correct": "21 centimetres", "wrong": "21 metres", "type": "length"},
            {"item": "the height of a basketball player", "correct": "2 metres", "wrong": "2 kilometres", "type": "length"},
            {"item": "the width of a smartphone", "correct": "7 centimetres", "wrong": "7 metres", "type": "length"},
            {"item": "the length of a shoe", "correct": "25 centimetres", "wrong": "25 metres", "type": "length"},
            
            # Mass  
            {"item": "the mass of a fork", "correct": "48 grams", "wrong": "48 kilograms", "type": "mass"},
            {"item": "the mass of a raccoon", "correct": "10 kilograms", "wrong": "10 grams", "type": "mass"},
            {"item": "the mass of a textbook", "correct": "1 kilogram", "wrong": "1 gram", "type": "mass"},
            {"item": "the mass of an apple", "correct": "150 grams", "wrong": "150 kilograms", "type": "mass"},
            {"item": "the mass of a bicycle", "correct": "15 kilograms", "wrong": "15 grams", "type": "mass"},
            
            # Volume
            {"item": "the volume of a grocery bag", "correct": "4 litres", "wrong": "4 millilitres", "type": "volume"},
            {"item": "the volume of a dose of cough syrup", "correct": "15 millilitres", "wrong": "15 litres", "type": "volume"},
            {"item": "the volume of a fish bowl", "correct": "2 litres", "wrong": "2 millilitres", "type": "volume"},
            {"item": "the volume of a water bottle", "correct": "500 millilitres", "wrong": "500 litres", "type": "volume"},
            {"item": "the volume of a soup bowl", "correct": "300 millilitres", "wrong": "300 litres", "type": "volume"},
            
            # Distance
            {"item": "the distance of a ten-minute walk", "correct": "1 kilometre", "wrong": "1 centimetre", "type": "length"},
            {"item": "the width of a classroom", "correct": "8 metres", "wrong": "8 kilometres", "type": "length"},
        ]
    
    elif difficulty == 3:
        # Mixed measurements with closer values
        questions = [
            # Length - closer comparisons
            {"item": "the height of a door", "correct": "2 metres", "wrong": "200 millimetres", "type": "length"},
            {"item": "the length of a pencil", "correct": "18 centimetres", "wrong": "180 millimetres", "type": "length"},
            {"item": "the thickness of a book", "correct": "3 centimetres", "wrong": "30 millimetres", "type": "length"},
            {"item": "the width of a notebook", "correct": "21 centimetres", "wrong": "210 metres", "type": "length"},
            {"item": "the length of a skateboard", "correct": "80 centimetres", "wrong": "0.8 millimetres", "type": "length"},
            
            # Mass - reasonable alternatives
            {"item": "the mass of a bag of sugar", "correct": "1 kilogram", "wrong": "1000 milligrams", "type": "mass"},
            {"item": "the mass of a laptop", "correct": "2 kilograms", "wrong": "2000 milligrams", "type": "mass"},
            {"item": "the mass of a watermelon", "correct": "5 kilograms", "wrong": "500 grams", "type": "mass"},
            {"item": "the mass of a smartphone", "correct": "150 grams", "wrong": "1.5 kilograms", "type": "mass"},
            
            # Volume - practical comparisons
            {"item": "the volume of a coffee mug", "correct": "250 millilitres", "wrong": "2.5 litres", "type": "volume"},
            {"item": "the volume of a milk carton", "correct": "1 litre", "wrong": "100 millilitres", "type": "volume"},
            {"item": "the volume of a medicine dropper", "correct": "5 millilitres", "wrong": "0.5 litres", "type": "volume"},
            {"item": "the volume of a bucket", "correct": "10 litres", "wrong": "1000 millilitres", "type": "volume"},
        ]
    
    elif difficulty == 4:
        # Challenging comparisons
        questions = [
            # Need to think about actual sizes
            {"item": "the length of an ant", "correct": "5 millimetres", "wrong": "5 centimetres", "type": "length"},
            {"item": "the height of a basketball hoop", "correct": "3 metres", "wrong": "30 centimetres", "type": "length"},
            {"item": "the thickness of a smartphone", "correct": "8 millimetres", "wrong": "8 centimetres", "type": "length"},
            {"item": "the wingspan of a bird", "correct": "30 centimetres", "wrong": "3 metres", "type": "length"},
            
            # Mass - need real-world knowledge
            {"item": "the mass of a newborn baby", "correct": "3 kilograms", "wrong": "30 grams", "type": "mass"},
            {"item": "the mass of a coin", "correct": "5 grams", "wrong": "50 grams", "type": "mass"},
            {"item": "the mass of a hamburger", "correct": "200 grams", "wrong": "2 kilograms", "type": "mass"},
            {"item": "the mass of a bowling ball", "correct": "7 kilograms", "wrong": "700 grams", "type": "mass"},
            
            # Volume - practical knowledge needed
            {"item": "the volume of a tablespoon", "correct": "15 millilitres", "wrong": "1.5 litres", "type": "volume"},
            {"item": "the volume of a kitchen sink", "correct": "30 litres", "wrong": "300 millilitres", "type": "volume"},
            {"item": "the volume of a shot glass", "correct": "30 millilitres", "wrong": "3 litres", "type": "volume"},
        ]
    
    else:  # difficulty 5
        # Expert level - very close or tricky comparisons
        questions = [
            # Very close values
            {"item": "the height of a table", "correct": "75 centimetres", "wrong": "7.5 metres", "type": "length"},
            {"item": "the length of a marathon", "correct": "42 kilometres", "wrong": "4200 metres", "type": "length"},
            {"item": "the width of a human hair", "correct": "0.1 millimetres", "wrong": "1 millimetre", "type": "length"},
            
            # Tricky mass comparisons
            {"item": "the mass of a litre of water", "correct": "1 kilogram", "wrong": "100 grams", "type": "mass"},
            {"item": "the mass of a grain of rice", "correct": "20 milligrams", "wrong": "2 grams", "type": "mass"},
            {"item": "the mass of a tennis ball", "correct": "58 grams", "wrong": "580 grams", "type": "mass"},
            
            # Complex volume comparisons
            {"item": "the volume of an Olympic pool", "correct": "2500000 litres", "wrong": "250000 litres", "type": "volume"},
            {"item": "the volume of a raindrop", "correct": "0.05 millilitres", "wrong": "5 millilitres", "type": "volume"},
            {"item": "the volume of human lungs", "correct": "6 litres", "wrong": "60 litres", "type": "volume"},
        ]
    
    # Select a random question
    question = random.choice(questions)
    
    # Randomize the order of options
    options = [question["correct"], question["wrong"]]
    random.shuffle(options)
    
    # Store question data
    st.session_state.question_data = {
        "item": question["item"],
        "correct_answer": question["correct"],
        "wrong_answer": question["wrong"],
        "options": options,
        "type": question["type"]
    }
    
    st.session_state.correct_answer = question["correct"]
    st.session_state.current_question = f"Which is a better estimate for {question['item']}?"

def display_question():
    """Display the current question"""
    
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Create answer tiles
    st.markdown("")  # Add some space
    
    if not st.session_state.answer_submitted:
        # Show clickable options
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
                elif option == st.session_state.selected_answer:
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
            old_difficulty = st.session_state.metric_units_difficulty
            st.session_state.metric_units_difficulty = min(
                st.session_state.metric_units_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.metric_units_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.metric_units_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** The better estimate is **{correct_answer}**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.metric_units_difficulty
            st.session_state.metric_units_difficulty = max(
                st.session_state.metric_units_difficulty - 1, 1
            )
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.metric_units_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.metric_units_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for why one answer is better"""
    
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Why this answer?")
        
        st.markdown(f"**Item:** {data['item']}")
        st.markdown(f"**Correct estimate:** {data['correct_answer']}")
        st.markdown(f"**Wrong estimate:** {data['wrong_answer']}")
        
        # Provide specific explanation based on measurement type
        if data["type"] == "length":
            st.markdown("""
            ### Length Comparison:
            Think about the actual size of the object:
            """)
            
            # Give context for the units
            if "millimetre" in data['correct_answer']:
                st.markdown("- **Millimetres** are very small - about the thickness of a credit card")
            elif "centimetre" in data['correct_answer']:
                st.markdown("- **Centimetres** are small - about the width of your finger")
            elif "metre" in data['correct_answer']:
                st.markdown("- **Metres** are medium - about half your height or more")
            elif "kilometre" in data['correct_answer']:
                st.markdown("- **Kilometres** are very long - you'd need to walk for 10-15 minutes")
            
        elif data["type"] == "mass":
            st.markdown("""
            ### Mass Comparison:
            Think about how heavy the object would feel:
            """)
            
            if "gram" in data['correct_answer'] and "kilogram" not in data['correct_answer']:
                st.markdown("- **Grams** are very light - like a paperclip or a few coins")
            elif "kilogram" in data['correct_answer']:
                st.markdown("- **Kilograms** are heavier - like a bag of flour or a textbook")
            
        elif data["type"] == "volume":
            st.markdown("""
            ### Volume Comparison:
            Think about how much liquid it could hold:
            """)
            
            if "millilitre" in data['correct_answer']:
                st.markdown("- **Millilitres** are small amounts - like medicine doses or spoonfuls")
            elif "litre" in data['correct_answer']:
                st.markdown("- **Litres** are larger amounts - like bottles or containers")
        
        # Common sense check
        st.markdown(f"""
        ### Quick Check:
        Ask yourself: Does it make sense for {data['item']} to be {data['wrong_answer']}?
        
        Sometimes the wrong answer is obviously too big or too small when you think about it!
        """)
        
        # Reference examples
        st.markdown("""
        ### Remember These References:
        - Paper thickness = about 0.1 mm
        - Finger width = about 1 cm  
        - Door height = about 2 m
        - 10-minute walk = about 1 km
        - Paperclip = about 1 g
        - Water bottle = about 500 mL
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None