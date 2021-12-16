<img src="https://github.com/superpeter55/superpeter55/blob/main/Peter%20Morgan.png" alt="banner that says Sarah hart Landolt - software developer, artist, designer">

# About Me

Currently a work in progress but feel free to take a look at what I have so far!

# Projects

<details>
  <summary><b> Are National Parks becoming more attractive to locals during and post-pandemic? </b></summary>
    
  ### Description
  
  With travel restrictions, border closures and shutdown of businesses across the globe throughout the pandemic, the
tourism industry has taken a significant financial hit and its outlook is still uncertain. According to the United Nations
World Tourism Organization (UNWTO), international tourist arrivals have fallen 72% between January 2020 and July
2021 for the Americas. And for the world, the overall decline in the same period was reported to be 85%.
  
  This report seeks to answer the following research question. With statewide travel guidelines to avoid non-essential out-of-state and out-of-country travel in effect throughout the pandemic, our hypothesis is that this would heighten residents’ interest in taking local trips and exploring nature in sites near them during and shortly post-reopening. The purpose of this research is to examine the effect of the pandemic on visitation to national parks. Our goal is to determine the relationship between the number of visitations to parks in the United States and variables including the number of COVID-19 cases and vaccination rate. We will use a causal model to address this research question and determine if higher vaccination rates and lower COVID cases cause more national park visits.

  Interestingly, we determined that monthly park visits have increased with increased COVID cases, COVID deaths, and vaccination numbers. We believe this is due to reduced out-of-state travel and forcing people to find alternative activities during the pandemic like visit parks. More details can be found in the final report below.

  ### Tools Used
   
  <img src="https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white" /> <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />
   <br/>
    
  ### Techniques Used
  - Linear Modeling / Least Squares Regression
  - F Tests for Coefficient Significance
  - Evaluation of Classical Linear Model (CLM) assumptions
  - Omitted Variable Bias analysis
  - Logarithmic transformation of data
  - Data visualization
  - Exploratory data analysis
  - Data cleaning
    
  ### Report and Code
  [Project Report](https://github.com/superpeter55/superpeter55/blob/main/Projects/w203_final/W203%20Final%20Report%2C%20Peter%2C%20Frances%2C%20Nitin.pdf)
  
  [R Markdown for Report](https://github.com/superpeter55/superpeter55/blob/main/Projects/w203_final/Final_Report.Rmd)  
  </details>

<details>
  <summary><b> Understanding User Behavior Through Event Tracking </b></summary>
  
  ### Description
  
  The data engineering court at Renaissance Games is pleased to present our lords and ladies with an analytics pipeline to keep a watchful eye on the activities of the merchants within the market and also to note the comings of knights and ladies in the guilds.
  
  Our sorcery (stack) of choice is as follows:
  
  - Apache Bench - "game client" sending player events into data pipeline
  - Flask - app that runs the game Application Programming Interface
  - Kafka - platform for ingesting streaming data and passing to downstream applications
  - Spark - tool to filter and transform data and push to or pull from HDFS (Hadoop Distributed File System)
  - Hadoop - distributed file system for managing parquet files
  - Hive - intermediary to track and agree upon schema and create tables
  - Presto - query tool for summarizing and reporting analytics on purchases and guild activity
  
  For a detailed breakdown of randomly and manually generated events, prithee see the project report linked below.

  Gramercy
  
  ### Additional Tools Used
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/> <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen"/> <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white"/> <img src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white"/> <img src="https://img.shields.io/badge/windows%20terminal-4D4D4D?style=for-the-badge&logo=windows%20terminal&logoColor=white"/> <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
  
  ### Report and Code
  [Report](https://github.com/superpeter55/superpeter55/blob/main/Projects/data-engineering-final-project/Project_3.ipynb)
  
  [Game API](https://github.com/superpeter55/superpeter55/blob/main/Projects/data-engineering-final-project/game_api.py)
  
  [Docker Compose File](https://github.com/superpeter55/superpeter55/blob/main/Projects/data-engineering-final-project/docker-compose.yml)
  </details>

<details>
  <summary><b> Command Line Playable Chess Game </b></summary>
  
  ### Description
  
  An interactive chess game that is playable at the command line of a terminal. Simply run the chess.py file linked below in a terminal to play. Development was executed using best practices in Object Oriented Programming. 
  
  The game features a menu system that has 4 options for the user to choose. Option 1 is to begin a game of chess. Option 2 brings up a URL to the rules of chess wikipedia page. Option 3 brings up instructions on how to make moves and option 4 exits the app. The game pieces are represented by abbreviations outlined in [this](https://github.com/superpeter55/superpeter55/blob/main/Projects/chess/Piece%20Keys.txt) file. Feel free to download the chess.py file and play!
  
  <img src="https://github.com/superpeter55/superpeter55/blob/main/Projects/chess/example%20image.PNG" />
  
  ### Tools Used
  
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" /> <img src="https://img.shields.io/badge/windows%20terminal-4D4D4D?style=for-the-badge&logo=windows%20terminal&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />
  
  ### Techniques Used
  - Object Oriented Programming
  
  ### Code
  [chess.py](https://github.com/superpeter55/superpeter55/blob/main/Projects/chess/chess.py)
  
</details>

<details>
  <summary><b> Tracking User Activity Pipeline</b></summary>
  
  ### Description
This is a pipeline that lands data in Hadoop Filesystem in a queryable format. Using Google Cloud Platform and Docker Containers to run all my applications, I fetch a nested json file of online assessment data and build a pipeline using Kafka and Spark. PySpark queries are used to perform analytics on the data. The report linked below has a detailed breakdown of how my pipeline was built as well as my findings from this dataset.
    <br/>
  ### Tools Used

<img src="https://img.shields.io/badge/Apache_Spark-FFFFFF?style=for-the-badge&logo=apachespark&logoColor=#E35A16" /> <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white" /> <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white" /> <img src="https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white" /> <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" /> <img src="https://img.shields.io/badge/windows%20terminal-4D4D4D?style=for-the-badge&logo=windows%20terminal&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" /> <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" />
  
  ### Report
  [Tracking User Activity](https://github.com/superpeter55/superpeter55/blob/main/Projects/data-engineering-project2-superpeter55/Project_2_Report.md)
  </details>
