from src.data_process import load_csv, clean_data_for_user_analytics, clean_data_for_longest_session, write_to_csv
from src.analytics import calculate_time_and_days, calculate_longest_session
from src.prediction import prepare_time_series, moving_average_forecast, save_forecast_to_csv
from src.clustering import employee_clustering, save_clusters_to_csv
import csv

def main():
    input_path = "data/datapao_homework_2023.csv"
    output_path_part1 = "output/user_analytics.csv"
    output_path_part2 = "output/longest_session.csv"
    output_path_clusters = "output/employee_clusters.csv"
    #output_path_forecast = "output/attendance_forecast.csv"



    print("Loading raw data...")
    raw_data = load_csv(input_path)

    print("Cleaning data...")
    cleaned_data_analytics = clean_data_for_user_analytics(raw_data)

    print("Calculating time, days, and rankings...")
    user_analytics = calculate_time_and_days(cleaned_data_analytics)

    print("Saving analytics results...")
    fieldnames_part1 = ['user_id', 'time', 'days', 'average_per_day', 'rank']
    write_to_csv(output_path_part1, user_analytics, fieldnames_part1)

    print(f"User analytics saved to: {output_path_part1}")


    #print("User Analytics Data Preview:", user_analytics[:5])

    #print("Cleaned Data Preview:", cleaned_data[:5])

    print("Calculating longest work sessions...")
    cleaned_data_session = clean_data_for_longest_session(raw_data)
    longest_sessions = calculate_longest_session(cleaned_data_session)
    #print(longest_sessions)
    print("Saving longest session results...")
    fieldnames_part2 = ['user_id', 'session_length']

    write_to_csv(output_path_part2, longest_sessions, fieldnames_part2)
    print(f"Longest session analytics saved to: {output_path_part2}")


    #print("Preparing time series data...")
    #time_series = prepare_time_series(cleaned_data)

    #if not time_series:
    #    print("No data available for forecasting. Exiting.")
    #    return

    #print("Forecasting future attendance using moving average...")
    #forecast = moving_average_forecast(time_series, window=3, steps=7)

    #print("Saving forecast results...")
    #save_forecast_to_csv(forecast, output_path_forecast)
    #print(f"Attendance forecast saved to: {output_path_forecast}")

    

    user_analytics_for_classification = load_csv(output_path_part1)

    for entry in user_analytics_for_classification:
        entry["time"] = float(entry["time"])
        entry["days"] = int(entry["days"])
        entry["average_per_day"] = float(entry["average_per_day"])
        entry["rank"] = int(entry["rank"])

    print("Clustering employees...")
    cluster_assignments = employee_clustering(user_analytics_for_classification, k=3)

    print("Saving cluster assignments...")
    save_clusters_to_csv(cluster_assignments, output_path_clusters)
    print(f"Cluster assignments saved to: {output_path_clusters}")

   
if __name__ == "__main__":
    main()