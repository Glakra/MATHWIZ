import streamlit as st
import random

def run():
    """
    Main function to run the Divisibility Rules: Word Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/divisibility_rules_word_problems.py
    """
    # Initialize session state
    if "div_word_difficulty" not in st.session_state:
        st.session_state.div_word_difficulty = 1
    
    if "current_div_word_problem" not in st.session_state:
        st.session_state.current_div_word_problem = None
        st.session_state.div_word_answer = None
        st.session_state.div_word_feedback = False
        st.session_state.div_word_submitted = False
        st.session_state.div_word_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("📝 Divisibility Rules: Word Problems")
    st.markdown("*Apply divisibility rules to solve real-world problems*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.div_word_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
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
    
    # Generate new question if needed
    if st.session_state.current_div_word_problem is None:
        generate_div_word_problem()
    
    # Display current question
    display_div_word_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Problem-Solving Strategy & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Divisibility Word Problems:
        
        #### **Step 1: Identify the Key Information**
        - **What number** needs to be divided?
        - **What are we dividing by** (groups, people, items)?
        - **What condition** must be met (equal groups, no remainder)?
        
        #### **Step 2: Apply Divisibility Rules**
        - **Divisibility by 2:** Even numbers (ends in 0,2,4,6,8)
        - **Divisibility by 3:** Sum of digits divisible by 3
        - **Divisibility by 4:** Last two digits divisible by 4
        - **Divisibility by 5:** Ends in 0 or 5
        - **Divisibility by 6:** Divisible by both 2 AND 3
        - **Divisibility by 8:** Last three digits divisible by 8
        - **Divisibility by 9:** Sum of digits divisible by 9
        - **Divisibility by 10:** Ends in 0
        
        #### **Step 3: Check Each Option**
        - Test each answer choice using the appropriate rule
        - Look for patterns and shortcuts
        - Eliminate impossible answers first
        
        ### **Example Problem:**
        **"240 students need to be divided into equal groups. Which group sizes are possible?"**
        
        **Analysis:**
        - Number to divide: 240
        - Need: Equal groups (no remainder)
        - Check: Which numbers divide 240 evenly?
        
        **Testing:**
        - **240 ÷ 5:** 240 ends in 0 → ✅ Divisible by 5
        - **240 ÷ 8:** Last three digits 240 → 240÷8=30 → ✅ Divisible by 8
        - **240 ÷ 12:** 240 is even ✅ and 2+4+0=6 (÷3) ✅ → ✅ Divisible by 12
        
        ### **Common Scenarios:**
        - **Elections/Voting:** Equal distribution of votes
        - **Classroom Organization:** Students in equal groups
        - **Sports Teams:** Players divided equally
        - **Packaging:** Items in equal containers
        - **Money Distribution:** Equal shares
        - **Event Planning:** Equal table arrangements
        - **Transportation:** Equal passengers per vehicle
        
        ### **Quick Elimination Tips:**
        - **Odd numbers** can't be divided by any even number
        - **Numbers not ending in 0 or 5** can't be divided by 5
        - **If sum of digits isn't divisible by 3**, not divisible by 3,6,9,12
        - **Large numbers** often have more factors than small ones
        """)

def generate_div_word_problem():
    """Generate a divisibility word problem based on difficulty level"""
    difficulty = st.session_state.div_word_difficulty
    
    if difficulty == 1:
        # Level 1: Simple divisibility by 2, 5, 10
        problems = [
            {
                "story": "Mrs. Chen has 120 stickers to share equally among her students. Which of these group sizes would work?",
                "number": 120,
                "context": "sharing stickers",
                "options": [4, 7, 5, 11],
                "correct": 5,
                "explanation": "120 ends in 0, so it's divisible by 5. 120 ÷ 5 = 24 students per group."
            },
            {
                "story": "A bakery made 84 cupcakes to pack in boxes. Each box must have the same number of cupcakes. How many cupcakes could go in each box?",
                "number": 84,
                "context": "packing cupcakes",
                "options": [6, 5, 7, 9],
                "correct": 6,
                "explanation": "84 is even (divisible by 2) and 8+4=12 (divisible by 3), so 84 is divisible by 6. 84 ÷ 6 = 14 cupcakes per box."
            },
            {
                "story": "The school has 150 students for a field trip. They want to divide into equal groups. Which group size is possible?",
                "number": 150,
                "context": "organizing field trip",
                "options": [4, 10, 7, 8],
                "correct": 10,
                "explanation": "150 ends in 0, so it's divisible by 10. 150 ÷ 10 = 15 students per group."
            },
            {
                "story": "A farmer has 96 apples to put in baskets. Each basket must have the same number of apples. How many apples could go in each basket?",
                "number": 96,
                "context": "organizing apples",
                "options": [8, 5, 7, 11],
                "correct": 8,
                "explanation": "For divisibility by 8, check last three digits: 096. Since 96 ÷ 8 = 12, 96 is divisible by 8."
            }
        ]
    
    elif difficulty == 2:
        # Level 2: Divisibility by 3, 4, 6, 9
        problems = [
            {
                "story": "2800 people voted in the Wellington City Council election. Each candidate received the exact same number of votes. How many city council candidates could there have been?",
                "number": 2800,
                "context": "election votes",
                "options": [3, 6, 10, 9],
                "correct": 10,
                "explanation": "2800 ends in 0, so it's divisible by 10. 2800 ÷ 10 = 280 votes per candidate."
            },
            {
                "story": "A library has 432 books to arrange on shelves. Each shelf must have the same number of books. How many books could go on each shelf?",
                "number": 432,
                "context": "arranging books",
                "options": [9, 5, 7, 11],
                "correct": 9,
                "explanation": "Sum of digits: 4+3+2=9. Since 9 is divisible by 9, 432 is divisible by 9. 432 ÷ 9 = 48 books per shelf."
            },
            {
                "story": "A theater has 276 seats arranged in equal rows. Which number of seats per row is possible?",
                "number": 276,
                "context": "theater seating",
                "options": [12, 5, 8, 7],
                "correct": 12,
                "explanation": "276 is even and 2+7+6=15 (divisible by 3), so 276 is divisible by 6. Also, 76 ÷ 4 = 19, so it's divisible by 4. Since it's divisible by both 3 and 4, it's divisible by 12."
            },
            {
                "story": "A chocolate factory made 168 chocolates to pack in gift boxes. Each box must contain the same number of chocolates. How many chocolates could be in each box?",
                "number": 168,
                "context": "packing chocolates",
                "options": [6, 5, 7, 9],
                "correct": 6,
                "explanation": "168 is even and 1+6+8=15 (divisible by 3), so 168 is divisible by 6. 168 ÷ 6 = 28 chocolates per box."
            }
        ]
    
    elif difficulty == 3:
        # Level 3: Multiple factors and larger numbers
        problems = [
            {
                "story": "A concert venue sold 1440 tickets. The organizers want to divide attendees into equal sections. Which section size would work?",
                "number": 1440,
                "context": "concert seating",
                "options": [16, 13, 17, 19],
                "correct": 16,
                "explanation": "1440 ÷ 16: Check by dividing. 1440 ÷ 16 = 90, so 16 people per section works perfectly."
            },
            {
                "story": "A shipping company has 864 packages to load equally onto trucks. How many packages could go on each truck?",
                "number": 864,
                "context": "loading packages",
                "options": [12, 13, 14, 15],
                "correct": 12,
                "explanation": "864 is even and 8+6+4=18 (divisible by 3), so divisible by 6. Also, 64 ÷ 4 = 16, so divisible by 4. Since divisible by both 3 and 4, it's divisible by 12."
            },
            {
                "story": "A sports tournament has 720 participants forming equal teams. Which team size is possible?",
                "number": 720,
                "context": "sports teams",
                "options": [15, 13, 17, 19],
                "correct": 15,
                "explanation": "720 ends in 0 (divisible by 5) and 7+2+0=9 (divisible by 3), so 720 is divisible by 15. 720 ÷ 15 = 48 teams."
            },
            {
                "story": "A factory produces 936 items per day and packages them in equal batches. How many items could be in each batch?",
                "number": 936,
                "context": "factory production",
                "options": [18, 13, 17, 19],
                "correct": 18,
                "explanation": "936 is even and 9+3+6=18 (divisible by 9), so 936 is divisible by 18. 936 ÷ 18 = 52 items per batch."
            }
        ]
    
    elif difficulty == 4:
        # Level 4: Complex scenarios with larger numbers
        problems = [
            {
                "story": "A tech company has 1848 employees to organize into project teams. Each team must have the same number of members. Which team size would work?",
                "number": 1848,
                "context": "organizing employees",
                "options": [22, 21, 23, 25],
                "correct": 21,
                "explanation": "1848 ÷ 21: Check digit sum 1+8+4+8=21, which is divisible by 3. Also, 1848 ÷ 3 = 616, and 616 ÷ 7 = 88, so 1848 = 3×7×88 = 21×88."
            },
            {
                "story": "A school fundraiser collected $2376. The money will be divided equally among classes. How much could each class receive?",
                "number": 2376,
                "context": "distributing money",
                "options": ["$22", "$24", "$26", "$28"],
                "correct": "$24",
                "explanation": "2376 is even and 2+3+7+6=18 (divisible by 9), making it divisible by 18. Also divisible by other factors. 2376 ÷ 24 = 99 classes."
            },
            {
                "story": "A delivery service has 1980 parcels to distribute equally across distribution centers. How many parcels could each center handle?",
                "number": 1980,
                "context": "parcel distribution",
                "options": [30, 31, 32, 33],
                "correct": 30,
                "explanation": "1980 ends in 0 (divisible by 10) and 1+9+8+0=18 (divisible by 3), so it's divisible by 30. 1980 ÷ 30 = 66 parcels per center."
            },
            {
                "story": "An online retailer processed 1512 orders and wants to assign them equally to customer service reps. How many orders could each rep handle?",
                "number": 1512,
                "context": "customer service",
                "options": [36, 35, 37, 38],
                "correct": 36,
                "explanation": "1512 is even, 1+5+1+2=9 (divisible by 9), and last two digits 12 ÷ 4 = 3, so divisible by 4. Since divisible by 4 and 9, it's divisible by 36."
            }
        ]
    
    else:  # difficulty == 5
        # Level 5: Very challenging scenarios
        problems = [
            {
                "story": "A massive outdoor festival expects 4620 attendees. Security teams of equal size will be stationed throughout. Which team size is feasible?",
                "number": 4620,
                "context": "security planning",
                "options": [42, 41, 43, 45],
                "correct": 42,
                "explanation": "4620 is even, 4+6+2+0=12 (divisible by 3), last two digits 20 ÷ 4 = 5, and ends in 0 (divisible by 5). Since divisible by 2, 3, and 7, it's divisible by 42."
            },
            {
                "story": "A data center needs to allocate 5544 processing tasks equally across servers. How many tasks could each server handle?",
                "number": 5544,
                "context": "server allocation",
                "options": [56, 55, 57, 58],
                "correct": 56,
                "explanation": "5544 ÷ 56: 5544 is divisible by 8 (544 ÷ 8 = 68) and by 7. Since 56 = 8 × 7, and 5544 ÷ 56 = 99, this works."
            },
            {
                "story": "A logistics company has 3960 items to pack equally into shipping containers. How many items could fit in each container?",
                "number": 3960,
                "context": "shipping logistics",
                "options": [44, 45, 46, 47],
                "correct": 44,
                "explanation": "3960 is even, 3+9+6+0=18 (divisible by 9), last two digits 60 ÷ 4 = 15. Testing: 3960 ÷ 44 = 90 containers exactly."
            },
            {
                "story": "A university assigns 6048 students to dormitory floors with equal numbers per floor. How many students could be on each floor?",
                "number": 6048,
                "context": "dormitory assignment",
                "options": [63, 64, 65, 66],
                "correct": 63,
                "explanation": "6048 ÷ 63: Sum of digits 6+0+4+8=18 (divisible by 9). Also, 6048 ÷ 9 = 672, and 672 ÷ 7 = 96, so 6048 = 9×7×96 = 63×96."
            }
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    # Shuffle options to make the correct answer appear in different positions
    options = problem["options"].copy()
    random.shuffle(options)
    
    st.session_state.div_word_data = {
        "story": problem["story"],
        "number": problem["number"],
        "context": problem["context"],
        "options": options,
        "correct": problem["correct"],
        "explanation": problem["explanation"]
    }
    st.session_state.div_word_answer = problem["correct"]
    st.session_state.current_div_word_problem = problem["story"]

def display_div_word_problem():
    """Display the current divisibility word problem with clickable tiles"""
    data = st.session_state.div_word_data
    story = data["story"]
    options = data["options"]
    
    # Initialize selected option in session state if not exists
    if "div_word_selected_option" not in st.session_state:
        st.session_state.div_word_selected_option = None
    
    # Display the word problem with clear formatting
    st.markdown("### 📖 Word Problem:")
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #4CAF50;
        font-size: 16px;
        line-height: 1.6;
        margin: 20px 0;
        color: #2c3e50;
    ">
        {story}
    </div>
    """, unsafe_allow_html=True)
    
    # Create clickable tiles in a 2x2 grid
    row1_col1, row1_col2 = st.columns(2, gap="medium")
    row2_col1, row2_col2 = st.columns(2, gap="medium")
    columns = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    # Display each option as a clickable tile
    for i, option in enumerate(options):
        with columns[i]:
            # Determine if this tile is selected
            is_selected = st.session_state.div_word_selected_option == option
            
            # Create button with conditional styling
            button_type = "primary" if is_selected else "secondary"
            button_text = f"✅ {option}" if is_selected else str(option)
            
            if st.button(
                button_text,
                key=f"word_tile_{i}",
                use_container_width=True,
                type=button_type,
                help=f"Click to select: {option}"
            ):
                st.session_state.div_word_selected_option = option
                st.rerun()
    
    # Show current selection status
    st.markdown("")
    if st.session_state.div_word_selected_option:
        st.success(f"**Selected:** {st.session_state.div_word_selected_option}")
    else:
        st.info("👆 **Click on one of the options above to select your answer**")
    
    # Submit section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button(
            "✅ Submit", 
            type="primary", 
            use_container_width=True,
            disabled=st.session_state.div_word_selected_option is None
        )
    
    # Handle submission
    if submit_button and st.session_state.div_word_selected_option:
        st.session_state.div_word_user_answer = st.session_state.div_word_selected_option
        st.session_state.div_word_feedback = True
        st.session_state.div_word_submitted = True
        st.rerun()
    
    # Show feedback and next button
    handle_div_word_feedback()

def handle_div_word_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("div_word_feedback", False):
        show_div_word_feedback()
    
    if st.session_state.get("div_word_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_div_word_state()
                st.rerun()

def show_div_word_feedback():
    """Display feedback for the divisibility word problem"""
    user_answer = st.session_state.get("div_word_user_answer")
    correct_answer = st.session_state.get("div_word_answer")
    data = st.session_state.get("div_word_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    number = data["number"]
    context = data["context"]
    explanation = data["explanation"]
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent!** {correct_answer} is the correct answer.")
        
        # Increase difficulty
        old_difficulty = st.session_state.div_word_difficulty
        st.session_state.div_word_difficulty = min(
            st.session_state.div_word_difficulty + 1, 5
        )
        
        if st.session_state.div_word_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered divisibility word problems!**")
        elif old_difficulty < st.session_state.div_word_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.div_word_difficulty}**")
        
        show_div_word_explanation(correct=True)
    
    else:
        st.error(f"❌ **Not quite.** The correct answer is **{correct_answer}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.div_word_difficulty
        st.session_state.div_word_difficulty = max(
            st.session_state.div_word_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.div_word_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.div_word_difficulty}. Keep practicing!**")
        
        show_div_word_explanation(correct=False)

def show_div_word_explanation(correct=True):
    """Show explanation for the divisibility word problem"""
    data = st.session_state.get("div_word_data", {})
    correct_answer = st.session_state.get("div_word_answer")
    user_answer = st.session_state.get("div_word_user_answer")
    
    if not data or correct_answer is None:
        return
        
    number = data["number"]
    context = data["context"]
    explanation = data["explanation"]
    options = data["options"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Problem Solution:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Number to work with: {number:,}
        ### Context: {context}
        ### Correct Answer: **{correct_answer}**
        
        ### Why this answer is correct:
        {explanation}
        
        ### Let's check all options:
        """)
        
        # Check each option and explain why it's right or wrong
        for option in options:
            # Remove $ or other prefixes for calculation
            clean_option = str(option).replace('$', '')
            try:
                option_num = int(clean_option)
                is_divisible = number % option_num == 0
                
                if option == correct_answer:
                    quotient = number // option_num
                    st.markdown(f"- **{option}** ✅ **CORRECT**: {number:,} ÷ {option_num} = {quotient:,} (exactly, no remainder)")
                else:
                    if is_divisible:
                        quotient = number // option_num
                        st.markdown(f"- **{option}** ❌ **Also works mathematically**: {number:,} ÷ {option_num} = {quotient:,}, but not the answer we're looking for in this context")
                    else:
                        quotient = number // option_num
                        remainder = number % option_num
                        st.markdown(f"- **{option}** ❌ **Doesn't work**: {number:,} ÷ {option_num} = {quotient:,} remainder {remainder}")
            except:
                st.markdown(f"- **{option}** ❌ Could not evaluate")
        
        # Show divisibility rule used
        st.markdown(f"""
        ### 🔍 Divisibility Rules Applied:
        
        To check if {number:,} is divisible by {str(correct_answer).replace('$', '')}:
        """)
        
        # Show specific rule application
        clean_correct = int(str(correct_answer).replace('$', ''))
        show_divisibility_check(number, clean_correct)

def show_divisibility_check(number, divisor):
    """Show how to check divisibility using rules"""
    if divisor == 2:
        st.markdown(f"- **Rule for 2**: Number must be even (end in 0,2,4,6,8)")
        st.markdown(f"- **Check**: {number} ends in {number % 10} → {'✅ Even' if number % 2 == 0 else '❌ Odd'}")
    
    elif divisor == 3:
        digit_sum = sum(int(d) for d in str(number))
        st.markdown(f"- **Rule for 3**: Sum of digits must be divisible by 3")
        st.markdown(f"- **Check**: {'+'.join(str(number))} = {digit_sum} → {digit_sum} ÷ 3 = {digit_sum/3}")
    
    elif divisor == 4:
        last_two = number % 100
        st.markdown(f"- **Rule for 4**: Last two digits must be divisible by 4")
        st.markdown(f"- **Check**: Last two digits = {last_two:02d} → {last_two} ÷ 4 = {last_two/4}")
    
    elif divisor == 5:
        st.markdown(f"- **Rule for 5**: Number must end in 0 or 5")
        st.markdown(f"- **Check**: {number} ends in {number % 10} → {'✅ Divisible' if number % 10 in [0,5] else '❌ Not divisible'}")
    
    elif divisor == 6:
        is_even = number % 2 == 0
        digit_sum = sum(int(d) for d in str(number))
        div_by_3 = digit_sum % 3 == 0
        st.markdown(f"- **Rule for 6**: Must be divisible by both 2 AND 3")
        st.markdown(f"- **Check**: Even? {'✅' if is_even else '❌'} | Sum of digits = {digit_sum} ({'✅ ÷3' if div_by_3 else '❌ not ÷3'})")
    
    elif divisor == 8:
        last_three = number % 1000
        st.markdown(f"- **Rule for 8**: Last three digits must be divisible by 8")
        st.markdown(f"- **Check**: Last three digits = {last_three:03d} → {last_three} ÷ 8 = {last_three/8}")
    
    elif divisor == 9:
        digit_sum = sum(int(d) for d in str(number))
        st.markdown(f"- **Rule for 9**: Sum of digits must be divisible by 9")
        st.markdown(f"- **Check**: {'+'.join(str(number))} = {digit_sum} → {digit_sum} ÷ 9 = {digit_sum/9}")
    
    elif divisor == 10:
        st.markdown(f"- **Rule for 10**: Number must end in 0")
        st.markdown(f"- **Check**: {number} ends in {number % 10} → {'✅ Divisible' if number % 10 == 0 else '❌ Not divisible'}")
    
    else:
        # For other numbers, do the division
        quotient = number // divisor
        remainder = number % divisor
        st.markdown(f"- **Direct division**: {number:,} ÷ {divisor} = {quotient:,}")
        if remainder == 0:
            st.markdown(f"- **Result**: Exactly {quotient:,} with no remainder ✅")
        else:
            st.markdown(f"- **Result**: {quotient:,} remainder {remainder} ❌")

def reset_div_word_state():
    """Reset the state for next problem"""
    st.session_state.current_div_word_problem = None
    st.session_state.div_word_answer = None
    st.session_state.div_word_feedback = False
    st.session_state.div_word_submitted = False
    st.session_state.div_word_data = {}
    st.session_state.div_word_selected_option = None  # Reset selection
    
    if "div_word_user_answer" in st.session_state:
        del st.session_state.div_word_user_answer