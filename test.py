# Import the main function from your main.py file!
from main import ask_unihack

if __name__ == "__main__":
    
    print("=== STARTING UNIHACK TESTS ===")

    # ---------------------------------------------------------
    # PART 1: 3 Different Universities (Web Search -> Save)
    # INSTRUCTIONS: Run these, wait for the AI to find an answer, and type 'yes' to save them.
    # ---------------------------------------------------------
    
    # Test 1
    #ask_unihack("best late night pizza near campus", "New York University", "New York, NY")
    
    # Test 2
    #ask_unihack("where to park for free without a permit", "University of Texas at Austin", "Austin, TX")
    
    # Test 3
    #ask_unihack("easiest elective classes to boost GPA", "University of Florida", "Gainesville, FL")


    # ---------------------------------------------------------
    # PART 2: 2 Database Retrievals (Instant Hits)
    # INSTRUCTIONS: Run these AFTER you finish Part 1. 
    # It should NOT search the web. It should instantly print the official solution.
    # ---------------------------------------------------------
    
    # Test 4 (Should pull the NYU pizza answer from Test 1)
    #ask_unihack("best late night pizza near campus", "New York University", "New York, NY")
    
    # Test 5 (Should pull the UT Austin parking answer from Test 2)
    # ask_unihack("where to park for free without a permit", "University of Texas at Austin", "Austin, TX")


    # ---------------------------------------------------------
    # PART 3: 4 Student Suggestions (Fail 3 Times -> Custom Entry)
    # INSTRUCTIONS: For these, type 'no' 3 times in a row! 
    # When it asks if you found a solution, type a fake hack and enter your name.
    # ---------------------------------------------------------

    # Test 6
    #ask_unihack("secret dorm hacks", "Harvard University", "Cambridge, MA")
    
    # Test 7
    # ask_unihack("how to get free printing in the library", "Stanford University", "Stanford, CA")
    
    # Test 8
    #ask_unihack("best professors for intro to psych", "Ohio State University", "Columbus, OH")
    
    # Test 9
    #ask_unihack("quietest place to take a nap", "University of Washington", "Seattle, WA")


    # ---------------------------------------------------------
    # PART 4: The Ultimate Verification (Test 10)
    # INSTRUCTIONS: Run this AFTER you complete Test 6. 
    # It should search the database, fail to find an 'official' answer, 
    # but it SHOULD print out the custom student hack you typed in Test 6!
    # ---------------------------------------------------------

    # Test 10
    #ask_unihack("secret dorm hacks", "Harvard University", "Cambridge, MA")