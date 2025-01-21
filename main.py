from src.data_process import load_csv, clean_data_for_user_analytics, clean_data_for_longest_session, write_to_csv
from src.analytics import calculate_time_and_days, calculate_longest_session
from src.clustering import employee_clustering, save_clusters_to_csv

def main():
    config = {
        "input_path": "data/datapao_homework_2023.csv",
        "output_paths": {
            "analytics": "output/user_analytics.csv",
            "longest_session": "output/longest_session.csv",
            "clusters": "output/employee_clusters.csv",
        },
        "clustering": {"k": 3},
    }

    try:
        print("Loading raw data...")
        raw_data = load_csv(config["input_path"])
        print(f"Loaded {len(raw_data)} rows of raw data.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    try:
        print("Cleaning data for user analytics...")
        cleaned_data_analytics = clean_data_for_user_analytics(raw_data)

        print("Calculating time, days, and rankings...")
        user_analytics = calculate_time_and_days(cleaned_data_analytics)

        print("Saving analytics results...")
        fieldnames_part1 = ['user_id', 'time', 'days', 'average_per_day', 'rank']
        write_to_csv(config["output_paths"]["analytics"], user_analytics, fieldnames_part1)
        print(f"User analytics saved to: {config['output_paths']['analytics']}")
    except Exception as e:
        print(f"Error processing user analytics: {e}")
        return

    try:
        print("Cleaning data for longest session analytics...")
        cleaned_data_session = clean_data_for_longest_session(raw_data)

        print("Calculating longest work sessions...")
        longest_sessions = calculate_longest_session(cleaned_data_session)

        print("Saving longest session results...")
        fieldnames_part2 = ['user_id', 'session_length']
        write_to_csv(config["output_paths"]["longest_session"], longest_sessions, fieldnames_part2)
        print(f"Longest session analytics saved to: {config['output_paths']['longest_session']}")
    except Exception as e:
        print(f"Error processing longest session analytics: {e}")
        return

    try:
        print("Clustering employees...")
        user_analytics_for_classification = load_csv(config["output_paths"]["analytics"])
        for entry in user_analytics_for_classification:
            entry["time"] = float(entry["time"])
            entry["days"] = int(entry["days"])
            entry["average_per_day"] = float(entry["average_per_day"])
            entry["rank"] = int(entry["rank"])

        cluster_assignments = employee_clustering(user_analytics_for_classification, k=config["clustering"]["k"])

        print("Saving cluster assignments...")
        save_clusters_to_csv(cluster_assignments, config["output_paths"]["clusters"])
        print(f"Cluster assignments saved to: {config['output_paths']['clusters']}")
    except Exception as e:
        print(f"Error clustering employees: {e}")
        return

    print("\nSummary:")
    print(f" - User analytics saved to: {config['output_paths']['analytics']}")
    print(f" - Longest session analytics saved to: {config['output_paths']['longest_session']}")
    print(f" - Employee cluster assignments saved to: {config['output_paths']['clusters']}")

if __name__ == "__main__":
    main()
