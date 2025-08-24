import streamlit as st
import random
import streamlit.components.v1 as components

def run():
    """
    Main function to run the Compare Decimals to a Model practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_decimals_to_model.py
    """
    # Initialize session state for difficulty and game state
    if "compare_to_model_difficulty" not in st.session_state:
        st.session_state.compare_to_model_difficulty = 1  # Start with tenths
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_option = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📊 Compare Decimals to a Model")
    st.markdown("*Compare given decimals to the visual model*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.compare_to_model_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Tenths models",
            2: "Hundredths models", 
            3: "Mixed comparisons",
            4: "Close value comparisons",
            5: "Advanced decimal models"
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
        - **Look at the visual model** showing a decimal number
        - **Count the shaded parts** to determine the decimal value
        - **Choose which option** is greater or less than the model
        - **Click on the correct answer tile**
        
        ### Understanding the Models:
        - **Tenths models:** 10 columns, each column = 0.1
        - **Hundredths models:** 100 squares (10×10), each square = 0.01
        - **Shaded areas** show the decimal value in the model
        
        ### Reading the Question:
        - **"Which decimal is greater than..."** - Find a larger number
        - **"Which decimal is less than..."** - Find a smaller number
        - **Count carefully** to know the model's value first
        
        ### Examples:
        - **Model shows 0.3:** Choose 0.4 for "greater than"
        - **Model shows 0.52:** Choose 0.3 for "less than"
        - **Model shows 0.95:** Choose 0.972 for "greater than"
        
        ### Tips for Success:
        - **First count the model** - know what decimal it represents
        - **Compare each option** to the model value
        - **Think about place value** - 0.6 = 60 hundredths
        - **Check your answer** before submitting
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Simple tenths models
        - **🟡 Level 2:** Hundredths models
        - **🟠 Level 3:** Mixed model types
        - **🔴 Level 4:** Close value comparisons
        - **🔴 Level 5:** Advanced decimal challenges
        
        ### Scoring:
        - ✅ **Correct answer:** Move to next level
        - ❌ **Wrong answer:** Practice more at current level
        - 🎯 **Goal:** Master all comparison levels!
        """)

def generate_new_question():
    """Generate a new compare to model question based on difficulty level"""
    difficulty = st.session_state.compare_to_model_difficulty
    
    if difficulty == 1:
        # Simple tenths comparisons
        model_decimal = round(random.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]), 1)
        model_type = "tenths"
        comparison_type = random.choice(["greater", "less"])
        
        if comparison_type == "greater":
            # Generate options with one correct answer
            correct = round(model_decimal + random.choice([0.1, 0.2, 0.3]), 1)
            correct = min(correct, 0.9)  # Keep within range
            options = [correct]
            # Add wrong options that are less than or equal
            for _ in range(3):
                wrong = round(random.choice([model_decimal - 0.1, model_decimal - 0.2, model_decimal]), 1)
                wrong = max(wrong, 0.1)
                if wrong not in options:
                    options.append(wrong)
        else:  # less than
            correct = round(model_decimal - random.choice([0.1, 0.2, 0.3]), 1)
            correct = max(correct, 0.1)  # Keep within range
            options = [correct]
            # Add wrong options that are greater than or equal
            for _ in range(3):
                wrong = round(random.choice([model_decimal + 0.1, model_decimal + 0.2, model_decimal]), 1)
                wrong = min(wrong, 0.9)
                if wrong not in options:
                    options.append(wrong)
    
    elif difficulty == 2:
        # Hundredths comparisons
        model_decimal = round(random.randint(20, 80) / 100, 2)
        model_type = "hundredths"
        comparison_type = random.choice(["greater", "less"])
        
        if comparison_type == "greater":
            correct = round(model_decimal + random.randint(5, 20) / 100, 2)
            correct = min(correct, 0.99)
            options = [correct]
            # Add wrong options
            for _ in range(3):
                wrong = round(model_decimal - random.randint(1, 15) / 100, 2)
                wrong = max(wrong, 0.01)
                if wrong not in options:
                    options.append(wrong)
        else:  # less than
            correct = round(model_decimal - random.randint(5, 20) / 100, 2)
            correct = max(correct, 0.01)
            options = [correct]
            # Add wrong options
            for _ in range(3):
                wrong = round(model_decimal + random.randint(1, 15) / 100, 2)
                wrong = min(wrong, 0.99)
                if wrong not in options:
                    options.append(wrong)
    
    elif difficulty == 3:
        # Mixed comparisons
        model_type = random.choice(["tenths", "hundredths"])
        if model_type == "tenths":
            model_decimal = round(random.choice([0.3, 0.5, 0.6, 0.7, 0.8]), 1)
        else:
            model_decimal = round(random.randint(25, 75) / 100, 2)
        
        comparison_type = random.choice(["greater", "less"])
        
        if comparison_type == "greater":
            if model_type == "tenths":
                correct = round(model_decimal + random.choice([0.099, 0.15, 0.2]), 3)
            else:
                correct = round(model_decimal + random.randint(10, 25) / 100, 2)
            correct = min(correct, 0.99)
            options = [correct]
            
            for _ in range(3):
                if model_type == "tenths":
                    wrong = round(model_decimal - random.choice([0.05, 0.1, 0.15]), 2)
                else:
                    wrong = round(model_decimal - random.randint(5, 20) / 100, 2)
                wrong = max(wrong, 0.01)
                if wrong not in options:
                    options.append(wrong)
        else:
            if model_type == "tenths":
                correct = round(model_decimal - random.choice([0.099, 0.15, 0.2]), 3)
            else:
                correct = round(model_decimal - random.randint(10, 25) / 100, 2)
            correct = max(correct, 0.01)
            options = [correct]
            
            for _ in range(3):
                if model_type == "tenths":
                    wrong = round(model_decimal + random.choice([0.05, 0.1, 0.15]), 2)
                else:
                    wrong = round(model_decimal + random.randint(5, 20) / 100, 2)
                wrong = min(wrong, 0.99)
                if wrong not in options:
                    options.append(wrong)
    
    elif difficulty == 4:
        # Close value comparisons
        model_decimal = round(random.randint(30, 70) / 100, 2)
        model_type = "hundredths"
        comparison_type = random.choice(["greater", "less"])
        
        if comparison_type == "greater":
            correct = round(model_decimal + random.randint(1, 5) / 100, 2)
            options = [correct]
            for _ in range(3):
                wrong = round(model_decimal - random.randint(1, 3) / 100, 2)
                wrong = max(wrong, 0.01)
                if wrong not in options:
                    options.append(wrong)
        else:
            correct = round(model_decimal - random.randint(1, 5) / 100, 2)
            correct = max(correct, 0.01)
            options = [correct]
            for _ in range(3):
                wrong = round(model_decimal + random.randint(1, 3) / 100, 2)
                wrong = min(wrong, 0.99)
                if wrong not in options:
                    options.append(wrong)
    
    else:  # difficulty == 5
        # Advanced comparisons
        model_decimal = round(random.randint(15, 95) / 100, 2)
        model_type = random.choice(["tenths", "hundredths"])
        comparison_type = random.choice(["greater", "less"])
        
        # Create challenging options with 3 decimal places
        if comparison_type == "greater":
            correct = round(model_decimal + random.randint(1, 10) / 1000, 3)
            options = [correct]
            for _ in range(3):
                wrong = round(model_decimal - random.randint(1, 5) / 1000, 3)
                wrong = max(wrong, 0.001)
                if wrong not in options:
                    options.append(wrong)
        else:
            correct = round(model_decimal - random.randint(1, 10) / 1000, 3)
            correct = max(correct, 0.001)
            options = [correct]
            for _ in range(3):
                wrong = round(model_decimal + random.randint(1, 5) / 1000, 3)
                wrong = min(wrong, 0.999)
                if wrong not in options:
                    options.append(wrong)
    
    # Ensure we have exactly 4 options
    while len(options) < 4:
        if comparison_type == "greater":
            additional = round(model_decimal - random.randint(1, 10) / 100, 2)
            additional = max(additional, 0.01)
        else:
            additional = round(model_decimal + random.randint(1, 10) / 100, 2)
            additional = min(additional, 0.99)
        
        if additional not in options:
            options.append(additional)
    
    # Shuffle options
    random.shuffle(options)
    
    # Store question data
    st.session_state.question_data = {
        "model_decimal": model_decimal,
        "model_type": model_type,
        "comparison_type": comparison_type,
        "options": options[:4]  # Ensure exactly 4 options
    }
    st.session_state.correct_answer = correct
    st.session_state.current_question = f"Which decimal is {comparison_type} than the one shown in this diagram?"

def create_decimal_model_svg(decimal_value, model_type):
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
        
        # Choose a color
        colors = ["#4ade80", "#60a5fa", "#a78bfa", "#f472b6"]  # green, blue, purple, pink
        fill_color = random.choice(colors)
        
        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        
        # Draw grid cells
        for col in range(cols):
            x = col * cell_width
            y = 0
            
            # Determine if this cell should be shaded
            is_shaded = col < shaded_cells
            color = fill_color if is_shaded else "white"
            
            svg += f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="{color}" stroke="#333" stroke-width="1"/>'
        
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
        
        # Choose a color
        colors = ["#4ade80", "#60a5fa", "#a78bfa", "#f472b6"]  # green, blue, purple, pink
        fill_color = random.choice(colors)
        
        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        
        # Draw grid cells
        for row in range(rows):
            for col in range(cols):
                x = col * cell_width
                y = row * cell_height
                
                # Calculate cell number (row-major order)
                cell_num = row * cols + col
                
                # Determine if this cell should be shaded
                is_shaded = cell_num < shaded_cells
                color = fill_color if is_shaded else "white"
                
                svg += f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="{color}" stroke="#333" stroke-width="0.5"/>'
        
        svg += '</svg>'
    
    return svg

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
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
    
    # Create and display the visual model
    model_decimal = data["model_decimal"]
    model_type = data["model_type"]
    
    model_svg = create_decimal_model_svg(model_decimal, model_type)
    
    # Use HTML component for proper SVG rendering
    html_content = f"""
    <div style="text-align: center; margin: 30px 0; background-color: white; padding: 20px;">
        {model_svg}
    </div>
    """
    
    components.html(html_content, height=200)
    
    # Display clickable answer options
    display_answer_options()

def display_answer_options():
    """Display clickable answer option tiles"""
    data = st.session_state.question_data
    options = data["options"]
    
    # Create a 2x2 grid of clickable tiles
    col1, col2 = st.columns(2)
    
    with col1:
        # First option
        if st.button(f"{options[0]}", key="option_0", use_container_width=True, 
                    disabled=st.session_state.answer_submitted):
            st.session_state.selected_option = options[0]
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
        
        # Third option
        if len(options) > 2:
            if st.button(f"{options[2]}", key="option_2", use_container_width=True,
                        disabled=st.session_state.answer_submitted):
                st.session_state.selected_option = options[2]
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
    
    with col2:
        # Second option
        if len(options) > 1:
            if st.button(f"{options[1]}", key="option_1", use_container_width=True,
                        disabled=st.session_state.answer_submitted):
                st.session_state.selected_option = options[1]
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
        
        # Fourth option
        if len(options) > 3:
            if st.button(f"{options[3]}", key="option_3", use_container_width=True,
                        disabled=st.session_state.answer_submitted):
                st.session_state.selected_option = options[3]
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
    
    # Show selected answer
    if st.session_state.selected_option:
        st.markdown(f"**Your answer:** {st.session_state.selected_option}")
    
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
    user_answer = st.session_state.selected_option
    correct_answer = st.session_state.correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max level 5)
        old_difficulty = st.session_state.compare_to_model_difficulty
        st.session_state.compare_to_model_difficulty = min(
            st.session_state.compare_to_model_difficulty + 1, 5
        )
        
        # Show encouragement based on difficulty
        if st.session_state.compare_to_model_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered decimal model comparisons!**")
        elif old_difficulty < st.session_state.compare_to_model_difficulty:
            difficulty_names = {
                2: "hundredths models",
                3: "mixed model comparisons", 
                4: "close value comparisons",
                5: "advanced decimal models"
            }
            next_level = difficulty_names.get(st.session_state.compare_to_model_difficulty, "next level")
            st.info(f"⬆️ **Level up! Now practicing {next_level}**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    model_decimal = data["model_decimal"]
    comparison_type = data["comparison_type"]
    correct_answer = st.session_state.correct_answer
    model_type = data["model_type"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### Step-by-step solution:
        
        **Model shows:** {model_decimal}
        **Looking for:** A decimal {comparison_type} than {model_decimal}
        **Correct answer:** {correct_answer}
        
        ### Understanding the model:
        """)
        
        if model_type == "tenths":
            shaded_parts = int(model_decimal * 10)
            st.markdown(f"""
            - **Model type:** Tenths (10 columns)
            - **Shaded columns:** {shaded_parts} out of 10
            - **Decimal value:** {model_decimal}
            """)
        else:  # hundredths
            shaded_parts = int(model_decimal * 100)
            st.markdown(f"""
            - **Model type:** Hundredths (100 squares)
            - **Shaded squares:** {shaded_parts} out of 100
            - **Decimal value:** {model_decimal}
            """)
        
        # Comparison explanation
        if comparison_type == "greater":
            st.markdown(f"""
            ### Why {correct_answer} is correct:
            - **{correct_answer} > {model_decimal}** ✅
            - **{correct_answer}** is larger than the model's value
            """)
        else:  # less than
            st.markdown(f"""
            ### Why {correct_answer} is correct:
            - **{correct_answer} < {model_decimal}** ✅  
            - **{correct_answer}** is smaller than the model's value
            """)
        
        st.markdown("""
        ### 💡 Tips for next time:
        - **First, count the shaded parts** to know the model's value
        - **Then compare each option** to that value
        - **Think carefully** about greater than (>) vs less than (<)
        - **Double-check** your answer before clicking!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_option = None