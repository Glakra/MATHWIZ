import streamlit as st
import random

def run():
    """
    Main function to run the Compare Metric Units of Mass practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/T. Units of measurement/compare_metric_units_of_mass.py
    """
    
    # Initialize session state
    if "compare_mass_difficulty" not in st.session_state:
        st.session_state.compare_mass_difficulty = 1
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
    st.title("⚖️ Compare Metric Units of Mass")
    st.markdown("*Compare measurements in different metric mass units*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.compare_mass_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple conversions (1000s)",
            2: "Standard comparisons", 
            3: "Mixed units with calculations",
            4: "Decimal and fraction conversions",
            5: "Complex with tonnes"
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
        - **Compare two mass measurements** in different units
        - **Choose which is more** or if they are equal
        - **Click your answer** then Submit to check
        
        ### Metric Mass Units:
        
        **⚖️ Conversion Chart:**
        ```
        1 tonne (t) = 1000 kilograms (kg)
        1 kilogram (kg) = 1000 grams (g)
        1 gram (g) = 1000 milligrams (mg)
        ```
        
        ### Quick Conversion Tips:
        
        **To convert TO a smaller unit → MULTIPLY:**
        - t → kg: × 1000
        - kg → g: × 1000
        - g → mg: × 1000
        
        **To convert TO a larger unit → DIVIDE:**
        - kg → t: ÷ 1000
        - g → kg: ÷ 1000
        - mg → g: ÷ 1000
        
        ### Real-World References:
        - **1 milligram:** a grain of sand
        - **1 gram:** a paperclip, a raisin
        - **1 kilogram:** a bag of flour, a textbook
        - **1 tonne:** a small car
        
        ### Examples:
        - **1000 mg = 1 g**
        - **1000 g = 1 kg**
        - **500 g = 0.5 kg**
        - **2500 g = 2.5 kg**
        - **1500 kg = 1.5 tonnes**
        
        ### Strategy:
        1. **Convert to the same unit** (usually grams or milligrams)
        2. **Compare the numbers**
        3. **Remember:** 1000 is the magic number!
        
        ### Memory Tricks:
        - **Kilo** = 1000 (kilogram = 1000 grams)
        - **Milli** = 1/1000 (milligram = 1/1000 gram)
        - A **tonne** is a metric ton (1000 kg)
        """)

def generate_new_question():
    """Generate a new mass comparison question based on difficulty"""
    
    difficulty = st.session_state.compare_mass_difficulty
    
    if difficulty == 1:
        # Simple conversions - often equal or very obvious
        comparisons = [
            # Equal comparisons - fundamental
            {"val1": "1000 grams", "val2": "1 kilogram", "answer": "equal", "val1_mg": 1000000, "val2_mg": 1000000},
            {"val1": "1000 milligrams", "val2": "1 gram", "answer": "equal", "val1_mg": 1000, "val2_mg": 1000},
            {"val1": "2000 grams", "val2": "2 kilograms", "answer": "equal", "val1_mg": 2000000, "val2_mg": 2000000},
            {"val1": "500 grams", "val2": "0.5 kilograms", "answer": "equal", "val1_mg": 500000, "val2_mg": 500000},
            {"val1": "100 milligrams", "val2": "0.1 grams", "answer": "equal", "val1_mg": 100, "val2_mg": 100},
            
            # Simple unequal
            {"val1": "500 grams", "val2": "1 kilogram", "answer": "second", "val1_mg": 500000, "val2_mg": 1000000},
            {"val1": "500 milligrams", "val2": "1 gram", "answer": "second", "val1_mg": 500, "val2_mg": 1000},
            {"val1": "2 kilograms", "val2": "1500 grams", "answer": "first", "val1_mg": 2000000, "val2_mg": 1500000},
            {"val1": "50 grams", "val2": "30000 milligrams", "answer": "first", "val1_mg": 50000, "val2_mg": 30000},
            {"val1": "3 kilograms", "val2": "3500 grams", "answer": "second", "val1_mg": 3000000, "val2_mg": 3500000},
        ]
    
    elif difficulty == 2:
        # Standard comparisons (like in the images)
        comparisons = [
            {"val1": "868 grams", "val2": "1 kilogram", "answer": "second", "val1_mg": 868000, "val2_mg": 1000000},
            {"val1": "1 gram", "val2": "890 milligrams", "answer": "first", "val1_mg": 1000, "val2_mg": 890},
            {"val1": "1629 grams", "val2": "1 kilogram", "answer": "first", "val1_mg": 1629000, "val2_mg": 1000000},
            {"val1": "1 gram", "val2": "197 milligrams", "answer": "first", "val1_mg": 1000, "val2_mg": 197},
            {"val1": "1000 grams", "val2": "1 kilogram", "answer": "equal", "val1_mg": 1000000, "val2_mg": 1000000},
            {"val1": "1 gram", "val2": "42 milligrams", "answer": "first", "val1_mg": 1000, "val2_mg": 42},
            {"val1": "1 kilogram", "val2": "1694 grams", "answer": "second", "val1_mg": 1000000, "val2_mg": 1694000},
            {"val1": "814 milligrams", "val2": "1 gram", "answer": "second", "val1_mg": 814, "val2_mg": 1000},
            {"val1": "750 grams", "val2": "1 kilogram", "answer": "second", "val1_mg": 750000, "val2_mg": 1000000},
            {"val1": "1250 milligrams", "val2": "1 gram", "answer": "first", "val1_mg": 1250, "val2_mg": 1000},
        ]
    
    elif difficulty == 3:
        # Mixed units with more complex numbers
        comparisons = [
            {"val1": "2.5 kilograms", "val2": "2500 grams", "answer": "equal", "val1_mg": 2500000, "val2_mg": 2500000},
            {"val1": "3450 grams", "val2": "3.4 kilograms", "answer": "first", "val1_mg": 3450000, "val2_mg": 3400000},
            {"val1": "7600 milligrams", "val2": "7.6 grams", "answer": "equal", "val1_mg": 7600, "val2_mg": 7600},
            {"val1": "0.5 kilograms", "val2": "550 grams", "answer": "second", "val1_mg": 500000, "val2_mg": 550000},
            {"val1": "125 milligrams", "val2": "0.125 grams", "answer": "equal", "val1_mg": 125, "val2_mg": 125},
            {"val1": "4.2 grams", "val2": "4200 milligrams", "answer": "equal", "val1_mg": 4200, "val2_mg": 4200},
            {"val1": "890 grams", "val2": "0.9 kilograms", "answer": "second", "val1_mg": 890000, "val2_mg": 900000},
            {"val1": "3.75 kilograms", "val2": "3750 grams", "answer": "equal", "val1_mg": 3750000, "val2_mg": 3750000},
            {"val1": "650 milligrams", "val2": "0.65 grams", "answer": "equal", "val1_mg": 650, "val2_mg": 650},
            {"val1": "2050 grams", "val2": "2.05 kilograms", "answer": "equal", "val1_mg": 2050000, "val2_mg": 2050000},
        ]
    
    elif difficulty == 4:
        # Decimal and fraction conversions
        comparisons = [
            {"val1": "0.75 kilograms", "val2": "750 grams", "answer": "equal", "val1_mg": 750000, "val2_mg": 750000},
            {"val1": "1.234 grams", "val2": "1234 milligrams", "answer": "equal", "val1_mg": 1234, "val2_mg": 1234},
            {"val1": "0.05 kilograms", "val2": "50 grams", "answer": "equal", "val1_mg": 50000, "val2_mg": 50000},
            {"val1": "2.8 grams", "val2": "2800 milligrams", "answer": "equal", "val1_mg": 2800, "val2_mg": 2800},
            {"val1": "0.456 kilograms", "val2": "460 grams", "answer": "second", "val1_mg": 456000, "val2_mg": 460000},
            {"val1": "3.14 grams", "val2": "3140 milligrams", "answer": "equal", "val1_mg": 3140, "val2_mg": 3140},
            {"val1": "0.999 kilograms", "val2": "1000 grams", "answer": "second", "val1_mg": 999000, "val2_mg": 1000000},
            {"val1": "15.5 grams", "val2": "15500 milligrams", "answer": "equal", "val1_mg": 15500, "val2_mg": 15500},
            {"val1": "7.25 kilograms", "val2": "7250 grams", "answer": "equal", "val1_mg": 7250000, "val2_mg": 7250000},
            {"val1": "0.089 grams", "val2": "89 milligrams", "answer": "equal", "val1_mg": 89, "val2_mg": 89},
            {"val1": "345.6 grams", "val2": "0.3456 kilograms", "answer": "equal", "val1_mg": 345600, "val2_mg": 345600},
            {"val1": "0.0025 kilograms", "val2": "2.5 grams", "answer": "equal", "val1_mg": 2500, "val2_mg": 2500},
        ]
    
    else:  # difficulty 5 - includes tonnes
        # Complex comparisons with tonnes and mixed decimals
        comparisons = [
            {"val1": "1 tonne", "val2": "1000 kilograms", "answer": "equal", "val1_mg": 1000000000, "val2_mg": 1000000000},
            {"val1": "0.5 tonnes", "val2": "500 kilograms", "answer": "equal", "val1_mg": 500000000, "val2_mg": 500000000},
            {"val1": "2.5 tonnes", "val2": "2500 kilograms", "answer": "equal", "val1_mg": 2500000000, "val2_mg": 2500000000},
            {"val1": "1500 kilograms", "val2": "1.5 tonnes", "answer": "equal", "val1_mg": 1500000000, "val2_mg": 1500000000},
            {"val1": "0.001 tonnes", "val2": "1 kilogram", "answer": "equal", "val1_mg": 1000000, "val2_mg": 1000000},
            {"val1": "12.345 kilograms", "val2": "12345 grams", "answer": "equal", "val1_mg": 12345000, "val2_mg": 12345000},
            {"val1": "0.0075 kilograms", "val2": "7.5 grams", "answer": "equal", "val1_mg": 7500, "val2_mg": 7500},
            {"val1": "999 milligrams", "val2": "0.999 grams", "answer": "equal", "val1_mg": 999, "val2_mg": 999},
            {"val1": "45.67 grams", "val2": "45670 milligrams", "answer": "equal", "val1_mg": 45670, "val2_mg": 45670},
            {"val1": "8.008 kilograms", "val2": "8008 grams", "answer": "equal", "val1_mg": 8008000, "val2_mg": 8008000},
            
            # Some unequal ones at this level
            {"val1": "1.2 tonnes", "val2": "1250 kilograms", "answer": "second", "val1_mg": 1200000000, "val2_mg": 1250000000},
            {"val1": "3.456 kilograms", "val2": "3465 grams", "answer": "second", "val1_mg": 3456000, "val2_mg": 3465000},
            {"val1": "789.5 grams", "val2": "0.79 kilograms", "answer": "second", "val1_mg": 789500, "val2_mg": 790000},
            {"val1": "0.751 tonnes", "val2": "750 kilograms", "answer": "first", "val1_mg": 751000000, "val2_mg": 750000000},
            {"val1": "50.01 grams", "val2": "50000 milligrams", "answer": "first", "val1_mg": 50010, "val2_mg": 50000},
        ]
    
    # Select a random comparison
    comparison = random.choice(comparisons)
    
    # Determine the correct answer text
    if comparison["answer"] == "first":
        correct_answer = comparison["val1"]
    elif comparison["answer"] == "second":
        correct_answer = comparison["val2"]
    else:
        correct_answer = "neither; they are equal"
    
    # Store question data
    st.session_state.question_data = {
        "val1": comparison["val1"],
        "val2": comparison["val2"],
        "val1_mg": comparison["val1_mg"],
        "val2_mg": comparison["val2_mg"],
        "answer_type": comparison["answer"],
        "options": [comparison["val1"], comparison["val2"], "neither; they are equal"]
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Which is more, {comparison['val1']} or {comparison['val2']}?"

def display_question():
    """Display the current question"""
    
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Create answer options
    st.markdown("")  # Add some space
    
    if not st.session_state.answer_submitted:
        # Show clickable options - one per row
        for option in data["options"]:
            # Style the button based on selection
            button_type = "primary" if option == st.session_state.selected_answer else "secondary"
            
            if st.button(
                option,
                key=f"option_{option}",
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
        for option in data["options"]:
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
            old_difficulty = st.session_state.compare_mass_difficulty
            st.session_state.compare_mass_difficulty = min(
                st.session_state.compare_mass_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.compare_mass_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.compare_mass_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.compare_mass_difficulty
            st.session_state.compare_mass_difficulty = max(
                st.session_state.compare_mass_difficulty - 1, 1
            )
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.compare_mass_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.compare_mass_difficulty}. Keep practicing!**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the comparison"""
    
    data = st.session_state.question_data
    
    with st.expander("📖 **See the solution**", expanded=True):
        st.markdown("### Step-by-Step Comparison:")
        
        # Convert both values to milligrams for comparison
        val1_mg = data["val1_mg"]
        val2_mg = data["val2_mg"]
        
        st.markdown(f"**First value:** {data['val1']}")
        st.markdown(f"**Second value:** {data['val2']}")
        
        st.markdown("### Convert to the same unit (milligrams):")
        
        # Show conversion for first value
        val1_conversion = get_conversion_explanation(data['val1'], val1_mg)
        st.markdown(f"**{data['val1']}** = {val1_conversion}")
        
        # Show conversion for second value
        val2_conversion = get_conversion_explanation(data['val2'], val2_mg)
        st.markdown(f"**{data['val2']}** = {val2_conversion}")
        
        st.markdown("### Compare:")
        
        if val1_mg > val2_mg:
            st.markdown(f"**{val1_mg:,} mg > {val2_mg:,} mg**")
            st.markdown(f"Therefore, **{data['val1']} is more** than {data['val2']}")
            difference = val1_mg - val2_mg
            st.markdown(f"Difference: {difference:,} mg")
            
            # Show difference in appropriate units
            if difference >= 1000000:
                st.markdown(f"That's {difference/1000000:.2f} grams difference")
        elif val2_mg > val1_mg:
            st.markdown(f"**{val2_mg:,} mg > {val1_mg:,} mg**")
            st.markdown(f"Therefore, **{data['val2']} is more** than {data['val1']}")
            difference = val2_mg - val1_mg
            st.markdown(f"Difference: {difference:,} mg")
            
            # Show difference in appropriate units
            if difference >= 1000000:
                st.markdown(f"That's {difference/1000000:.2f} grams difference")
        else:
            st.markdown(f"**{val1_mg:,} mg = {val2_mg:,} mg**")
            st.markdown(f"Therefore, **they are equal**")
        
        # Quick conversion reminder
        st.markdown("""
        ### Remember:
        - 1 tonne = 1,000 kg = 1,000,000 g = 1,000,000,000 mg
        - 1 kg = 1,000 g = 1,000,000 mg
        - 1 g = 1,000 mg
        
        ### Real-World Examples:
        - A paperclip ≈ 1 g
        - An apple ≈ 150 g
        - A textbook ≈ 1 kg
        - A small car ≈ 1 tonne
        """)

def get_conversion_explanation(value_str, mg_value):
    """Get a detailed conversion explanation"""
    
    if "tonne" in value_str:
        # Extract number
        num = float(value_str.split()[0])
        kg = num * 1000
        g = num * 1000000
        return f"{num} × 1,000,000,000 = **{mg_value:,} mg**"
    elif "kilogram" in value_str:
        num = float(value_str.split()[0])
        g = num * 1000
        return f"{num} × 1,000,000 = **{mg_value:,} mg**"
    elif "gram" in value_str and "milli" not in value_str and "kilo" not in value_str:
        num = float(value_str.split()[0])
        return f"{num} × 1,000 = **{mg_value:,} mg**"
    elif "milligram" in value_str:
        return f"**{mg_value:,} mg** (already in milligrams)"
    else:
        return f"**{mg_value:,} mg**"

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None