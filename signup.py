

from datetime import date
from tabnanny import check
import sys
from signin.file_client import signIn, signUp, checkUser, forgetPassword, checkCurrentUserStatus, updateField


def intro_choice(choice):
    if choice == 1:
        userInfo = client_Signup()
        if not userInfo:
            print("Sign Up failed")
            return intro_choice(choice)
        return userInfo

    elif choice  == 2:
        userInfo = client_Signin()
        if not userInfo:
            print("Sign In failed")
            return intro_choice(choice)
        return userInfo

    else:
        print("invalid choice - exiting app.")
        exit()

def client_Signup():
    print("Welcome to Sign Up Page")
    username = input("Enter your username\n")
    password = input("Enter your password\n")
    
    # Check for entry in database
    hasAccount = checkUser(username)
    if hasAccount:
        print("Username already exists. Please try again")
        client_Signup()

    else:
        print("Username available. Creating account...")
        userInfo = signUp(username, password)
        print("You have signed up with username " + userInfo["username"])
        return userInfo

def client_Signin():
    print("Welcome to Sign In page\n")
    i = 3
    while(i):
        print("Number of Attempts: ", i-1)
        username = input("Enter your username\n")
        password = input("Enter your password\n")
        x = signIn(username, password)
        i -= 1
        if x == None and i == 1:
            forgotpassword()
            return main()
        if x:
            return x

def forgotpassword():
    print("You have entered your password incorrectly\n")
    print("Welcome to Forgot Password Page")

    username = input("Reenter your username:\n")
    new_password = input("Enter your new password:\n")
    new_password_2 = input("Re-enter your password:\n")

    if new_password == new_password_2:
        isChanged = forgetPassword(username, new_password)
        print(isChanged)
        if isChanged:
            print("You have successfully changed your password")
            return isChanged
        else:
            print("Password change failed. Username does not exist.")
            main()
    else:
        print("Passwords do not match. Redirecting to main menu...")
        main()

def waterquestions(userInfo):
    #this is the water questionnaire where average water usage can be computed 
    print("Water Questionnaire")
    print("Let us get a better idea of your latest water consumption")
    print("============================")

    #Laundry Question
    print("How much laundry do you do per week?\n")
    print("1| 1-2 times a week\n")
    print("2| 3-4 times a week\n")
    print("3| 5-7 times a week\n")
    while True:
        try:        
            select_1 = int(input("Enter your option (1/2/3)"))
            if select_1<1 or select_1>3:
                print("That is not a valid number.")
            else:
                if select_1 ==1:
                    select_1=504
                if select_1==2:
                    select_1=1008
                if select_1==3:
                    select_1=1764
                break
        except ValueError:
            print("That is not a valid number.")
        
    #try & except, if & else are used to avoid the system from crashing 
    
    #Dishes Question
    print("Amount of time used to wash dishes\n")
    print("1| Less than 5 minutes\n")
    print("2| Between 5 to 10 minutes\n")
    print("3| 11-15 minutes\n")
    print("4| 16-20 minutes\n")
    print("5| More than 20 minutes\n")
    while True:
        try:
            select_2 = int(input("Enter your option (1/2/3/4/5)"))
            if select_2<1 or select_2>5:
                print("That is not a valid number.")
            else:
                break
        except ValueError:
            print("That is not a valid number.")
    
    #Shower Question
    print("How long is your average shower?\n")
    print("1| Less than 5 minutes\n")
    print("2| Between 5 to 10 minutes\n")
    print("3| 11-15 minutes\n")
    print("4| 16-20 minutes\n")
    print("5| More than 20 minutes")
    while True:
        try:
            select_3 = int(input("Enter your option (1/2/3/4/5)"))
            if select_3<1 or select_3>5:
                print("That is not a valid number.")
            else:
                break
        except ValueError:
            print("That is not a valid number.")

    #Toilet Flush Question
    print("Does your toilet have a full or dual flush?")
    print("1| Full Flush")
    print("2| Dual Flush")
    while True:
        try:
            select_4 = int(input("Enter your option (1/2)")) 
            if select_4<1 or select_4>2:
                print("That is not a valid number.")
            else:
                break
        except ValueError:
            print("That is not a valid number.") 
    
    #Household Question      
    while True:
        try:
            house_mem = int(input("How many members are there in your household?"))
            if house_mem<1 or house_mem>20:
                print("That is not a valid household size.")
            else:
                updateField("householdMembers", house_mem, userInfo["username"])
                break
        except ValueError:
            print("That is not a valid number.") 
    
    calc_consumption(select_1, select_2, select_3, select_4, house_mem, userInfo)
    set_Target(house_mem, userInfo)
    
    
    return

