import streamlit as st
import random

def run():
    """
    Main function to run the Find the order activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/L.Problem_solving/find_the_order.py
    """
    # Initialize session state
    if "order_difficulty" not in st.session_state:
        st.session_state.order_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > L. Problem solving**")
    st.title("🔢 Find the Order")
    st.markdown("*Use logical thinking to determine the correct order*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.order_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Intermediate", "Advanced", "Complex", "Master"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level-1]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Easy**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_order_problem()
    
    # Display current problem
    display_order_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Solve Ordering Problems**", expanded=False):
        st.markdown("""
        ### Understanding Order Problems:
        
        **Key Words to Watch For:**
        - **More/Less than**: A > B or A < B
        - **Farther/Closer than**: Distance comparisons
        - **Taller/Shorter than**: Height comparisons
        - **Before/After**: Time or sequence
        - **Not** (reverses the meaning!)
        
        ### Problem-Solving Steps:
        
        **1. Identify the relationships** 📝
        - Write down what you know
        - Use symbols: > (greater) < (less)
        
        **2. Chain the clues together** 🔗
        - If A > B and B > C, then A > C
        - Draw a line or use arrows
        
        **3. Watch for tricky words** ⚠️
        - "Not taller" = shorter or equal
        - "No more than" = less or equal
        
        **4. Check your logic** ✅
        - Does your answer make sense?
        - Did you use all the clues?
        
        ### Example:
        
        **Problem:** "Tom is taller than Sue. Sue is taller than Max."
        
        **Solution:**
        - Tom > Sue (Tom is taller)
        - Sue > Max (Sue is taller)
        - Therefore: Tom > Sue > Max
        - Tom is tallest, Max is shortest
        
        ### Types of Ordering:
        
        **Simple Chain (2 clues):**
        - A > B, B > C → A > B > C
        
        **Negative Statements:**
        - A is not taller than B → A ≤ B
        - Use carefully!
        
        **Mixed Comparisons:**
        - A > B but < C → C > A > B
        
        **Multiple Attributes:**
        - Compare same attribute only
        - Can't mix height with speed!
        
        ### Pro Tips:
        
        🎯 **Draw it out**: Make a number line or diagram
        
        🎯 **Use initials**: T > S > M is easier than writing full names
        
        🎯 **Start with extremes**: Find the biggest/smallest first
        
        🎯 **Eliminate options**: Cross out what can't be true
        
        🎯 **Check both ways**: If A > B, then B < A
        """)

