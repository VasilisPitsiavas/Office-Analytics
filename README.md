# Smart Office Analytics

## **Table of Contents**
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
  - [Clustering](#clustering)
- [Data Assumptions](#data-assumptions)
- [Testing Highlights](#testing-highlights)

---

## **Project Description**
The **Smart Office Analytics** project processes IoT-generated event data to provide insights about employee movements. It features:
- **User Analytics**: Calculates time spent, days present, and productivity rankings.
- **Longest Session Analytics**: Identifies the longest uninterrupted work sessions.
- **Employee Clustering**: Groups employees into clusters based on their attendance patterns.

---

## **Features**
- **User Analytics**:
  - Calculates total hours spent in the office (`time`).
  - Computes the number of days present (`days`).
  - Determines average hours per day (`average_per_day`).
  - Ranks users based on `average_per_day`.

- **Longest Session Analytics**:
  - Identifies the longest continuous session per user.
  - Accounts for breaks exceeding 2 hours as session end.
  - Handles consecutive events appropriately.

- **Employee Clustering**:
  - Groups employees into clusters using K-Means clustering.
  - Uses `average_per_day` and `days` as input features.
  - Provides insights into employee attendance behavior.

---

## **Project Structure**
```plaintext
smart_office_analytics/
├── data/
│   └── datapao_homework_2023.csv    # Input data file
├── output/
│   ├── user_analytics.csv          # User analytics output
│   ├── longest_session.csv         # Longest session analytics output
│   └── employee_clusters.csv       # Employee clustering output
├── src/
│   ├── __init__.py                 # Initializes the src package
│   ├── data_process.py             # Data loading and cleaning functions
│   ├── analytics.py                # Core analytics functions
│   ├── clustering.py               # Employee clustering functions
├── tests/
│   ├── test_data_process.py        # Tests for data processing functions
│   ├── test_analytics.py           # Tests for analytics functions
│   └── test_clustering.py          # Tests for clustering functions
├── main.py                         # Main script to run the project
└── README.md                       # Documentation
```

---

## **Setup and Usage**
### **Prerequisites**
- Python 3.8 or higher.
- Required library: `pytest` (for testing).

---

### **Installation**
```bash
# Clone the repository:
git clone https://github.com/vasilis_pitsiavas/office-analytics.git
cd office-analytics
```

---

### **Running the Project**
```bash
# Run the project:
python3 main.py
```

---

### **Outputs**
- **User Analytics**: `output/user_analytics.csv`
  - Contains employee time, days, average per day, and rank.
- **Longest Session Analytics**: `output/longest_session.csv`
  - Contains each employee's longest continuous session.
- **Employee Clusters**: `output/employee_clusters.csv`
  - Contains cluster assignments for each employee.

---

## **Testing**
Run all tests to validate the project's functionality:
```bash
pytest tests/
```

---

## **Function Descriptions**
### **Data Processing**
- **`load_csv`**: Loads raw data from a CSV file.
- **`clean_data_for_user_analytics`**: Cleans raw data for user analytics.
- **`clean_data_for_longest_session`**: Cleans raw data for longest session analytics.
- **`write_to_csv`**: Writes processed data to a CSV file.

### **Analytics**
- **`calculate_time_and_days`**: Computes total time, days present, average time per day, and rank for each user.
- **`calculate_longest_session`**: Identifies the longest work session for each user.

### **Clustering**
- **`employee_clustering`**: Groups employees into clusters using the K-Means algorithm. It uses `average_per_day` and `days` as features.
- **`save_clusters_to_csv`**: Saves cluster assignments to a CSV file.

---

## **Data Assumptions**
- **User Analytics**:
  - Input data must include `user_id`, `event_type`, and `event_time`.
  - Event types are either `GATE_IN` or `GATE_OUT`.
- **Clustering**:
  - Clustering is performed on `average_per_day` and `days` from the user analytics output.

---

## **Testing Highlights**
- **Data Processing**:
  - Validates CSV loading and data cleaning for analytics and session data.
- **Analytics**:
  - Ensures time, days, and rankings are calculated correctly.
  - Tests longest session calculation with various input scenarios.
- **Clustering**:
  - Verifies K-Means clustering groups employees correctly based on attendance patterns.
  - Handles edge cases such as empty input or mismatched data.

---