def calc_consumption(select_1, select_2, select_3, select_4, house_mem, userInfo):
    current_WaterUsage = 0.0
    #current_WaterUsage (variable) will first be set as 0.
    current_WaterUsage = (select_1) + (select_2* 900) + (select_3 * 2100)
    #
    if select_4 == 1:
        current_WaterUsage += 600
    else:
        current_WaterUsage += 480
        
    current_WaterUsage *= house_mem
    #past_WaterUsage = userInfo["waterUsage"]
    #current_WaterUsage = (current_WaterUsage + past_WaterUsage)/2
    

    updateField("waterUsage", current_WaterUsage, userInfo["username"])
    
    print("=======================================================")
    print(f'Your water usage has been stored. Your estimated water usage is {current_WaterUsage} litres.')
    cost = current_WaterUsage * 0.00369 * 1.07 
    #Cost = total water (in litres) * cost of water($/litre) * 1.07 (incl. 7% GST)
    print("Your water usage will cost (incl. GST): $ {:^.2f}".format(cost))
    print("=======================================================")


   # # if there is no record for past water usage, the estimated water usage will only take account of 
       # the calculated water usage through the questionaire
   # # if there is record for past water usage, the estimated water usage will average 
       # both the calculated water usage from the questionaire and past water usage, 
       # hence providing Moving average of water usage based on each input bill 
       

def set_Target(house_mem,userInfo):
    try:
        bench_target = house_mem * 130 * 30.5
        bench_cost = bench_target * 0.00369
        #allow users to have a background info about the benchmark for their individual household size, 
        #so that they can set a feasible, practical target in the next step
        print("=======================================================")
        print(f"The benchmark target for your household size is: {bench_target} litres.")
        print("The benchmark target for your household size will be equivilent to $ {:^.2f}".format(bench_cost))
        print("Time to set a target for yourself. Remember to set a target wisely.")
        print("=======================================================")
        
        targetWaterUsage = int(input("Set a target Water Usage in litres: "))
        #targetWaterUsage is on monthly basis in terms of litres 
        updateField("targetWaterUsage", targetWaterUsage, userInfo["username"])
        #everytime user answers the water questionnaire to get the updated real-time average water usage
        #he can modify his target accordingly and it will be updated and stored in userInfo.
    except ValueError:
        print("Error! Enter a valid integer")

def reco_type1(userInfo):
    while True:
        try:
            print("=======================================================")
            print("Choose to get recommendations frzom any category")
            print("End program by entering a character into search field")
            print("1| Laundry Recommendations")
            print("2| Sink Recommendations")
            print("3| Shower Recommendations")
            print("4| Toilet Flush Recommendations")
            print("5| Return to Dashboard")
            print("=======================================================1")

            try:
                reco_choice = int(input("What option would like (1,2,3,4 or 5): "))
                if reco_choice<1 or reco_choice>5:
                    print("That is not a valid number.")
            except ValueError:
                print("Enter a valid numerical option.")
                
            if reco_choice == 1:
                print("Hi, since you have a small household, you can save water for laundry by running on a full load or  use the “small load” option. ")
        
            elif reco_choice ==2:
                print("Hi, since you have a small household, you can consider switching to a low-flow faucet that can save you half the amount of water per minute!!")

            elif reco_choice == 3:
                print("Hi, since you have a small household, you can consider installing a low-flow showerhead to save you half the amount of water per minute!!")
            
            elif reco_choice  == 4:
                print("Hi, since you have a small household, you can consider putting a plastic bottle filled with water in your toilet to reduce the amount of water used per flush!!")

            else:
                dashboard(userInfo)
                
        except ValueError or UnboundLocalError:
            print("Enter a valid numerical option.")

def reco_type2(userInfo):
    while True:
        try:
            print("=======================================================")
            print("Choose to get recommendations from any category")
            print("End program by entering a character into search field")
            print("1| Laundry Recommendations")
            print("2| Sink Recommendations")
            print("3| Shower Recommendations")
            print("4| Toilet Flush Recommendations")
            print("5| Return to Dashboard")
            print("=======================================================2")

            
            reco_choice = int(input("What option would like (1,2,3,4 or 5): "))
            if reco_choice<1 or reco_choice>5:
                print("That is not a valid number.")
            
            elif reco_choice == 1:
                print("Hi, since you have a medium household, you can save water for laundry by running on a full load or  use the “small load” option.")

            elif reco_choice ==2:
                print("Hi, since you have a medium household, you can consider switching to a low-flow faucet that can save you half the amount of water per minute!!")

            elif reco_choice == 3:
                print("Hi, since you have a medium household, you can consider installing a low-flow showerhead to save you half the amount of water per minute!")
                
            elif reco_choice == 4:
                print("Hi, since you have a medium household, you can consider putting a large plastic bottle filled with water in your toilet to reduce the amount of water used per flush!!")
            else:
                print("Returning to Dashboard...")
                dashboard(userInfo)
        
        except ValueError or UnboundLocalError:
            print("Enter a valid numerical option.")
        
