import streamlit as st
import random
import streamlit.components.v1 as components

def run():
    """
    Main function to run the Compare Decimals Using Models practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_decimals_models.py
    """
    # Initialize session state for difficulty and game state
    if "compare_models_difficulty" not in st.session_state:
        st.session_state.compare_models_difficulty = 1  # Start with tenths
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_comparison = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📊 Compare Decimals Using Models")
    st.markdown("*Use visual models to compare decimal numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.compare_models_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Tenths (0.1 to 0.9)",
            2: "Hundredths (0.01 to 0.99)", 
            3: "Mixed tenths & hundredths",
            4: "Advanced comparisons",
            5: "Complex decimal models"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 5 levels)
        progress = (difficulty_level - 1) / 4  # Convert 1-5 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
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
        - **Look at both visual models** showing decimal numbers
        - **Count the shaded parts** in each model
        - **Choose the correct comparison sign** (>, <, or =)
        
        ### Understanding the Models:
        - **Tenths models:** 10 columns, each column = 0.1
        - **Hundredths models:** 100 squares (10×10), each square = 0.01
        - **Pink/shaded areas** show the decimal value
        
        ### Comparison Signs:
        - **>** means "greater than" (left number is bigger)
        - **<** means "less than" (left number is smaller)  
        - **=** means "equal to" (both numbers are the same)
        
        ### Examples:
        - **0.2 vs 0.1:** 2 tenths > 1 tenth, so 0.2 > 0.1
        - **0.88 vs 0.34:** 88 hundredths > 34 hundredths, so 0.88 > 0.34
        - **0.5 vs 0.50:** Same value, so 0.5 = 0.50
        
        ### Tips for Success:
        - **Count carefully** - each shaded part has a specific value
        - **More shaded = larger number**
        - **Use the models** - they make comparison easier than just numbers
        - **Think about place value** - 0.8 = 8 tenths = 80 hundredths
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple tenths (0.1, 0.2, 0.3...)
        - **🟡 Level 2:** Hundredths (0.01, 0.02... 0.99)
        - **🟠 Level 3:** Mix tenths and hundredths
        - **🔴 Level 4:** Trickier comparisons
        - **🔴 Level 5:** Complex decimal models
        
        ### Scoring:
        - ✅ **Correct answer:** Move to next level
        - ❌ **Wrong answer:** Practice more at current level
        - 🎯 **Goal:** Master all comparison levels!
        """)

def generate_new_question():
    """Generate a new decimal comparison question based on difficulty level"""
    difficulty = st.session_state.compare_models_difficulty
    
    if difficulty == 1:
        # Simple tenths comparisons
        decimals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        decimal1 = random.choice(decimals)
        decimal2 = random.choice([d for d in decimals if d != decimal1])
        model_type = "tenths"
        
    elif difficulty == 2:
        # Hundredths comparisons
        decimal1 = round(random.randint(1, 99) / 100, 2)
        decimal2 = round(random.randint(1, 99) / 100, 2)
        # Ensure they're different
        while decimal1 == decimal2:
            decimal2 = round(random.randint(1, 99) / 100, 2)
        model_type = "hundredths"
        
    elif difficulty == 3:
        # Mix tenths and hundredths
        if random.choice([True, False]):
            # One tenth, one hundredth
            decimal1 = round(random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]), 1)
            decimal2 = round(random.randint(1, 99) / 100, 2)
        else:
            # Both hundredths but one equivalent to tenths
            decimal1 = round(random.choice([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]), 2)
            decimal2 = round(random.randint(1, 99) / 100, 2)
        model_type = "hundredths"
        
    elif difficulty == 4:
        # Advanced comparisons with close values
        base = random.randint(10, 90)
        decimal1 = round(base / 100, 2)
        decimal2 = round((base + random.choice([-5, -3, -2, -1, 1, 2, 3, 5])) / 100, 2)
        decimal2 = max(0.01, min(0.99, decimal2))  # Keep in valid range
        model_type = "hundredths"
        
    else:  # difficulty == 5
        # Complex comparisons including equivalent decimals
        if random.random() < 0.3:  # 30% chance of equal decimals
            decimal1 = round(random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]), 1)
            decimal2 = round(decimal1, 2)  # Same value, different representation
        else:
            decimal1 = round(random.randint(1, 99) / 100, 2)
            decimal2 = round(random.randint(1, 99) / 100, 2)
        model_type = "hundredths"
    
    # Determine correct comparison
    if decimal1 > decimal2:
        correct_answer = ">"
    elif decimal1 < decimal2:
        correct_answer = "<"
    else:
        correct_answer = "="
    
    # Store question data
    st.session_state.question_data = {
        "decimal1": decimal1,
        "decimal2": decimal2,
        "model_type": model_type
    }
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = f"Compare {decimal1} and {decimal2}. Use the models to help."

def create_decimal_model_svg(decimal_value, model_type, side="left"):
    """Create an SVG visual model for a decimal"""
    
    if model_type == "tenths":
        # Create a 1x10 grid for tenths
        width = 200
        height = 80
        cols = 10
        rows = 1
        cell_width = width / cols
        cell_height = height / rows
        
        # Calculate how many cells to shade
        shaded_cells = int(decimal_value * 10)
        
        svg = f'<svg width="{width}" height="{height + 40}" viewBox="0 0 {width} {height + 40}">'
        
        # Draw grid cells
        for col in range(cols):
            x = col * cell_width
            y = 10
            
            # Determine if this cell should be shaded
            is_shaded = col < shaded_cells
            fill_color = "#ff69b4" if is_shaded else "white"
            
            svg += f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="{fill_color}" stroke="#333" stroke-width="1"/>'
        
        # Add label
        svg += f'<text x="{width/2}" y="{height + 30}" text-anchor="middle" font-size="16" font-weight="bold">{decimal_value}</text>'
        svg += '</svg>'
        
    else:  # hundredths
        # Create a 10x10 grid for hundredths
        width = 150
        height = 150
        cols = 10
        rows = 10
        cell_width = width / cols
        cell_height = height / rows
        
        # Calculate how many cells to shade
        shaded_cells = int(decimal_value * 100)
        
        svg = f'<svg width="{width}" height="{height + 40}" viewBox="0 0 {width} {height + 40}">'
        
        # Draw grid cells
        for row in range(rows):
            for col in range(cols):
                x = col * cell_width
                y = row * cell_height + 10
                
                # Calculate cell number (row-major order)
                cell_num = row * cols + col
                
                # Determine if this cell should be shaded
                is_shaded = cell_num < shaded_cells
                fill_color = "#ff69b4" if is_shaded else "white"
                
                svg += f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="{fill_color}" stroke="#333" stroke-width="0.5"/>'
        
        # Add label
        svg += f'<text x="{width/2}" y="{height + 30}" text-anchor="middle" font-size="16" font-weight="bold">{decimal_value}</text>'
        svg += '</svg>'
    
    return svg

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📊 Question:")
    
    # Display the question text
    question_text = st.session_state.current_question
    
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #007acc;
        font-size: 18px;
        margin: 20px 0;
        color: #333;
    ">
        {question_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Create the visual models
    decimal1 = data["decimal1"]
    decimal2 = data["decimal2"]
    model_type = data["model_type"]
    
    # Display both models side by side
    model1_svg = create_decimal_model_svg(decimal1, model_type, "left")
    model2_svg = create_decimal_model_svg(decimal2, model_type, "right")
    
    # Use HTML component for proper SVG rendering
    html_content = f"""
    <div style="display: flex; justify-content: space-around; align-items: center; margin: 30px 0; background-color: white; padding: 20px;">
        <div style="text-align: center;">
            {model1_svg}
        </div>
        <div style="text-align: center;">
            {model2_svg}
        </div>
    </div>
    """
    
    components.html(html_content, height=250)
    
    # Comparison question
    st.markdown("### Which sign makes the statement true?")
    
    # Display the comparison with question mark
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0;">
            {decimal1} ? {decimal2}
        </div>
        """, unsafe_allow_html=True)
    
    # Comparison buttons with clear labels
    st.markdown("**Choose the correct comparison:**")
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col2:
        if st.button("Greater\n(>)", key="greater_btn", use_container_width=True):
            st.session_state.selected_comparison = ">"
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    with col3:
        if st.button("Less\n(<)", key="less_btn", use_container_width=True):
            st.session_state.selected_comparison = "<"
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    with col4:
        if st.button("Equal\n(=)", key="equal_btn", use_container_width=True):
            st.session_state.selected_comparison = "="
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show selected answer
    if st.session_state.selected_comparison:
        st.markdown(f"**Your answer:** {decimal1} {st.session_state.selected_comparison} {decimal2}")
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.selected_comparison
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 5)
        old_difficulty = st.session_state.compare_models_difficulty
        st.session_state.compare_models_difficulty = min(
            st.session_state.compare_models_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.compare_models_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal comparison with models!**")
        elif old_difficulty < st.session_state.compare_models_difficulty:
            difficulty_names = {
                2: "hundredths models",
                3: "mixed tenths & hundredths", 
                4: "advanced comparisons",
                5: "complex decimal models"
            }
            next_level = difficulty_names.get(st.session_state.compare_models_difficulty, "next level")
            st.info(f"⬆️ **Level up! Now practicing {next_level}**")
    
    else:
        decimal1 = st.session_state.question_data["decimal1"]
        decimal2 = st.session_state.question_data["decimal2"]
        st.error(f"❌ **Not quite right.** The correct answer is **{decimal1} {correct_answer} {decimal2}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    decimal1 = data["decimal1"]
    decimal2 = data["decimal2"]
    correct_answer = st.session_state.correct_answer
    model_type = data["model_type"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step comparison:
        
        **Comparing:** {decimal1} {correct_answer} {decimal2}
        
        ### Using the models:
        """)
        
        if model_type == "tenths":
            shaded1 = int(decimal1 * 10)
            shaded2 = int(decimal2 * 10)
            st.markdown(f"""
            - **{decimal1}** has {shaded1} shaded columns (out of 10)
            - **{decimal2}** has {shaded2} shaded columns (out of 10)
            - **{shaded1} {">" if shaded1 > shaded2 else "<" if shaded1 < shaded2 else "="} {shaded2}**, so **{decimal1} {correct_answer} {decimal2}**
            """)
        else:  # hundredths
            shaded1 = int(decimal1 * 100)
            shaded2 = int(decimal2 * 100)
            st.markdown(f"""
            - **{decimal1}** has {shaded1} shaded squares (out of 100)
            - **{decimal2}** has {shaded2} shaded squares (out of 100)
            - **{shaded1} {">" if shaded1 > shaded2 else "<" if shaded1 < shaded2 else "="} {shaded2}**, so **{decimal1} {correct_answer} {decimal2}**
            """)
        
        # General explanation
        if correct_answer == ">":
            st.markdown("💡 **Remember:** More shaded parts means a larger decimal number!")
        elif correct_answer == "<":
            st.markdown("💡 **Remember:** Fewer shaded parts means a smaller decimal number!")
        else:
            st.markdown("💡 **Remember:** Same amount shaded means equal decimal values!")
        
        st.markdown("""
        ### 💡 Tips for comparing decimals:
        - **Count the shaded parts** in each model
        - **More shaded = larger number**
        - **Use place value:** 0.8 = 8 tenths = 80 hundredths
        - **Visual models** make comparison easier than just numbers!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_comparison = None