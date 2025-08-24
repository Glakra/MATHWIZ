import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Fractions of a Number Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I.Fractions and mixed numbers/fractions_of_a_number_word_problems.py
    """
    # Initialize session state for difficulty and game state
    if "fractions_word_difficulty" not in st.session_state:
        st.session_state.fractions_word_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("📖 Fractions of a Number: Word Problems")
    st.markdown("*Solve real-world problems with fractions*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fractions_word_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Unit fractions with small numbers",
            2: "Simple fractions with everyday items",
            3: "Mixed contexts with larger numbers",
            4: "Complex fractions and scenarios",
            5: "Challenging multi-step problems"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
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
        ### How to Solve Word Problems:
        1. **Read carefully** - What fraction? What total?
        2. **Identify** - The fraction and the number
        3. **Calculate** - Multiply fraction × number
        4. **Check** - Does your answer make sense?
        
        ### Example Problems:
        - **"1/3 of 12 students wear glasses"** → 12 ÷ 3 = 4 students
        - **"2/5 of 30 apples are red"** → 30 ÷ 5 × 2 = 12 apples
        - **"3/4 of 20 books are fiction"** → 20 ÷ 4 × 3 = 15 books
        
        ### Quick Tips:
        - **Unit fractions (1/n):** Just divide by the denominator
        - **Other fractions:** Divide by denominator, then multiply by numerator
        - **Check reasonableness:** The answer should be less than the total (unless improper fraction)
        
        ### Common Contexts:
        - 🍎 Food and cooking
        - 🎒 School and classroom
        - 🏃 Sports and activities
        - 🎨 Arts and crafts
        - 🌍 Nature and environment
        """)

