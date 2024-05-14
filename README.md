# Data Science Project : analysis of elite athletes' performances in World Athletics

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [License](#license)

## Project Description
This project aims to give an overview of the performances of the best runners in the world over the past few years, using data scraped on [World Athletics](https://worldathletics.org/) 
It will try to characterise and quantify athlete's progression and the evolution of theri profile throughout their carreer

## Features
- You will have access to a first folder containing all the code necessary to the scraping of the different databases in the Web_scraping folder. This contains one file for the athlete database scraping, and another one for the performances.
- The folder Data contains all the data generated within this project (or needed for the report), from the tables scraped to the figures generated in the analysis part.
- The folder Preprocessing contains the code that helps process the data, one file for each type of database, one file to modify them.
- The folder analysis focuses on the generation of the analysis of the data, the different models fitted on the data and the figures obtained. It contains one file for the clustering part, one file for the map generation and one file for the age distribution task (all are described in the report).

## Installation

To install all the dependencies needed to run this code:
    ```bash
    pip install -r requirements.txt
   
 ```

To clone the repository, download : 
git clone https://github.com/vincentmichelangeli/Data-Science-Project.git
cd Data-Science-Project

To run it you have a few parts : 

Web scraping : This takes a few hours to run so be mindful (you have access to the database directly in the folders)
python Web_scraping/athlete_scraping.py
python Web_scraping/performance_scraping.py 

Preprocessing : Once you have downloaded the previous database, one way or another, to get the clean ones :
python Preprocessing/preprocessed_data_generation.py

Analysis : To plot all the relevant data
python Analysis/plot_generation.py

In the report file you have the tex file you can run to generate the pdf that is in the same folder





