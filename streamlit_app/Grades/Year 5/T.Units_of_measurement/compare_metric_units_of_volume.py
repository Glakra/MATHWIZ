import streamlit as st
import random

def run():
    """
    Main function to run the Compare Metric Units of Volume practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/T. Units of measurement/compare_metric_units_of_volume.py
    """
    
    # Initialize session state
    if "compare_volume_difficulty" not in st.session_state:
        st.session_state.compare_volume_difficulty = 1
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
    st.title("🥤 Compare Metric Units of Volume")
    st.markdown("*Compare measurements in different metric volume units*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.compare_volume_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple conversions (1000s)",
            2: "Standard comparisons",
            3: "Mixed units with calculations",
            4: "Decimal conversions",
            5: "Complex with megalitres"
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
        - **Compare two volume measurements** in different units
        - **Choose which is more** or if they are equal
        - **Click your answer** then Submit to check
        
        ### Metric Volume/Capacity Units:
        
        **🥤 Conversion Chart:**
        ```
        1 kilolitre (kL) = 1000 litres (L)
        1 litre (L) = 1000 millilitres (mL)
        1 millilitre (mL) = 1 cubic centimetre (cm³)
        ```
        
        ### Quick Conversion Tips:
        
        **To convert TO a smaller unit → MULTIPLY:**
        - kL → L: × 1000
        - L → mL: × 1000
        
        **To convert TO a larger unit → DIVIDE:**
        - L → kL: ÷ 1000
        - mL → L: ÷ 1000
        
        ### Real-World References:
        - **1 millilitre:** a medicine spoonful, eye drop
        - **250 mL:** a cup of water
        - **500 mL:** a water bottle
        - **1 litre:** a large milk carton
        - **2 litres:** a large soft drink bottle
        - **1 kilolitre:** 1000 litres (small swimming pool)
        
        ### Examples:
        - **1000 mL = 1 L**
        - **1000 L = 1 kL**
        - **500 mL = 0.5 L**
        - **2500 mL = 2.5 L**
        - **1500 L = 1.5 kL**
        
        ### Strategy:
        1. **Convert to the same unit** (usually millilitres)
        2. **Compare the numbers**
        3. **Remember:** 1000 is the magic number!
        
        ### Memory Tricks:
        - **Kilo** = 1000 (kilolitre = 1000 litres)
        - **Milli** = 1/1000 (millilitre = 1/1000 litre)
        - Think of a **litre** as a large milk carton
        - Think of a **millilitre** as drops or spoonfuls
        """)

def generate_new_question():
    """Generate a new volume comparison question based on difficulty"""
    
    difficulty = st.session_state.compare_volume_difficulty
    
    if difficulty == 1:
        # Simple conversions - often equal or very obvious
        comparisons = [
            # Equal comparisons - fundamental
            {"val1": "1000 millilitres", "val2": "1 litre", "answer": "equal", "val1_ml": 1000, "val2_ml": 1000},
            {"val1": "1000 litres", "val2": "1 kilolitre", "answer": "equal", "val1_ml": 1000000, "val2_ml": 1000000},
            {"val1": "2000 millilitres", "val2": "2 litres", "answer": "equal", "val1_ml": 2000, "val2_ml": 2000},
            {"val1": "500 millilitres", "val2": "0.5 litres", "answer": "equal", "val1_ml": 500, "val2_ml": 500},
            {"val1": "3000 litres", "val2": "3 kilolitres", "answer": "equal", "val1_ml": 3000000, "val2_ml": 3000000},
            
            # Simple unequal
            {"val1": "500 millilitres", "val2": "1 litre", "answer": "second", "val1_ml": 500, "val2_ml": 1000},
            {"val1": "500 litres", "val2": "1 kilolitre", "answer": "second", "val1_ml": 500000, "val2_ml": 1000000},
            {"val1": "2 litres", "val2": "1500 millilitres", "answer": "first", "val1_ml": 2000, "val2_ml": 1500},
            {"val1": "2 kilolitres", "val2": "1500 litres", "answer": "first", "val1_ml": 2000000, "val2_ml": 1500000},
            {"val1": "750 millilitres", "val2": "1 litre", "answer": "second", "val1_ml": 750, "val2_ml": 1000},
        ]
    
    elif difficulty == 2:
        # Standard comparisons (like in the images)
        comparisons = [
            {"val1": "154 litres", "val2": "1 kilolitre", "answer": "second", "val1_ml": 154000, "val2_ml": 1000000},
            {"val1": "1 litre", "val2": "1682 millilitres", "answer": "second", "val1_ml": 1000, "val2_ml": 1682},
            {"val1": "688 litres", "val2": "1 kilolitre", "answer": "second", "val1_ml": 688000, "val2_ml": 1000000},
            {"val1": "792 millilitres", "val2": "1 litre", "answer": "second", "val1_ml": 792, "val2_ml": 1000},
            {"val1": "1136 litres", "val2": "1 kilolitre", "answer": "first", "val1_ml": 1136000, "val2_ml": 1000000},
            {"val1": "120 millilitres", "val2": "1 litre", "answer": "second", "val1_ml": 120, "val2_ml": 1000},
            {"val1": "1000 litres", "val2": "1 kilolitre", "answer": "equal", "val1_ml": 1000000, "val2_ml": 1000000},
            {"val1": "1363 millilitres", "val2": "1 litre", "answer": "first", "val1_ml": 1363, "val2_ml": 1000},
            {"val1": "127 litres", "val2": "1 kilolitre", "answer": "second", "val1_ml": 127000, "val2_ml": 1000000},
            {"val1": "1 litre", "val2": "167 millilitres", "answer": "first", "val1_ml": 1000, "val2_ml": 167},
            {"val1": "1245 millilitres", "val2": "1 litre", "answer": "first", "val1_ml": 1245, "val2_ml": 1000},
            {"val1": "890 litres", "val2": "1 kilolitre", "answer": "second", "val1_ml": 890000, "val2_ml": 1000000},
        ]
    
    elif difficulty == 3:
        # Mixed units with more complex numbers
        comparisons = [
            {"val1": "2.5 litres", "val2": "2500 millilitres", "answer": "equal", "val1_ml": 2500, "val2_ml": 2500},
            {"val1": "3.45 litres", "val2": "3400 millilitres", "answer": "first", "val1_ml": 3450, "val2_ml": 3400},
            {"val1": "1.5 kilolitres", "val2": "1500 litres", "answer": "equal", "val1_ml": 1500000, "val2_ml": 1500000},
            {"val1": "0.5 kilolitres", "val2": "550 litres", "answer": "second", "val1_ml": 500000, "val2_ml": 550000},
            {"val1": "125 millilitres", "val2": "0.125 litres", "answer": "equal", "val1_ml": 125, "val2_ml": 125},
            {"val1": "4200 millilitres", "val2": "4.2 litres", "answer": "equal", "val1_ml": 4200, "val2_ml": 4200},
            {"val1": "890 litres", "val2": "0.9 kilolitres", "answer": "second", "val1_ml": 890000, "val2_ml": 900000},
            {"val1": "3.75 kilolitres", "val2": "3750 litres", "answer": "equal", "val1_ml": 3750000, "val2_ml": 3750000},
            {"val1": "650 millilitres", "val2": "0.65 litres", "answer": "equal", "val1_ml": 650, "val2_ml": 650},
            {"val1": "2050 litres", "val2": "2.05 kilolitres", "answer": "equal", "val1_ml": 2050000, "val2_ml": 2050000},
            {"val1": "1.234 litres", "val2": "1234 millilitres", "answer": "equal", "val1_ml": 1234, "val2_ml": 1234},
            {"val1": "7.6 litres", "val2": "7600 millilitres", "answer": "equal", "val1_ml": 7600, "val2_ml": 7600},
        ]
    
    elif difficulty == 4:
        # Decimal conversions and practical measurements
        comparisons = [
            {"val1": "0.75 litres", "val2": "750 millilitres", "answer": "equal", "val1_ml": 750, "val2_ml": 750},
            {"val1": "1.234 litres", "val2": "1234 millilitres", "answer": "equal", "val1_ml": 1234, "val2_ml": 1234},
            {"val1": "0.05 kilolitres", "val2": "50 litres", "answer": "equal", "val1_ml": 50000, "val2_ml": 50000},
            {"val1": "2.8 litres", "val2": "2800 millilitres", "answer": "equal", "val1_ml": 2800, "val2_ml": 2800},
            {"val1": "0.456 litres", "val2": "460 millilitres", "answer": "second", "val1_ml": 456, "val2_ml": 460},
            {"val1": "3.14 litres", "val2": "3140 millilitres", "answer": "equal", "val1_ml": 3140, "val2_ml": 3140},
            {"val1": "0.999 kilolitres", "val2": "1000 litres", "answer": "second", "val1_ml": 999000, "val2_ml": 1000000},
            {"val1": "15.5 litres", "val2": "15500 millilitres", "answer": "equal", "val1_ml": 15500, "val2_ml": 15500},
            {"val1": "7.25 kilolitres", "val2": "7250 litres", "answer": "equal", "val1_ml": 7250000, "val2_ml": 7250000},
            {"val1": "0.089 litres", "val2": "89 millilitres", "answer": "equal", "val1_ml": 89, "val2_ml": 89},
            {"val1": "345.6 millilitres", "val2": "0.3456 litres", "answer": "equal", "val1_ml": 345.6, "val2_ml": 345.6},
            {"val1": "0.0025 kilolitres", "val2": "2.5 litres", "answer": "equal", "val1_ml": 2500, "val2_ml": 2500},
            {"val1": "1.75 litres", "val2": "1750 millilitres", "answer": "equal", "val1_ml": 1750, "val2_ml": 1750},
            {"val1": "0.375 litres", "val2": "375 millilitres", "answer": "equal", "val1_ml": 375, "val2_ml": 375},
        ]
    
    else:  # difficulty 5 - includes megalitres and complex decimals
        # Complex comparisons with megalitres and mixed decimals
        comparisons = [
            {"val1": "1 megalitre", "val2": "1000 kilolitres", "answer": "equal", "val1_ml": 1000000000, "val2_ml": 1000000000},
            {"val1": "0.001 megalitres", "val2": "1 kilolitre", "answer": "equal", "val1_ml": 1000000, "val2_ml": 1000000},
            {"val1": "12.345 litres", "val2": "12345 millilitres", "answer": "equal", "val1_ml": 12345, "val2_ml": 12345},
            {"val1": "0.0075 kilolitres", "val2": "7.5 litres", "answer": "equal", "val1_ml": 7500, "val2_ml": 7500},
            {"val1": "999 millilitres", "val2": "0.999 litres", "answer": "equal", "val1_ml": 999, "val2_ml": 999},
            {"val1": "45.67 litres", "val2": "45670 millilitres", "answer": "equal", "val1_ml": 45670, "val2_ml": 45670},
            {"val1": "8.008 kilolitres", "val2": "8008 litres", "answer": "equal", "val1_ml": 8008000, "val2_ml": 8008000},
            {"val1": "234.5 millilitres", "val2": "0.2345 litres", "answer": "equal", "val1_ml": 234.5, "val2_ml": 234.5},
            {"val1": "0.00123 kilolitres", "val2": "1.23 litres", "answer": "equal", "val1_ml": 1230, "val2_ml": 1230},
            {"val1": "5555 millilitres", "val2": "5.555 litres", "answer": "equal", "val1_ml": 5555, "val2_ml": 5555},
            
            # Some unequal ones at this level
            {"val1": "3.456 kilolitres", "val2": "3465 litres", "answer": "second", "val1_ml": 3456000, "val2_ml": 3465000},
            {"val1": "789.5 millilitres", "val2": "0.79 litres", "answer": "second", "val1_ml": 789.5, "val2_ml": 790},
            {"val1": "0.501 kilolitres", "val2": "500 litres", "answer": "first", "val1_ml": 501000, "val2_ml": 500000},
            {"val1": "12.34 litres", "val2": "12340 millilitres", "answer": "equal", "val1_ml": 12340, "val2_ml": 12340},
            {"val1": "0.5 megalitres", "val2": "500 kilolitres", "answer": "equal", "val1_ml": 500000000, "val2_ml": 500000000},
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
        "val1_ml": comparison["val1_ml"],
        "val2_ml": comparison["val2_ml"],
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
            old_difficulty = st.session_state.compare_volume_difficulty
            st.session_state.compare_volume_difficulty = min(
                st.session_state.compare_volume_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.compare_volume_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.compare_volume_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.compare_volume_difficulty
            st.session_state.compare_volume_difficulty = max(
                st.session_state.compare_volume_difficulty - 1, 1
            )
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.compare_volume_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.compare_volume_difficulty}. Keep practicing!**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the comparison"""
    
    data = st.session_state.question_data
    
    with st.expander("📖 **See the solution**", expanded=True):
        st.markdown("### Step-by-Step Comparison:")
        
        # Convert both values to millilitres for comparison
        val1_ml = data["val1_ml"]
        val2_ml = data["val2_ml"]
        
        st.markdown(f"**First value:** {data['val1']}")
        st.markdown(f"**Second value:** {data['val2']}")
        
        st.markdown("### Convert to the same unit (millilitres):")
        
        # Show conversion for first value
        val1_conversion = get_conversion_explanation(data['val1'], val1_ml)
        st.markdown(f"**{data['val1']}** = {val1_conversion}")
        
        # Show conversion for second value
        val2_conversion = get_conversion_explanation(data['val2'], val2_ml)
        st.markdown(f"**{data['val2']}** = {val2_conversion}")
        
        st.markdown("### Compare:")
        
        if val1_ml > val2_ml:
            st.markdown(f"**{val1_ml:,.1f} mL > {val2_ml:,.1f} mL**")
            st.markdown(f"Therefore, **{data['val1']} is more** than {data['val2']}")
            difference = val1_ml - val2_ml
            st.markdown(f"Difference: {difference:,.1f} mL")
            
            # Show difference in appropriate units
            if difference >= 1000:
                st.markdown(f"That's {difference/1000:.2f} litres difference")
        elif val2_ml > val1_ml:
            st.markdown(f"**{val2_ml:,.1f} mL > {val1_ml:,.1f} mL**")
            st.markdown(f"Therefore, **{data['val2']} is more** than {data['val1']}")
            difference = val2_ml - val1_ml
            st.markdown(f"Difference: {difference:,.1f} mL")
            
            # Show difference in appropriate units
            if difference >= 1000:
                st.markdown(f"That's {difference/1000:.2f} litres difference")
        else:
            st.markdown(f"**{val1_ml:,.1f} mL = {val2_ml:,.1f} mL**")
            st.markdown(f"Therefore, **they are equal**")
        
        # Quick conversion reminder
        st.markdown("""
        ### Remember:
        - 1 megalitre (ML) = 1,000 kL = 1,000,000 L
        - 1 kilolitre (kL) = 1,000 L = 1,000,000 mL
        - 1 litre (L) = 1,000 mL
        
        ### Real-World Examples:
        - A teaspoon ≈ 5 mL
        - A cup ≈ 250 mL
        - A water bottle ≈ 500 mL
        - A milk carton ≈ 1 L
        - A bathtub ≈ 200 L
        - A small pool ≈ 1 kL
        """)

def get_conversion_explanation(value_str, ml_value):
    """Get a detailed conversion explanation"""
    
    if "megalitre" in value_str:
        # Extract number
        num = float(value_str.split()[0])
        kl = num * 1000
        l = num * 1000000
        return f"{num} × 1,000,000 = **{ml_value:,.1f} mL**"
    elif "kilolitre" in value_str:
        num = float(value_str.split()[0])
        l = num * 1000
        return f"{num} × 1,000,000 = **{ml_value:,.1f} mL**"
    elif "litre" in value_str and "milli" not in value_str and "kilo" not in value_str and "mega" not in value_str:
        num = float(value_str.split()[0])
        return f"{num} × 1,000 = **{ml_value:,.1f} mL**"
    elif "millilitre" in value_str:
        return f"**{ml_value:,.1f} mL** (already in millilitres)"
    else:
        return f"**{ml_value:,.1f} mL**"

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None