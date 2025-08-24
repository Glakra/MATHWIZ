import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def run():
    """
    Main function to run the Identify Independent and Dependent Events activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/R.Probability_and_statistics/identify_independent_and_dependent_events.py
    """
    # Initialize session state
    if "independence_difficulty" not in st.session_state:
        st.session_state.independence_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.problem_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header
    st.markdown("**📚 Year 5 > R. Probability and statistics**")
    st.title("🔗 Identify Independent and Dependent Events")
    st.markdown("*Determine whether events affect each other's probability*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.independence_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Scenarios",
            2: "Complex Events",
            3: "Real-World Applications",
            4: "Advanced Concepts"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Basic')}")
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level}/4")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level == 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("📚 **Understanding Independent and Dependent Events**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🔓 Independent Events
            
            **Definition:** The outcome of the first event does NOT affect the probability of the second event.
            
            **Examples:**
            - Flipping a coin twice
            - Rolling a die twice
            - Picking a marble, **putting it back**, then picking again
            - Spinning a spinner twice
            - Drawing a card, **replacing it**, then drawing again
            
            **Key Phrases to Look For:**
            - "puts it back"
            - "with replacement"
            - "replaces the card"
            - "returns it"
            - Different random devices (coin then die)
            """)
        
        with col2:
            st.markdown("""
            ### 🔒 Dependent Events
            
            **Definition:** The outcome of the first event DOES affect the probability of the second event.
            
            **Examples:**
            - Picking two marbles **without** putting the first back
            - Drawing two cards **without** replacement
            - Eating cookies from a jar
            - Selecting team members one by one
            - Weather on consecutive days
            
            **Key Phrases to Look For:**
            - "without putting it back"
            - "without replacement"
            - "keeps the first one"
            - "removes it"
            - Events that naturally influence each other
            """)

def generate_new_problem():
    """Generate a new independence problem"""
    difficulty = st.session_state.independence_difficulty
    
    if difficulty == 1:
        problem_types = [
            "marble_with_replacement", "marble_without_replacement",
            "cards_simple", "spinner_twice", "dice_twice", "coin_twice"
        ]
    elif difficulty == 2:
        problem_types = [
            "mixed_marbles", "complex_cards", "multiple_spinners",
            "dice_and_coin", "bag_scenarios", "number_selection"
        ]
    elif difficulty == 3:
        problem_types = [
            "weather_events", "sports_scenarios", "classroom_selection",
            "game_scenarios", "shopping_events", "traffic_lights"
        ]
    else:
        problem_types = [
            "conditional_probability", "tree_diagrams", "manufacturing",
            "medical_tests", "survey_sampling", "sequential_games"
        ]
    
    problem_type = random.choice(problem_types)
    problem_data = generate_specific_problem(problem_type)
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_specific_problem(problem_type):
    """Generate specific independence problem"""
    
    if problem_type == "marble_with_replacement":
        names = ["Herman", "Sarah", "Alex", "Maya", "Jordan", "Emily"]
        name = random.choice(names)
        
        colors = ["orange", "pink", "blue", "green", "purple", "red", "yellow"]
        num_colors = random.choice([2, 3])
        selected_colors = random.sample(colors, num_colors)
        
        marbles = {}
        for color in selected_colors:
            marbles[color] = random.randint(2, 4)
        
        question = f"{name} picks a marble at random, puts it back, and then picks another marble at random."
        
        return {
            "question": question,
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "marbles",
            "visual_data": marbles,
            "correct_answer": "independent",
            "explanation": "Since the marble is put back, the first pick doesn't affect the second pick. The probabilities remain the same.",
            "problem_type": problem_type
        }
    
    elif problem_type == "marble_without_replacement":
        names = ["Josie", "Nathan", "Kai", "Sophia", "Liam", "Ava"]
        name = random.choice(names)
        
        colors = ["purple", "green", "orange", "blue", "red", "yellow"]
        num_colors = random.choice([2, 3])
        selected_colors = random.sample(colors, num_colors)
        
        marbles = {}
        for color in selected_colors:
            marbles[color] = random.randint(2, 5)
        
        question = f"{name} picks a marble at random. Without putting the first marble back, {name.split()[0].lower() if ' ' in name else 'they'} picks a second marble at random."
        
        return {
            "question": question,
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "marbles",
            "visual_data": marbles,
            "correct_answer": "dependent",
            "explanation": "Since the first marble is NOT put back, it changes the total number and composition of marbles for the second pick.",
            "problem_type": problem_type
        }
    
    elif problem_type == "cards_simple":
        names = ["Khalil", "Leo", "Valentina", "Marcus", "Isabella", "Diego"]
        name = random.choice(names)
        
        # Generate card scenarios
        num_cards = random.choice([5, 6, 7, 8])
        card_values = list(range(3, 3 + num_cards))
        
        if random.random() < 0.5:
            # With replacement
            question = f"{name} picks a card at random, puts it back, and then picks another card at random."
            answer = "independent"
            explanation = "The card is put back, so the second pick has the same options as the first."
        else:
            # Without replacement
            question = f"{name} picks a card at random. Without putting the first card back, {name.split()[0].lower() if ' ' in name else 'they'} picks a second card at random."
            answer = "dependent"
            explanation = "The first card is not returned, changing the available cards for the second pick."
        
        return {
            "question": question,
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "cards",
            "visual_data": {"cards": card_values},
            "correct_answer": answer,
            "explanation": explanation,
            "problem_type": problem_type
        }
    
    elif problem_type == "spinner_twice":
        names = ["Logan", "Emma", "Noah", "Olivia", "Ethan", "Sophia"]
        name = random.choice(names)
        
        # Create spinner configuration
        sections = {
            "section1": random.randint(3, 8),
            "section2": random.randint(3, 8),
            "section3": random.randint(3, 8),
            "section4": random.randint(3, 8)
        }
        
        question = f"{name} spins the spinner twice."
        
        return {
            "question": question,
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "spinner",
            "visual_data": sections,
            "correct_answer": "independent",
            "explanation": "Spinning a spinner doesn't change the spinner. Each spin has the same probabilities.",
            "problem_type": problem_type
        }
    
    elif problem_type == "dice_twice":
        names = ["Jake", "Mia", "Ryan", "Chloe", "Tyler", "Zoe"]
        name = random.choice(names)
        
        scenarios = [
            f"{name} rolls a die twice.",
            f"{name} rolls a die, records the number, then rolls it again.",
            f"{name} rolls two dice at the same time."
        ]
        
        question = random.choice(scenarios)
        
        return {
            "question": question,
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "dice",
            "visual_data": {},
            "correct_answer": "independent",
            "explanation": "Each die roll is independent. The first roll doesn't affect what the second roll will be.",
            "problem_type": problem_type
        }
    
    elif problem_type == "coin_twice":
        names = ["Sam", "Taylor", "Jordan", "Casey", "Morgan", "Riley"]
        name = random.choice(names)
        
        scenarios = [
            f"{name} flips a coin twice.",
            f"{name} flips two coins at the same time.",
            f"{name} flips a coin, records the result, then flips it again."
        ]
        
        question = random.choice(scenarios)
        
        return {
            "question": question,
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "coin",
            "visual_data": {},
            "correct_answer": "independent",
            "explanation": "Each coin flip is independent. The first flip doesn't affect the probability of heads or tails on the second flip.",
            "problem_type": problem_type
        }
    
    elif problem_type == "mixed_marbles":
        # Complex marble scenarios
        scenarios = [
            {
                "setup": "A bag has 5 red and 3 blue marbles.",
                "event1": "Pick a red marble",
                "event2": "Pick another red marble (with replacement)",
                "answer": "independent",
                "explanation": "With replacement means the first pick doesn't affect the second."
            },
            {
                "setup": "A jar contains 4 green and 6 yellow balls.",
                "event1": "Pick a green ball",
                "event2": "Pick a yellow ball (without replacement)",
                "answer": "dependent",
                "explanation": "Without replacement means the first pick changes what's available for the second."
            },
            {
                "setup": "Two identical bags each have 3 white and 2 black marbles.",
                "event1": "Pick a marble from bag 1",
                "event2": "Pick a marble from bag 2",
                "answer": "independent",
                "explanation": "Picking from different bags means the events don't affect each other."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']} Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "text_scenario",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "complex_cards":
        scenarios = [
            {
                "setup": "From a deck of 52 cards",
                "event1": "Draw a heart",
                "event2": "Draw a king (with replacement)",
                "answer": "independent",
                "explanation": "With replacement, the deck is the same for both draws."
            },
            {
                "setup": "From a deck of 52 cards",
                "event1": "Draw an ace",
                "event2": "Draw another ace (without replacement)",
                "answer": "dependent",
                "explanation": "Without replacement, drawing the first ace reduces the number of aces available."
            },
            {
                "setup": "From two separate decks",
                "event1": "Draw a red card from deck 1",
                "event2": "Draw a black card from deck 2",
                "answer": "independent",
                "explanation": "Drawing from different decks means the events don't affect each other."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}: Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "text_scenario",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "multiple_spinners":
        scenarios = [
            {
                "setup": "You have two identical spinners",
                "event1": "Spin the first spinner and get blue",
                "event2": "Spin the second spinner and get red",
                "answer": "independent",
                "explanation": "Different spinners operate independently of each other."
            },
            {
                "setup": "You have one spinner with moveable sections",
                "event1": "Spin and get yellow",
                "event2": "Move sections around, then spin again",
                "answer": "independent",
                "explanation": "Even though the spinner changed, the first spin doesn't affect the second spin's outcome."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "text_scenario",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "dice_and_coin":
        scenarios = [
            {
                "event1": "Roll a die and get a 6",
                "event2": "Flip a coin and get heads",
                "answer": "independent",
                "explanation": "A die roll and a coin flip are completely separate events."
            },
            {
                "event1": "Roll two dice and get a sum of 7",
                "event2": "Roll the same two dice again and get a sum of 7",
                "answer": "independent",
                "explanation": "Each roll of the dice is independent of previous rolls."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "dice_coin",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "bag_scenarios":
        scenarios = [
            {
                "setup": "A bag of 10 candies: 6 chocolate, 4 vanilla",
                "event1": "Pick a chocolate candy and eat it",
                "event2": "Pick another candy",
                "answer": "dependent",
                "explanation": "Eating the first candy changes what's left in the bag."
            },
            {
                "setup": "A bag of numbered balls (1-10)",
                "event1": "Pick ball #5, note it, and return it",
                "event2": "Pick another ball",
                "answer": "independent",
                "explanation": "Returning the ball keeps the bag contents the same."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "text_scenario",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "number_selection":
        scenarios = [
            {
                "setup": "Numbers 1-20 in a hat",
                "event1": "Draw number 13 and keep it",
                "event2": "Draw another number",
                "answer": "dependent",
                "explanation": "Keeping the first number reduces the available numbers."
            },
            {
                "setup": "Random number generator (1-100)",
                "event1": "Generate a number",
                "event2": "Generate another number",
                "answer": "independent",
                "explanation": "Each random generation is independent."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "text_scenario",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "weather_events":
        scenarios = [
            {
                "event1": "It rains on Monday",
                "event2": "It rains on Tuesday",
                "answer": "dependent",
                "explanation": "Weather patterns often persist, so rain one day affects the probability of rain the next day."
            },
            {
                "event1": "It snows in January in New York",
                "event2": "It's sunny in July in Los Angeles",
                "answer": "independent",
                "explanation": "Weather in different seasons and locations are essentially independent."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "weather",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "sports_scenarios":
        scenarios = [
            {
                "event1": "A basketball player makes their first free throw",
                "event2": "The same player makes their second free throw",
                "answer": "independent",
                "explanation": "Each free throw is a separate attempt with the same probability (though psychology might play a role in real life)."
            },
            {
                "event1": "Team A wins the first game of a series",
                "event2": "Team A has home advantage in game 2",
                "answer": "dependent",
                "explanation": "In many sports series, winning affects home/away scheduling."
            },
            {
                "event1": "A soccer player scores a penalty",
                "event2": "A different player scores the next penalty",
                "answer": "independent",
                "explanation": "Different players taking penalties are independent events."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "sports",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "classroom_selection":
        scenarios = [
            {
                "setup": "30 students in a class",
                "event1": "Select a student for team captain",
                "event2": "Select another student for co-captain",
                "answer": "dependent",
                "explanation": "The first student selected can't be selected again, changing the pool."
            },
            {
                "setup": "Two different classes",
                "event1": "Pick a student from Class A",
                "event2": "Pick a student from Class B",
                "answer": "independent",
                "explanation": "Selecting from different classes means the events don't affect each other."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "classroom",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "game_scenarios":
        scenarios = [
            {
                "setup": "Playing cards game",
                "event1": "Player 1 is dealt an ace",
                "event2": "Player 2 is dealt an ace",
                "answer": "dependent",
                "explanation": "Cards dealt to Player 1 aren't available for Player 2."
            },
            {
                "setup": "Online game with random loot",
                "event1": "Find a rare item in chest 1",
                "event2": "Find a rare item in chest 2",
                "answer": "independent",
                "explanation": "Each chest has independent random generation."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "game",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "shopping_events":
        scenarios = [
            {
                "event1": "The price of gas increases",
                "event2": "Fewer people drive to the mall",
                "answer": "dependent",
                "explanation": "Higher gas prices can affect people's driving decisions."
            },
            {
                "event1": "Store A has a sale",
                "event2": "Store B (different mall) has a sale",
                "answer": "independent",
                "explanation": "Sales at unrelated stores are typically independent."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "shopping",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "traffic_lights":
        scenarios = [
            {
                "event1": "Hit a red light at 1st Street",
                "event2": "Hit a red light at 2nd Street (synchronized lights)",
                "answer": "dependent",
                "explanation": "Synchronized traffic lights are designed to be dependent."
            },
            {
                "event1": "Hit a red light at Main Street",
                "event2": "Hit a red light across town at Park Avenue",
                "answer": "independent",
                "explanation": "Traffic lights far apart operate independently."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "traffic",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    # Level 4 - Advanced
    elif problem_type == "conditional_probability":
        scenarios = [
            {
                "setup": "In a school, 60% play sports, 40% play music",
                "event1": "A student plays sports",
                "event2": "The same student plays music",
                "answer": "independent",
                "explanation": "Without additional information linking sports and music, we assume independence."
            },
            {
                "setup": "Drawing from a deck where all hearts have been removed",
                "event1": "Draw a red card",
                "event2": "Draw a diamond",
                "answer": "dependent",
                "explanation": "If you draw a red card, it must be a diamond (since hearts are removed)."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "text_scenario",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "tree_diagrams":
        scenarios = [
            {
                "setup": "A two-stage process",
                "event1": "Pass the first quality check",
                "event2": "Pass the second quality check",
                "answer": "independent",
                "explanation": "Typically, quality checks are independent tests."
            },
            {
                "setup": "Genetic inheritance",
                "event1": "Child has brown eyes",
                "event2": "Child has brown hair",
                "answer": "dependent",
                "explanation": "Genetic traits can be linked and inherited together."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "text_scenario",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "manufacturing":
        scenarios = [
            {
                "setup": "Assembly line with two machines",
                "event1": "Machine A produces a defective part",
                "event2": "Machine B produces a defective part",
                "answer": "independent",
                "explanation": "Different machines typically fail independently."
            },
            {
                "setup": "Sequential processing",
                "event1": "Part fails initial inspection",
                "event2": "Part is scrapped",
                "answer": "dependent",
                "explanation": "Failed parts are more likely to be scrapped."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "manufacturing",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "medical_tests":
        scenarios = [
            {
                "event1": "Test positive for condition A",
                "event2": "Test positive for unrelated condition B",
                "answer": "independent",
                "explanation": "Unrelated medical conditions are independent."
            },
            {
                "event1": "Have high blood pressure",
                "event2": "Have heart disease",
                "answer": "dependent",
                "explanation": "High blood pressure increases risk of heart disease."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "medical",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "survey_sampling":
        scenarios = [
            {
                "setup": "Phone survey",
                "event1": "First person answers the phone",
                "event2": "Second person (different household) answers",
                "answer": "independent",
                "explanation": "Different households are independent."
            },
            {
                "setup": "Survey with screening question",
                "event1": "Person qualifies on screening question",
                "event2": "Person completes the full survey",
                "answer": "dependent",
                "explanation": "Must qualify to continue the survey."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "survey",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    elif problem_type == "sequential_games":
        scenarios = [
            {
                "setup": "Tournament bracket",
                "event1": "Win in round 1",
                "event2": "Play in round 2",
                "answer": "dependent",
                "explanation": "Must win round 1 to advance to round 2."
            },
            {
                "setup": "Lottery drawings on different days",
                "event1": "Win Monday's lottery",
                "event2": "Win Friday's lottery",
                "answer": "independent",
                "explanation": "Separate lottery drawings are independent."
            }
        ]
        
        scenario = random.choice(scenarios)
        
        return {
            "question": f"{scenario['setup']}. Event 1: {scenario['event1']}. Event 2: {scenario['event2']}.",
            "prompt": "Are these two events dependent or independent?",
            "visual_type": "game",
            "visual_data": {},
            "correct_answer": scenario["answer"],
            "explanation": scenario["explanation"],
            "problem_type": problem_type
        }
    
    # Default fallback
    return generate_specific_problem("marble_with_replacement")

def display_problem():
    """Display the current problem with visualization"""
    data = st.session_state.problem_data
    
    # Display the scenario
    st.markdown(f"### 📝 Scenario {st.session_state.total_attempted + 1}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    # Display visualization
    visual_type = data.get("visual_type", "text_scenario")
    
    if visual_type == "marbles":
        display_marbles(data["visual_data"])
    elif visual_type == "cards":
        display_cards(data["visual_data"])
    elif visual_type == "spinner":
        display_spinner(data["visual_data"])
    elif visual_type == "dice":
        display_dice()
    elif visual_type == "coin":
        display_coin()
    elif visual_type == "dice_coin":
        display_dice_and_coin()
    elif visual_type == "weather":
        display_weather_icon()
    elif visual_type == "sports":
        display_sports_icon()
    elif visual_type == "classroom":
        display_classroom_icon()
    elif visual_type == "game":
        display_game_icon()
    elif visual_type == "shopping":
        display_shopping_icon()
    elif visual_type == "traffic":
        display_traffic_icon()
    elif visual_type == "manufacturing":
        display_manufacturing_icon()
    elif visual_type == "medical":
        display_medical_icon()
    elif visual_type == "survey":
        display_survey_icon()
    
    st.markdown("---")
    
    # Display the question
    st.markdown(f"**{data['prompt']}**")
    
    # Answer buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(
            "dependent",
            key="dependent_btn",
            use_container_width=True,
            type="secondary" if not st.session_state.answer_submitted else "primary" if st.session_state.user_answer == "dependent" else "secondary",
            disabled=st.session_state.answer_submitted
        ):
            st.session_state.user_answer = "dependent"
            check_answer()
    
    with col2:
        if st.button(
            "independent", 
            key="independent_btn",
            use_container_width=True,
            type="secondary" if not st.session_state.answer_submitted else "primary" if st.session_state.user_answer == "independent" else "secondary",
            disabled=st.session_state.answer_submitted
        ):
            st.session_state.user_answer = "independent"
            check_answer()
    
    with col3:
        if st.button("Skip", type="secondary", disabled=st.session_state.answer_submitted):
            st.session_state.user_answer = None
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.rerun()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Navigation
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📖 Learn More", type="secondary", use_container_width=True):
                show_detailed_explanation()
            
            if st.button("Next Problem →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%")

def display_marbles(config):
    """Display marble visualization"""
    colors_map = {
        "red": "#FF6B6B",
        "blue": "#4DABF7",
        "green": "#51CF66",
        "yellow": "#FFD43B",
        "purple": "#9775FA",
        "orange": "#FF922B",
        "pink": "#FFB6C1",
        "white": "#F8F9FA",
        "brown": "#8B4513"
    }
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Calculate positions
    total_marbles = sum(config.values())
    cols = min(6, total_marbles)
    rows = (total_marbles + cols - 1) // cols
    
    # Draw marbles
    marble_index = 0
    for color, count in config.items():
        for _ in range(count):
            row = marble_index // cols
            col = marble_index % cols
            
            circle = plt.Circle(
                (col * 1.2 + 0.6, rows - row - 0.5),
                0.4,
                color=colors_map.get(color, "#CCCCCC"),
                ec='black',
                linewidth=2
            )
            ax.add_patch(circle)
            marble_index += 1
    
    ax.set_xlim(0, cols * 1.2)
    ax.set_ylim(0, max(rows, 1))
    ax.set_aspect('equal')
    ax.axis('off')
    
    st.pyplot(fig)
    plt.close()

def display_cards(data):
    """Display cards visualization"""
    cards = data.get("cards", [3, 4, 5, 6, 7])
    
    colors = ["#90EE90", "#9370DB", "#87CEEB", "#FFD700", "#90EE90", "#87CEEB", "#FFA500"]
    
    fig, ax = plt.subplots(figsize=(8, 2))
    
    for i, card in enumerate(cards):
        # Draw card rectangle
        rect = patches.Rectangle(
            (i * 1.5, 0), 1.2, 1.8,
            linewidth=2, edgecolor='black',
            facecolor=colors[i % len(colors)]
        )
        ax.add_patch(rect)
        
        # Add card number
        ax.text(i * 1.5 + 0.6, 0.9, str(card),
                ha='center', va='center',
                fontsize=20, fontweight='bold',
                color='white')
    
    ax.set_xlim(-0.2, len(cards) * 1.5)
    ax.set_ylim(-0.2, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    st.pyplot(fig)
    plt.close()

def display_spinner(sections):
    """Display spinner visualization"""
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Create spinner sections with numbers
    total = sum(sections.values())
    sizes = list(sections.values())
    colors = ["#87CEEB", "#90EE90", "#9370DB", "#90EE90"]
    
    wedges, texts = ax.pie(
        sizes,
        labels=[str(v) for v in sections.values()],
        colors=colors,
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 2}
    )
    
    # Make text bigger
    for text in texts:
        text.set_fontsize(14)
        text.set_fontweight('bold')
    
    # Add center dot
    centre_circle = plt.Circle((0, 0), 0.1, fc='black')
    ax.add_artist(centre_circle)
    
    ax.set_aspect('equal')
    st.pyplot(fig)
    plt.close()

def display_dice():
    """Display dice icon"""
    st.info("🎲 **Rolling a standard 6-sided die**")

def display_coin():
    """Display coin icon"""
    st.info("🪙 **Flipping a fair coin (Heads/Tails)**")

def display_dice_and_coin():
    """Display dice and coin"""
    st.info("🎲🪙 **Rolling dice and flipping coins**")

def display_weather_icon():
    """Display weather scenario"""
    st.info("🌦️ **Weather Events**")

def display_sports_icon():
    """Display sports scenario"""
    st.info("⚽🏀 **Sports Events**")

def display_classroom_icon():
    """Display classroom scenario"""
    st.info("👥 **Classroom Selection**")

def display_game_icon():
    """Display game scenario"""
    st.info("🎮 **Game Events**")

def display_shopping_icon():
    """Display shopping scenario"""
    st.info("🛒 **Shopping/Economic Events**")

def display_traffic_icon():
    """Display traffic scenario"""
    st.info("🚦 **Traffic Light Events**")

def display_manufacturing_icon():
    """Display manufacturing scenario"""
    st.info("🏭 **Manufacturing Process**")

def display_medical_icon():
    """Display medical scenario"""
    st.info("⚕️ **Medical/Health Events**")

def display_survey_icon():
    """Display survey scenario"""
    st.info("📊 **Survey/Research Events**")

def check_answer():
    """Check the user's answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    
    st.session_state.answer_correct = (user_answer == correct_answer)
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1
    
    if st.session_state.answer_correct:
        st.session_state.total_correct += 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.problem_data
    
    if st.session_state.user_answer is None:
        st.info(f"⏭️ **Skipped.** The correct answer was **{data['correct_answer']}**")
        st.markdown(f"📚 {data['explanation']}")
    elif st.session_state.answer_correct:
        st.success(f"✅ **Correct! These events are {data['correct_answer']}.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.independence_difficulty
            st.session_state.independence_difficulty = min(
                st.session_state.independence_difficulty + 1, 4
            )
            
            if st.session_state.independence_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Excellent! Moving to Level {st.session_state.independence_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite. You said {st.session_state.user_answer}, but these events are {data['correct_answer']}.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.independence_difficulty
            st.session_state.independence_difficulty = max(
                st.session_state.independence_difficulty - 1, 1
            )
            
            if st.session_state.independence_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.independence_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_detailed_explanation():
    """Show detailed explanation of independence"""
    with st.expander("📚 **Understanding Why**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown(f"### This scenario is **{data['correct_answer'].upper()}**")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        
        if data['correct_answer'] == 'independent':
            st.markdown("""
            ### 🔓 Why These Events Are Independent:
            
            **Key Question:** Does the outcome of the first event change the probability of the second event?
            
            **Answer:** NO - The probabilities remain the same.
            
            **Common Independent Scenarios:**
            - **With Replacement:** The item is returned, keeping probabilities constant
            - **Different Sources:** Events from separate, unconnected sources
            - **Random Devices:** Coins, dice, spinners - each use is fresh
            - **Separate Populations:** Selecting from different groups
            
            **Mathematical Test:**
            P(Event 2 | Event 1 happened) = P(Event 2)
            
            The probability of Event 2 is the same whether or not Event 1 happened.
            """)
        else:
            st.markdown("""
            ### 🔒 Why These Events Are Dependent:
            
            **Key Question:** Does the outcome of the first event change the probability of the second event?
            
            **Answer:** YES - The probabilities change based on what happened first.
            
            **Common Dependent Scenarios:**
            - **Without Replacement:** Items are removed, changing the remaining pool
            - **Sequential Selection:** Choosing items one after another from the same group
            - **Cause and Effect:** One event influences the likelihood of another
            - **Shared Resources:** Events competing for the same limited resource
            
            **Mathematical Test:**
            P(Event 2 | Event 1 happened) ≠ P(Event 2)
            
            The probability of Event 2 changes based on the outcome of Event 1.
            """)

def reset_problem_state():
    """Reset for next problem"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.problem_data = {}
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None
    if 'answer_correct' in st.session_state:
        del st.session_state.answer_correct