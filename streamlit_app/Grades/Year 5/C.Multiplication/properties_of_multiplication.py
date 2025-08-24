import streamlit as st
import random

def run():
    """
    Main function to run the Properties of Multiplication practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/C. Multiplication/properties_of_multiplication.py
    """
    # Initialize session state for difficulty and game state
    if "properties_difficulty" not in st.session_state:
        st.session_state.properties_difficulty = 1  # Start with basic properties
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.properties_score = 0
        st.session_state.total_questions = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > C. Multiplication**")
    st.title("🔢 Properties of Multiplication")
    st.markdown("*Identify and understand multiplication properties*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.properties_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        level_names = {1: "Basic Properties", 2: "Mixed Properties", 3: "Advanced Applications"}
        st.markdown(f"**Current Level:** {level_names.get(difficulty_level, 'Basic Properties')}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Mixed**")
        else:
            st.markdown("**🔴 Advanced**")
        
        # Show score
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.properties_score / st.session_state.total_questions) * 100
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
    with st.expander("💡 **Instructions & Properties Guide**", expanded=False):
        st.markdown("""
        ### Multiplication Properties:
        
        #### 🔹 **Identity Property**
        - Any number multiplied by 1 equals itself
        - **Examples:** 7 × 1 = 7, 1 × 15 = 15
        
        #### 🔹 **Zero Property**
        - Any number multiplied by 0 equals 0
        - **Examples:** 8 × 0 = 0, 0 × 25 = 0
        
        #### 🔹 **Commutative Property**
        - Order doesn't matter in multiplication
        - **Examples:** 4 × 5 = 5 × 4, 3 × 7 = 7 × 3
        
        #### 🔹 **Associative Property**
        - Grouping doesn't matter in multiplication
        - **Examples:** (2 × 3) × 4 = 2 × (3 × 4), (5 × 2) × 6 = 5 × (2 × 6)
        
        #### 🔹 **Distributive Property**
        - Multiply a sum/difference by distributing
        - **Examples:** 3 × (4 + 5) = 3 × 4 + 3 × 5, 6 × (8 - 2) = 6 × 8 - 6 × 2
        
        ### How to Play:
        - **Read the equation or expression carefully**
        - **Identify which property is being demonstrated**
        - **Select the correct property from the options**
        
        ### Tips for Success:
        - **Look for patterns:** Does the order change? Are numbers grouped differently?
        - **Check for 1s and 0s:** These often indicate identity or zero properties
        - **Look for parentheses:** These might show associative or distributive properties
        
        ### Difficulty Levels:
        - **🟢 Basic:** Simple examples of each property
        - **🟡 Mixed:** Multiple properties to choose from
        - **🔴 Advanced:** Complex expressions and applications
        """)

