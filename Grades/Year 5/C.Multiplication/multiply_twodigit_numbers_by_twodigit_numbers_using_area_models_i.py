import streamlit as st
import random

def run():
    """
    Main function to run the Area Models: Two-Digit × Two-Digit I practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/multiply_two_digit_area_models_I.py
    """
    # Initialize session state for difficulty and game state
    if "area_models_difficulty" not in st.session_state:
        st.session_state.area_models_difficulty = 1  # Start with basic models
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.area_models_score = 0
        st.session_state.total_questions = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("📐 Area Models: Two-Digit × Two-Digit I")
    st.markdown("*Use area models to understand multiplication*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.area_models_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Basic Models", 2: "Intermediate", 3: "Advanced"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Basic Models')}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
        
        # Show score
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.area_models_score / st.session_state.total_questions) * 100
            st.markdown(f"**Score:** {accuracy:.0f}%")
    
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
    with st.expander("💡 **Instructions & Area Model Guide**", expanded=False):
        st.markdown("""
        ### How Area Models Work:
        
        #### 🔹 **Breaking Down Numbers**
        - Split each two-digit number into **tens** and **ones**
        - Example: 33 = 30 + 3, and 18 = 10 + 8
        
        #### 🔹 **Creating the Model**
        - Draw a rectangle divided into **4 parts**
        - Each part represents one multiplication:
          - **Top-left:** tens × tens (30 × 10 = 300)
          - **Top-right:** tens × ones (30 × 8 = 240)
          - **Bottom-left:** ones × tens (3 × 10 = 30)
          - **Bottom-right:** ones × ones (3 × 8 = 24)
        
        #### 🔹 **Finding the Answer**
        - Add all four parts together
        - 300 + 240 + 30 + 24 = **594**
        
        ### 📊 **Example: 33 × 18**
        ```
        Split: 33 = 30 + 3, 18 = 10 + 8
        
        Area Model:
        ┌─────────┬─────────┐
        │ 30 × 10 │ 30 × 8  │
        │   300   │   240   │
        ├─────────┼─────────┤
        │ 3 × 10  │ 3 × 8   │
        │   30    │   24    │
        └─────────┴─────────┘
        
        Total: 300 + 240 + 30 + 24 = 594
        ```
        
        ### 🎯 **Question Types:**
        - **Model Recognition:** Which model represents the multiplication?
        - **Calculate Total:** Use the given areas to find the answer
        
        ### 💡 **Tips for Success:**
        - **Check the dimensions:** Do the sides match the original numbers?
        - **Verify partial products:** Are the areas calculated correctly?
        - **Add carefully:** Sum all four rectangular areas
        - **Think logically:** Does your answer make sense?
        
        ### 🏆 **Why Area Models Help:**
        - **Visual understanding** of multiplication
        - **Breaks down complex** problems into simpler parts
        - **Shows the connection** between multiplication and area
        - **Builds foundation** for algebraic thinking
        """)

