# Students Performance in Exams


https://github.com/peter-zold/Data-Analytics-Projects/assets/116908950/421535f6-8c0f-4709-9b8c-8417673e19aa


## Introduction
I stumbled across the Students Performance in Exams dataset by chance and instantly fell in love with it! It is a practice dataset with data of students socioeconomic status, preparation and exam results. I made a report with summarization of the student's overall performance and some aspects of their individual performance.

## Dataset
### Source: 
https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

### Description:
This public dataset consists of a CSV file. It hold records of students' gender, parents' education level, luch price reduction, ethnicity, test preparation status, and of course math, reading and writing exam results.

## Technologies used:
- Power BI
- Power Query

## Main Objective:
Create a report of two pages:
- Visualizations of statistics of math, reading, writing and average total scores and their distribution, with possible filtering on all socioecenomic values
- Visualizations of individuals' scores: difference between subjects, best and worst subjects, key influencers on scoring high or low.

## Other tasks carried out:
- Checked if any cleaning is required. (Data was clean)
- Made several helper column for statistical analysis in Power Query (average total score, difference in all three subject's score).
- Made 2 calculated columns and 15 measures written in DAX. (Can be viewed in the list below)

<details>
  <summary>Codes of measures and custom columns (contains only one of each of the similar functionality)</summary>
 
  

  ```javascript
  average math score = CALCULATE(AVERAGE(StudentsPerformance[math score]), ALL())

  math gauge comparison = 
    VAR target = [average math score] 
    VAR actual = AVERAGE(StudentsPerformance[math score])
    RETURN IF(actual > target, "Greater than average", IF(actual = target, "", "Less than average"))

    Title = IF(NOT(ISBLANK(SELECTEDVALUE(StudentsPerformance[gender], BLANK()))), SELECTEDVALUE(StudentsPerformance[gender]),
            IF(NOT(ISBLANK(SELECTEDVALUE(StudentsPerformance[lunch], BLANK()))), SELECTEDVALUE(StudentsPerformance[lunch]),
            IF(NOT(ISBLANK(SELECTEDVALUE(StudentsPerformance[race/ethnicity], BLANK()))), SELECTEDVALUE(StudentsPerformance[race/ethnicity]),
            IF(NOT(ISBLANK(SELECTEDVALUE(StudentsPerformance[parental level of education], BLANK()))), SELECTEDVALUE(StudentsPerformance[parental level of education]),
            IF(NOT(ISBLANK(SELECTEDVALUE(StudentsPerformance[test preparation course], BLANK()))), SELECTEDVALUE(StudentsPerformance[test preparation course]),
            "Overall")))))

  Best subject = 
    VAR SummaryTable =
      UNION (
        ROW ( "best score", "math score", "Column Value", 'StudentsPerformance'[math score] ),
        ROW ( "best score", "reading score", "Column Value", 'StudentsPerformance'[reading score] ),
        ROW ( "best score", "writing score", "Column Value", 'StudentsPerformance'[writing score] )
      )
      VAR Result =
    CONCATENATEX ( TOPN ( 1, SummaryTable, [Column Value] ), [best score], ", " )
      RETURN Result

    % of best subject is math = DIVIDE(COUNTROWS(FILTER('StudentsPerformance', CONTAINSSTRING(StudentsPerformance[Best subject], "math"))), COUNT(StudentsPerformance[math score]))
  ```
  
</details>

