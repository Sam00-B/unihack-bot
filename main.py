import database
import search_test
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
def ask_unihack(problem,university,location):
    print(f"student asked '{problem}'")
    db_resutls=database.search_library(problem)
    documents=db_resutls['documents'][0]
    metadatas=db_resutls['metadatas'][0]
    distances=db_resutls['distances'][0]
    main_answer=None
    pending_hacks=[]
    for i in range(len(documents)):
        if distances[i]<1.0:
            status=metadatas[i]['status']
            aurthor=metadatas[i]['author']
            if status in ['ai_generated','verified'] and main_answer is None:
                main_answer=documents[i]
            elif status=='pending':
                pending_hacks.append((aurthor,documents[i]))
    if main_answer is  None:
        print("No good solutions found in the library. Searching the web...")
        main_answer=search_test.get_solutions_from_web(problem,university,location)
        database.save_to_library(problem,main_answer,"UniHack AI","ai_generated")
    else:
        print("Found a good solution in the library!")
    print("\n=======================================")
    print("🎓 UNIHACK OFFICIAL SOLUTION:")
    print("=======================================")
    print(main_answer)
    if pending_hacks:
        print("\n=======================================")
        print("🧑‍🎓 Hacks provided by students:")
        print("=======================================")
        for aurthor,hack in pending_hacks:
            print(f"👤 {aurthor} says: {hack}\n")
# --- RUN THE APP ---
if __name__ == "__main__":
    uni = "University of South Dakota"
    loc = "Vermillion, SD"
    
    # Test 1: A question the database already knows about
    ask_unihack("where to get cheap groceries near campus", uni, loc)
    
    # Test 2: A brand new question it has to search the web for!
   # ask_unihack("best quiet study spots on campus", uni, loc)