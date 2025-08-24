import streamlit as st
import random

def run():
    """
    Main function to run the Properties of Addition practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/properties_of_addition.py
    """
    # Initialize session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.question_count = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("🏗️ Properties of Addition")
    st.markdown("*Learn the commutative, associative, and identity properties*")
    st.markdown("---")
    
    # Progress indicator
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Questions completed:** {st.session_state.question_count}")
        # Show progress as a simple counter
        progress_text = f"Question #{st.session_state.question_count + 1}"
        st.markdown(f"*{progress_text}*")
    
    with col2:
        st.markdown("**🧮 Math Properties**")
    
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
    with st.expander("💡 **Learn About Addition Properties**", expanded=False):
        st.markdown("""
        ### 🏗️ The Three Properties of Addition:
        
        #### 1️⃣ **Commutative Property** 
        *"Order doesn't matter"*
        - **Rule:** a + b = b + a
        - **Example:** 5 + 3 = 3 + 5 (both equal 8)
        - **Meaning:** You can add numbers in any order and get the same answer
        
        #### 2️⃣ **Associative Property**
        *"Grouping doesn't matter"*
        - **Rule:** (a + b) + c = a + (b + c)  
        - **Example:** (4 + 2) + 3 = 4 + (2 + 3) (both equal 9)
        - **Meaning:** You can group numbers differently and get the same answer
        
        #### 3️⃣ **Identity Property**
        *"Adding zero doesn't change anything"*
        - **Rule:** a + 0 = a
        - **Example:** 7 + 0 = 7
        - **Meaning:** Zero is the "identity" for addition - it doesn't change the other number
        
        ### 🎯 **How to Identify Each Property:**
        
        **Look for Commutative Property when:**
        - Two numbers are switched: 8 + 5 = 5 + 8
        - Same numbers, different order: a + b = b + a
        
        **Look for Associative Property when:**
        - Parentheses are moved: (6 + 4) + 2 = 6 + (4 + 2)
        - Three numbers with different grouping: (a + b) + c = a + (b + c)
        
        **Look for Identity Property when:**
        - Zero is being added: 9 + 0 = 9
        - A number plus zero equals itself: a + 0 = a
        
        ### 💭 **Memory Tips:**
        - **Commutative** = "Commute" (travel back and forth) = numbers can switch places
        - **Associative** = "Associate" (group together) = numbers can be grouped differently  
        - **Identity** = "Same identity" = the number stays the same when you add zero
        
        ### 🧮 **Practice Strategy:**
        1. **Read the equation carefully**
        2. **Look for the pattern:** switching, grouping, or zero?
        3. **Ask yourself:** What makes this equation special?
        4. **Choose the property** that matches the pattern
        """)

def generate_new_question():
    """Generate a new properties question"""
    
    # Define property examples
    property_examples = [
        # Commutative Property Examples
        {"equation": "7 + 3 = 3 + 7", "property": "commutative"},
        {"equation": "15 + 8 = 8 + 15", "property": "commutative"},
        {"equation": "9 + 6 = 6 + 9", "property": "commutative"},
        {"equation": "12 + 4 = 4 + 12", "property": "commutative"},
        {"equation": "25 + 17 = 17 + 25", "property": "commutative"},
        {"equation": "11 + 14 = 14 + 11", "property": "commutative"},
        {"equation": "19 + 23 = 23 + 19", "property": "commutative"},
        {"equation": "35 + 28 = 28 + 35", "property": "commutative"},
        
        # Associative Property Examples  
        {"equation": "(5 + 3) + 4 = 5 + (3 + 4)", "property": "associative"},
        {"equation": "(8 + 2) + 6 = 8 + (2 + 6)", "property": "associative"},
        {"equation": "(9 + 7) + 1 = 9 + (7 + 1)", "property": "associative"},
        {"equation": "(12 + 5) + 8 = 12 + (5 + 8)", "property": "associative"},
        {"equation": "(15 + 10) + 3 = 15 + (10 + 3)", "property": "associative"},
        {"equation": "(6 + 4) + 9 = 6 + (4 + 9)", "property": "associative"},
        {"equation": "(11 + 7) + 2 = 11 + (7 + 2)", "property": "associative"},
        {"equation": "(20 + 15) + 5 = 20 + (15 + 5)", "property": "associative"},
        
        # Identity Property Examples
        {"equation": "8 + 0 = 8", "property": "identity"},
        {"equation": "15 + 0 = 15", "property": "identity"},
        {"equation": "0 + 12 = 12", "property": "identity"},
        {"equation": "23 + 0 = 23", "property": "identity"},
        {"equation": "0 + 7 = 7", "property": "identity"},
        {"equation": "34 + 0 = 34", "property": "identity"},
        {"equation": "0 + 19 = 19", "property": "identity"},
        {"equation": "45 + 0 = 45", "property": "identity"},
    ]
    
    # Choose question type randomly
    question_type = random.choice(["type1", "type2"])
    
    if question_type == "type1":
        # Type 1: Show equation, identify property
        question = random.choice(property_examples)
        st.session_state.problem_data = {
            "type": "identify_property",
            "equation": question["equation"],
            "correct_property": question["property"],
            "options": ["commutative", "associative", "identity"]
        }
        st.session_state.current_question = "Which property of addition is shown?"
        
    else:
        # Type 2: Show property, identify equation
        target_property = random.choice(["commutative", "associative", "identity"])
        
        # Get equations that match the target property
        matching_equations = [q["equation"] for q in property_examples if q["property"] == target_property]
        non_matching_equations = [q["equation"] for q in property_examples if q["property"] != target_property]
        
        # Create 4 choices: 1 correct + 3 incorrect
        correct_equation = random.choice(matching_equations)
        incorrect_equations = random.sample(non_matching_equations, 3)
        all_choices = [correct_equation] + incorrect_equations
        random.shuffle(all_choices)
        
        st.session_state.problem_data = {
            "type": "identify_equation",
            "target_property": target_property,
            "choices": all_choices,
            "correct_equation": correct_equation,
            "matching_equations": matching_equations
        }
        st.session_state.current_question = f"Which equation shows the **{target_property}** property of addition?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display question with nice formatting
    st.markdown("### 🏗️ Addition Properties Challenge:")
    
    if data["type"] == "identify_property":
        display_identify_property_question()
    else:
        display_identify_equation_question()

