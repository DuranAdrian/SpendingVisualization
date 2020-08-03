from math import pi
import pandas
import json
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

# TODO: Use Tinker as GUI to view current category json data and generate pie chart

# If new categories/stores are added to json file, call this method to uppercase all keys and values
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
        for index in range(0, len(categories[cat]), 1):
            try:
                transaction.upper().index(categories[cat][index])
            except ValueError:
                continue
            else:
                return cat
    return "NO RESULTS FOUND"

# Set pie chart output file
output_file("pie.html")

# Open Category JSON file
with open("categories.json") as file:
    categories = json.load(file)
    file.close()

# TODO: Determine if csv file exist, if not, close program - alert user later
# Show list of available csv files

# Parse CSV file
accountData = pandas.read_csv("BankData.csv")

results = {}
income = 0.0

# Assume successful file
for descrip, amount in zip(accountData["Description"], accountData["Amount"]):
    found_cat = findCategory(descrip)
    
    if found_cat != "NO RESULTS FOUND":
        if found_cat == "INCOME":
            income = income + amount
        elif found_cat in results:
            results[found_cat] = float("{:.2f}".format(results[found_cat] + amount))
        else:
            results[found_cat] = amount
    else:
        # TODO: Let user know an manually insert to correct section
        # Temporary fix for missed income/deposits
        if "MONEY TRANSFER" in descrip and "FROM" in descrip:
            income = income + amount 

# Create Pie Chart from Data
data = pandas.Series(results).reset_index(name='value').rename(columns={'index':'category'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(results)]

fig = figure(plot_height=350, sizing_mode='scale_both',title="Income %s" % income, toolbar_location=None, tools="hover", tooltips="@category: @value", x_range=(-0.5, 1.0))
fig.wedge(x=0, y=1, radius=0.35, start_angle=cumsum("angle", include_zero=True), end_angle=cumsum("angle"), line_color="white", fill_color="color", legend_field="category", source=data)

fig.axis.axis_label=None
fig.axis.visible=False
fig.grid.grid_line_color = None

show(fig)
