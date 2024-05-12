import json

def get_demo_user():
    global demo_user
    print("Entering demo mode")

    # Read company domains from the JSON file
    user_data = 'user_submitted_data.json'
    with open(user_data, 'r') as file:
        user_submitted_data = json.load(file)
        user_names_and_ids = [{"ID": user["ID"], "name": user["name"]} for user in user_submitted_data["users"]]
    user_count = len(user_submitted_data["users"])
    print(f"Found {user_count} users: ")
    for user_name_and_id in user_names_and_ids:
        print(user_name_and_id)

    demo_user_id = int(input(f"Choose a user to demo, by ID, from 1 to {user_count}: " ))
    print(demo_user_id)
    for demo_user in user_submitted_data["users"]:
        if demo_user["ID"] == demo_user_id:
            return demo_user

def run_demo_user(input_type: dict) -> dict:
    # takes the demo user data and outputs, extract only first if multiple locations, job roles given
    demo_user_criteria =  {
    "job role": demo_user["roles"][0],
    "location": demo_user["location"][0],
    "industries": demo_user["industries"], ## need to overwrite this due to mapping issue
    "keywords": demo_user["keywords"],
    "company size (minimum)": demo_user["company size (minimum)"],
    "company size (maximum)": demo_user["company size (maximum)"]
    }
    print(f"running for user {demo_user['ID']}, {demo_user['name']}")
    return demo_user_criteria