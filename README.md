# SpendingVisualization
Takes in downloaded bank activity CSV file and uses Bokeh and Python to create a local webpage to visualize spending.

I created this small project in Python to visualize my spending habits since the beginning of this year. It's not precised yet, but as a proof of concept, it works to give a semi accurate image of what my spending habits are. 
I had to create a JSON file that contains categories that contain an array of stores/activity to determine what that transaction was for.
For privacy purposes, before uploading my own CSV test file to Github, I manually scubbed out numbers, names, and ref numbers from the CSV file.

Using Pandas, I parsed through the values and used Bokeh to generate a Pie Chart that is viewable on a web browser.

## SCREENSHOT
<img src="https://github.com/DuranAdrian/SpendingVisualization/blob/master/SpendingVisualization/Screenshot/BankPieChart.png" width = 500>
