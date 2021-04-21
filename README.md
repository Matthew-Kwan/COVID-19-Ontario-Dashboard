# COVID-19-Ontario-Dashboard
This repository will hold my code for developing a small web-based COVID-19 dashboard focused on emphasizing the severity of the spread of the disease in Ontario, Canada.

## Technical Specs
I am using:
- Python 3.8.3
- Google Chrome
- Screen size - 24in Monitor (In case it looks really weird on anything smaller, screenshot attached below for reference)

## Installation Guide

1. Clone the repository.
2. Open a terminal and navigate to the root directory.
3. In terminal, type `pip install -r requirements.txt` to install the necessary packages.
4. In the root directory, run the following in terminal: `python app.py`.
5. In a browser, navigate to `http://localhost:8050`

# Additional Notes
Below I have some notes on different topics regarding this case study. Please give it a read through if you have the chance!

## Data Cleaning and Exploration
A lot of the data cleaning I did to explore the data and come up with the visualizations happened in the `covid_data_exploration.ipynb` file in the root directory. Feel free to peruse it to see some of what I did. This was used to create some novel metrics now inherently in the raw data, such as for the proportion of new cases by covid-19 variant graph.

## Note about chosen visualizations / metrics
I decided on these metrics based on my knowledge of what would be important bottlenecks and metrics for the public health officials to make the necessary decisions. If given the opportunity, more thorough user research would have been conducted with stakeholders involved to ensure that the metrics chosen were of use.

In addition, I followed the 2-4 mark strictly, to ensure that I chose the most pertinent data visualizations / metrics I could think of. If there were more freedom, I would've included interactive line graphs for more of the Hospitalization, Death, Recovery and ICU metrics to allow stakeholders to explore historical data more freely on their own. Here I just wanted to sample some of what I could do.

## Future Work

Admittedly, my exams took longer than expected so it forced me into a time crunch for this dashboard. Future work I would consider are:

- Make the date range slider more user friendly - add calendar view for selection
- Include more basic visualizations for stakeholder exploration (if the 2-4 limit is removed)
- Make everything look a bit nicer and work a bit more responsively for different monitor sizes.

### Screenshot
![Alt text](./images/screenshot.PNG?raw=true "Optional Title")