def generate_problem_scenarios():
    """Generate diverse scenarios for ordering problems"""
    return {
        "distance": [
            {
                "template": "{person1} lives {comparison1} from the {place} than {person2}. {person2} {comparison2} live {comparison3} to the {place} than {person3}. Who lives {question} from the {place}, {person3} or {person1}?",
                "people": ["Ryan", "Evan", "Isaac", "Maria", "Chen", "Aisha", "Diego", "Fatima"],
                "places": ["park", "school", "library", "mall", "beach", "city center", "train station"],
                "comparisons": {
                    "farther": ["farther", "does not", "closer"],
                    "closer": ["closer", "does not", "farther"]
                }
            },
            {
                "template": "{person1} walks {comparison1} to school than {person2}. {person2} walks {comparison1} than {person3}. Who has the {question} walk to school?",
                "people": ["Sam", "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Drew", "Avery"],
                "comparisons": {
                    "farther": "farther",
                    "less": "less"
                },
                "questions": {
                    "farther": "longest",
                    "less": "shortest"
                }
            }
        ],
        
        "sports_scores": [
            {
                "template": "The {team1} scored {comparison1} points than the {team2} but {comparison2} points than the {team3}. Which team scored the {question} points?",
                "teams": ["Dolphins", "Lions", "Eagles", "Tigers", "Panthers", "Wolves", "Hawks", "Bears", "Sharks", "Rams"],
                "comparisons": {
                    "fewer_more": ["fewer", "more"],
                    "more_fewer": ["more", "fewer"]
                },
                "questions": {
                    "fewer_more": "fewest",
                    "more_fewer": "most"
                }
            },
            {
                "template": "The {color1} team scored {comparison1} points than the {color2} team but {comparison2} points than the {color3} team. Which team scored {question} points, the {color3} team or the {color2} team?",
                "colors": ["red", "blue", "green", "yellow", "orange", "purple", "grey", "black", "white", "pink"],
                "comparisons": {
                    "more_fewer": ["more", "fewer"],
                    "fewer_more": ["fewer", "more"]
                },
                "questions": {
                    "more_fewer": "more",
                    "fewer_more": "fewer"
                }
            }
        ],
        
        "size_comparisons": [
            {
                "template": "The {color1} {animal} is {comparison1} than the {color2} {animal} but {comparison2} than the {color3} {animal}. Which {animal} is {question}, the {color2} {animal} or the {color3} {animal}?",
                "animals": ["dog", "cat", "rabbit", "hamster", "bird", "fish", "turtle"],
                "colors": ["brown", "grey", "white", "black", "spotted", "striped"],
                "comparisons": {
                    "smaller_larger": ["smaller", "larger"],
                    "larger_smaller": ["larger", "smaller"]
                },
                "questions": {
                    "smaller_larger": "smaller",
                    "larger_smaller": "larger"
                }
            },
            {
                "template": "The {item1} is {comparison1} than the {item2}. The {item2} is {comparison1} than the {item3}. Which is the {question}?",
                "items": ["red box", "blue box", "green box", "wooden crate", "plastic container", "metal bin"],
                "comparisons": {
                    "heavier": "heavier",
                    "lighter": "lighter",
                    "taller": "taller",
                    "shorter": "shorter"
                },
                "questions": {
                    "heavier": "heaviest",
                    "lighter": "lightest",
                    "taller": "tallest",
                    "shorter": "shortest"
                }
            }
        ],
        
        "quantity_comparisons": [
            {
                "template": "{person1} has {comparison1} {items} than {person2} but {comparison2} {items} than {person3}. Who has the {question} {items}?",
                "people": ["Shivani", "Anthony", "David", "Emma", "Lucas", "Sophia", "Noah", "Olivia"],
                "items": ["cousins", "books", "marbles", "stickers", "cards", "stamps", "coins", "toys"],
                "comparisons": {
                    "more_fewer": ["more", "fewer"],
                    "fewer_more": ["fewer", "more"]
                },
                "questions": {
                    "more_fewer": "most",
                    "fewer_more": "fewest"
                }
            },
            {
                "template": "{person1} collected {comparison1} {items} than {person2}. {person2} collected {comparison1} than {person3}. List the people from most to fewest {items}.",
                "people": ["Maya", "Raj", "Kim", "Luis", "Zara", "Omar", "Yuki", "Hassan"],
                "items": ["seashells", "leaves", "rocks", "flowers", "buttons", "badges"],
                "comparisons": {
                    "more": "more",
                    "fewer": "fewer"
                }
            }
        ],
        
        "height_comparisons": [
            {
                "template": "{person1} is {negation} {comparison1} than {person2}. {person2} is {comparison2} than {person3}. Who is {question}, {person1} or {person3}?",
                "people": ["Nathan", "Will", "Brendan", "Jake", "Ethan", "Mason", "Logan", "Aiden"],
                "negations": ["not", ""],
                "comparisons": {
                    "taller_shorter": ["taller", "shorter"],
                    "shorter_taller": ["shorter", "taller"]
                },
                "questions": {
                    "taller_shorter": "taller",
                    "shorter_taller": "shorter"
                }
            }
        ],
        
        "age_comparisons": [
            {
                "template": "{person1} is {comparison1} than {person2}. {person2} is {comparison1} than {person3}. Who is the {question}?",
                "people": ["Alice", "Bob", "Carol", "Dan", "Eve", "Frank", "Grace", "Henry"],
                "comparisons": {
                    "older": "older",
                    "younger": "younger"
                },
                "questions": {
                    "older": "oldest",
                    "younger": "youngest"
                }
            }
        ],
        
        "speed_comparisons": [
            {
                "template": "{person1} runs {comparison1} than {person2} but {comparison2} than {person3}. Who is the {question} runner?",
                "people": ["Tom", "Jerry", "Mike", "Sarah", "Lisa", "Kevin", "Rachel", "Steve"],
                "comparisons": {
                    "faster_slower": ["faster", "slower"],
                    "slower_faster": ["slower", "faster"]
                },
                "questions": {
                    "faster_slower": "fastest",
                    "slower_faster": "slowest"
                }
            }
        ],
        
        "test_scores": [
            {
                "template": "{person1} scored {comparison1} on the test than {person2}. {person2} scored {comparison1} than {person3}. Rank the students from highest to lowest score.",
                "people": ["Amy", "Ben", "Chloe", "Derek", "Emily", "Fred", "Gina", "Harry"],
                "comparisons": {
                    "higher": "higher",
                    "lower": "lower"
                }
            }
        ],
        
        "time_comparisons": [
            {
                "template": "{person1} finished the race {comparison1} than {person2}. {person2} finished {comparison1} than {person3}. Who came in {question} place?",
                "people": ["Lin", "Pat", "Sam", "Ali", "Max", "Joy", "Leo", "Zoe"],
                "comparisons": {
                    "earlier": "earlier",
                    "later": "later"
                },
                "questions": {
                    "earlier": "first",
                    "later": "last"
                }
            }
        ],
        
        "price_comparisons": [
            {
                "template": "The {item1} costs {comparison1} than the {item2} but {comparison2} than the {item3}. Which item is the {question} expensive?",
                "items": ["laptop", "tablet", "phone", "watch", "camera", "headphones", "speaker", "monitor"],
                "comparisons": {
                    "more_less": ["more", "less"],
                    "less_more": ["less", "more"]
                },
                "questions": {
                    "more_less": "most",
                    "less_more": "least"
                }
            }
        ]
    }

