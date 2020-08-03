from math import pi
import pandas
import json
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

def upperCaseAllValues():
    # Open Category JSON file
    with open("categories.json") as file:
        categories = json.load(file)
        file.close()

    for category in categories:
        new_value = category.upper()
        categories[new_value] = categories.pop(category)

        for index in range(0, len(categories[category]), 1):
            categories[category][index] = categories[category][index].upper() 


    with open("categories.json", "w") as file:
        json.dump(categories, file)
        file.close()

def findCategory(transaction):
    # Read in Categories to data variable 
    for cat in categories:
        # print("LOOKING AT CATEGORY: %s" % cat)
        # print("PARSING THROUGH ALL VALUES....")
        for index in range(0, len(categories[cat]), 1):
            try:
                transaction.upper().index(categories[cat][index])
            except ValueError:
                # This will just item not found in given position
                continue
            else:
                # if cat == "INCOME":
                #     print("FOUND IN VALUE: %s" % categories[cat][index])
                
                return cat
    return "NO RESULTS FOUND"

# Set pie chart output file
output_file("pie.html")

# Open Category JSON file to read category contents
with open("categories.json") as file:
    categories = json.load(file)
    file.close()

# TODO: Determine if csv file exist, if not, close program - alert user later
# Show list of available csv files

# Parse CSV file
accountData = pandas.read_csv("Adrian_CheckingData.csv")

results = {}
income = 0.0

# -------------------------------------------------------------------------------------

# for descrip, amount in zip(accountData["Description"], accountData["Amount"]):
#     found_cat = findCategory(descrip)
#     if found_cat != "NO RESULTS FOUND":
        # if found_cat == "TRANSFERS":
            # print("%s ------ %s" % (descrip, amount))
        # if found_cat in results:
        #     results[found_cat] = float("{:.2f}".format(results[found_cat] + amount))
        # else:
        #     results[found_cat] = amount

# -------------------------------------------------------------------------------------





# Assume successful file
for descrip, amount in zip(accountData["Description"], accountData["Amount"]):
    # print("---------------")
    # print(descrip + " ---- " + str(amount))
    # print("---------------")
    # print(findCategory(descrip))
    found_cat = findCategory(descrip)
    if found_cat != "NO RESULTS FOUND":
        # print("---------------")
        # print("FOUND CAT: %s" % found_cat)
        if found_cat == "INCOME":
            income = income + amount
        elif found_cat in results:
            results[found_cat] = float("{:.2f}".format(results[found_cat] + amount))
        else:
            results[found_cat] = amount
    else:
        # TODO: Let user know an manually insert to correct section
        if "MONEY TRANSFER" in descrip and "FROM" in descrip:
            income = income + amount
print(results)

    


# Create Pie Chart from Data
data = pandas.Series(results).reset_index(name='value').rename(columns={'index':'category'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(results)]

fig = figure(plot_height=1000, plot_width=800, sizing_mode='scale_both',title="Income %s" % income, toolbar_location=None, tools="hover", tooltips="@category: @value", x_range=(-0.5, 1.0))
fig.wedge(x=0, y=1, radius=0.50, start_angle=cumsum("angle", include_zero=True), end_angle=cumsum("angle"), line_color="white", fill_color="color", legend_field="category", source=data)

fig.axis.axis_label=None
fig.axis.visible=False
fig.grid.grid_line_color = None

#Show Completed Pie Chart
show(fig)
# -------------------------------------------------------------------
# Code Testing Below
# Comment out after testing
# -------------------------------------------------------------------
# data = pandas.read_csv("Adrian_CheckingData.csv")

# Read each list name, and count the length of its values

# with open("categories.json") as file:
#     categories = json.load(file)
#     file.close()

# pie_values = {}
# for category in categories:
#     pie_values[category] = len(categories[category])

# print(pie_values)

# print(data.columns.tolist())
# for value in data["Description"].values:
#     print(value)
#     user_input = input()
#     if user_input == "c":
#         continue
#     elif user_input == "q" :
#         break