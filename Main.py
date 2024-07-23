import difflib
import pandas as pd

from Suggestion import *

global df


class Search():

    def init(self, search, min_calories, max_calories, max_price, antiPrompt, n):
        self.search = search
        self.min_calories = min_calories
        self.max_calories = max_calories
        self.max_price = max_price
        self.antiPrompt = antiPrompt
        self.n = n
        self.df_list = []

    def filter(self):
        if self.n > 1:
            matches = difflib.get_close_matches(self.search.lower(), df['Name'].str.lower(), n=(self.n))
            filtered_df = df[df['Name'].str.lower().isin(matches)]
            filtered_df1 = filtered_df[(filtered_df['Calories'] >= self.min_calories) & (filtered_df['Calories'] <= self.max_calories)]
            filtered_df2 = filtered_df1[(filtered_df1['Price'] <= self.max_price)]
            filtered_df3 = filtered_df2[~filtered_df2['RecipeIngredientParts'].str.contains(self.antiPrompt, case=False)]
        
            df_list = [row.tolist() for _, row in filtered_df3.iterrows()] 

            if filtered_df3.empty == False:
                for i in df_list:
                    i[3] = str(i[3])
                    i[5] = str(i[5])
                for i in df_list:
                    i[3] = i[3][2:-1]
                    i[5] = i[5][2:-1]


            self.df_list = df_list

        elif self.n ==1:
            matches = difflib.get_close_matches(self.search.lower(), df['Name'].str.lower(), n=(self.n))
            filtered_df = df[df['Name'].str.lower().isin(matches)]

            df_list = [row.tolist() for _, row in filtered_df.iterrows()]

            if filtered_df.empty == False:
                for i in df_list:
                    i[3] = str(i[3])
                    i[5] = str(i[5])
                for i in df_list:
                    i[3] = i[3][2:-1]
                    i[5] = i[5][2:-1]
            self.df_list = df_list

    def __str__(self):
        return str(self.df_list)

def load_csv(file_path):
    TempDf = pd.read_csv(file_path, usecols=[1, 6, 8, 13, 16, 27, 28])
    return TempDf

def createSuggestions(suggestions):
    mealSuggestions = []

    for food in suggestions:
        tempSuggestionVal = Search(food, 0, 0, 0, 0, 1)
        tempSuggestionVal = tempSuggestionVal.filter()
        
        mealSuggestions.append(tempSuggestionVal.__str__())

    return mealSuggestions

def functionMain():
    global df

    file_path = 'modified_recipes.csv'  # Replace with your CSV file path
    df = load_csv(file_path)

    suggestionMain()
    suggestionVal = createSuggestions(suggestion)
    print(suggestionVal)


functionMain()