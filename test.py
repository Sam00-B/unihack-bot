import time
from main import ask_unihack

def print_banner(title):
    print("\n" + "="*60)
    print(f" {title} ".center(60, "="))
    print("="*60)

if __name__ == "__main__":
    
    '''print_banner("STARTING UNIHACK INTEGRATION TESTS")
    print("Follow the terminal prompts carefully to verify the ChromaDB + Gemini logic.")

    # ---------------------------------------------------------
    # PART 1: Web Search -> Save (Testing empty DB fallback)
    # ---------------------------------------------------------
    print_banner("PART 1: WEB SEARCH & SAVE PIPELINE")
    print("👉 INSTRUCTIONS: Wait for Gemini's response, then type 'yes' to save it.")
    input("Press Enter to start Part 1...")
    
    print("\n[Running Test 1...]")
    ask_unihack("best late night pizza near campus", "New York University", "New York, NY")
    
    print("\n[Running Test 2...]")
    ask_unihack("where to park for free without a permit", "University of Texas at Austin", "Austin, TX")


    # ---------------------------------------------------------
    # PART 2: Database Retrievals (Testing Low Distance / Instant Hits)
    # ---------------------------------------------------------
    print_banner("PART 2: INSTANT DATABASE RETRIEVAL")
    print("👉 INSTRUCTIONS: These should hit your loop thresholds (< 1.0 or 1.5).")
    print("   They should print the solution INSTANTLY without triggering a web search.")
    input("Press Enter to start Part 2...")
    
    print("\n[Running Test 3 - Checking NYU Pizza (Should match Test 1)...]")
    ask_unihack("best late night pizza near campus", "New York University", "New York, NY")
    
    print("\n[Running Test 4 - Checking UT Austin Parking (Should match Test 2)...]")
    ask_unihack("where to park for free without a permit", "University of Texas at Austin", "Austin, TX")


    # ---------------------------------------------------------
    # PART 3: Student Suggestions (Testing 'pending' metadata status)
    # ---------------------------------------------------------
    print_banner("PART 3: PENDING STUDENT SUGGESTIONS")
    print("👉 INSTRUCTIONS: Type 'no' to the AI solutions.")
    print("   When prompted, type a CUSTOM HACK (e.g., 'Sleep in the library basement')")
    print("   and enter your name as the author.")
    input("Press Enter to start Part 3...")

    print("\n[Running Test 5...]")
    ask_unihack("secret dorm hacks", "Harvard University", "Cambridge, MA")


    # ---------------------------------------------------------
    # PART 4: Verification of Pending Hacks (Testing your distance loops)
    # ---------------------------------------------------------
    print_banner("PART 4: THE ULTIMATE VERIFICATION")
    print("👉 INSTRUCTIONS: This searches for 'secret dorm hacks' again.")
    print("   Your loop should see the distance, skip 'verified', but catch the 'pending'")
    print("   status and print out the custom hack you just typed in Part 3!")
    input("Press Enter to start Part 4...")

    print("\n[Running Test 6 - Verifying Harvard Custom Hack...]")
    ask_unihack("secret dorm hacks", "Harvard University", "Cambridge, MA")

    print_banner("TEST RUN COMPLETE")
    print("If the custom hack showed up correctly in Part 4, your loops are working flawlessly!")'''
    '''ask_unihack("How to survive Trac", "Brac University", "Dhaka, BD") 

    ask_unihack("where to park for free without a permit", "University of Texas at Austin", "Austin, TX")'''