# DEV NOTE: The 'pending' status was originally meant for moderation, 
# but right now it is exclusively used to identify student-submitted hacks 
# so we can display them separately from 'ai_generated' or 'verified' solutions.
import database
import search_test
import time

def search_answer_from_web(problem,university,location,rejected_answers=[]):
    return search_test.get_solutions_from_web(problem,university,location,rejected_answers)
def ask_unihack(problem,university,location):
    print(f"student asked '{problem}'")
    db_results=database.search_library(problem,university,location)
    print("\n--- DATABASE DIAGNOSTIC ---")
    print(db_results)
    print("---------------------------\n")
    documents=db_results['documents'][0]
    metadatas=db_results['metadatas'][0]
    distances=db_results['distances'][0]
    main_answer=None
    pending_hacks=[]
    for max_distance in [1.0, 1.5, 2.0, 2.5]: 
        for i in range(len(documents)):
            if distances[i] < max_distance:
                status=metadatas[i]['status']
                aurthor=metadatas[i]['author']
                if status in ['ai_generated','verified'] and main_answer is None:
                    main_answer=documents[i]
                elif status=='pending':
                   if (aurthor, documents[i]) not in pending_hacks:
                        pending_hacks.append((aurthor, documents[i]))
        if main_answer or pending_hacks:
            break
    if main_answer is  None and not pending_hacks :
        print("No good solutions found in the library. Searching the web...")
        attempts = 0
        max_attempts = 3
        rejected_answers = [] # Keep track of bad answers
        solution_found = False
        while attempts < max_attempts:
            time.sleep(3)
            main_answer=search_answer_from_web(problem,university,location,rejected_answers)
            print(main_answer)
            while True:
                feedback = input("Did this solution work for you? (yes/no): ").strip().lower()
        
                if feedback in ['yes','y']:
                    print("Great! Saving this solution to the library for future students...")
                    database.save_to_library(problem,main_answer,"UniHack AI","verified",university,location)
                    solution_found = True
                    break
                elif feedback in ['no','n']:
                    print("Sorry to hear that. we won't save this solution, but we'll keep trying again to find a better one!")
                    rejected_answers.append(main_answer) # Add this answer to the rejected list
                    attempts += 1
                    break
                else:
                    print("Invalid feedback. Please enter 'yes' or 'no'.")
            if solution_found:
                break
        if not solution_found:
            print("\nSorry, we couldn't find a good solution from the web after 3 tries.")
            print("Did you manage to find the answer yourself?")
            user_solution = input("If yes, please enter your solution here to help future students (or press Enter to skip): ").strip()
        
            if user_solution:
                author_name = input("What is your name? (Press Enter to stay Anonymous): ").strip()
                if not author_name:
                    author_name = "Anonymous Student"
                
                print("Thank you! Saving your hack to the database...")
            # Save as 'pending' so it shows up in the pending_hacks section for others!
                database.save_to_library(problem, user_solution, author_name, "pending", university, location)
        return
    if pending_hacks:
        print("\n=======================================")
        print("🧑‍🎓 Hacks provided by students:")
        print("=======================================")
        for aurthor, hack in pending_hacks:
            print(f"👤 {aurthor} says: {hack}\n")
            
                
            
    else:
        print("Found a good solution in the library!")
        print("\n=======================================")
        print("🎓 UNIHACK OFFICIAL SOLUTION:")
        print("=======================================")
        print(main_answer)
    

'''if __name__ == "__main__":
    # Test 3
    ask_unihack("easiest elective classes to boost GPA", "University of South Dakota", "Vermillion, SD")'''