def generate_new_question():
    """Generate a new properties of multiplication question"""
    difficulty = st.session_state.properties_difficulty
    
    # Randomly choose question format (50/50 chance)
    question_format = random.choice(["identify_property", "find_equation"])
    
    # Generate equations for each property
    property_equations = {
        "identity": [
            "8 = 8 × 1",
            "1 × 15 = 15", 
            "12 × 1 = 12",
            "1 × 7 = 7",
            "25 × 1 = 25"
        ],
        "zero": [
            "7 × 0 = 0",
            "0 × 12 = 0",
            "9 × 0 = 0", 
            "0 × 15 = 0",
            "11 × 0 = 0"
        ],
        "commutative": [
            "5 × 3 = 3 × 5",
            "9 × 4 = 4 × 9",
            "8 × 7 = 7 × 8",
            "6 × 2 = 2 × 6", 
            "11 × 3 = 3 × 11"
        ],
        "associative": [
            "7 × (2 × 5) = (7 × 2) × 5",
            "2 × (3 × 4) = (2 × 3) × 4",
            "(6 × 2) × 5 = 6 × (2 × 5)",
            "4 × (5 × 3) = (4 × 5) × 3",
            "(8 × 2) × 3 = 8 × (2 × 3)"
        ],
        "distributive": [
            "3 × (4 + 5) = 3 × 4 + 3 × 5",
            "6 × (7 - 2) = 6 × 7 - 6 × 2", 
            "4 × (2 + 3) = 4 × 2 + 4 × 3",
            "5 × (8 - 1) = 5 × 8 - 5 × 1",
            "2 × (6 + 4) = 2 × 6 + 2 × 4"
        ]
    }
    
    # Add some special cases for higher difficulty
    if difficulty >= 2:
        property_equations["distributive"].extend([
            "7 × (3 + 8 + 1) = 7 × 3 + 7 × 8 + 7 × 1",
            "(8 - 3) × 6 = 8 × 6 - 3 × 6"
        ])
        property_equations["associative"].extend([
            "(9 × 3) × 2 = 9 × (3 × 2)"
        ])
    
    properties = ["identity", "zero", "commutative", "associative", "distributive"]
    explanations = {
        "identity": "The identity property states that any number multiplied by 1 equals itself.",
        "zero": "The zero property states that any number multiplied by 0 equals 0.",
        "commutative": "The commutative property shows that order doesn't matter in multiplication (a × b = b × a).",
        "associative": "The associative property shows that grouping doesn't matter in multiplication ((a × b) × c = a × (b × c)).",
        "distributive": "The distributive property shows that multiplication distributes over addition and subtraction (a × (b + c) = a × b + a × c)."
    }
    
    if question_format == "identify_property":
        # FORMAT 1: Show one equation → "Which property is this?"
        target_property = random.choice(properties)
        equation = random.choice(property_equations[target_property])
        
        # Create property options (shuffle them)
        property_options = ["Identity", "Zero", "Commutative", "Associative", "Distributive"]
        random.shuffle(property_options)
        
        st.session_state.question_data = {
            "format": "identify_property",
            "equation": equation,
            "target_property": target_property,
            "correct_answer": target_property.title(),
            "options": property_options,
            "explanation": explanations[target_property]
        }
        st.session_state.correct_answer = target_property.title()
        st.session_state.current_question = "Which property of multiplication is shown?"
        
    else:
        # FORMAT 2: "Which equation shows the [property] property?" → Show 4 equations
        target_property = random.choice(properties)
        
        # Special equations that might confuse students (repeated addition)
        other_equations = [
            "5 × 7 = 5 + 5 + 5 + 5 + 5 + 5 + 5",
            "4 × 6 = 4 + 4 + 4 + 4 + 4 + 4",
            "3 × 8 = 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3"
        ]
        
        correct_equation = random.choice(property_equations[target_property])
        
        # Generate 3 distractor equations from other properties
        distractors = []
        other_properties = [p for p in properties if p != target_property]
        
        # Pick equations from other properties
        for prop in random.sample(other_properties, min(3, len(other_properties))):
            distractors.append(random.choice(property_equations[prop]))
        
        # If we need more distractors, add some repeated addition examples
        while len(distractors) < 3:
            distractors.append(random.choice(other_equations))
        
        # Take only 3 distractors
        distractors = distractors[:3]
        
        # Create options list and shuffle
        options = [correct_equation] + distractors
        random.shuffle(options)
        
        st.session_state.question_data = {
            "format": "find_equation",
            "target_property": target_property,
            "options": options,
            "correct_answer": correct_equation,
            "explanation": explanations[target_property]
        }
        st.session_state.correct_answer = correct_equation
        st.session_state.current_question = f"Which equation shows the {target_property} property of multiplication?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 🤔 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Check question format
    if data["format"] == "identify_property":
        # FORMAT 1: Show equation → "Which property is this?"
        
        # Display the equation in a highlighted box
        st.markdown(f"""
        <div style="
            background-color: #f0f8ff; 
            padding: 30px; 
            border-radius: 15px; 
            border-left: 5px solid #4CAF50;
            font-size: 24px;
            text-align: center;
            margin: 30px 0;
            font-weight: bold;
            color: #2c3e50;
            font-family: 'Courier New', monospace;
        ">
            {data['equation']}
        </div>
        """, unsafe_allow_html=True)
        
        # Answer selection for properties
        with st.form("answer_form", clear_on_submit=False):
            st.markdown("**Choose the correct property:**")
            
            user_answer = st.radio(
                "Select your answer:",
                options=data['options'],
                key="property_choice",
                label_visibility="collapsed"
            )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button and user_answer:
                st.session_state.user_answer = user_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.session_state.total_questions += 1
    
    else:
        # FORMAT 2: "Which equation shows the [property] property?" → Show equations
        
        # Answer selection for equations
        with st.form("answer_form", clear_on_submit=False):
            st.markdown("**Choose the correct equation:**")
            
            # Display each equation option in a nice format
            user_answer = st.radio(
                "Select your answer:",
                options=data['options'],
                key="equation_choice",
                label_visibility="collapsed",
                format_func=lambda x: f"   {x}"  # Add some indentation for better formatting
            )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button and user_answer:
                st.session_state.user_answer = user_answer
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
        st.session_state.properties_score += 1
        
        # Increase difficulty based on performance
        if st.session_state.total_questions % 3 == 0:  # Every 3 questions
            accuracy = st.session_state.properties_score / st.session_state.total_questions
            if accuracy >= 0.8 and st.session_state.properties_difficulty < 3:
                old_difficulty = st.session_state.properties_difficulty
                st.session_state.properties_difficulty += 1
                if old_difficulty < st.session_state.properties_difficulty:
                    st.info(f"⬆️ **Level Up! Now at Level {st.session_state.properties_difficulty}**")
                    if st.session_state.properties_difficulty == 3:
                        st.balloons()
    
    else:
        if data["format"] == "identify_property":
            # FORMAT 1: Show property name as correct answer
            st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer} Property**.")
        else:
            # FORMAT 2: Show equation as correct answer
            st.error(f"❌ **Not quite right.** The correct answer was:")
            st.markdown(f"""
            <div style="
                background-color: #ffe6e6; 
                padding: 20px; 
                border-radius: 10px; 
                border-left: 5px solid #ff4444;
                font-size: 18px;
                text-align: center;
                margin: 20px 0;
                font-weight: bold;
                color: #cc0000;
                font-family: 'Courier New', monospace;
            ">
                {correct_answer}
            </div>
            """, unsafe_allow_html=True)
        
        # Decrease difficulty if struggling
        if st.session_state.total_questions % 3 == 0:  # Every 3 questions
            accuracy = st.session_state.properties_score / st.session_state.total_questions
            if accuracy < 0.5 and st.session_state.properties_difficulty > 1:
                old_difficulty = st.session_state.properties_difficulty
                st.session_state.properties_difficulty = max(st.session_state.properties_difficulty - 1, 1)
                if old_difficulty > st.session_state.properties_difficulty:
                    st.warning(f"⬇️ **Let's practice the basics. Back to Level {st.session_state.properties_difficulty}**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if data["format"] == "identify_property":
            # FORMAT 1: Showed equation, asked for property
            target_property = data['target_property']
            equation = data['equation']
            
            st.markdown(f"""
            ### Why **{equation}** shows the **{target_property.title()} Property**:
            
            **{data['explanation']}**
            """)
            
            # Property-specific explanations
            if target_property == "identity":
                st.markdown("""
                ### 🔹 Identity Property Details:
                - The **Identity Property** says any number × 1 = that number
                - Look for multiplication by 1 in the expression
                - The number stays the same (keeps its "identity")
                - Examples: 8 × 1 = 8, 1 × 15 = 15
                """)
            elif target_property == "zero":
                st.markdown("""
                ### 🔹 Zero Property Details:
                - The **Zero Property** says any number × 0 = 0
                - Look for multiplication by 0 in the expression
                - The result is always zero, no matter what the other number is
                - Examples: 7 × 0 = 0, 0 × 12 = 0
                """)
            elif target_property == "commutative":
                st.markdown("""
                ### 🔹 Commutative Property Details:
                - The **Commutative Property** says a × b = b × a
                - Look for the same numbers in different order
                - "Commute" means to switch places
                - Examples: 5 × 3 = 3 × 5, 9 × 4 = 4 × 9
                """)
            elif target_property == "associative":
                st.markdown("""
                ### 🔹 Associative Property Details:
                - The **Associative Property** says (a × b) × c = a × (b × c)
                - Look for parentheses in different positions
                - The grouping changes but the numbers stay the same
                - Examples: (2 × 3) × 4 = 2 × (3 × 4), 7 × (2 × 5) = (7 × 2) × 5
                """)
            elif target_property == "distributive":
                st.markdown("""
                ### 🔹 Distributive Property Details:
                - The **Distributive Property** says a × (b + c) = a × b + a × c
                - Look for multiplication being "distributed" over addition/subtraction
                - One number multiplies everything inside the parentheses
                - Examples: 3 × (4 + 5) = 3 × 4 + 3 × 5, 6 × (7 - 2) = 6 × 7 - 6 × 2
                """)
        
        else:
            # FORMAT 2: Asked for property, showed equations
            target_property = data['target_property']
            correct_equation = data['correct_answer']
            
            st.markdown(f"""
            ### Why **{correct_equation}** shows the **{target_property.title()} Property**:
            
            **{data['explanation']}**
            """)
            
            # Property-specific explanations
            if target_property == "identity":
                st.markdown("""
                ### 🔹 Identity Property Details:
                - The **Identity Property** says any number × 1 = that number
                - Look for multiplication by 1 in the expression
                - The number stays the same (keeps its "identity")
                - Examples: 8 × 1 = 8, 1 × 15 = 15
                """)
            elif target_property == "zero":
                st.markdown("""
                ### 🔹 Zero Property Details:
                - The **Zero Property** says any number × 0 = 0
                - Look for multiplication by 0 in the expression
                - The result is always zero, no matter what the other number is
                - Examples: 7 × 0 = 0, 0 × 12 = 0
                """)
            elif target_property == "commutative":
                st.markdown("""
                ### 🔹 Commutative Property Details:
                - The **Commutative Property** says a × b = b × a
                - Look for the same numbers in different order
                - "Commute" means to switch places
                - Examples: 5 × 3 = 3 × 5, 9 × 4 = 4 × 9
                """)
            elif target_property == "associative":
                st.markdown("""
                ### 🔹 Associative Property Details:
                - The **Associative Property** says (a × b) × c = a × (b × c)
                - Look for parentheses in different positions
                - The grouping changes but the numbers stay the same
                - Examples: (2 × 3) × 4 = 2 × (3 × 4), 7 × (2 × 5) = (7 × 2) × 5
                """)
            elif target_property == "distributive":
                st.markdown("""
                ### 🔹 Distributive Property Details:
                - The **Distributive Property** says a × (b + c) = a × b + a × c
                - Look for multiplication being "distributed" over addition/subtraction
                - One number multiplies everything inside the parentheses
                - Examples: 3 × (4 + 5) = 3 × 4 + 3 × 5, 6 × (7 - 2) = 6 × 7 - 6 × 2
                """)
            
            # Show what the other options represent
            st.markdown("### 📝 About the other options:")
            user_answer = st.session_state.user_answer
            if user_answer != correct_equation:
                if "=" in user_answer and "+" in user_answer and "×" in user_answer and user_answer.count('+') > user_answer.count('×'):
                    st.markdown("- Your choice shows **repeated addition**, not a multiplication property")
                elif "× 1" in user_answer or "1 ×" in user_answer:
                    st.markdown("- Your choice shows the **identity property** (multiplication by 1)")
                elif "× 0" in user_answer or "0 ×" in user_answer:
                    st.markdown("- Your choice shows the **zero property** (multiplication by 0)")
                elif "(" in user_answer and ")" in user_answer:
                    if "+" in user_answer or "-" in user_answer:
                        st.markdown("- Your choice shows the **distributive property** (distributing multiplication)")
                    else:
                        st.markdown("- Your choice shows the **associative property** (changing grouping)")
                else:
                    st.markdown("- Your choice may show a different multiplication property")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer