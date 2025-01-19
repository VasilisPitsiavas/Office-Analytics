# Smart Office Analytics

##  **Table of Contents**
- [Project Description](#project-description)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Usage](#setup-and-usage)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
  - [Outputs](#outputs)
- [Testing](#testing)
- [Function Descriptions](#function-descriptions)
  - [Data Processing](#data-processing)
  - [Analytics](#analytics)
- [Data Assumptions](#data-assumptions)
- [Testing Highlights](#testing-highlights)

---

##  **Project Description**
The **Smart Office Analytics** project processes IoT-generated event data to provide insights about employee movements. It features:
- **User Analytics**: Calculates time spent, days present, and productivity rankings.
- **Longest Session Analytics**: Identifies the longest uninterrupted work sessions.

---

##  **Features**
- **User Analytics**:
  - Calculates total hours spent in the office (`time`).
  - Computes the number of days present (`days`).
  - Determines average hours per day (`average_per_day`).
  - Ranks users based on `average_per_day`.

- **Longest Session Analytics**:
  - Identifies the longest continuous session per user.
  - Accounts for breaks exceeding 2 hours as session end.
  - Handles consecutive events appropriately.

---
## **Prerequisites**
-Python 3.8 or higher
-Required library: pytest (for testing)

---
## **Installation**
-Clone the repository: git clone https://github.com/your-username/smart-office-analytics.git
cd smart-office-analytics
---
## **Running the Project**
-Run the project using: python3 main.py
---
## **Outputs**
-User Analytics: output/user_analytics.csv
-Longest Session Analytics: output/longest_session.csv
---
## **Testing**
-Run all tests using: pytest tests/

---
##  **Project Structure**
```plaintext
smart_office_analytics/
├── data/
│   └── datapao_homework_2023.csv    # Input data file
├── output/
│   ├── user_analytics.csv          # User analytics output
│   └── longest_session.csv         # Longest session analytics output
├── src/
│   ├── __init__.py                 # Initializes the src package
│   ├── data_process.py             # Data loading and cleaning functions
│   ├── analytics.py                # Core analytics functions
├── tests/
│   ├── test_data_process.py        # Tests for data processing functions
│   └── test_analytics.py           # Tests for analytics functions
├── main.py                         # Main script to run the project
└── README.md                       # Documentation
