import difflib
import pandas as pd
import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
from Main import Search as s
from Main import *


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("University of Toronto Meal Plan.py")
        self.geometry(f"{1100}x{700}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        calorie_filter_range = customtkinter.StringVar(
            value='RANGE (eg. 300 - 500)')
        max_price_filter = customtkinter.StringVar(value='MAX PRICE (eg. 15)')
        self.search_filter = customtkinter.StringVar(
            value='SEARCH (eg. Biryani)')

        self.accountImage = customtkinter.CTkImage(
            Image.open("Circle-icons-profile.png"))
        self.accountButton = customtkinter.CTkButton(
            self, height=30, corner_radius=25, text="Account", image=self.accountImage)
        self.accountButton.grid(row=0, column=0, sticky="n", pady=(30, 0))

        self.titleframe = customtkinter.CTkFrame(
            self, width=600, height=10, corner_radius=5)
        self.titleframe.grid(row=0, column=0, columnspan=2,
                             sticky="n", pady=(20, 0))
        self.logo_label = customtkinter.CTkLabel(
            self.titleframe, text="Meal Planner", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.tab_options = customtkinter.CTkTabview(self, width=400)
        self.tab_options.grid(row=1, column=1, sticky="new", padx=(5, 5))

        self.tab_options.add("View Mealplan Recipes")
        self.tab_options.add("AI Meal Suggestion")
        self.tab_options.add("Edit/View Profile")

        self.sideframe = customtkinter.CTkFrame(
            self, width=200, height=230, corner_radius=5)
        self.sideframe.grid(row=1, column=0, sticky="n",
                            padx=(5, 5), pady=(19, 0))

        self.budgetlabel = customtkinter.CTkLabel(
            self.sideframe, text="Budget Goal:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.budgetlabel.grid(row=0, column=0, padx=5, pady=5)
        self.budgetbar = customtkinter.CTkProgressBar(
            self.sideframe, width=150)
        self.budgetbar.grid(row=1, column=0)

        self.calorielabel = customtkinter.CTkLabel(
            self.sideframe, text="Daily Calorie Intake:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.calorielabel.grid(row=2, column=0, padx=5, pady=5)
        self.caloriebar = customtkinter.CTkProgressBar(
            self.sideframe, width=150)
        self.caloriebar.grid(row=3, column=0)

        self.sort_label = customtkinter.CTkLabel(self.tab_options.tab(
            "View Mealplan Recipes"), text="Sort: ", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.sort_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        self.caloriesort_label = customtkinter.CTkLabel(self.tab_options.tab(
            "View Mealplan Recipes"), text="Sort By Calories:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.caloriesort_label.grid(
            row=1, column=0, columnspan=2, pady=(10, 0))
        self.caloriesort_entry = customtkinter.CTkEntry(self.tab_options.tab("View Mealplan Recipes"), width=165, placeholder_text='RANGE (eg. 300 - 500)',
                                                        placeholder_text_color="white", textvariable=calorie_filter_range, font=customtkinter.CTkFont(size=13, weight="bold"))
        self.caloriesort_entry.grid(row=2, column=0, sticky='e')

        self.pricesort_label = customtkinter.CTkLabel(self.tab_options.tab(
            "View Mealplan Recipes"), text="Sort By Price:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.pricesort_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        self.pricesort_max = customtkinter.CTkEntry(self.tab_options.tab("View Mealplan Recipes"), width=165, placeholder_text='MAX',
                                                    placeholder_text_color="white", textvariable=max_price_filter, font=customtkinter.CTkFont(size=13, weight="bold"))
        self.pricesort_max.grid(row=4, column=0, columnspan=2)

        self.searchsort_label = customtkinter.CTkLabel(self.tab_options.tab(
            "View Mealplan Recipes"), text="Search:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.searchsort_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        self.searchsort_max = customtkinter.CTkEntry(self.tab_options.tab("View Mealplan Recipes"), width=165, placeholder_text='SEARCH',
                                                     placeholder_text_color="white", textvariable=self.search_filter, font=customtkinter.CTkFont(size=13, weight="bold"))
        self.searchsort_max.grid(row=6, column=0, columnspan=2)

        self.search_button = customtkinter.CTkButton(self.tab_options.tab(
            "View Mealplan Recipes"), text="FILTER", font=customtkinter.CTkFont(size=15, weight="bold"), command=self.filter_results)
        self.search_button.grid(row=7, column=0, pady=(10, 10), columnspan=2)

        self.scrollable_results = customtkinter.CTkScrollableFrame(self.tab_options.tab(
            "View Mealplan Recipes"), width=300, height=300, corner_radius=5, fg_color="white", )
        self.scrollable_results.grid(
            row=8, column=0, columnspan=2, pady=(20, 0), padx=(20, 0))

        self.full_meal_info_frame = customtkinter.CTkFrame(self.tab_options.tab(
            "View Mealplan Recipes"), width=900, height=500, fg_color="grey")
        self.full_meal_info_frame.grid(row=0, column=3, rowspan=9, pady=(
            30, 0), padx=(30, 0), sticky="e")

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.titleframe, text="Appearance Mode:", font=customtkinter.CTkFont(size=13, weight="bold"), anchor="w")
        self.appearance_mode_label.grid(
            row=0, column=2, padx=20, pady=(10, 10))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(
            self.titleframe, values=["Light", "Dark", "System"])
        self.appearance_mode_optionmenu.grid(
            row=0, column=3, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.titleframe, text="UI Scaling:", font=customtkinter.CTkFont(size=13, weight="bold"), anchor="w")
        self.scaling_label.grid(row=0, column=4, padx=20, pady=(10, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.titleframe, values=["80%", "90%", "100%", "110%", "120%"])
        self.scaling_optionemenu.grid(row=0, column=5, padx=20, pady=(10, 10))

    def filter_results(self):

        global df, x, finalfilter

        file_path = 'modified_recipes.csv'
        df = TempDf = pd.read_csv(file_path, usecols=[1, 6, 8, 13, 16, 27, 28])

        search_variable = self.searchsort_max.cget("textvariable").get()
        price_variable = int(self.pricesort_max.cget("textvariable").get())
        calories_list = self.caloriesort_entry.cget(
            "textvariable").get().split("-")

        min_calories = int(calories_list[0])
        max_calories = int(calories_list[1])
        budget = 100
        keyword = "strawberry"

        final_filtered_df = s(search_variable, min_calories,
                              max_calories, budget, keyword, 50)
        finalfilter = final_filtered_df.filter()
        x = 0
        for i in finalfilter:
            name = str(i[0])
            price = str(i[4])
            listItemVar = customtkinter.IntVar(value=0)
            self.listItem = customtkinter.CTkRadioButton(
                self.scrollable_results, text=name + '  ' + price, variable=listItemVar, command=self.displayinfo, value=x)
            self.listItem.grid(row=x, column=0, pady=5)
            x += 1

    def displayinfo(self):
        global x, finalfilter
        self.textinfo = customtkinter.CTkLabel(
            self.full_meal_info_frame, text=finalfilter[self.listItem.cget("variable").get()])
        self.textinfo.grid(row=0, column=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