def generate_new_question():
    """Generate a new fraction word problem"""
    difficulty = st.session_state.fractions_word_difficulty
    
    # Define scenario templates based on difficulty
    if difficulty == 1:
        # Level 1: Unit fractions with small numbers
        scenarios = [
            {
                "template": "There are {total} {items} in a {container}. {fraction_words} of the {items} are {type}. How many {type} {items} are in the {container}?",
                "contexts": [
                    {"total": 6, "items": "cookies", "container": "jar", "fraction": (1, 2), "fraction_words": "One-half", "type": "chocolate chip"},
                    {"total": 9, "items": "candies", "container": "bowl", "fraction": (1, 3), "fraction_words": "One-third", "type": "peppermints"},
                    {"total": 8, "items": "marbles", "container": "bag", "fraction": (1, 4), "fraction_words": "One-quarter", "type": "blue"},
                    {"total": 10, "items": "pencils", "container": "box", "fraction": (1, 5), "fraction_words": "One-fifth", "type": "red"},
                    {"total": 12, "items": "eggs", "container": "carton", "fraction": (1, 6), "fraction_words": "One-sixth", "type": "brown"},
                ]
            },
            {
                "template": "{fraction_words} of the {total} {people} at the {place} are {doing}. How many {people} are {doing}?",
                "contexts": [
                    {"total": 6, "people": "people", "place": "beach", "fraction": (1, 3), "fraction_words": "One-third", "doing": "wearing sunglasses"},
                    {"total": 8, "people": "students", "place": "playground", "fraction": (1, 2), "fraction_words": "One-half", "doing": "playing soccer"},
                    {"total": 10, "people": "children", "place": "party", "fraction": (1, 5), "fraction_words": "One-fifth", "doing": "wearing hats"},
                    {"total": 12, "people": "students", "place": "classroom", "fraction": (1, 4), "fraction_words": "One-quarter", "doing": "reading books"},
                ]
            }
        ]
        
    elif difficulty == 2:
        # Level 2: Simple fractions with everyday items
        scenarios = [
            {
                "template": "Of the {total} {items} in the {place}, {fraction_words} are {type}. How many {type} are in the {place}?",
                "contexts": [
                    {"total": 8, "items": "pieces of fruit", "place": "kitchen", "fraction": (3, 4), "fraction_words": "three-quarters", "type": "peaches"},
                    {"total": 15, "items": "flowers", "place": "garden", "fraction": (2, 3), "fraction_words": "two-thirds", "type": "roses"},
                    {"total": 12, "items": "biscuits", "place": "tin", "fraction": (5, 6), "fraction_words": "five-sixths", "type": "chocolate"},
                    {"total": 20, "items": "cars", "place": "parking lot", "fraction": (3, 5), "fraction_words": "three-fifths", "type": "red cars"},
                    {"total": 18, "items": "books", "place": "shelf", "fraction": (2, 3), "fraction_words": "two-thirds", "type": "fiction books"},
                ]
            },
            {
                "template": "{person} has {total} {items}. {fraction_words} of them are {type}. How many {type} does {person} have?",
                "contexts": [
                    {"person": "Sarah", "total": 16, "items": "stickers", "fraction": (3, 8), "fraction_words": "Three-eighths", "type": "star stickers"},
                    {"person": "Tom", "total": 24, "items": "marbles", "fraction": (5, 8), "fraction_words": "Five-eighths", "type": "red marbles"},
                    {"person": "Emma", "total": 20, "items": "crayons", "fraction": (3, 4), "fraction_words": "Three-quarters", "type": "broken"},
                    {"person": "Jack", "total": 30, "items": "cards", "fraction": (2, 5), "fraction_words": "Two-fifths", "type": "picture cards"},
                ]
            }
        ]
        
    elif difficulty == 3:
        # Level 3: Mixed contexts with larger numbers
        scenarios = [
            {
                "template": "A {place} has {total} {items}. {fraction_words} of the {items} are {type}. How many {items} are {type}?",
                "contexts": [
                    {"place": "library", "total": 36, "items": "DVDs", "fraction": (5, 9), "fraction_words": "Five-ninths", "type": "documentaries"},
                    {"place": "bakery", "total": 48, "items": "cupcakes", "fraction": (7, 12), "fraction_words": "Seven-twelfths", "type": "vanilla"},
                    {"place": "school", "total": 40, "items": "computers", "fraction": (3, 8), "fraction_words": "Three-eighths", "type": "laptops"},
                    {"place": "farm", "total": 54, "items": "animals", "fraction": (4, 9), "fraction_words": "Four-ninths", "type": "chickens"},
                ]
            },
            {
                "template": "In a {event} with {total} {participants}, {fraction_words} are {type}. How many {type} are there?",
                "contexts": [
                    {"event": "marathon", "total": 60, "participants": "runners", "fraction": (7, 10), "fraction_words": "seven-tenths", "type": "first-time runners"},
                    {"event": "concert", "total": 72, "participants": "musicians", "fraction": (5, 12), "fraction_words": "five-twelfths", "type": "playing strings"},
                    {"event": "art show", "total": 45, "participants": "paintings", "fraction": (8, 15), "fraction_words": "eight-fifteenths", "type": "landscapes"},
                ]
            }
        ]
        
    elif difficulty == 4:
        # Level 4: Complex fractions and scenarios
        scenarios = [
            {
                "template": "A {business} sold {total} {items} last {time}. {fraction_words} of the {items} were {type}. How many {type} {items} were sold?",
                "contexts": [
                    {"business": "bookstore", "total": 84, "items": "books", "time": "week", "fraction": (11, 14), "fraction_words": "Eleven-fourteenths", "type": "fiction"},
                    {"business": "toy shop", "total": 96, "items": "toys", "time": "month", "fraction": (7, 16), "fraction_words": "Seven-sixteenths", "type": "board games"},
                    {"business": "electronics store", "total": 90, "items": "devices", "time": "day", "fraction": (13, 18), "fraction_words": "Thirteen-eighteenths", "type": "smartphones"},
                ]
            },
            {
                "template": "A survey of {total} {people} showed that {fraction_words} {preference}. How many {people} {preference}?",
                "contexts": [
                    {"total": 80, "people": "students", "fraction": (9, 16), "fraction_words": "nine-sixteenths", "preference": "prefer online learning"},
                    {"total": 105, "people": "voters", "fraction": (11, 15), "fraction_words": "eleven-fifteenths", "preference": "support the proposal"},
                    {"total": 88, "people": "customers", "fraction": (15, 22), "fraction_words": "fifteen twenty-seconds", "preference": "shop online"},
                ]
            }
        ]
        
    else:  # difficulty == 5
        # Level 5: Challenging multi-step problems
        scenarios = [
            {
                "template": "A factory produces {total} {items} per day. {fraction_words} of the {items} pass quality control. How many {items} pass quality control?",
                "contexts": [
                    {"total": 144, "items": "widgets", "fraction": (17, 24), "fraction_words": "Seventeen twenty-fourths"},
                    {"total": 156, "items": "components", "fraction": (19, 26), "fraction_words": "Nineteen twenty-sixths"},
                    {"total": 180, "items": "products", "fraction": (23, 30), "fraction_words": "Twenty-three thirtieths"},
                ]
            },
            {
                "template": "In a school with {total} students, {fraction_words} participate in {activity}. How many students participate in {activity}?",
                "contexts": [
                    {"total": 240, "students": "students", "fraction": (7, 12), "fraction_words": "seven-twelfths", "activity": "after-school sports"},
                    {"total": 315, "students": "students", "fraction": (8, 15), "fraction_words": "eight-fifteenths", "activity": "the music program"},
                    {"total": 360, "students": "students", "fraction": (13, 20), "fraction_words": "thirteen-twentieths", "activity": "volunteer work"},
                ]
            }
        ]
    
    # Select a random scenario and context
    scenario_group = random.choice(scenarios)
    context = random.choice(scenario_group["contexts"])
    
    # Generate the question text
    question_text = scenario_group["template"].format(**context)
    
    # Calculate the answer
    numerator, denominator = context["fraction"]
    total = context["total"]
    answer = (total * numerator) // denominator
    
    # Determine the answer unit (for display)
    if "items" in context:
        unit = context.get("type", "") + " " + context["items"]
    elif "people" in context:
        unit = context["people"]
    elif "participants" in context:
        unit = context.get("type", context["participants"])
    else:
        unit = "items"
    
    # Clean up unit text
    unit = unit.strip().replace("  ", " ")
    
    st.session_state.question_data = {
        "question_text": question_text,
        "numerator": numerator,
        "denominator": denominator,
        "total": total,
        "fraction_str": f"{numerator}/{denominator}",
        "fraction_words": context["fraction_words"],
        "unit": unit
    }
    st.session_state.correct_answer = answer
    st.session_state.current_question = question_text

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Problem:")
    
    # Display the question in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #28a745;
        font-size: 20px;
        line-height: 1.6;
        margin: 20px 0;
        color: #2c3e50;
    ">
        {data['question_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Visual representation for lower difficulties
    if st.session_state.fractions_word_difficulty <= 2 and data['total'] <= 20:
        show_visual_representation(data)
    
    # Answer input form
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Create input with unit label
            input_cols = st.columns([2, 1])
            
            with input_cols[0]:
                user_answer = st.number_input(
                    "Your answer:",
                    min_value=0,
                    max_value=1000,
                    step=1,
                    key="word_problem_answer_input",
                    label_visibility="collapsed",
                    placeholder="Enter your answer..."
                )
            
            with input_cols[1]:
                st.markdown(f"<p style='margin-top: 8px; color: #666;'>{data['unit']}</p>", unsafe_allow_html=True)
            
            # Submit button
            submit_button = st.form_submit_button(
                "✅ Submit Answer", 
                type="primary", 
                use_container_width=True
            )
        
        if submit_button:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def show_visual_representation(data):
    """Show visual representation for easier understanding"""
    total = data['total']
    numerator = data['numerator']
    denominator = data['denominator']
    
    if total <= 20:
        st.markdown("#### 🎯 Visual Helper:")
        
        # Calculate how many items to highlight
        highlighted = (total * numerator) // denominator
        
        # Create visual grid
        cols_per_row = min(10, total)
        rows_needed = (total + cols_per_row - 1) // cols_per_row
        
        item_symbols = ["🟦", "🟩", "🟨", "🟧", "🟥", "🟪", "⬜", "🔵", "🔴", "🟢"]
        symbol = random.choice(item_symbols)
        
        visual_html = "<div style='text-align: center; margin: 20px 0;'>"
        
        item_count = 0
        for row in range(rows_needed):
            visual_html += "<div style='margin: 5px 0;'>"
            for col in range(cols_per_row):
                if item_count < total:
                    if item_count < highlighted:
                        visual_html += f"<span style='font-size: 24px; margin: 2px;'>{symbol}</span>"
                    else:
                        visual_html += "<span style='font-size: 24px; margin: 2px;'>⬜</span>"
                    item_count += 1
            visual_html += "</div>"
        
        visual_html += "</div>"
        st.markdown(visual_html, unsafe_allow_html=True)
        
        st.caption(f"Total: {total} | Highlighted: {highlighted} ({data['fraction_words']})")

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent! That's correct!**")
        st.success(f"✓ The answer is **{correct_answer} {data['unit']}**")
        
        # Increase difficulty (max 5)
        old_difficulty = st.session_state.fractions_word_difficulty
        st.session_state.fractions_word_difficulty = min(
            st.session_state.fractions_word_difficulty + 1, 5
        )
        
        if st.session_state.fractions_word_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Amazing! You've mastered fraction word problems!**")
        elif old_difficulty < st.session_state.fractions_word_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.fractions_word_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.** You answered: {user_answer} {data['unit']}")
        st.error(f"The correct answer is **{correct_answer} {data['unit']}**")
        
        # Decrease difficulty (min 1)
        old_difficulty = st.session_state.fractions_word_difficulty
        st.session_state.fractions_word_difficulty = max(
            st.session_state.fractions_word_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.fractions_word_difficulty:
            st.warning(f"⬇️ **Level adjusted to {st.session_state.fractions_word_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show step-by-step explanation for the correct answer"""
    data = st.session_state.question_data
    numerator = data['numerator']
    denominator = data['denominator']
    total = data['total']
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **See step-by-step solution**", expanded=True):
        st.markdown(f"""
        ### Understanding the Problem
        
        **Question:** {data['question_text']}
        
        **What we know:**
        - Total amount: **{total}**
        - Fraction: **{data['fraction_words']} = {numerator}/{denominator}**
        - We need to find: {numerator}/{denominator} of {total}
        
        ---
        
        ### Solution Steps
        
        **Step 1: Write the calculation**
        {numerator}/{denominator} × {total}
        
        **Step 2: Calculate**
        Method 1 - Divide first:
        - {total} ÷ {denominator} = {total // denominator} {f"(with remainder {total % denominator})" if total % denominator != 0 else ""}
        - {total // denominator} × {numerator} = {(total // denominator) * numerator}
        
        Method 2 - Multiply first:
        - {numerator} × {total} = {numerator * total}
        - {numerator * total} ÷ {denominator} = {correct_answer}
        
        **Step 3: Write the answer**
        ✓ **{correct_answer} {data['unit']}**
        
        ---
        
        ### Checking Our Answer
        
        Does this make sense?
        - {data['fraction_words']} means {numerator} out of every {denominator} parts
        - We have {total} total, divided into {denominator} groups = {total // denominator} per group
        - We need {numerator} groups = {numerator} × {total // denominator} = **{correct_answer}**
        
        ✓ Yes, our answer of **{correct_answer} {data['unit']}** is reasonable!
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