def generate_new_order_problem():
    """Generate a new ordering problem"""
    difficulty = st.session_state.order_difficulty
    scenarios = generate_problem_scenarios()
    
    # Choose scenario types based on difficulty
    if difficulty == 1:
        # Simple direct comparisons
        scenario_types = ["sports_scores", "size_comparisons", "quantity_comparisons"]
        use_negation = False
        chain_length = 2
    elif difficulty == 2:
        # Add distance and height
        scenario_types = ["distance", "sports_scores", "size_comparisons", "quantity_comparisons", "height_comparisons"]
        use_negation = False
        chain_length = 2
    elif difficulty == 3:
        # Add negations
        scenario_types = ["distance", "height_comparisons", "age_comparisons", "speed_comparisons"]
        use_negation = True
        chain_length = 2
    elif difficulty == 4:
        # More complex scenarios
        scenario_types = ["test_scores", "time_comparisons", "price_comparisons", "speed_comparisons"]
        use_negation = True
        chain_length = 3
    else:  # difficulty == 5
        # All scenarios, complex chains
        scenario_types = list(scenarios.keys())
        use_negation = True
        chain_length = 3
    
    # Select random scenario
    scenario_type = random.choice(scenario_types)
    templates = scenarios[scenario_type]
    template = random.choice(templates)
    
    # Generate problem based on template
    problem_text = template["template"]
    
    # Initialize variables to track entities
    entities = {}
    
    # Select people/items
    if "people" in template:
        people = random.sample(template["people"], 3)
        person1, person2, person3 = people
        entities['person1'] = person1
        entities['person2'] = person2
        entities['person3'] = person3
        problem_text = problem_text.replace("{person1}", person1)
        problem_text = problem_text.replace("{person2}", person2)
        problem_text = problem_text.replace("{person3}", person3)
    
    if "teams" in template:
        teams = random.sample(template["teams"], 3)
        team1, team2, team3 = teams
        entities['team1'] = team1
        entities['team2'] = team2
        entities['team3'] = team3
        problem_text = problem_text.replace("{team1}", team1)
        problem_text = problem_text.replace("{team2}", team2)
        problem_text = problem_text.replace("{team3}", team3)
    
    if "colors" in template:
        colors = random.sample(template["colors"], 3)
        entities['colors'] = colors
        if "{color1}" in problem_text:
            problem_text = problem_text.replace("{color1}", colors[0])
            problem_text = problem_text.replace("{color2}", colors[1])
            problem_text = problem_text.replace("{color3}", colors[2])
            # Store color team entities for later use
            entities['color1_team'] = f"the {colors[0]} team"
            entities['color2_team'] = f"the {colors[1]} team"
            entities['color3_team'] = f"the {colors[2]} team"
    
    if "items" in template:
        if isinstance(template["items"][0], str) and " " in template["items"][0]:
            # Multi-word items (like "red box", "blue box")
            items = random.sample(template["items"], 3)
            entities['item1'] = items[0]
            entities['item2'] = items[1]
            entities['item3'] = items[2]
            problem_text = problem_text.replace("{item1}", items[0])
            problem_text = problem_text.replace("{item2}", items[1])
            problem_text = problem_text.replace("{item3}", items[2])
        else:
            # Single word items
            item = random.choice(template["items"])
            entities['item_type'] = item
            problem_text = problem_text.replace("{items}", item)
    
    # Handle other replacements
    if "animals" in template:
        animal = random.choice(template["animals"])
        entities['animal'] = animal
        problem_text = problem_text.replace("{animal}", animal)
    
    if "places" in template:
        place = random.choice(template["places"])
        problem_text = problem_text.replace("{place}", place)
    
    # Handle comparisons and determine correct answer
    correct_answer = None
    answer_options = []
    
    if scenario_type == "distance":
        # Special handling for distance problems
        comparison_type = random.choice(["farther", "closer"])
        comparisons = template["comparisons"][comparison_type]
        problem_text = problem_text.replace("{comparison1}", comparisons[0])
        problem_text = problem_text.replace("{comparison2}", comparisons[1])
        problem_text = problem_text.replace("{comparison3}", comparisons[2])
        
        if comparison_type == "farther" and comparisons[1] == "does not":
            # Ryan > Evan, Evan >= Isaac → Ryan > Isaac
            problem_text = problem_text.replace("{question}", "farther")
            correct_answer = entities['person1']
            answer_options = [entities['person3'], entities['person1']]
        else:
            problem_text = problem_text.replace("{question}", "farther")
            correct_answer = entities['person3']
            answer_options = [entities['person3'], entities['person1']]
    
    elif scenario_type == "sports_scores":
        comp_type = random.choice(list(template["comparisons"].keys()))
        comp1, comp2 = template["comparisons"][comp_type]
        problem_text = problem_text.replace("{comparison1}", comp1)
        problem_text = problem_text.replace("{comparison2}", comp2)
        
        question = template["questions"][comp_type]
        problem_text = problem_text.replace("{question}", question)
        
        # Check if we're using teams or colors
        if "teams" in template and 'team1' in entities:
            # Using team names directly
            if comp_type == "fewer_more":
                if "fewest" in question:
                    correct_answer = entities['team3']
                    answer_options = [entities['team1'], entities['team2'], entities['team3']]
                else:
                    correct_answer = entities['team2']
                    answer_options = [entities['team2'], entities['team3']]
            else:
                if "most" in question:
                    correct_answer = entities['team1']
                    answer_options = [entities['team1'], entities['team2'], entities['team3']]
                else:
                    correct_answer = entities['team3']
                    answer_options = [entities['team3'], entities['team2']]
        else:
            # Using color teams
            color1_team = entities['color1_team']
            color2_team = entities['color2_team']
            color3_team = entities['color3_team']
            
            if comp_type == "more_fewer":
                if "more" in question:
                    correct_answer = color3_team
                    answer_options = [color3_team, color2_team]
                else:
                    correct_answer = color2_team
                    answer_options = [color3_team, color2_team]
            else:  # fewer_more
                if "fewer" in question:
                    correct_answer = color2_team
                    answer_options = [color3_team, color2_team]
                else:
                    correct_answer = color3_team
                    answer_options = [color3_team, color2_team]
    
    elif scenario_type == "size_comparisons":
        comp_type = random.choice(list(template["comparisons"].keys()))
        
        # Check if we're dealing with the simple item comparison template
        if "{item1}" in template["template"] and "item1" in entities:
            # This is the "red box", "blue box" type problem
            comparison = template["comparisons"][comp_type]
            problem_text = problem_text.replace("{comparison1}", comparison)
            
            question = template["questions"][comp_type]
            problem_text = problem_text.replace("{question}", question)
            
            # For "The item1 is lighter than item2. The item2 is lighter than item3. Which is the heaviest?"
            # Order: item3 > item2 > item1 (for weight)
            if comparison == "lighter":
                if "heaviest" in question:
                    correct_answer = entities['item3']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
                else:  # lightest
                    correct_answer = entities['item1']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
            elif comparison == "heavier":
                if "heaviest" in question:
                    correct_answer = entities['item1']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
                else:  # lightest
                    correct_answer = entities['item3']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
            elif comparison == "taller":
                if "tallest" in question:
                    correct_answer = entities['item1']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
                else:  # shortest
                    correct_answer = entities['item3']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
            elif comparison == "shorter":
                if "tallest" in question:
                    correct_answer = entities['item3']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
                else:  # shortest
                    correct_answer = entities['item1']
                    answer_options = [entities['item1'], entities['item2'], entities['item3']]
        
        else:
            # This is the colored animal type problem
            comp1, comp2 = template["comparisons"][comp_type]
            problem_text = problem_text.replace("{comparison1}", comp1)
            problem_text = problem_text.replace("{comparison2}", comp2)
            
            question = template["questions"][comp_type]
            problem_text = problem_text.replace("{question}", question)
            
            if comp_type == "smaller_larger":
                if "smaller" in question:
                    correct_answer = f"the {entities['colors'][2]} {entities['animal']}"
                    answer_options = [f"the {entities['colors'][1]} {entities['animal']}", 
                                    f"the {entities['colors'][2]} {entities['animal']}"]
                else:
                    correct_answer = f"the {entities['colors'][1]} {entities['animal']}"
                    answer_options = [f"the {entities['colors'][1]} {entities['animal']}", 
                                    f"the {entities['colors'][2]} {entities['animal']}"]
    
    elif scenario_type == "quantity_comparisons":
        comp_type = random.choice(list(template["comparisons"].keys()))
        
        if isinstance(template["comparisons"][comp_type], list):
            comp1, comp2 = template["comparisons"][comp_type]
            problem_text = problem_text.replace("{comparison1}", comp1)
            problem_text = problem_text.replace("{comparison2}", comp2)
        else:
            comp = template["comparisons"][comp_type]
            problem_text = problem_text.replace("{comparison1}", comp)
            problem_text = problem_text.replace("{comparison2}", comp)
        
        if "questions" in template:
            question = template["questions"][comp_type]
            problem_text = problem_text.replace("{question}", question)
        
        # Determine correct answer
        if comp_type == "more_fewer":
            # Person1 > Person3 > Person2
            if "most" in problem_text.lower():
                correct_answer = entities['person1']
            else:  # fewest
                correct_answer = entities['person2']
            answer_options = [entities['person1'], entities['person2'], entities['person3']]
        else:
            # Person3 > Person1 > Person2
            if "most" in problem_text.lower():
                correct_answer = entities['person3']
            else:  # fewest
                correct_answer = entities['person2']
            answer_options = [entities['person1'], entities['person2'], entities['person3']]
    
    elif scenario_type == "height_comparisons":
        # Handle negation
        if use_negation and difficulty >= 3:
            negation = "not"
        else:
            negation = ""
        problem_text = problem_text.replace("{negation}", negation)
        
        if negation == "not":
            # Nathan is not taller than Will → Nathan <= Will
            # Will is shorter than Brendan → Will < Brendan
            # So: Brendan > Will >= Nathan
            problem_text = problem_text.replace("{comparison1}", "taller")
            problem_text = problem_text.replace("{comparison2}", "shorter")
            problem_text = problem_text.replace("{question}", "taller")
            correct_answer = entities['person3']  # Brendan
            answer_options = [entities['person3'], entities['person1']]  # Brendan, Nathan
        else:
            comp_type = random.choice(["taller_shorter", "shorter_taller"])
            comps = template["comparisons"][comp_type]
            problem_text = problem_text.replace("{comparison1}", comps[0])
            problem_text = problem_text.replace("{comparison2}", comps[1])
            question = template["questions"][comp_type]
            problem_text = problem_text.replace("{question}", question)
            
            if comp_type == "taller_shorter" and "taller" in question:
                correct_answer = entities['person1']
            elif comp_type == "shorter_taller" and "shorter" in question:
                correct_answer = entities['person1']
            else:
                correct_answer = entities['person3']
            answer_options = [entities['person1'], entities['person3']]
    
    elif scenario_type == "age_comparisons":
        comparison = template["comparisons"]["older"]
        problem_text = problem_text.replace("{comparison1}", comparison)
        question = template["questions"]["older"]
        problem_text = problem_text.replace("{question}", question)
        
        if "oldest" in question:
            correct_answer = entities['person1']
        else:
            correct_answer = entities['person3']
        answer_options = [entities['person1'], entities['person2'], entities['person3']]
    
    elif scenario_type == "speed_comparisons":
        comp_type = random.choice(list(template["comparisons"].keys()))
        comp1, comp2 = template["comparisons"][comp_type]
        problem_text = problem_text.replace("{comparison1}", comp1)
        problem_text = problem_text.replace("{comparison2}", comp2)
        question = template["questions"][comp_type]
        problem_text = problem_text.replace("{question}", question)
        
        if comp_type == "faster_slower":
            if "fastest" in question:
                correct_answer = entities['person1']
            else:
                correct_answer = entities['person2']
        else:
            if "slowest" in question:
                correct_answer = entities['person1']
            else:
                correct_answer = entities['person3']
        answer_options = [entities['person1'], entities['person2'], entities['person3']]
    
    elif scenario_type == "price_comparisons":
        comp_type = random.choice(list(template["comparisons"].keys()))
        comp1, comp2 = template["comparisons"][comp_type]
        problem_text = problem_text.replace("{comparison1}", comp1)
        problem_text = problem_text.replace("{comparison2}", comp2)
        question = template["questions"][comp_type]
        problem_text = problem_text.replace("{question}", question)
        
        if comp_type == "more_less":
            if "most" in question:
                correct_answer = entities['item1']
            else:
                correct_answer = entities['item3']
        else:
            if "least" in question:
                correct_answer = entities['item1']
            else:
                correct_answer = entities['item3']
        answer_options = [entities['item1'], entities['item2'], entities['item3']]
    
    elif scenario_type == "test_scores":
        comparison = random.choice(["higher", "lower"])
        problem_text = problem_text.replace("{comparison1}", comparison)
        
        if comparison == "higher":
            # Person1 > Person2 > Person3
            correct_answer = f"{entities['person1']}, {entities['person2']}, {entities['person3']}"
        else:
            # Person3 > Person2 > Person1
            correct_answer = f"{entities['person3']}, {entities['person2']}, {entities['person1']}"
        
        answer_options = [
            f"{entities['person1']}, {entities['person2']}, {entities['person3']}",
            f"{entities['person3']}, {entities['person2']}, {entities['person1']}",
            f"{entities['person2']}, {entities['person1']}, {entities['person3']}"
        ]
    
    elif scenario_type == "time_comparisons":
        comparison = random.choice(["earlier", "later"])
        problem_text = problem_text.replace("{comparison1}", comparison)
        question = template["questions"][comparison]
        problem_text = problem_text.replace("{question}", question)
        
        if comparison == "earlier":
            if "first" in question:
                correct_answer = entities['person1']
            else:
                correct_answer = entities['person3']
        else:
            if "last" in question:
                correct_answer = entities['person1']
            else:
                correct_answer = entities['person3']
        answer_options = [entities['person1'], entities['person2'], entities['person3']]
    
    # Final fallback - this should rarely happen now
    if not answer_options:
        st.error("Error generating problem. Please try again.")
        reset_problem_state()
        st.rerun()
    
    # Randomize answer order
    random.shuffle(answer_options)
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "correct_answer": correct_answer,
        "answer_options": answer_options,
        "scenario_type": scenario_type,
        "difficulty": difficulty,
        "entities": entities
    }
    st.session_state.current_problem = problem_text

