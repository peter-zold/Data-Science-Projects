#  Suicide Rates

https://github.com/peter-zold/Data-Analytics-Projects/assets/116908950/ddce44af-cdd0-4ec9-8f86-2c5928be514d

## Introduction
I have always been interested in how to prevent tragedies and find out why they happen. As the first project of an upcoming series I decided to do an exploratory analysis on a database of suicide counts. I set up separate statistics for worldwide data, and for continents and countries. Also I have visualised the main factors influencing the number of suicides

## Dataset
### Source: 
https://www.kaggle.com/code/ashfakyeafi/suicide-rates-overview-1985-to-2016-around-globe
https://www.kaggle.com/datasets/andradaolteanu/country-mapping-iso-continent-region

### Description:
The first on is a public datasets consisting of a CSV file, holding records of the number of suicides broken down into different age groups for many countries from 1985 to 2016. Also the it has record of corresponding GDP and population data.
The other dataset is only used to map continents to the countries of the first dataset.

## Technologies used:
- Power BI
- Power Query

## Main objective:
Create a report with the following pages: 
1) Visualizations of suicide counts (per 100K people) worldwide, changes in suicide counts, and possible highlighting by gender and age groups
2) Visualizations of suicide counts (per 100K people) by continents, and possible highlighting by gender and age groups
3) Visualizations of suicide counts (per 100K people) by countries, featuring GDP per capita.  
4) A dedicated page featuring key factors incfluencing suicide count.

## Preparation:
- The datasets had to be cleaned first. I removed the HDI for year column, because it had few valid data, and the country_year column, because it hold no additional information. I set the types of numerical data to integer or decimal number and set the year to date. Also properly formatted currencies.
- During the mapping of the continents to the countries, some names had to be corrected for a proper match.
- Finally we have a fully functional and valid dataset to conduct further analysis on.
- I made 7 custom measures and 2 custom columns using DAX to create expressive measures for the analysis.

<details>
  <summary>Codes of measures and custom columns</summary>
  
  

  ```javascript
  %_of_change_in_suicide_count_per_100K = 
    VAR prev_year = CALCULATE([Average Suicide Count per 100K], DATEADD(suicide_rates_data[Date].[Date], -1, YEAR))
    VAR actual_year = CALCULATE([Average Suicide Count per 100K])
    RETURN DIVIDE(actual_year - prev_year, prev_year)

  %_of_change_in_suicide_count_per_100K = 
    VAR prev_year = CALCULATE([Average Suicide Count per 100K], DATEADD(suicide_rates_data[Date].[Date], -1, YEAR))
    VAR actual_year = CALCULATE([Average Suicide Count per 100K])
    RETURN DIVIDE(actual_year - prev_year, prev_year)

  Average Suicide Count per 100K = 
    VAR pop = SUM(suicide_rates_data[population])
    VAR suicides = SUM(suicide_rates_data[suicides_no])
    RETURN DIVIDE(suicides, pop)*100000

  Average Yearly GDP per capita = 
    VAR pop = SUM(suicide_rates_data[population])
    VAR gdp = SUM(suicide_rates_data[ gdp_for_year ($) ])
    RETURN DIVIDE(gdp, pop)

  Countries in GPD Groups = CALCULATE(DISTINCTCOUNT(suicide_rates_data[Country]), ALLEXCEPT(suicide_rates_data, suicide_rates_data[GDP per Capita Groups]))

  Latest GDP per Capita = 
    VAR country = SELECTEDVALUE(suicide_rates_data[Country])
    VAR last_year = CALCULATE(MAX(suicide_rates_data[Date].[Year]), FILTER(suicide_rates_data, suicide_rates_data[Country] = country))
    RETURN CALCULATE (
    MAX(suicide_rates_data[gdp_per_capita ($)]),
    FILTER (
        suicide_rates_data,
        suicide_rates_data[Date].[Year] = last_year)
    )

  Title GDP In Latest Year = 
    VAR country = SELECTEDVALUE(suicide_rates_data[Country])
    VAR year = CALCULATE(MAX(suicide_rates_data[Date].[Year]), FILTER(suicide_rates_data, suicide_rates_data[Country] = country))
    RETURN "GDP per Capita In " & year

  Total Average Suicide Count by 100K = 
    VAR pop = CALCULATE(SUM(suicide_rates_data[population]), ALL())
    VAR suicides = CALCULATE(SUM(suicide_rates_data[suicides_no]), ALL())
    RETURN DIVIDE(suicides, pop)*100000

  GDP per Capita Groups = MROUND(suicide_rates_data[AVG GDP per Capita], 5000)

  AVG GDP per Capita = CALCULATE(AVERAGE(suicide_rates_data[gdp_per_capita ($)]), ALLEXCEPT(suicide_rates_data, suicide_rates_data[Country]))
  ```
  
</details>
