# US Baby Names

## Introduction
In my teaching work over the past few years, I have observed how quickly naming trends evolve.
So I thought I'd look at a database of names to find out what are the specificities of naming trends, how and why did the changes happen possibly uncover the reasons behind it. I focused on more popular names, be they annual hits or evergreen ones.

If the Jupyter Nootbook file doesn't render on GitHub, please visit this link for viewing:

https://nbviewer.org/github/peter-zold/Data-Analytics-Projects/blob/main/US%20Baby%20Names/Baby%20Names%20Analysis.ipynb

## Dataset
### Source: 
https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-state-and-district-of-columbia-data

### Description:
This public dataset consists of many CSV files, holding records of baby names in each year from 1910 to 2022.
A file from the dataset consists of names, which gender they belong and how many times were they given in that year.
The name of each file refers to the US state which the data belongs to.

## Technologies used:
Python with numpy, pandas, matplotlib, seaborn and plotpy libraries used in Jupyter Notebook.

## Questions answered:
- How naming diversity changed from 1910 to 2022?
- What are the most used names per year and of all time? What trends can we observe in their usage?
- What are names which had a steep increase in popularity once?
- What names could perform in a balanced way over the years?
- How the trends evolved in different states?
- What other trends can be observed?

## Other tasks carried out:
- Raw CSV files had to be merged and cleaned. A dataframe without state information was created for optimizing the process time of analysis.
- Some uniqe metrics were created to express a name's popularty more efficiently.

## Credits:
Thanks to Alexander Hagmann for his analysis on a similar dataset, providing many ideas for my own work.
