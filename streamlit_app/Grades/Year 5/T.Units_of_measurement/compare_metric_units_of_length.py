import streamlit as st
import random

def run():
    """
    Main function to run the Compare Metric Units of Length practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/T. Units of measurement/compare_metric_units_of_length.py
    """
    
    # Initialize session state
    if "compare_units_difficulty" not in st.session_state:
        st.session_state.compare_units_difficulty = 1
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
    st.title("📏 Compare Metric Units of Length")
    st.markdown("*Compare measurements in different metric units*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.compare_units_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple conversions (10, 100, 1000)",
            2: "Standard comparisons",
            3: "Mixed units with calculations",
            4: "Decimal conversions",
            5: "Complex comparisons"
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
        - **Compare two measurements** in different units
        - **Choose which is more** or if they are equal
        - **Click your answer** then Submit to check
        
        ### Metric Length Units:
        
        **📏 Conversion Chart:**
        ```
        1 kilometre (km) = 1000 metres (m)
        1 metre (m) = 100 centimetres (cm)
        1 metre (m) = 1000 millimetres (mm)
        1 centimetre (cm) = 10 millimetres (mm)
        ```
        
        ### Quick Conversion Tips:
        
        **To convert TO a smaller unit → MULTIPLY:**
        - km → m: × 1000
        - m → cm: × 100
        - m → mm: × 1000
        - cm → mm: × 10
        
        **To convert TO a larger unit → DIVIDE:**
        - m → km: ÷ 1000
        - cm → m: ÷ 100
        - mm → m: ÷ 1000
        - mm → cm: ÷ 10
        
        ### Examples:
        - **2 km = 2000 m** (2 × 1000)
        - **500 cm = 5 m** (500 ÷ 100)
        - **3.5 m = 350 cm** (3.5 × 100)
        - **1500 mm = 1.5 m** (1500 ÷ 1000)
        
        ### Strategy:
        1. **Convert to the same unit** (usually the smaller one)
        2. **Compare the numbers**
        3. **Check if they're equal**
        
        ### Memory Tricks:
        - **Kilo** means 1000 (kilometer = 1000 meters)
        - **Centi** means 1/100 (centimeter = 1/100 meter)
        - **Milli** means 1/1000 (millimeter = 1/1000 meter)
        """)

def generate_new_question():
    """Generate a new comparison question based on difficulty"""
    
    difficulty = st.session_state.compare_units_difficulty
    
    if difficulty == 1:
        # Simple conversions - often equal or very obvious
        comparisons = [
            # Equal comparisons
            {"val1": "100 centimetres", "val2": "1 metre", "answer": "equal", "val1_mm": 1000, "val2_mm": 1000},
            {"val1": "1000 millimetres", "val2": "1 metre", "answer": "equal", "val1_mm": 1000, "val2_mm": 1000},
            {"val1": "10 millimetres", "val2": "1 centimetre", "answer": "equal", "val1_mm": 10, "val2_mm": 10},
            {"val1": "1000 metres", "val2": "1 kilometre", "answer": "equal", "val1_mm": 1000000, "val2_mm": 1000000},
            {"val1": "100 millimetres", "val2": "10 centimetres", "answer": "equal", "val1_mm": 100, "val2_mm": 100},
            
            # Simple unequal
            {"val1": "50 centimetres", "val2": "1 metre", "answer": "second", "val1_mm": 500, "val2_mm": 1000},
            {"val1": "500 millimetres", "val2": "1 metre", "answer": "second", "val1_mm": 500, "val2_mm": 1000},
            {"val1": "2 metres", "val2": "150 centimetres", "answer": "first", "val1_mm": 2000, "val2_mm": 1500},
            {"val1": "5 centimetres", "val2": "30 millimetres", "answer": "first", "val1_mm": 50, "val2_mm": 30},
            {"val1": "2 kilometres", "val2": "1500 metres", "answer": "first", "val1_mm": 2000000, "val2_mm": 1500000},
        ]
    
    elif difficulty == 2:
        # Standard comparisons (like in the images)
        comparisons = [
            {"val1": "99 centimetres", "val2": "1 metre", "answer": "second", "val1_mm": 990, "val2_mm": 1000},
            {"val1": "1244 millimetres", "val2": "1 metre", "answer": "first", "val1_mm": 1244, "val2_mm": 1000},
            {"val1": "1 kilometre", "val2": "441 metres", "answer": "first", "val1_mm": 1000000, "val2_mm": 441000},
            {"val1": "14 millimetres", "val2": "1 centimetre", "answer": "first", "val1_mm": 14, "val2_mm": 10},
            {"val1": "48 centimetres", "val2": "1 metre", "answer": "second", "val1_mm": 480, "val2_mm": 1000},
            {"val1": "695 millimetres", "val2": "1 metre", "answer": "second", "val1_mm": 695, "val2_mm": 1000},
            {"val1": "1 kilometre", "val2": "1704 metres", "answer": "second", "val1_mm": 1000000, "val2_mm": 1704000},
            {"val1": "250 centimetres", "val2": "2.5 metres", "answer": "equal", "val1_mm": 2500, "val2_mm": 2500},
            {"val1": "3 metres", "val2": "295 centimetres", "answer": "first", "val1_mm": 3000, "val2_mm": 2950},
            {"val1": "1050 metres", "val2": "1 kilometre", "answer": "first", "val1_mm": 1050000, "val2_mm": 1000000},
        ]
    
    elif difficulty == 3:
        # Mixed units with more complex numbers
        comparisons = [
            {"val1": "2.5 kilometres", "val2": "2500 metres", "answer": "equal", "val1_mm": 2500000, "val2_mm": 2500000},
            {"val1": "345 centimetres", "val2": "3.4 metres", "answer": "first", "val1_mm": 3450, "val2_mm": 3400},
            {"val1": "7600 millimetres", "val2": "7.6 metres", "answer": "equal", "val1_mm": 7600, "val2_mm": 7600},
            {"val1": "0.5 kilometres", "val2": "550 metres", "answer": "second", "val1_mm": 500000, "val2_mm": 550000},
            {"val1": "125 millimetres", "val2": "12.5 centimetres", "answer": "equal", "val1_mm": 125, "val2_mm": 125},
            {"val1": "4.2 metres", "val2": "4200 millimetres", "answer": "equal", "val1_mm": 4200, "val2_mm": 4200},
            {"val1": "890 centimetres", "val2": "9 metres", "answer": "second", "val1_mm": 8900, "val2_mm": 9000},
            {"val1": "3.75 kilometres", "val2": "3750 metres", "answer": "equal", "val1_mm": 3750000, "val2_mm": 3750000},
            {"val1": "65 centimetres", "val2": "0.65 metres", "answer": "equal", "val1_mm": 650, "val2_mm": 650},
            {"val1": "2050 metres", "val2": "2.05 kilometres", "answer": "equal", "val1_mm": 2050000, "val2_mm": 2050000},
        ]
    
    elif difficulty == 4:
        # Decimal conversions
        comparisons = [
            {"val1": "0.75 metres", "val2": "75 centimetres", "answer": "equal", "val1_mm": 750, "val2_mm": 750},
            {"val1": "1.234 metres", "val2": "123.4 centimetres", "answer": "equal", "val1_mm": 1234, "val2_mm": 1234},
            {"val1": "0.05 kilometres", "val2": "50 metres", "answer": "equal", "val1_mm": 50000, "val2_mm": 50000},
            {"val1": "2.8 centimetres", "val2": "28 millimetres", "answer": "equal", "val1_mm": 28, "val2_mm": 28},
            {"val1": "0.456 metres", "val2": "460 millimetres", "answer": "second", "val1_mm": 456, "val2_mm": 460},
            {"val1": "3.14 metres", "val2": "314 centimetres", "answer": "equal", "val1_mm": 3140, "val2_mm": 3140},
            {"val1": "0.999 kilometres", "val2": "1000 metres", "answer": "second", "val1_mm": 999000, "val2_mm": 1000000},
            {"val1": "15.5 centimetres", "val2": "0.155 metres", "answer": "equal", "val1_mm": 155, "val2_mm": 155},
            {"val1": "7.25 metres", "val2": "7250 millimetres", "answer": "equal", "val1_mm": 7250, "val2_mm": 7250},
            {"val1": "0.089 kilometres", "val2": "89 metres", "answer": "equal", "val1_mm": 89000, "val2_mm": 89000},
        ]
    
    else:  # difficulty 5
        # Complex comparisons with mixed decimals and larger numbers
        comparisons = [
            {"val1": "12.345 kilometres", "val2": "12345 metres", "answer": "equal", "val1_mm": 12345000, "val2_mm": 12345000},
            {"val1": "0.0075 kilometres", "val2": "750 centimetres", "answer": "equal", "val1_mm": 7500, "val2_mm": 7500},
            {"val1": "999 millimetres", "val2": "0.999 metres", "answer": "equal", "val1_mm": 999, "val2_mm": 999},
            {"val1": "45.67 metres", "val2": "4567 centimetres", "answer": "equal", "val1_mm": 45670, "val2_mm": 45670},
            {"val1": "8.008 kilometres", "val2": "8008 metres", "answer": "equal", "val1_mm": 8008000, "val2_mm": 8008000},
            {"val1": "234.5 centimetres", "val2": "2.345 metres", "answer": "equal", "val1_mm": 2345, "val2_mm": 2345},
            {"val1": "0.00123 kilometres", "val2": "123 centimetres", "answer": "equal", "val1_mm": 1230, "val2_mm": 1230},
            {"val1": "5555 millimetres", "val2": "5.555 metres", "answer": "equal", "val1_mm": 5555, "val2_mm": 5555},
            {"val1": "76.54 metres", "val2": "0.07654 kilometres", "answer": "equal", "val1_mm": 76540, "val2_mm": 76540},
            {"val1": "989.9 centimetres", "val2": "9.899 metres", "answer": "equal", "val1_mm": 9899, "val2_mm": 9899},
            
            # Some unequal ones at this level
            {"val1": "3.456 kilometres", "val2": "3465 metres", "answer": "second", "val1_mm": 3456000, "val2_mm": 3465000},
            {"val1": "789.5 centimetres", "val2": "7.9 metres", "answer": "second", "val1_mm": 7895, "val2_mm": 7900},
            {"val1": "0.0501 kilometres", "val2": "50 metres", "answer": "first", "val1_mm": 50100, "val2_mm": 50000},
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
        "val1_mm": comparison["val1_mm"],
        "val2_mm": comparison["val2_mm"],
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
            old_difficulty = st.session_state.compare_units_difficulty
            st.session_state.compare_units_difficulty = min(
                st.session_state.compare_units_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.compare_units_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.compare_units_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.compare_units_difficulty
            st.session_state.compare_units_difficulty = max(
                st.session_state.compare_units_difficulty - 1, 1
            )
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.compare_units_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.compare_units_difficulty}. Keep practicing!**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the comparison"""
    
    data = st.session_state.question_data
    
    with st.expander("📖 **See the solution**", expanded=True):
        st.markdown("### Step-by-Step Comparison:")
        
        # Convert both values to millimeters for comparison
        val1_mm = data["val1_mm"]
        val2_mm = data["val2_mm"]
        
        st.markdown(f"**First value:** {data['val1']}")
        st.markdown(f"**Second value:** {data['val2']}")
        
        st.markdown("### Convert to the same unit (millimetres):")
        
        # Show conversion for first value
        val1_conversion = get_conversion_explanation(data['val1'], val1_mm)
        st.markdown(f"**{data['val1']}** = {val1_conversion}")
        
        # Show conversion for second value
        val2_conversion = get_conversion_explanation(data['val2'], val2_mm)
        st.markdown(f"**{data['val2']}** = {val2_conversion}")
        
        st.markdown("### Compare:")
        
        if val1_mm > val2_mm:
            st.markdown(f"**{val1_mm:,} mm > {val2_mm:,} mm**")
            st.markdown(f"Therefore, **{data['val1']} is more** than {data['val2']}")
            difference = val1_mm - val2_mm
            st.markdown(f"Difference: {difference:,} mm")
        elif val2_mm > val1_mm:
            st.markdown(f"**{val2_mm:,} mm > {val1_mm:,} mm**")
            st.markdown(f"Therefore, **{data['val2']} is more** than {data['val1']}")
            difference = val2_mm - val1_mm
            st.markdown(f"Difference: {difference:,} mm")
        else:
            st.markdown(f"**{val1_mm:,} mm = {val2_mm:,} mm**")
            st.markdown(f"Therefore, **they are equal**")
        
        # Quick conversion reminder
        st.markdown("""
        ### Remember:
        - 1 km = 1000 m = 100,000 cm = 1,000,000 mm
        - 1 m = 100 cm = 1000 mm
        - 1 cm = 10 mm
        """)

def get_conversion_explanation(value_str, mm_value):
    """Get a detailed conversion explanation"""
    
    if "kilometre" in value_str:
        # Extract number
        num = float(value_str.split()[0])
        metres = num * 1000
        cm = num * 100000
        return f"{num} × 1,000,000 = **{mm_value:,} mm**"
    elif "metre" in value_str and "centi" not in value_str and "milli" not in value_str:
        num = float(value_str.split()[0])
        cm = num * 100
        return f"{num} × 1,000 = **{mm_value:,} mm**"
    elif "centimetre" in value_str:
        num = float(value_str.split()[0])
        return f"{num} × 10 = **{mm_value:,} mm**"
    elif "millimetre" in value_str:
        return f"**{mm_value:,} mm** (already in millimetres)"
    else:
        return f"**{mm_value:,} mm**"

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None