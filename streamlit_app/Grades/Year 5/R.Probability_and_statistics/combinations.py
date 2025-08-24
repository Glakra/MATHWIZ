import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np

def run():
    """
    Main function to run the Combinations activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/R.Probability_and_statistics/combinations.py
    """
    # Initialize session state
    if "combinations_difficulty" not in st.session_state:
        st.session_state.combinations_difficulty = 1
    
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
    st.title("🎯 Combinations")
    st.markdown("*Use the counting principle to find the number of possible combinations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.combinations_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Simple Choices (2×2, 3×2)",
            2: "Multiple Options (3×3, 4×3)",
            3: "Complex Scenarios (3 steps)",
            4: "Advanced Problems (4+ steps)"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Simple')}")
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
    with st.expander("📚 **How to Count Combinations**", expanded=False):
        st.markdown("""
        ### 🔢 The Multiplication Principle (Counting Principle)
        
        **When making multiple choices in sequence, multiply the number of options for each choice.**
        
        ### 📝 Examples:
        
        **2 Choices:**
        - 3 shirts × 2 pants = 6 outfits
        - 4 appetizers × 5 main courses = 20 meals
        
        **3 Choices:**
        - 2 breads × 3 meats × 4 cheeses = 24 sandwiches
        - 3 colors × 2 sizes × 2 styles = 12 options
        
        **Tree Diagram Method:**
        ```
        Choice 1: A or B (2 options)
        Choice 2: X, Y, or Z (3 options)
        
        Combinations:
        A-X, A-Y, A-Z
        B-X, B-Y, B-Z
        Total: 2 × 3 = 6
        ```
        
        ### 💡 Key Points:
        - Each choice is independent
        - Order matters for the counting principle
        - Different from choosing multiple items at once
        - Always multiply the number of options
        """)

def generate_new_problem():
    """Generate a new combinations problem"""
    difficulty = st.session_state.combinations_difficulty
    
    if difficulty == 1:
        problem_types = [
            "outfit_simple", "meal_simple", "route_simple",
            "ice_cream_simple", "activity_simple", "color_simple"
        ]
    elif difficulty == 2:
        problem_types = [
            "outfit_complex", "meal_complex", "schedule_complex",
            "ice_cream_complex", "party_planning", "sports_equipment"
        ]
    elif difficulty == 3:
        problem_types = [
            "three_step_outfit", "three_step_meal", "three_step_trip",
            "three_step_party", "three_step_game", "three_step_craft"
        ]
    else:
        problem_types = [
            "four_step_event", "password_creation", "menu_design",
            "tournament_bracket", "travel_itinerary", "custom_product"
        ]
    
    problem_type = random.choice(problem_types)
    problem_data = generate_specific_problem(problem_type)
    
    st.session_state.problem_data = problem_data
    st.session_state.correct_answer = problem_data["correct_answer"]
    st.session_state.current_problem = problem_data["question"]

def generate_specific_problem(problem_type):
    """Generate specific combination problem"""
    
    # Level 1 - Simple 2-choice problems
    if problem_type == "outfit_simple":
        names = ["Danny", "Sophie", "Alex", "Maya", "Jordan", "Emily"]
        name = random.choice(names)
        
        scenarios = [
            {
                "tops": ["purple shirt", "blue shirt"],
                "bottoms": ["blue trousers", "beige trousers"],
                "tops_count": 2,
                "bottoms_count": 2
            },
            {
                "tops": ["red jumper", "green jumper", "yellow jumper"],
                "bottoms": ["black jeans", "blue jeans"],
                "tops_count": 3,
                "bottoms_count": 2
            },
            {
                "tops": ["polo neck", "sweatshirt", "jumper", "T-shirt"],
                "bottoms": ["sweatpants", "jeans"],
                "tops_count": 4,
                "bottoms_count": 2
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = scenario["tops_count"] * scenario["bottoms_count"]
        
        if len(scenario["tops"]) > 2:
            tops_text = ", ".join(scenario["tops"][:-1]) + f", and {scenario['tops'][-1]}"
        else:
            tops_text = " and ".join(scenario["tops"])
        bottoms_text = " and ".join(scenario["bottoms"])
        
        question = f"{name} is deciding what to wear to school. He has {tops_text}, and he has {bottoms_text}. If he can wear any colour shirt with any pair of trousers, how many different combinations can {name} pick?"
        
        return {
            "question": question,
            "visual_type": "outfit",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{scenario['tops_count']} tops × {scenario['bottoms_count']} bottoms = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "meal_simple":
        scenarios = [
            {
                "context": "Kenny is planning his day. This morning, he can",
                "choice1_options": ["get a haircut", "pay bills", "clean the gutters"],
                "choice2_options": ["soup", "a burrito", "a salad", "a sandwich"],
                "choice1_name": "morning activities",
                "choice2_name": "lunch options",
                "choice1_count": 3,
                "choice2_count": 4
            },
            {
                "context": "Jerry is planning his day at the beach. This afternoon, he can",
                "choice1_options": ["fly a kite", "collect seashells", "go surfing"],
                "choice2_options": ["the oyster house", "the pizza place", "the fish restaurant"],
                "choice1_name": "afternoon activities",
                "choice2_name": "dinner places",
                "choice1_count": 3,
                "choice2_count": 3
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = scenario["choice1_count"] * scenario["choice2_count"]
        
        choice1_text = ", ".join(scenario["choice1_options"][:-1]) + f", or {scenario['choice1_options'][-1]}"
        choice2_text = ", ".join(scenario["choice2_options"][:-1]) + f", or {scenario['choice2_options'][-1]}"
        
        if "beach" in scenario["context"]:
            question = f"{scenario['context']} {choice1_text}. For dinner, he can go to {choice2_text}. Given these choices, how many different combinations does Jerry have to choose from?"
        else:
            question = f"{scenario['context']} {choice1_text}. For lunch, he can have {choice2_text}. Given these choices, how many different combinations does Kenny have to choose from?"
        
        return {
            "question": question,
            "visual_type": "choices",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{scenario['choice1_count']} {scenario['choice1_name']} × {scenario['choice2_count']} {scenario['choice2_name']} = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "route_simple":
        names = ["Scarlett", "Marcus", "Lily", "Noah", "Ava", "Ethan"]
        name = random.choice(names)
        
        activities = ["bike", "skate", "run", "walk", "jog"]
        routes = ["through the woods", "over the hills", "around the lake", "into the valley", "along the river", "through the park"]
        
        num_activities = random.choice([2, 3, 4])
        num_routes = random.choice([3, 4, 5])
        
        selected_activities = random.sample(activities, num_activities)
        selected_routes = random.sample(routes, num_routes)
        
        answer = num_activities * num_routes
        
        activities_text = ", ".join(selected_activities[:-1]) + f", or {selected_activities[-1]}"
        routes_text = ", ".join(selected_routes[:-1]) + f", or {selected_routes[-1]}"
        
        question = f"{name} is planning her workout. She can {activities_text}. For each activity, she can go {routes_text}. How many different combinations does {name} have to choose from?"
        
        return {
            "question": question,
            "visual_type": "route",
            "visual_data": {
                "activities": selected_activities,
                "routes": selected_routes
            },
            "correct_answer": answer,
            "explanation": f"{num_activities} activities × {num_routes} routes = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "ice_cream_simple":
        names = ["Kira", "Ben", "Zoe", "Ryan", "Mia", "Jake"]
        name = random.choice(names)
        
        cones = ["sugar cone", "dish", "plain cone", "waffle cone"]
        flavors = ["vanilla", "chocolate", "mint", "strawberry", "caramel", "coffee"]
        
        num_cones = random.choice([2, 3])
        num_flavors = random.choice([3, 4, 5])
        
        selected_cones = random.sample(cones, num_cones)
        selected_flavors = random.sample(flavors, num_flavors)
        
        answer = num_cones * num_flavors
        
        if len(selected_cones) > 2:
            cones_text = ", ".join(selected_cones[:-1]) + f", or {selected_cones[-1]}"
        else:
            cones_text = " or ".join(selected_cones)
        flavors_text = ", ".join(selected_flavors[:-1]) + f", or {selected_flavors[-1]}"
        
        question = f"{name} is deciding what to order at the ice cream shop. She can choose a {cones_text}, and she can have {flavors_text} ice cream. How many different combinations can {name} order?"
        
        return {
            "question": question,
            "visual_type": "ice_cream",
            "visual_data": {
                "containers": selected_cones,
                "flavors": selected_flavors
            },
            "correct_answer": answer,
            "explanation": f"{num_cones} cone types × {num_flavors} flavors = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "activity_simple":
        scenarios = [
            {
                "person": "Pedro",
                "context": "picking his class schedule for next year",
                "choice1": "one elective class",
                "choice2": "one language class",
                "options1": ["journalism", "drama", "band"],
                "options2": ["French", "Spanish"],
                "label1": "elective classes",
                "label2": "languages"
            },
            {
                "person": "Sarah",
                "context": "planning her weekend",
                "choice1": "one morning activity",
                "choice2": "one afternoon activity",
                "options1": ["yoga", "swimming", "hiking"],
                "options2": ["shopping", "movie", "museum"],
                "label1": "morning activities",
                "label2": "afternoon activities"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["options1"]) * len(scenario["options2"])
        
        options1_text = ", ".join(scenario["options1"][:-1]) + f", and {scenario['options1'][-1]}"
        options2_text = " and ".join(scenario["options2"])
        
        question = f"{scenario['person']} is {scenario['context']}. He gets to pick {scenario['choice1']} and {scenario['choice2']}. The {scenario['label1']} are {options1_text}. The {scenario['label2']} available are {options2_text}. How many different combinations of classes can {scenario['person']} create?"
        
        return {
            "question": question,
            "visual_type": "schedule",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['options1'])} {scenario['label1']} × {len(scenario['options2'])} {scenario['label2']} = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "color_simple":
        scenarios = [
            {
                "context": "A girls' choir is choosing a uniform for their concert",
                "item1": "jumpers",
                "item2": "skirts",
                "colors1": ["blue", "red"],
                "colors2": ["black", "brown"]
            },
            {
                "context": "The soccer team is choosing their kit",
                "item1": "jerseys",
                "item2": "shorts",
                "colors1": ["green", "white", "blue"],
                "colors2": ["black", "white"]
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["colors1"]) * len(scenario["colors2"])
        
        colors1_text = " or ".join(scenario["colors1"])
        colors2_text = " or ".join(scenario["colors2"])
        
        question = f"{scenario['context']}. They can pick {colors1_text} {scenario['item1']}, and they can pick {colors2_text} {scenario['item2']}. Assuming all the colours go together, how many different combinations can the choir pick?"
        
        return {
            "question": question,
            "visual_type": "uniform",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['colors1'])} {scenario['item1']} colors × {len(scenario['colors2'])} {scenario['item2']} colors = {answer} combinations",
            "problem_type": problem_type
        }
    
    # Level 2 - More complex 2-choice problems
    elif problem_type == "outfit_complex":
        scenarios = [
            {
                "person": "Preston",
                "context": "ordering matching shirts for the debate team",
                "types": ["tennis shirts", "polo necks", "jumpers", "sweatshirts"],
                "colors": ["red", "green", "yellow", "purple"],
                "item_name": "shirt types"
            },
            {
                "person": "Lisa",
                "context": "choosing her dance costume",
                "types": ["leotard", "tutu", "unitard", "dress", "two-piece"],
                "colors": ["pink", "black", "white"],
                "item_name": "costume styles"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["types"]) * len(scenario["colors"])
        
        types_text = ", ".join(scenario["types"][:-1]) + f", or {scenario['types'][-1]}"
        colors_text = ", ".join(scenario["colors"][:-1]) + f", or {scenario['colors'][-1]}"
        
        question = f"{scenario['person']} is {scenario['context']}. They can get {types_text}. Each type of shirt comes in {colors_text}. Given these choices, how many different combinations does {scenario['person']} have to choose from?"
        
        return {
            "question": question,
            "visual_type": "product",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['types'])} {scenario['item_name']} × {len(scenario['colors'])} colors = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "meal_complex":
        scenarios = [
            {
                "person": "Tracy",
                "context": "ordering a birthday cake for a friend",
                "choice1": "cake flavours",
                "choice2": "frosting colors",
                "options1": ["chocolate", "vanilla", "lemon"],
                "options2": ["white", "brown", "yellow", "pink"]
            },
            {
                "person": "Marcus",
                "context": "creating a custom pizza",
                "choice1": "crust types",
                "choice2": "sauce options",
                "options1": ["thin", "thick", "stuffed", "gluten-free"],
                "options2": ["tomato", "white", "pesto", "BBQ", "olive oil"]
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["options1"]) * len(scenario["options2"])
        
        options1_text = ", ".join(scenario["options1"][:-1]) + f", and {scenario['options1'][-1]}"
        options2_text = ", ".join(scenario["options2"][:-1]) + f", or {scenario['options2'][-1]}"
        
        question = f"{scenario['person']} is {scenario['context']}. The bakery makes {options1_text} flavoured cakes. Each flavour of cake can come with {options2_text} frosting. How many different combinations can {scenario['person']} choose from?"
        
        return {
            "question": question,
            "visual_type": "food",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['options1'])} {scenario['choice1']} × {len(scenario['options2'])} {scenario['choice2']} = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "schedule_complex":
        scenarios = [
            {
                "context": "The school is planning the spring festival",
                "slot1": "morning performances",
                "slot2": "afternoon activities",
                "options1": ["band concert", "choir show", "dance recital", "drama play"],
                "options2": ["art exhibition", "science fair", "sports tournament", "talent show", "food festival"]
            },
            {
                "context": "The community center is organizing weekend classes",
                "slot1": "Saturday sessions",
                "slot2": "Sunday sessions",
                "options1": ["pottery", "painting", "photography", "sculpture", "drawing"],
                "options2": ["yoga", "pilates", "meditation", "tai chi"]
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["options1"]) * len(scenario["options2"])
        
        options1_text = ", ".join(scenario["options1"])
        options2_text = ", ".join(scenario["options2"])
        
        question = f"{scenario['context']}. For {scenario['slot1']}, they can schedule: {options1_text}. For {scenario['slot2']}, they can have: {options2_text}. How many different schedule combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "schedule",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['options1'])} {scenario['slot1']} × {len(scenario['options2'])} {scenario['slot2']} = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "ice_cream_complex":
        scenarios = [
            {
                "person": "Jamie",
                "containers": ["cup", "sugar cone", "waffle cone", "bowl"],
                "flavors": ["vanilla", "chocolate", "strawberry", "mint", "caramel"],
                "toppings": ["sprinkles", "nuts", "fudge"],
                "use_toppings": False
            },
            {
                "person": "Alex",
                "containers": ["cone", "cup", "sundae dish"],
                "flavors": ["cookies & cream", "rocky road", "butter pecan", "pistachio", "coffee", "cherry"],
                "toppings": [],
                "use_toppings": False
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["containers"]) * len(scenario["flavors"])
        
        containers_text = ", ".join(scenario["containers"])
        flavors_text = ", ".join(scenario["flavors"])
        
        question = f"{scenario['person']} is at the ice cream parlor. They can choose from {len(scenario['containers'])} types of containers ({containers_text}) and {len(scenario['flavors'])} flavors ({flavors_text}). How many different combinations can they order?"
        
        return {
            "question": question,
            "visual_type": "ice_cream",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['containers'])} containers × {len(scenario['flavors'])} flavors = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "party_planning":
        scenarios = [
            {
                "context": "planning a birthday party",
                "choice1": "themes",
                "choice2": "venues",
                "options1": ["superhero", "princess", "pirate", "space"],
                "options2": ["park", "indoor playground", "pool", "backyard", "community center"]
            },
            {
                "context": "organizing a wedding reception",
                "choice1": "meal options",
                "choice2": "music styles",
                "options1": ["buffet", "plated dinner", "cocktail style"],
                "options2": ["DJ", "live band", "string quartet", "jazz ensemble"]
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["options1"]) * len(scenario["options2"])
        
        options1_text = ", ".join(scenario["options1"])
        options2_text = ", ".join(scenario["options2"])
        
        question = f"When {scenario['context']}, you need to choose {scenario['choice1']} and {scenario['choice2']}. The {scenario['choice1']} available are: {options1_text}. The {scenario['choice2']} options are: {options2_text}. How many different combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "event",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['options1'])} {scenario['choice1']} × {len(scenario['options2'])} {scenario['choice2']} = {answer} combinations",
            "problem_type": problem_type
        }
    
    elif problem_type == "sports_equipment":
        scenarios = [
            {
                "sport": "tennis",
                "item1": "rackets",
                "item2": "shoe types",
                "options1": ["Wilson", "Head", "Babolat", "Prince"],
                "options2": ["clay court", "hard court", "grass court"]
            },
            {
                "sport": "skiing",
                "item1": "ski types",
                "item2": "boot colors",
                "options1": ["racing", "all-mountain", "powder", "freestyle", "touring"],
                "options2": ["black", "red", "blue", "white"]
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["options1"]) * len(scenario["options2"])
        
        options1_text = ", ".join(scenario["options1"])
        options2_text = ", ".join(scenario["options2"])
        
        question = f"At the {scenario['sport']} shop, you can choose from {len(scenario['options1'])} types of {scenario['item1']} ({options1_text}) and {len(scenario['options2'])} {scenario['item2']} ({options2_text}). How many different combinations can you select?"
        
        return {
            "question": question,
            "visual_type": "sports",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['options1'])} {scenario['item1']} × {len(scenario['options2'])} {scenario['item2']} = {answer} combinations",
            "problem_type": problem_type
        }
    
    # Level 3 - Three-step problems
    elif problem_type == "three_step_outfit":
        scenarios = [
            {
                "person": "Emma",
                "tops": ["blouse", "shirt", "sweater"],
                "bottoms": ["skirt", "pants"],
                "shoes": ["flats", "heels", "boots"]
            },
            {
                "person": "David",
                "tops": ["t-shirt", "polo", "button-up", "henley"],
                "bottoms": ["jeans", "khakis", "shorts"],
                "shoes": ["sneakers", "loafers"]
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["tops"]) * len(scenario["bottoms"]) * len(scenario["shoes"])
        
        tops_text = ", ".join(scenario["tops"])
        bottoms_text = ", ".join(scenario["bottoms"])
        shoes_text = ", ".join(scenario["shoes"])
        
        question = f"{scenario['person']} is getting dressed. They have {len(scenario['tops'])} tops ({tops_text}), {len(scenario['bottoms'])} bottoms ({bottoms_text}), and {len(scenario['shoes'])} pairs of shoes ({shoes_text}). How many different outfits can they create?"
        
        return {
            "question": question,
            "visual_type": "three_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['tops'])} tops × {len(scenario['bottoms'])} bottoms × {len(scenario['shoes'])} shoes = {answer} combinations",
            "problem_type": problem_type,
            "steps": 3
        }
    
    elif problem_type == "three_step_meal":
        scenarios = [
            {
                "restaurant": "Italian restaurant",
                "appetizers": ["salad", "soup", "bruschetta"],
                "mains": ["pasta", "pizza", "risotto", "fish"],
                "desserts": ["tiramisu", "gelato"]
            },
            {
                "restaurant": "diner",
                "appetizers": ["wings", "nachos", "onion rings", "mozzarella sticks"],
                "mains": ["burger", "sandwich", "salad"],
                "desserts": ["pie", "ice cream", "brownie"]
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = len(scenario["appetizers"]) * len(scenario["mains"]) * len(scenario["desserts"])
        
        question = f"At the {scenario['restaurant']}, you can choose one appetizer from {len(scenario['appetizers'])} options, one main course from {len(scenario['mains'])} options, and one dessert from {len(scenario['desserts'])} options. How many different three-course meals can you create?"
        
        return {
            "question": question,
            "visual_type": "three_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"{len(scenario['appetizers'])} appetizers × {len(scenario['mains'])} mains × {len(scenario['desserts'])} desserts = {answer} combinations",
            "problem_type": problem_type,
            "steps": 3
        }
    
    elif problem_type == "three_step_trip":
        scenarios = [
            {
                "context": "weekend trip",
                "transport": ["car", "train", "bus"],
                "accommodation": ["hotel", "motel", "Airbnb", "hostel"],
                "activities": ["museum", "hiking", "beach", "shopping", "sightseeing"]
            },
            {
                "context": "school field trip",
                "transport": ["school bus", "charter bus"],
                "lunch": ["packed lunch", "restaurant", "picnic"],
                "destinations": ["science center", "zoo", "aquarium", "historical site"]
            }
        ]
        
        scenario = random.choice(scenarios)
        
        if "accommodation" in scenario:
            answer = len(scenario["transport"]) * len(scenario["accommodation"]) * len(scenario["activities"])
            explanation = f"{len(scenario['transport'])} transport × {len(scenario['accommodation'])} accommodation × {len(scenario['activities'])} activities = {answer}"
        else:
            answer = len(scenario["transport"]) * len(scenario["lunch"]) * len(scenario["destinations"])
            explanation = f"{len(scenario['transport'])} transport × {len(scenario['lunch'])} lunch × {len(scenario['destinations'])} destinations = {answer}"
        
        key1 = "transport"
        key2 = "accommodation" if "accommodation" in scenario else "lunch"
        key3 = "activities" if "activities" in scenario else "destinations"
        
        question = f"Planning a {scenario['context']} involves choosing transportation, accommodation/lunch, and activities. With {len(scenario[key1])} transport options, {len(scenario[key2])} accommodation/lunch choices, and {len(scenario[key3])} activity options, how many different combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "three_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": explanation,
            "problem_type": problem_type,
            "steps": 3
        }
    
    elif problem_type == "three_step_party":
        scenarios = [
            {
                "event": "birthday party",
                "decorations": ["balloons", "streamers", "banners"],
                "cakes": ["chocolate", "vanilla", "red velvet", "carrot"],
                "entertainment": ["magician", "clown", "games", "karaoke", "DJ"]
            },
            {
                "event": "graduation party",
                "venues": ["backyard", "park", "restaurant", "hall"],
                "catering": ["BBQ", "Italian", "Mexican"],
                "favors": ["photo frames", "keychains", "magnets"]
            }
        ]
        
        scenario = random.choice(scenarios)
        keys = [k for k in scenario.keys() if k != "event"]
        
        answer = 1
        for key in keys:
            answer *= len(scenario[key])
        
        options_text = ", ".join([f"{len(scenario[k])} {k} options" for k in keys])
        
        question = f"For a {scenario['event']}, you need to make three choices: {', '.join(keys)}. With {options_text}, how many different party combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "three_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([f"{len(scenario[k])} {k}" for k in keys]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": 3
        }
    
    elif problem_type == "three_step_game":
        scenarios = [
            {
                "game": "video game character",
                "classes": ["warrior", "mage", "rogue", "ranger"],
                "races": ["human", "elf", "dwarf"],
                "weapons": ["sword", "staff", "bow", "dagger", "axe"]
            },
            {
                "game": "board game setup",
                "boards": ["forest", "desert", "ocean"],
                "difficulties": ["easy", "medium", "hard", "expert"],
                "characters": ["red", "blue", "green", "yellow", "purple", "orange"]
            }
        ]
        
        scenario = random.choice(scenarios)
        keys = [k for k in scenario.keys() if k != "game"]
        
        answer = 1
        for key in keys:
            answer *= len(scenario[key])
        
        options_text = ", ".join([f"{len(scenario[k])} {k}" for k in keys])
        
        question = f"Creating a {scenario['game']} requires choosing: {options_text}. How many different combinations can you create?"
        
        return {
            "question": question,
            "visual_type": "three_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([f"{len(scenario[k])} {k}" for k in keys]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": 3
        }
    
    elif problem_type == "three_step_craft":
        scenarios = [
            {
                "project": "custom jewelry",
                "materials": ["silver", "gold", "copper"],
                "stones": ["diamond", "ruby", "emerald", "sapphire"],
                "styles": ["necklace", "bracelet", "ring", "earrings", "anklet"]
            },
            {
                "project": "art project",
                "canvases": ["small", "medium", "large", "extra large"],
                "paints": ["acrylic", "oil", "watercolor"],
                "subjects": ["landscape", "portrait", "abstract", "still life"]
            }
        ]
        
        scenario = random.choice(scenarios)
        keys = [k for k in scenario.keys() if k != "project"]
        
        answer = 1
        for key in keys:
            answer *= len(scenario[key])
        
        options_text = ", ".join([f"{len(scenario[k])} {k}" for k in keys])
        
        question = f"For a {scenario['project']}, you can choose from: {options_text}. How many different combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "three_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([f"{len(scenario[k])} {k}" for k in keys]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": 3
        }
    
    # Level 4 - Four or more step problems
    elif problem_type == "four_step_event":
        scenarios = [
            {
                "context": "wedding planning",
                "choices": {
                    "venues": 3,
                    "caterers": 4,
                    "photographers": 2,
                    "bands": 3
                }
            },
            {
                "context": "conference organization",
                "choices": {
                    "locations": 4,
                    "keynote speakers": 3,
                    "lunch options": 3,
                    "workshop tracks": 2
                }
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = 1
        for count in scenario["choices"].values():
            answer *= count
        
        choices_text = ", ".join([f"{count} {name}" for name, count in scenario["choices"].items()])
        
        question = f"For {scenario['context']}, you need to choose from: {choices_text}. How many different combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "multi_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([str(count) for count in scenario["choices"].values()]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": len(scenario["choices"])
        }
    
    elif problem_type == "password_creation":
        scenarios = [
            {
                "positions": 4,
                "choices": [10, 10, 10, 10],
                "description": "4-digit PIN (0-9 for each digit)"
            },
            {
                "positions": 3,
                "choices": [26, 26, 10],
                "description": "password with 2 letters (A-Z) followed by 1 digit (0-9)"
            },
            {
                "positions": 4,
                "choices": [26, 26, 26, 26],
                "description": "4-letter code (A-Z for each position)"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = 1
        for choice in scenario["choices"]:
            answer *= choice
        
        question = f"Creating a {scenario['description']}, how many different combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "password",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([str(c) for c in scenario["choices"]]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": scenario["positions"]
        }
    
    elif problem_type == "menu_design":
        scenarios = [
            {
                "restaurant": "café",
                "breakfast": 5,
                "lunch": 8,
                "dinner": 6,
                "dessert": 4
            },
            {
                "restaurant": "food truck",
                "appetizers": 3,
                "mains": 6,
                "sides": 4,
                "drinks": 5
            }
        ]
        
        scenario = random.choice(scenarios)
        items = {k: v for k, v in scenario.items() if k != "restaurant"}
        answer = 1
        for count in items.values():
            answer *= count
        
        items_text = ", ".join([f"{v} {k} options" for k, v in items.items()])
        
        question = f"A {scenario['restaurant']} offers: {items_text}. If a customer chooses one from each category, how many different meal combinations are possible?"
        
        return {
            "question": question,
            "visual_type": "multi_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([str(v) for v in items.values()]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": len(items)
        }
    
    elif problem_type == "tournament_bracket":
        scenarios = [
            {
                "sport": "tennis",
                "rounds": [16, 8, 4, 2],
                "description": "Single elimination with 16 players"
            },
            {
                "sport": "chess",
                "rounds": [8, 4, 2],
                "description": "Tournament starting with 8 players"
            }
        ]
        
        scenario = random.choice(scenarios)
        answer = 2 ** (len(scenario["rounds"]) - 1)
        
        question = f"In a {scenario['sport']} tournament ({scenario['description']}), how many different paths can lead a player to the finals (considering only win/lose at each round)?"
        
        return {
            "question": question,
            "visual_type": "tournament",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": f"2 choices per round × {len(scenario['rounds'])-1} rounds = {answer} paths",
            "problem_type": problem_type,
            "steps": len(scenario["rounds"]) - 1
        }
    
    elif problem_type == "travel_itinerary":
        scenarios = [
            {
                "trip": "European vacation",
                "flights": 3,
                "hotels": 5,
                "tours": 4,
                "restaurants": 6
            },
            {
                "trip": "weekend getaway",
                "transport": 4,
                "accommodation": 3,
                "activities_day1": 5,
                "activities_day2": 4
            }
        ]
        
        scenario = random.choice(scenarios)
        items = {k: v for k, v in scenario.items() if k != "trip"}
        answer = 1
        for count in items.values():
            answer *= count
        
        items_text = ", ".join([f"{v} {k.replace('_', ' ')} options" for k, v in items.items()])
        
        question = f"Planning a {scenario['trip']} with: {items_text}. How many different itineraries are possible?"
        
        return {
            "question": question,
            "visual_type": "multi_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([str(v) for v in items.values()]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": len(items)
        }
    
    elif problem_type == "custom_product":
        scenarios = [
            {
                "product": "custom laptop",
                "processor": 3,
                "memory": 4,
                "storage": 3,
                "color": 5
            },
            {
                "product": "custom bike",
                "frame": 4,
                "wheels": 3,
                "gears": 3,
                "color": 6
            }
        ]
        
        scenario = random.choice(scenarios)
        items = {k: v for k, v in scenario.items() if k != "product"}
        answer = 1
        for count in items.values():
            answer *= count
        
        items_text = ", ".join([f"{v} {k} options" for k, v in items.items()])
        
        question = f"Building a {scenario['product']} with: {items_text}. How many different configurations are possible?"
        
        return {
            "question": question,
            "visual_type": "multi_step",
            "visual_data": scenario,
            "correct_answer": answer,
            "explanation": " × ".join([str(v) for v in items.values()]) + f" = {answer} combinations",
            "problem_type": problem_type,
            "steps": len(items)
        }
    
    # Default fallback
    return generate_specific_problem("outfit_simple")

def display_problem():
    """Display the current problem with visualization"""
    data = st.session_state.problem_data
    
    # Display question
    st.markdown(f"### 📝 Problem {st.session_state.total_attempted + 1}")
    st.markdown(f"**{st.session_state.current_problem}**")
    
    # Display visualization based on type
    visual_type = data.get("visual_type", "text")
    
    if visual_type == "outfit":
        display_outfit_visual(data["visual_data"])
    elif visual_type == "choices":
        display_choices_visual(data["visual_data"])
    elif visual_type == "route":
        display_route_visual(data["visual_data"])
    elif visual_type == "ice_cream":
        display_ice_cream_visual(data["visual_data"])
    elif visual_type == "schedule":
        display_schedule_visual(data["visual_data"])
    elif visual_type == "uniform":
        display_uniform_visual(data["visual_data"])
    elif visual_type == "product":
        display_product_visual(data["visual_data"])
    elif visual_type == "food":
        display_food_visual(data["visual_data"])
    elif visual_type == "event":
        display_event_visual(data["visual_data"])
    elif visual_type == "sports":
        display_sports_visual(data["visual_data"])
    elif visual_type == "three_step":
        display_three_step_visual(data["visual_data"])
    elif visual_type == "multi_step":
        display_multi_step_visual(data["visual_data"])
    elif visual_type == "password":
        display_password_visual(data["visual_data"])
    elif visual_type == "tournament":
        display_tournament_visual(data["visual_data"])
    
    st.markdown("---")
    
    # Input form
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Your answer:",
            placeholder="Enter number",
            disabled=st.session_state.answer_submitted,
            key="combinations_input"
        )
        st.caption("combinations")
    
    with col2:
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            if user_input:
                try:
                    user_answer = int(user_input)
                    if user_answer > 0:
                        st.session_state.user_answer = user_answer
                        check_answer()
                    else:
                        st.error("Please enter a positive number.")
                except ValueError:
                    st.error("Please enter a whole number.")
            else:
                st.warning("Please enter your answer.")
    
    with col3:
        if st.button("Skip", type="secondary", disabled=st.session_state.answer_submitted):
            st.session_state.user_answer = None
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.rerun()
    
    # Show feedback if submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Navigation
    if st.session_state.answer_submitted:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📖 See Solution", type="secondary", use_container_width=True):
                show_tree_diagram()
            
            if st.button("Next Problem →", type="primary", use_container_width=True):
                reset_problem_state()
                st.rerun()
        
        with col3:
            if st.session_state.total_attempted > 0:
                accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
                st.metric("Accuracy", f"{accuracy:.0f}%")

def display_outfit_visual(data):
    """Display outfit choices visually"""
    st.info(f"👕 **Tops:** {data['tops_count']} options | 👖 **Bottoms:** {data['bottoms_count']} options")

def display_choices_visual(data):
    """Display general choices"""
    st.info(f"**{data['choice1_name'].title()}:** {data['choice1_count']} | **{data['choice2_name'].title()}:** {data['choice2_count']}")

def display_route_visual(data):
    """Display route choices"""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🏃 Activities:**")
        for activity in data["activities"]:
            st.markdown(f"• {activity}")
    with col2:
        st.markdown("**📍 Routes:**")
        for route in data["routes"]:
            st.markdown(f"• {route}")

def display_ice_cream_visual(data):
    """Display ice cream choices"""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🍦 Containers:**")
        for container in data.get("containers", []):
            st.markdown(f"• {container}")
    with col2:
        st.markdown("**🍨 Flavors:**")
        for flavor in data.get("flavors", []):
            st.markdown(f"• {flavor}")

def display_schedule_visual(data):
    """Display schedule options"""
    if "options1" in data:
        st.info(f"**{data['label1'].title()}:** {len(data['options1'])} | **{data['label2'].title()}:** {len(data['options2'])}")

def display_uniform_visual(data):
    """Display uniform choices"""
    st.info(f"**{data['item1'].title()}:** {len(data['colors1'])} colors | **{data['item2'].title()}:** {len(data['colors2'])} colors")

def display_product_visual(data):
    """Display product options"""
    st.info(f"**{data['item_name'].title()}:** {len(data['types'])} | **Colors:** {len(data['colors'])}")

def display_food_visual(data):
    """Display food choices"""
    st.info(f"**{data['choice1'].title()}:** {len(data['options1'])} | **{data['choice2'].title()}:** {len(data['options2'])}")

def display_event_visual(data):
    """Display event planning choices"""
    st.info(f"**{data['choice1'].title()}:** {len(data['options1'])} | **{data['choice2'].title()}:** {len(data['options2'])}")

def display_sports_visual(data):
    """Display sports equipment choices"""
    st.info(f"**{data['item1'].title()}:** {len(data['options1'])} | **{data['item2'].title()}:** {len(data['options2'])}")

def display_three_step_visual(data):
    """Display three-step choices"""
    st.markdown("**Three choices to make:**")
    count = 1
    for key, value in data.items():
        if isinstance(value, list):
            st.markdown(f"{count}. **{key.title()}:** {len(value)} options")
            count += 1

def display_multi_step_visual(data):
    """Display multi-step choices"""
    if "choices" in data:
        st.markdown("**Multiple choices to make:**")
        for i, (name, count) in enumerate(data["choices"].items(), 1):
            st.markdown(f"{i}. **{name.title()}:** {count} options")

def display_password_visual(data):
    """Display password creation info"""
    st.info(f"**Creating:** {data['description']}")
    st.markdown(f"**Positions:** {data['positions']} | **Choices per position:** {data['choices']}")

def display_tournament_visual(data):
    """Display tournament structure"""
    st.info(f"**{data['sport'].title()} Tournament:** {data['description']}")
    st.markdown(f"**Rounds:** {len(data['rounds'])}")

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
        st.info(f"⏭️ **Skipped.** The correct answer was **{data['correct_answer']} combinations**")
        st.markdown(f"📚 {data['explanation']}")
    elif st.session_state.answer_correct:
        st.success(f"✅ **Correct! {data['correct_answer']} combinations!**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.combinations_difficulty
            st.session_state.combinations_difficulty = min(
                st.session_state.combinations_difficulty + 1, 4
            )
            
            if st.session_state.combinations_difficulty > old_difficulty:
                st.balloons()
                st.info(f"🎉 **Excellent! Moving to Level {st.session_state.combinations_difficulty}**")
                st.session_state.consecutive_correct = 0
    else:
        st.error(f"❌ **Not quite. You said {st.session_state.user_answer}, but the correct answer is {data['correct_answer']} combinations.**")
        st.markdown(f"📚 {data['explanation']}")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 3:
            old_difficulty = st.session_state.combinations_difficulty
            st.session_state.combinations_difficulty = max(
                st.session_state.combinations_difficulty - 1, 1
            )
            
            if st.session_state.combinations_difficulty < old_difficulty:
                st.warning(f"⬇️ **Let's practice at Level {st.session_state.combinations_difficulty}**")
                st.session_state.consecutive_wrong = 0

def show_tree_diagram():
    """Show tree diagram or detailed solution"""
    with st.expander("📚 **Understanding the Solution**", expanded=True):
        data = st.session_state.problem_data
        
        st.markdown("### 🌳 Using the Multiplication Principle")
        st.markdown(data['explanation'])
        
        st.markdown("---")
        
        # Show visual representation based on problem type
        steps = data.get("steps", 2)
        
        if steps == 2:
            st.markdown("""
            ### Tree Diagram Example:
            
            For 2 choices, imagine a tree:
            ```
            Start
              ├─ Choice 1 Option A
              │    ├─ Choice 2 Option 1
              │    ├─ Choice 2 Option 2
              │    └─ Choice 2 Option 3
              ├─ Choice 1 Option B
              │    ├─ Choice 2 Option 1
              │    ├─ Choice 2 Option 2
              │    └─ Choice 2 Option 3
              ...
            ```
            
            **Count all the endpoints (leaves) of the tree!**
            """)
        elif steps == 3:
            st.markdown("""
            ### Three-Step Multiplication:
            
            ```
            Choice 1 × Choice 2 × Choice 3 = Total
            ```
            
            Each combination is a unique path through all three choices.
            
            **Example:** 3 × 4 × 2 = 24 combinations
            - 3 options for first choice
            - 4 options for second choice  
            - 2 options for third choice
            - Total: 3 × 4 × 2 = 24
            """)
        else:
            st.markdown(f"""
            ### Multi-Step Combination:
            
            With {steps} choices, multiply all the options:
            
            {data['explanation']}
            
            **Remember:** Each choice is independent, so we multiply!
            """)
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Quick Tips:
        - **ADD** when choosing one thing OR another
        - **MULTIPLY** when choosing one thing AND another
        - The order of multiplication doesn't matter (3 × 4 = 4 × 3)
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