def display_order_problem():
    """Display the current ordering problem"""
    problem_data = st.session_state.problem_data
    
    # Display problem in a nice box
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 25px;
        font-size: 18px;
        line-height: 1.8;
    ">
        {problem_data['problem_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Display answer options as buttons
    st.markdown("### Choose your answer:")
    
    # Determine number of columns based on number of options
    num_options = len(problem_data['answer_options'])
    if num_options == 2:
        cols = st.columns(2)
    elif num_options == 3:
        cols = st.columns(3)
    else:
        cols = st.columns(2)
    
    for i, option in enumerate(problem_data['answer_options']):
        with cols[i % len(cols)]:
            if st.button(
                option,
                key=f"answer_{i}",
                use_container_width=True,
                disabled=st.session_state.answer_submitted
            ):
                handle_answer(option)
    
    # Show feedback if answer submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next problem button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def handle_answer(answer):
    """Handle user's answer selection"""
    st.session_state.user_answer = answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_feedback():
    """Display feedback for the submitted answer"""
    problem_data = st.session_state.problem_data
    user_answer = st.session_state.user_answer
    correct_answer = problem_data['correct_answer']
    
    if user_answer == correct_answer:
        st.success("✅ **Correct! Excellent logical thinking!**")
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.order_difficulty
            st.session_state.order_difficulty = min(
                st.session_state.order_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.order_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Amazing! You've mastered ordering problems!**")
            elif old_difficulty < st.session_state.order_difficulty:
                st.info(f"⬆️ **Level up! Now at Level {st.session_state.order_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is: {correct_answer}**")
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty
        old_difficulty = st.session_state.order_difficulty
        st.session_state.order_difficulty = max(
            st.session_state.order_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.order_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.order_difficulty}. Keep practicing!**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation of the logical chain"""
    problem_data = st.session_state.problem_data
    scenario_type = problem_data['scenario_type']
    
    with st.expander("📖 **See the logical steps**", expanded=True):
        st.markdown("### Let's work through this step by step:")
        
        # Extract names/items from the problem text
        problem_text = problem_data['problem_text']
        
        # Show different explanations based on scenario type
        if scenario_type == "distance":
            st.markdown("""
            **Step 1: Identify the relationships**
            - Look at who lives farther or closer
            - Pay attention to "does not" - it reverses meaning!
            
            **Step 2: Chain the clues**
            - If A is farther than B
            - And B is not closer than C (meaning B ≥ C)
            - Then A is farther than both B and C
            
            **Step 3: Answer the question**
            - Compare the two people asked about
            - Use the chain to determine who is farther
            """)
            
        elif scenario_type == "sports_scores":
            st.markdown("""
            **Step 1: Set up the relationships**
            - Identify which team scored more/fewer
            - Create a chain: highest → middle → lowest
            
            **Step 2: Place teams in order**
            - Use the clues to arrange teams
            - Check both conditions are met
            
            **Step 3: Find the answer**
            - Look for most/fewest as asked
            - The ends of the chain are the extremes
            """)
            
        elif scenario_type == "size_comparisons":
            st.markdown("""
            **Step 1: Understand size relationships**
            - Larger/smaller creates an order
            - Middle item connects the extremes
            
            **Step 2: Arrange by size**
            - Biggest → middle → smallest
            - Or reverse for different comparisons
            
            **Step 3: Compare the requested items**
            - Look at specific comparison asked
            - Use the chain to determine answer
            """)
            
        elif scenario_type == "quantity_comparisons":
            st.markdown("""
            **Step 1: Track who has more/fewer**
            - More means higher in the order
            - Fewer means lower in the order
            
            **Step 2: Create the sequence**
            - Most → middle → fewest
            - All clues must be satisfied
            
            **Step 3: Identify extremes**
            - Most = top of the chain
            - Fewest = bottom of the chain
            """)
            
        elif scenario_type == "height_comparisons":
            st.markdown("""
            **Step 1: Handle "not" statements**
            - "Not taller than" = shorter than or equal to
            - This is tricky - be careful!
            
            **Step 2: Combine the clues**
            - If A ≤ B (not taller)
            - And B < C (shorter)
            - Then C > B ≥ A
            
            **Step 3: Find the answer**
            - Tallest is at the top
            - Shortest is at the bottom
            """)
        
        # Add a visual representation
        st.markdown("\n**Visual representation:**")
        
        # Create a simple diagram based on the problem
        if scenario_type in ["sports_scores", "quantity_comparisons", "size_comparisons"]:
            st.markdown("""
            ```
            Highest/Most/Largest
                    ↓
                Middle
                    ↓
            Lowest/Fewest/Smallest
            ```
            """)
        elif scenario_type in ["distance", "height_comparisons"]:
            st.markdown("""
            ```
            Position 1 → Position 2 → Position 3
            (Use arrows to show relationships)
            ```
            """)
        
        # Remind about the answer
        st.markdown(f"\n**Therefore, the answer is: {problem_data['correct_answer']}**")

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None