def display_identify_property_question():
    """Display Type 1: Identify property from equation"""
    data = st.session_state.problem_data
    
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Display the equation in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #e3f2fd; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #2196f3;
        font-family: 'Courier New', monospace;
        font-size: 28px;
        text-align: center;
        margin: 30px 0;
        color: #0d47a1;
        font-weight: bold;
    ">
        {data['equation']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer selection
    with st.form("property_form", clear_on_submit=False):
        st.markdown("**🤔 Which property does this equation demonstrate?**")
        
        user_answer = st.radio(
            "Choose the correct property:",
            options=data["options"],
            format_func=lambda x: f"**{x.title()}** Property",
            key="property_choice"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_identify_equation_question():
    """Display Type 2: Identify equation from property"""
    data = st.session_state.problem_data
    
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Answer selection
    with st.form("equation_form", clear_on_submit=False):
        st.markdown("**🤔 Which equation demonstrates this property?**")
        
        user_answer = st.radio(
            "Choose the correct equation:",
            options=data["choices"],
            key="equation_choice"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
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
                st.session_state.question_count += 1
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.problem_data
    user_answer = st.session_state.user_answer
    
    if data["type"] == "identify_property":
        correct_answer = data["correct_property"]
        if user_answer == correct_answer:
            st.success("🎉 **Correct! Well done!**")
            show_property_explanation(correct_answer, data["equation"])
        else:
            st.error(f"❌ **Incorrect.** The correct answer was **{correct_answer}**.")
            show_property_explanation(correct_answer, data["equation"], show_why_wrong=True, wrong_answer=user_answer)
    
    else:  # identify_equation
        if user_answer == data["correct_equation"]:
            st.success("🎉 **Correct!** That equation shows the selected property.")
            show_equation_explanation(data["target_property"], user_answer)
        else:
            st.error(f"❌ **Incorrect.** A correct example is **{data['correct_equation']}**.")
            show_equation_explanation(data["target_property"], data["correct_equation"], show_why_wrong=True, wrong_answer=user_answer)

def show_property_explanation(property_name, equation, show_why_wrong=False, wrong_answer=None):
    """Show explanation for why an equation demonstrates a specific property"""
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"### 🏗️ **{property_name.title()} Property Explanation:**")
        st.markdown(f"**Equation:** {equation}")
        
        if property_name == "commutative":
            st.markdown("**Why it's commutative:**")
            st.markdown("- The same two numbers are being added")
            st.markdown("- They appear in different orders on each side")
            st.markdown("- This shows that **order doesn't matter** in addition")
            st.markdown("- Pattern: a + b = b + a")
            
        elif property_name == "associative":
            st.markdown("**Why it's associative:**")
            st.markdown("- Three numbers are being added")
            st.markdown("- The parentheses group them differently on each side")
            st.markdown("- This shows that **grouping doesn't matter** in addition")
            st.markdown("- Pattern: (a + b) + c = a + (b + c)")
            
        elif property_name == "identity":
            st.markdown("**Why it's identity:**")
            st.markdown("- Zero is being added to a number")
            st.markdown("- The result is the same as the original number")
            st.markdown("- This shows that **zero doesn't change the value**")
            st.markdown("- Pattern: a + 0 = a or 0 + a = a")
        
        if show_why_wrong and wrong_answer:
            st.markdown(f"### ❌ **Why '{wrong_answer}' is incorrect:**")
            if wrong_answer == "commutative" and property_name != "commutative":
                st.markdown("- Commutative means switching the order of two numbers")
                st.markdown("- Look for: a + b = b + a")
            elif wrong_answer == "associative" and property_name != "associative":
                st.markdown("- Associative means changing how three numbers are grouped")
                st.markdown("- Look for: (a + b) + c = a + (b + c)")
            elif wrong_answer == "identity" and property_name != "identity":
                st.markdown("- Identity means adding zero to a number")
                st.markdown("- Look for: a + 0 = a")

def show_equation_explanation(property_name, equation, show_why_wrong=False, wrong_answer=None):
    """Show explanation for why an equation demonstrates a specific property"""
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"### 🏗️ **Why this equation shows the {property_name} property:**")
        st.markdown(f"**Equation:** {equation}")
        
        if property_name == "commutative":
            st.markdown("**This demonstrates the commutative property because:**")
            st.markdown("- The same numbers appear on both sides")
            st.markdown("- They are in different order (switched)")
            st.markdown("- This proves that order doesn't matter in addition")
            
        elif property_name == "associative":
            st.markdown("**This demonstrates the associative property because:**")
            st.markdown("- Three numbers are being added")
            st.markdown("- The parentheses create different groupings")
            st.markdown("- This proves that grouping doesn't matter in addition")
            
        elif property_name == "identity":
            st.markdown("**This demonstrates the identity property because:**")
            st.markdown("- Zero is being added to a number")
            st.markdown("- The number stays exactly the same")
            st.markdown("- This proves that zero is the additive identity")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer