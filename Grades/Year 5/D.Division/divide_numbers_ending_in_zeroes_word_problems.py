import streamlit as st
import random

def run():
    """
    Main function to run the Divide Numbers Ending in Zeroes: Word Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/divide_numbers_ending_in_zeroes_word_problems.py
    """
    # Initialize session state
    if "word_problems_difficulty" not in st.session_state:
        st.session_state.word_problems_difficulty = 1
    
    if "current_word_problem" not in st.session_state:
        st.session_state.current_word_problem = None
        st.session_state.word_problem_answer = None
        st.session_state.word_problem_feedback = False
        st.session_state.word_problem_submitted = False
        st.session_state.word_problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("📖 Divide Numbers Ending in Zeroes: Word Problems")
    st.markdown("*Solve real-world division problems with large numbers*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_problems_difficulty
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
    if st.session_state.current_word_problem is None:
        generate_word_problem()
    
    # Display current question
    display_word_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Division Word Problems:
        
        **Step 1:** Read the problem carefully and identify:
        - What you need to find (the question)
        - The total amount (dividend)
        - The amount per group (divisor)
        
        **Step 2:** Set up the division:
        - Total ÷ Amount per group = Number of groups
        
        **Step 3:** Use the zeros strategy:
        - Remove zeros from the dividend
        - Divide the simplified numbers
        - Add the zeros back to your answer
        
        ### Example Strategy:
        **Problem:** "A school ordered 240,000 pencils. If each box contains 8,000 pencils, how many boxes did they order?"
        
        **Solution:** 240,000 ÷ 8,000
        - Remove 3 zeros from both: 240 ÷ 8 = 30
        - Answer: 30 boxes
        
        ### Types of Problems:
        - **🟡 Level 1-2:** Simple scenarios with thousands
        - **🟠 Level 3:** More complex situations
        - **🔴 Level 4-5:** Multi-step problems with millions
        
        ### Keywords to Look For:
        - "How many groups/boxes/buses/etc.?"
        - "divided equally among"
        - "each contains/holds"
        - "per person/item"
        """)

def generate_word_problem():
    """Generate a word problem based on difficulty level"""
    difficulty = st.session_state.word_problems_difficulty
    
    # Define problems by difficulty and category
    if difficulty == 1:
        # Level 1: Simple thousands
        problems = [
            {
                "scenario": "A school library received 24,000 new books. If they put 3,000 books on each shelf, how many shelves will they need?",
                "dividend": 24000, "divisor": 3000, "answer": 8, "unit": "shelves"
            },
            {
                "scenario": "A factory produces 35,000 toys per week. If they pack 7,000 toys per day, how many days does it take?",
                "dividend": 35000, "divisor": 7000, "answer": 5, "unit": "days"
            },
            {
                "scenario": "A concert venue has 48,000 seats. If each section has 6,000 seats, how many sections are there?",
                "dividend": 48000, "divisor": 6000, "answer": 8, "unit": "sections"
            },
            {
                "scenario": "A farm harvested 56,000 apples. If they put 8,000 apples in each crate, how many crates do they need?",
                "dividend": 56000, "divisor": 8000, "answer": 7, "unit": "crates"
            },
            {
                "scenario": "A delivery company has 42,000 packages to deliver. If each truck can carry 7,000 packages, how many trucks are needed?",
                "dividend": 42000, "divisor": 7000, "answer": 6, "unit": "trucks"
            }
        ]
    elif difficulty == 2:
        # Level 2: Larger thousands
        problems = [
            {
                "scenario": "A stadium sold 240,000 tickets for the season. If each game sells 8,000 tickets, how many games are there?",
                "dividend": 240000, "divisor": 8000, "answer": 30, "unit": "games"
            },
            {
                "scenario": "A warehouse stores 450,000 boxes. If each aisle holds 9,000 boxes, how many aisles are there?",
                "dividend": 450000, "divisor": 9000, "answer": 50, "unit": "aisles"
            },
            {
                "scenario": "A printing company produced 360,000 flyers. If they bundle 6,000 flyers together, how many bundles are there?",
                "dividend": 360000, "divisor": 6000, "answer": 60, "unit": "bundles"
            },
            {
                "scenario": "A zoo expects 280,000 visitors this year. If 7,000 people visit each week, how many weeks is that?",
                "dividend": 280000, "divisor": 7000, "answer": 40, "unit": "weeks"
            },
            {
                "scenario": "A company ordered 540,000 pens. If each case contains 9,000 pens, how many cases did they order?",
                "dividend": 540000, "divisor": 9000, "answer": 60, "unit": "cases"
            }
        ]
    elif difficulty == 3:
        # Level 3: Millions
        problems = [
            {
                "scenario": "The government budgeted $3,600,000 to buy new helicopters. The cost of each helicopter is $900,000. How many new helicopters will the government be able to buy?",
                "dividend": 3600000, "divisor": 900000, "answer": 4, "unit": "helicopters"
            },
            {
                "scenario": "A city planted 4,800,000 trees in a reforestation project. If they planted 600,000 trees in each district, how many districts participated?",
                "dividend": 4800000, "divisor": 600000, "answer": 8, "unit": "districts"
            },
            {
                "scenario": "A tech company manufactured 7,200,000 computer chips. If each batch contains 800,000 chips, how many batches were produced?",
                "dividend": 7200000, "divisor": 800000, "answer": 9, "unit": "batches"
            },
            {
                "scenario": "An airline transported 5,600,000 passengers last year. If each plane carries 700,000 passengers annually, how many planes do they operate?",
                "dividend": 5600000, "divisor": 700000, "answer": 8, "unit": "planes"
            },
            {
                "scenario": "A solar farm generates 6,300,000 kilowatts of energy. If each solar panel generates 700,000 kilowatts, how many solar panels are there?",
                "dividend": 6300000, "divisor": 700000, "answer": 9, "unit": "solar panels"
            }
        ]
    elif difficulty == 4:
        # Level 4: Complex scenarios with two-digit divisors
        problems = [
            {
                "scenario": "A university has 840,000 students enrolled across all campuses. If each campus has 12,000 students, how many campuses does the university have?",
                "dividend": 840000, "divisor": 12000, "answer": 70, "unit": "campuses"
            },
            {
                "scenario": "A shipping company delivered 960,000 packages last month. If each delivery route handles 16,000 packages, how many routes do they operate?",
                "dividend": 960000, "divisor": 16000, "answer": 60, "unit": "routes"
            },
            {
                "scenario": "A food bank distributed 750,000 meals this year. If each volunteer prepared 15,000 meals, how many volunteers helped?",
                "dividend": 750000, "divisor": 15000, "answer": 50, "unit": "volunteers"
            },
            {
                "scenario": "A mining operation extracted 880,000 tons of ore. If each excavator can handle 11,000 tons, how many excavators were used?",
                "dividend": 880000, "divisor": 11000, "answer": 80, "unit": "excavators"
            },
            {
                "scenario": "A telecommunications company installed 1,440,000 meters of cable. If each crew installed 18,000 meters, how many crews worked on the project?",
                "dividend": 1440000, "divisor": 18000, "answer": 80, "unit": "crews"
            }
        ]
    else:  # difficulty == 5
        # Level 5: Very large numbers and complex scenarios
        problems = [
            {
                "scenario": "A space agency's budget is $320,000,000 for satellite launches. If each launch costs $4,000,000, how many satellites can they launch?",
                "dividend": 320000000, "divisor": 4000000, "answer": 80, "unit": "satellites"
            },
            {
                "scenario": "A renewable energy project will install 15,000,000 solar panels. If each installation team can install 25,000 panels, how many teams are needed?",
                "dividend": 15000000, "divisor": 25000, "answer": 600, "unit": "teams"
            },
            {
                "scenario": "A global aid organization distributed 24,000,000 water bottles. If each shipment contained 48,000 bottles, how many shipments were sent?",
                "dividend": 24000000, "divisor": 48000, "answer": 500, "unit": "shipments"
            },
            {
                "scenario": "A data center processes 18,000,000 transactions daily. If each server handles 36,000 transactions, how many servers are running?",
                "dividend": 18000000, "divisor": 36000, "answer": 500, "unit": "servers"
            },
            {
                "scenario": "A construction project used 21,000,000 bricks. If each pallet holds 42,000 bricks, how many pallets were delivered?",
                "dividend": 21000000, "divisor": 42000, "answer": 500, "unit": "pallets"
            }
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    st.session_state.word_problem_data = problem
    st.session_state.word_problem_answer = problem["answer"]
    st.session_state.current_word_problem = problem["scenario"]

def display_word_problem():
    """Display the current word problem interface"""
    data = st.session_state.word_problem_data
    
    # Display the word problem in a clean, readable format
    st.markdown("### 📖 Word Problem:")
    
    # Display the problem text in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 10px; 
        border-left: 5px solid #28a745;
        margin: 20px 0;
        line-height: 1.6;
    ">
        <div style="font-size: 18px; color: #333;">
            {data['scenario']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input with unit
    with st.form("word_problem_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_input = st.text_input(
                f"Answer:",
                key="word_problem_input",
                placeholder="Enter your answer (numbers only)",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown(f"<div style='padding-top: 8px; font-weight: bold;'>{data['unit']}</div>", unsafe_allow_html=True)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_input:
            try:
                user_answer = int(user_input.replace(",", "").strip())
                st.session_state.word_problem_user_answer = user_answer
                st.session_state.word_problem_feedback = True
                st.session_state.word_problem_submitted = True
            except ValueError:
                st.error("Please enter a valid number")
    
    # Show feedback and next button
    handle_word_problem_feedback()

def handle_word_problem_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.word_problem_feedback:
        show_word_problem_feedback()
    
    if st.session_state.word_problem_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_word_problem_state()
                st.rerun()

def show_word_problem_feedback():
    """Display feedback for the word problem"""
    user_answer = st.session_state.word_problem_user_answer
    correct_answer = st.session_state.word_problem_answer
    data = st.session_state.word_problem_data
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent!** The answer is {correct_answer:,} {data['unit']}!")
        
        # Increase difficulty
        old_difficulty = st.session_state.word_problems_difficulty
        st.session_state.word_problems_difficulty = min(
            st.session_state.word_problems_difficulty + 1, 5
        )
        
        if st.session_state.word_problems_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered division word problems!**")
        elif old_difficulty < st.session_state.word_problems_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.word_problems_difficulty}**")
        
        show_word_problem_solution(correct=True)
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer:,} {data['unit']}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.word_problems_difficulty
        st.session_state.word_problems_difficulty = max(
            st.session_state.word_problems_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.word_problems_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.word_problems_difficulty}. Keep practicing!**")
        
        show_word_problem_solution(correct=False)

def show_word_problem_solution(correct=True):
    """Show the step-by-step solution"""
    data = st.session_state.word_problem_data
    correct_answer = st.session_state.word_problem_answer
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Step-by-Step Solution:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Extract key information from the problem
        dividend = data['dividend']
        divisor = data['divisor']
        
        st.markdown(f"""
        ### Problem Analysis:
        **Question:** {data['scenario']}
        
        ### Step 1: Identify the numbers
        - **Total amount:** {dividend:,}
        - **Amount per group:** {divisor:,}
        - **Find:** Number of groups ({data['unit']})
        
        ### Step 2: Set up the division
        **{dividend:,} ÷ {divisor:,} = ?**
        
        ### Step 3: Use the zeros strategy
        """)
        
        # Count zeros and show the strategy
        dividend_str = str(dividend)
        divisor_str = str(divisor)
        
        # Find trailing zeros
        dividend_zeros = len(dividend_str) - len(dividend_str.rstrip('0'))
        divisor_zeros = len(divisor_str) - len(divisor_str.rstrip('0'))
        
        if dividend_zeros > 0 and divisor_zeros > 0:
            # Both have zeros - can remove equal number
            zeros_removed = min(dividend_zeros, divisor_zeros)
            simplified_dividend = dividend // (10 ** zeros_removed)
            simplified_divisor = divisor // (10 ** zeros_removed)
            
            st.markdown(f"""
            - **Remove {zeros_removed} zeros from both numbers:**
            - {dividend:,} becomes **{simplified_dividend:,}**
            - {divisor:,} becomes **{simplified_divisor:,}**
            - **Divide:** {simplified_dividend:,} ÷ {simplified_divisor:,} = **{correct_answer:,}**
            """)
        else:
            # Direct division
            st.markdown(f"""
            - **Direct division:** {dividend:,} ÷ {divisor:,} = **{correct_answer:,}**
            """)
        
        st.markdown(f"""
        ### Final Answer:
        **{correct_answer:,} {data['unit']}**
        
        ### Check:
        {correct_answer:,} × {divisor:,} = {correct_answer * divisor:,} ✓
        """)

def reset_word_problem_state():
    """Reset the state for next problem"""
    st.session_state.current_word_problem = None
    st.session_state.word_problem_answer = None
    st.session_state.word_problem_feedback = False
    st.session_state.word_problem_submitted = False
    st.session_state.word_problem_data = {}
    if "word_problem_user_answer" in st.session_state:
        del st.session_state.word_problem_user_answer