def reco_type3(userInfo):
    while True:
        try:
            print("=======================================================")
            print("Choose to get recommendations from any category")
            print("End program by entering a character into search field")
            print("1| Laundry Recommendations")
            print("2| Sink Recommendations")
            print("3| Shower Recommendations")
            print("4| Toilet Flush Recommendations")
            print("5| Return to Dashboard")
            print("=======================================================3")


        
            reco_choice = int(input("What option would like (1,2,3,4 or 5): "))
            if reco_choice<1 or reco_choice>5:
                    print("That is not a valid number.")
            if reco_choice == 1:
                print("Hi, since you have a large household, you can save water for laundry by running on a full load or  use the “small load” option.")
        
            elif reco_choice ==2:
                print("Hi, since you have a large household, you can consider switching to a low-flow faucet that can save you half the amount of water per minute!!")

            elif reco_choice == 3:
                    print("Hi, since you have a large household, you can consider installing a low-flow showerhead to save you half the amount of water per minute!!")
                
            elif reco_choice == 4:
                print("Hi, since you have a large household, you can consider putting a large plastic bottle filled with water in your toilet to reduce the amount of water used per flush!!!")
                
            else:
                print("Returning to Dashboard... ")
                dashboard(userInfo)
        
        except ValueError or UnboundLocalError:
            print("Enter a valid numerical option.")

def points(userInfo):
    bill = float(input("What is your total water bill for the past month?   $"))
    waterUsage = round(bill/0.00369*1.07)
    #past month water bill ($) is divided by $0.00369(included 7% GST) to convert to waterUsage in litres 
    
    targetWaterUsage = userInfo["targetWaterUsage"]
    points = userInfo["totalPoints"] 

    if waterUsage>targetWaterUsage:
        print("You did not meet your set target")
        points  -= (waterUsage-targetWaterUsage)
        print("Total Points: ", points)
        updateField("totalPoints", points, userInfo["username"])
        recommendations(userInfo)
        
    elif waterUsage == targetWaterUsage:
        print("You have met the target. Continue with the current consumption usage")
        points +=10
        print("Total Points: ", points)
    else:
        print("Congradulations, you have outperformed your target")
        points = points + (targetWaterUsage-waterUsage)
        print("Total Points: ", points)

    updateField("totalPoints", points, userInfo["username"])

def recommendations(userInfo):
    size = userInfo["householdMembers"]
    print("household size:", size)
    if 1<= size and size <= 2:
        reco_type1(userInfo)
    if 3 <=  size and size <=4:
        reco_type2(userInfo)
    else:
        reco_type3(userInfo)
        
def main():
    print("Welcome to Smart Water Tracker\n")
    print("==============================\n")
    print("1| New User Sign Up\n")
    print("2| Existing User Sign In\n")
    print("==============================\n")

    while True:
        try:
            choice = int(input("Enter your preferred choice: "))
            

            login = intro_choice(choice)

            print("Welcome to Smart Tracker Dashboard", login["username"])
            dashboard(login)
        except ValueError:
            print("Enter one of the above 2 options")
    
def dashboard(userInfo):
    '''
    Takes in userInfo and displays the dashboard
    Example
        userInfo = {
            "username": "luke",
            "password": "12345",
            "waterUsage": 200,
            "waterUsageCost": 0,
            "targetWaterUsage": 170,
            "lastUpdated": datetime.now(),
            "totalPoints":0,
            "householdSize: 1; 
        }
    '''
    avg_water = userInfo["waterUsage"]
    avg_cost = avg_water * 0.00369 
    #
    print("==============================================")
    print(f"Your average monthly water usage is: {avg_water} litres.")
    print("Your average monthly water usage is equivilent to ${:^.2f}".format(avg_cost))
    print(f'You have {userInfo["totalPoints"]} accumulated points\n')
    print(f'Your target is {userInfo["targetWaterUsage"]}L\n')
    ## As of today, your estimated water usage is (1/2-21/2): avgconsumption (L) * days/30 = pro-rated L
    print("==============================================")

    #ONLY for 1st time user
    ## DO NOT redirect to water questions again. Only input current month total consumption
    
   
    while True:
        try:
            print("=======================================================")
            print("1| Answer the Water Questions and set your target\n")
            print("2| Add the past month's water bill to the records\n")
            print("3| Exit the Smart Water Tracker Application")
            print("=======================================================")
            choice_2 = int(input("Select options 1, 2 or 3: \n"))
            if choice_2<1 or choice_2 > 3:
                print("This is not a valid number")
            
            elif choice_2 == 1:
                waterquestions(userInfo)
            elif choice_2 == 2:
                points(userInfo)
            else:
                print("Thank you for using Smart Water Tracker!")
                print("Every drop saved will help save the Earth!")
                sys.exit()
            
        except ValueError or TypeError or UnboundLocalError:
            print("Error! Enter a valid number")
    

main()