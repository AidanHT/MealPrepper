import wave, struct, os
import random
from openai import OpenAI
from dotenv import load_dotenv

global suggestion

def configure():
    load_dotenv()

def generateSuggestions(meals):

    MealComparisonList = ["very similar", "somewhat similar", "different"]
    UniqueMealList = ["popular", "healthy"]

    client = OpenAI(api_key = os.getenv('api_key'))

    SuggestionList = []
    for i in range(2):
        for comparison in MealComparisonList: 

            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a dictionary that can only output one name of a food"},
                    {"role": "user", "content": f'Name one food that is {comparison} but not the same as the following foods: {meals} and {SuggestionList}'},
                ]
            )
    
            SuggestionList.append(response.choices[0].message.content)

        for category in UniqueMealList:

            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a dictionary that can only output one name of a food"},
                    {"role": "user", "content": f'Name one food that is {category} and not in {SuggestionList}'},
                ]
            )
    
            SuggestionList.append(response.choices[0].message.content)            

    random.shuffle(SuggestionList)
    return SuggestionList

def suggestionMain():
    global suggestion 

    configure()
    #suggestion = generateSuggestions(["Pie", "Pizza", "Chicken", "Burger", "Lasagna"])
    suggestion = ["Pie", "Pizza", "Chicken", "Burger", "Lasagna", "Potato", "Rice", "Egg", "Cabbage", "Pineapple"]


suggestionMain()