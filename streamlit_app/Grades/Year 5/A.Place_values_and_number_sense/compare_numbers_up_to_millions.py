import streamlit as st
import random

def run():
    """
    Main function to run the Compare Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_numbers_up_to_millions.py
    """
    # Initialize session state for difficulty and game state - FIXED: All keys properly prefixed
    if "compare_numbers_difficulty" not in st.session_state:
        st.session_state.compare_numbers_difficulty = 5  # Start with 5-digit numbers
    
    if "compare_numbers_current_question" not in st.session_state:
        st.session_state.compare_numbers_current_question = None
        st.session_state.compare_numbers_question_type = None
        st.session_state.compare_numbers_correct_answer = None
        st.session_state.compare_numbers_show_feedback = False
        st.session_state.compare_numbers_answer_submitted = False
        st.session_state.compare_numbers_question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Compare Numbers up to Millions")
    st.markdown("*Compare large numbers and find patterns in data*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.compare_numbers_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level}-digit numbers")
        # Progress bar (4 to 7 digits)
        progress = (difficulty_level - 4) / 3  # Convert 4-7 to 0-1
        st.progress(progress, text=f"{difficulty_level}-digit numbers")
    
    with col2:
        if difficulty_level <= 4:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 5:
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
    if st.session_state.compare_numbers_current_question is None:
        generate_new_question()
    
    # Display current question based on type
    if st.session_state.compare_numbers_question_type == "sign_comparison":
        display_sign_comparison_question()
    else:
        display_table_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Types of Questions:
        
        **🔢 Sign Comparison:**
        - Choose the correct sign (>, <, =) to compare two large numbers
        - Look at digits from left to right to compare
        
        **📊 Data Table Analysis:**
        - Find the smallest or largest value in real-world data tables
        - Read the table carefully and compare all values
        
        ### Difficulty Levels:
        - **🟡 4-digit numbers:** (1,000s)
        - **🟠 5-digit numbers:** (10,000s)  
        - **🔴 6-7 digit numbers:** (100,000s - millions)
        
        ### Scoring:
        - ✅ **Correct answer:** Numbers get bigger
        - ❌ **Wrong answer:** Numbers get smaller
        - 🎯 **Goal:** Master 7-digit numbers!
        """)

def generate_new_question():
    """Generate a new comparison question"""
    digits = st.session_state.compare_numbers_difficulty
    
    # Randomly choose question type
    question_type = random.choice(["sign_comparison", "table_analysis"])
    
    st.session_state.compare_numbers_question_type = question_type
    
    if question_type == "sign_comparison":
        generate_sign_comparison_question(digits)
    else:
        generate_table_question(digits)

def generate_sign_comparison_question(digits):
    """Generate a sign comparison question"""
    # Generate two random numbers with the specified number of digits
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)
    
    # Determine correct answer
    if a > b:
        correct = ">"
    elif a < b:
        correct = "<"
    else:
        correct = "="
    
    st.session_state.compare_numbers_question_data = {
        "number_a": a,
        "number_b": b,
        "options": [">", "<", "="]
    }
    st.session_state.compare_numbers_correct_answer = correct
    st.session_state.compare_numbers_current_question = f"Which sign makes the statement true?"

def generate_table_question(digits):
    """Generate a table analysis question"""
    themes = [
        {
            "title": "Books Sold",
            "unit": "Number of books",
            "labels": ["January", "February", "March", "April", "May", "June", "July"],
            "label_type": "Month",
            "question": "In which month were the **fewest** books sold?"
        },
        {
            "title": "Taffy Made",
            "unit": "Pieces of taffy",
            "labels": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "label_type": "Day",
            "question": "On which day did the factory make the **least** taffy?"
        },
        {
            "title": "Apples Exported", 
            "unit": "Apples exported",
            "labels": ["India", "Brazil", "Kenya", "Vietnam", "Peru", "Spain"],
            "label_type": "Country",
            "question": "Which country exported the **fewest** apples?"
        },
        {
            "title": "Bikes Sold",
            "unit": "Bikes sold", 
            "labels": ["Store A", "Store B", "Store C", "Store D", "Store E"],
            "label_type": "Store",
            "question": "Which store sold the **fewest** bikes?"
        },
        {
            "title": "Packages Delivered",
            "unit": "Packages delivered",
            "labels": ["Warehouse 1", "Warehouse 2", "Warehouse 3", "Warehouse 4"],
            "label_type": "Location", 
            "question": "Which warehouse delivered the **fewest** packages?"
        }
    ]
    
    scenario = random.choice(themes)
    labels = random.sample(scenario["labels"], 4)
    
    # Generate random numbers
    min_val = 10**(digits - 1)
    max_val = 10**digits - 1
    
    values = {label: random.randint(min_val, max_val) for label in labels}
    correct_label = min(values, key=values.get)
    
    st.session_state.compare_numbers_question_data = {
        "scenario": scenario,
        "labels": labels,
        "values": values
    }
    st.session_state.compare_numbers_correct_answer = correct_label
    st.session_state.compare_numbers_current_question = scenario["question"]

def display_sign_comparison_question():
    """Display sign comparison question interface"""
    data = st.session_state.compare_numbers_question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.compare_numbers_current_question}**")
    
    # Display the comparison with large numbers
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; font-size: 28px; padding: 20px; 
                    background-color: #f0f2f6; border-radius: 10px; margin: 10px;">
            <strong>{data['number_a']:,}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 36px; padding: 20px;">
            <strong>❓</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; font-size: 28px; padding: 20px; 
                    background-color: #f0f2f6; border-radius: 10px; margin: 10px;">
            <strong>{data['number_b']:,}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.radio(
                "Choose the correct sign:",
                options=data['options'],
                horizontal=True,
                key="compare_sign_choice"
            )
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.compare_numbers_user_answer = user_answer
            st.session_state.compare_numbers_show_feedback = True
            st.session_state.compare_numbers_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def display_table_question():
    """Display table analysis question interface"""
    data = st.session_state.compare_numbers_question_data
    scenario = data['scenario']
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{scenario['title']}**")
    
    # Create and display table
    table_data = []
    for label in data['labels']:
        table_data.append({
            scenario['label_type']: label,
            scenario['unit']: f"{data['values'][label]:,}"
        })
    
    st.table(table_data)
    
    # Display question
    st.markdown(f"**{st.session_state.compare_numbers_current_question}**")
    
    # Answer selection
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.radio(
                f"Choose the {scenario['label_type'].lower()}:",
                options=data['labels'],
                key="compare_table_choice"
            )
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.compare_numbers_user_answer = user_answer
            st.session_state.compare_numbers_show_feedback = True
            st.session_state.compare_numbers_answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.compare_numbers_show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.compare_numbers_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.compare_numbers_user_answer
    correct_answer = st.session_state.compare_numbers_correct_answer
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 7 digits)
        old_difficulty = st.session_state.compare_numbers_difficulty
        st.session_state.compare_numbers_difficulty = min(
            st.session_state.compare_numbers_difficulty + 1, 7
        )
        
        # Show encouragement based on difficulty
        if st.session_state.compare_numbers_difficulty == 7 and old_difficulty < 7:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered million-digit numbers!**")
        elif old_difficulty < st.session_state.compare_numbers_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.compare_numbers_difficulty}-digit numbers**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**.")
        
        # Decrease difficulty (min 4 digits)
        old_difficulty = st.session_state.compare_numbers_difficulty
        st.session_state.compare_numbers_difficulty = max(
            st.session_state.compare_numbers_difficulty - 1, 4
        )
        
        if old_difficulty > st.session_state.compare_numbers_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.compare_numbers_difficulty}-digit numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    question_type = st.session_state.compare_numbers_question_type
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if question_type == "sign_comparison":
            data = st.session_state.compare_numbers_question_data
            a, b = data['number_a'], data['number_b']
            correct = st.session_state.compare_numbers_correct_answer
            
            st.markdown(f"""
            ### Step-by-step comparison:
            
            **Numbers:** {a:,} vs {b:,}
            
            **How to compare large numbers:**
            1. **Start from the left** - compare the leftmost digits first
            2. **If they're the same**, move to the next digit
            3. **The first different digit** determines which number is larger
            
            **Result:** {a:,} {correct} {b:,}
            """)
        
        else:  # table_analysis
            data = st.session_state.compare_numbers_question_data
            values = data['values']
            correct = st.session_state.compare_numbers_correct_answer
            
            # Show all values for comparison
            comparison_text = "**All values:**\n"
            for label, value in sorted(values.items(), key=lambda x: x[1]):
                marker = "👈 **SMALLEST**" if label == correct else ""
                comparison_text += f"- {label}: {value:,} {marker}\n"
            
            st.markdown(comparison_text)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.compare_numbers_current_question = None
    st.session_state.compare_numbers_question_type = None
    st.session_state.compare_numbers_correct_answer = None
    st.session_state.compare_numbers_show_feedback = False
    st.session_state.compare_numbers_answer_submitted = False
    st.session_state.compare_numbers_question_data = {}
    if "compare_numbers_user_answer" in st.session_state:
        del st.session_state.compare_numbers_user_answer