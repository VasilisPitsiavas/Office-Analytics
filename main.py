from src.data_process import load_csv, clean_data_for_user_analytics, clean_data_for_longest_session, write_to_csv
from src.analytics import calculate_time_and_days, calculate_longest_session


def main():
    input_path = "data/datapao_homework_2023.csv"
    output_path_part1 = "output/user_analytics.csv"
    output_path_part2 = "output/longest_session.csv"

    print("Loading raw data...")
    raw_data = load_csv(input_path)

    print("Cleaning data...")
    cleaned_data_analytics = clean_data_for_user_analytics(raw_data)

    #print("Calculating time, days, and rankings...")
    user_analytics = calculate_time_and_days(cleaned_data_analytics)
    
    #print("Saving analytics results...")
    fieldnames_part1 = ['user_id', 'time', 'days', 'average_per_day', 'rank']
    write_to_csv(output_path_part1, user_analytics, fieldnames_part1)

    #print(f"User analytics saved to: {output_path_part1}")


    #print("User Analytics Data Preview:", user_analytics[:5])

    #print("Cleaned Data Preview:", cleaned_data[:5])

    #print("Calculating longest work sessions...")
    cleaned_data_session = clean_data_for_longest_session(raw_data)
    longest_sessions = calculate_longest_session(cleaned_data_session)
    #print(longest_sessions)
    #print("Saving longest session results...")
    fieldnames_part2 = ['user_id', 'session_length']

    write_to_csv(output_path_part2, longest_sessions, fieldnames_part2)
    #print(f"Longest session analytics saved to: {output_path_part2}")


if __name__ == "__main__":
    main()