# FITNESS WORKOUT LOG

import requests

# API Configuration
BASE_URL = "http://localhost:5000/api/"


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("FITNESS WORKOUT LOG".center(50))
    print("=" * 50)
    print("1. Log New Workout")
    print("2. Edit Workout Details")
    print("3. Delete Workout")
    print("4. View Workouts")
    print("5. Search Workouts")
    print("6. Exit")
    print("=" * 50)


def log_workout():
    """Log a new workout"""
    print("\nEnter workout details:")
    exercise = input("Exercise: ")
    sets = input("Sets: ")
    reps = input("Reps: ")
    weights = input("Weights (optional): ")
    workout_date = input("Workout Date (YYYY-MM-DD): ")
    notes = input("Notes: ")

    if not exercise or not sets or not reps:
        print("\nExercise, sets, and reps are required!")
        return

    try:
        sets=int(sets)
        reps=int(reps)
        weights = float(weights)if weights else 0
    except ValueError:
        print("\nSets, reps must be integers and weight must be a number or decimals.")
        return

    workout_data = {
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weights":weights,
        "workout_date": workout_date if workout_date else None,
        "notes": notes if notes else None
    }

    try:
        response = requests.post(f"{BASE_URL}/workouts", json=workout_data)
        if response.status_code == 201:
            print("\nWorkout logged successfully!")
            new_workout = response.json()
            print(f"New Workout ID: {new_workout['id']}")
        else:
            print(f"\nError logging workout: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def edit_workout():
    """Edit an existing workout"""
    workout_id = input("\nEnter workout ID to edit: ")

    # First get the current workout details
    try:
        response = requests.get(f"{BASE_URL}/workouts/{workout_id}")
        if response.status_code != 200:
            print(f"\nError: {response.text if response.status_code != 404 else 'Workout not found!'}")
            return

        current_workout = response.json()
        print("\nCurrent workout details:")
        print(f"1. Exercise: {current_workout['exercise']}")
        print(f"2. Sets: {current_workout['sets']}")
        print(f"3. Reps: {current_workout['reps']}")
        print(f"4. Weights:{current_workout['weights']}")
        print(f"5. Workout Date: {current_workout['workout_date']}")
        print(f"6. Notes: {current_workout['notes']}")

        print("\nEnter new values (leave blank to keep current):")
        updates = {}

        exercise = input("New exercise: ")
        if exercise: updates["exercise"] = exercise

        sets = input("New sets: ")
        if sets:
            try:
                updates["sets"] = int(sets)
            except ValueError:
                print("Sets must be an integer!")
                return

        reps = input("New reps: ")
        if reps:
            try:
                updates["reps"] = int(reps)
            except ValueError:
                print("Reps must be an integer!")
                return

        weight = input("New weights: ")
        if weight:
            try:
                updates["weights"] = float(weight)
            except ValueError:
                print("Weight must be a number!")
                return

        workout_date = input("New workout date: ")
        if workout_date: updates["workout_date"] = workout_date

        notes = input("New notes: ")
        if notes: updates["notes"] = notes

        if not updates:
            print("\nNo changes made!")
            return

        try:
            response = requests.put(f"{BASE_URL}/workouts/{workout_id}", json=updates)
            if response.status_code == 200:
                print("\nWorkout updated successfully!")
            else:
                print(f"\nError updating workout: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\nConnection error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


    


def delete_workout():
    """Delete a workout"""
    workout_id = input("\nEnter workout ID to delete: ")
    confirm = input(f"Are you sure you want to delete workout {workout_id}? (y/n): ")

    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/workouts/{workout_id}")
        if response.status_code == 200:
            print("\nWorkout deleted successfully!")
        else:
            print(f"\nError deleting workout: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def view_workouts():
    """View progress charts"""
    try:
        response = requests.get(f"{BASE_URL}/workouts")
              
        if response.status_code == 200:
            workouts = response.json()
            if not workouts:
                print("\nNo Exercises found!")
                return
           
            print("\n" + "-" * 140)
            print(f"{'Id':<5}{'Exercises':<30}{'Sets':<15}{'Reps':<20}{'Weights':<15}{'Workout Date':<40}{'Notes':<20}")
            print("-" * 140)
            for workout in workouts:
                print(f"{workout['id']:<5}{workout['exercise']:<30}{workout['sets']:<15}{workout['reps']:<20}{float(workout['weights']):<15}{workout['workout_date']:<40}{workout['notes'][:20]:<20}")
            print("-" * 140)
        else:
            print(f"\nError fetching workout progress: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")



def search_workout():
    """View progress charts"""
    value = int(input("Enter excercise ID to search: "))
    try:
        response = requests.get(f"{BASE_URL}/workouts")
              
        if response.status_code == 200:
            workouts = response.json()
            if not workouts:
                print("\nNo Exercises found!")
                return
            
            for workout in workouts:
                if value == workout['id']:
                    print(f"Excercise: {workout['exercise']}\n Sets: {workout['sets']}\nReps: {workout['reps']}\nWeights: {float(workout['weights'])}\nDate: {workout['workout_date']}\nNote: {workout['notes'][:20]:<20}")
                    print("-" * 140)
        else:
            print(f"\nError fetching workout progress: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")






def main():
    """Main program loop"""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            log_workout()
        elif choice == '2':
            edit_workout()
        elif choice == '3':
            delete_workout()
        elif choice == '4':
            view_workouts()
        elif choice == '5':
            search_workout()

        elif choice == '6':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1-5.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