def generate_new_question():
    """Generate a new area model question"""
    difficulty = st.session_state.area_models_difficulty
    
    # Choose question type (50/50 split)
    question_type = random.choice(["identify_model", "calculate_total"])
    
    # Generate appropriate numbers based on difficulty
    if difficulty == 1:
        # Basic: smaller numbers, easier calculations
        tens_options = [20, 30, 40, 50]
        ones_options = [2, 3, 4, 5, 6, 7, 8, 9]
    elif difficulty == 2:
        # Intermediate: medium numbers
        tens_options = [20, 30, 40, 50, 60, 70]
        ones_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:  # difficulty == 3
        # Advanced: larger numbers
        tens_options = [20, 30, 40, 50, 60, 70, 80, 90]
        ones_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Generate the two numbers to multiply
    first_tens = random.choice(tens_options)
    first_ones = random.choice(ones_options)
    first_number = first_tens + first_ones
    
    second_tens = random.choice([10, 20, 30, 40, 50])
    second_ones = random.choice(ones_options)
    second_number = second_tens + second_ones
    
    # Calculate all the parts
    tl_product = first_tens * second_tens  # top-left
    tr_product = first_tens * second_ones  # top-right
    bl_product = first_ones * second_tens  # bottom-left
    br_product = first_ones * second_ones  # bottom-right
    
    total_product = tl_product + tr_product + bl_product + br_product
    
    if question_type == "identify_model":
        # TYPE 1: Which model represents the multiplication?
        
        # Create correct model breakdown
        correct_model = {
            "first_tens": first_tens,
            "first_ones": first_ones,
            "second_tens": second_tens,
            "second_ones": second_ones,
            "tl": tl_product,
            "tr": tr_product,
            "bl": bl_product,
            "br": br_product
        }
        
        # Create incorrect model (swap some dimensions)
        if random.choice([True, False]):
            # Swap the breakdown of first number
            wrong_model = {
                "first_tens": first_ones * 10,  # Wrong breakdown
                "first_ones": first_tens // 10,
                "second_tens": second_tens,
                "second_ones": second_ones,
                "tl": (first_ones * 10) * second_tens,
                "tr": (first_ones * 10) * second_ones,
                "bl": (first_tens // 10) * second_tens,
                "br": (first_tens // 10) * second_ones
            }
        else:
            # Swap the breakdown of second number
            wrong_model = {
                "first_tens": first_tens,
                "first_ones": first_ones,
                "second_tens": second_ones * 10,  # Wrong breakdown
                "second_ones": second_tens // 10,
                "tl": first_tens * (second_ones * 10),
                "tr": first_tens * (second_tens // 10),
                "bl": first_ones * (second_ones * 10),
                "br": first_ones * (second_tens // 10)
            }
        
        # Randomly order the models
        models = [correct_model, wrong_model]
        random.shuffle(models)
        correct_index = models.index(correct_model)
        
        st.session_state.question_data = {
            "type": "identify_model",
            "first_number": first_number,
            "second_number": second_number,
            "models": models,
            "correct_index": correct_index,
            "multiplication": f"{first_number} × {second_number}"
        }
        st.session_state.correct_answer = correct_index
        st.session_state.current_question = f"Which model represents {first_number} × {second_number}?"
        
    else:
        # TYPE 2: Calculate using the given model
        st.session_state.question_data = {
            "type": "calculate_total",
            "first_number": first_number,
            "second_number": second_number,
            "first_tens": first_tens,
            "first_ones": first_ones,
            "second_tens": second_tens,
            "second_ones": second_ones,
            "tl_product": tl_product,
            "tr_product": tr_product,
            "bl_product": bl_product,
            "br_product": br_product,
            "total_product": total_product,
            "multiplication": f"{first_number} × {second_number}"
        }
        st.session_state.correct_answer = total_product
        st.session_state.current_question = f"What is {first_number} × {second_number}? Use the areas shown on the model to help."

def create_area_model_visual(model_data, show_products=False):
    """Create area model using pure Streamlit markdown with emoji blocks"""
    
    first_tens = model_data["first_tens"]
    first_ones = model_data["first_ones"]
    second_tens = model_data["second_tens"] 
    second_ones = model_data["second_ones"]
    tl = model_data["tl"]
    tr = model_data["tr"]
    bl = model_data["bl"]
    br = model_data["br"]
    
    # Display the breakdown first
    st.markdown(f"**Breaking down the numbers:**")
    st.markdown(f"- First number: {first_tens + first_ones} = {first_tens} + {first_ones}")
    st.markdown(f"- Second number: {second_tens + second_ones} = {second_tens} + {second_ones}")
    
    st.markdown("")
    st.markdown("**Area Model:**")
    
    # Create visual representation using text and containers
    
    # Header row with dimensions
    col_empty, col_tens, col_ones = st.columns([1, 3, 2])
    with col_empty:
        st.markdown("")
    with col_tens:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;'>{second_tens}</div>", unsafe_allow_html=True)
    with col_ones:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;'>{second_ones}</div>", unsafe_allow_html=True)
    
    # First row
    col_left, col_tl, col_tr = st.columns([1, 3, 2])
    with col_left:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; background-color: #f0f0f0; padding: 20px 5px; border: 1px solid #ccc;'>{first_tens}</div>", unsafe_allow_html=True)
    with col_tl:
        content = str(tl) if show_products else ""
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; background-color: #FFE082; padding: 30px 10px; border: 2px solid #333; min-height: 60px; display: flex; align-items: center; justify-content: center;'>{content}</div>", unsafe_allow_html=True)
    with col_tr:
        content = str(tr) if show_products else ""
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; background-color: #81C784; padding: 30px 10px; border: 2px solid #333; min-height: 60px; display: flex; align-items: center; justify-content: center;'>{content}</div>", unsafe_allow_html=True)
    
    # Second row
    col_left, col_bl, col_br = st.columns([1, 3, 2])
    with col_left:
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; background-color: #f0f0f0; padding: 15px 5px; border: 1px solid #ccc;'>{first_ones}</div>", unsafe_allow_html=True)
    with col_bl:
        content = str(bl) if show_products else ""
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; background-color: #FFAB91; padding: 20px 10px; border: 2px solid #333; min-height: 40px; display: flex; align-items: center; justify-content: center;'>{content}</div>", unsafe_allow_html=True)
    with col_br:
        content = str(br) if show_products else ""
        st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px; background-color: #F48FB1; padding: 20px 10px; border: 2px solid #333; min-height: 40px; display: flex; align-items: center; justify-content: center;'>{content}</div>", unsafe_allow_html=True)
    
    st.markdown("")
    
    if show_products:
        st.markdown(f"**Calculation:** {tl} + {tr} + {bl} + {br} = **{tl + tr + bl + br}**")

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 🤔 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    if data["type"] == "identify_model":
        # TYPE 1: Multiple choice between models
        
        st.markdown("### Choose the correct model:")
        
        # Display Model A
        st.markdown("**Model A**")
        with st.container():
            create_area_model_visual(data["models"][0], show_products=False)
        
        st.markdown("---")  # Visual separator
        
        # Display Model B  
        st.markdown("**Model B**")
        with st.container():
            create_area_model_visual(data["models"][1], show_products=False)
        
        # Answer selection
        with st.form("answer_form", clear_on_submit=False):
            user_answer = st.radio(
                "Which model correctly represents the multiplication?",
                options=["Model A", "Model B"],
                key="model_choice"
            )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button and user_answer:
                selected_index = 0 if user_answer == "Model A" else 1
                st.session_state.user_answer = selected_index
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.total_questions += 1
    
    else:
        # TYPE 2: Calculate using given model
        
        # Create model data for display
        model_data = {
            "first_tens": data["first_tens"],
            "first_ones": data["first_ones"],
            "second_tens": data["second_tens"],
            "second_ones": data["second_ones"],
            "tl": data["tl_product"],
            "tr": data["tr_product"],
            "bl": data["bl_product"],
            "br": data["br_product"]
        }
        
        # Display the model with products shown
        create_area_model_visual(model_data, show_products=True)
        
        # Answer input
        with st.form("answer_form", clear_on_submit=False):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown(f"**{data['multiplication']} =**")
                user_answer = st.number_input(
                    "Enter your answer:",
                    min_value=0,
                    max_value=10000,
                    value=None,
                    step=1,
                    key="calculation_input",
                    label_visibility="collapsed",
                    placeholder="Enter the total"
                )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button and user_answer is not None:
                st.session_state.user_answer = int(user_answer)
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.total_questions += 1
    
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
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.area_models_score += 1
        
        # Increase difficulty based on performance
        if st.session_state.total_questions % 4 == 0:  # Every 4 questions
            accuracy = st.session_state.area_models_score / st.session_state.total_questions
            if accuracy >= 0.75 and st.session_state.area_models_difficulty < 3:
                old_difficulty = st.session_state.area_models_difficulty
                st.session_state.area_models_difficulty += 1
                if old_difficulty < st.session_state.area_models_difficulty:
                    st.info(f"⬆️ **Level Up! Now at Level {st.session_state.area_models_difficulty}**")
                    if st.session_state.area_models_difficulty == 3:
                        st.balloons()
    
    else:
        if data["type"] == "identify_model":
            correct_model_name = "Model A" if correct_answer == 0 else "Model B"
            st.error(f"❌ **Not quite right.** The correct model was **{correct_model_name}**.")
        else:
            st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty if struggling
        if st.session_state.total_questions % 4 == 0:  # Every 4 questions
            accuracy = st.session_state.area_models_score / st.session_state.total_questions
            if accuracy < 0.4 and st.session_state.area_models_difficulty > 1:
                old_difficulty = st.session_state.area_models_difficulty
                st.session_state.area_models_difficulty = max(st.session_state.area_models_difficulty - 1, 1)
                if old_difficulty > st.session_state.area_models_difficulty:
                    st.warning(f"⬇️ **Let's practice simpler models. Back to Level {st.session_state.area_models_difficulty}**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the area model"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=True):
        if data["type"] == "identify_model":
            # Explanation for model identification
            first_num = data["first_number"]
            second_num = data["second_number"]
            correct_model = data["models"][data["correct_index"]]
            
            st.markdown(f"""
            ### Step-by-Step Model Analysis:
            
            **Multiplication:** {first_num} × {second_num}
            
            **Step 1: Break down the numbers**
            - {first_num} = {correct_model["first_tens"]} + {correct_model["first_ones"]}
            - {second_num} = {correct_model["second_tens"]} + {correct_model["second_ones"]}
            
            **Step 2: Check the model dimensions**
            - **Left side should be:** {correct_model["first_tens"]} (top) and {correct_model["first_ones"]} (bottom)
            - **Top side should be:** {correct_model["second_tens"]} (left) and {correct_model["second_ones"]} (right)
            
            **Step 3: Verify the rectangles represent:**
            - **Top-left:** {correct_model["first_tens"]} × {correct_model["second_tens"]} = {correct_model["tl"]}
            - **Top-right:** {correct_model["first_tens"]} × {correct_model["second_ones"]} = {correct_model["tr"]}
            - **Bottom-left:** {correct_model["first_ones"]} × {correct_model["second_tens"]} = {correct_model["bl"]}
            - **Bottom-right:** {correct_model["first_ones"]} × {correct_model["second_ones"]} = {correct_model["br"]}
            """)
            
        else:
            # Explanation for calculation
            first_num = data["first_number"]
            second_num = data["second_number"]
            
            st.markdown(f"""
            ### Step-by-Step Calculation:
            
            **Multiplication:** {first_num} × {second_num}
            
            **Step 1: Identify the partial products**
            - **Top-left:** {data["first_tens"]} × {data["second_tens"]} = {data["tl_product"]}
            - **Top-right:** {data["first_tens"]} × {data["second_ones"]} = {data["tr_product"]}
            - **Bottom-left:** {data["first_ones"]} × {data["second_tens"]} = {data["bl_product"]}
            - **Bottom-right:** {data["first_ones"]} × {data["second_ones"]} = {data["br_product"]}
            
            **Step 2: Add all the areas together**
            {data["tl_product"]} + {data["tr_product"]} + {data["bl_product"]} + {data["br_product"]} = **{data["total_product"]}**
            """)
        
        # General tips
        st.markdown(f"""
        ### 💡 **Area Model Tips:**
        - **Visual Check:** The model should clearly show how each number is split
        - **Dimension Labels:** Each side should be labeled with the correct values
        - **Partial Products:** Each rectangle represents a simple multiplication
        - **Final Sum:** Add all rectangles to get the total product
        
        ### 🎯 **Why This Works:**
        Area models show that multiplication is really about finding the area of a rectangle. When we have two-digit numbers, we split them into smaller, easier parts (tens and ones) and find the area of each part separately, then add them all together!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer