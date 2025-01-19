from src.data_process import load_csv, clean_data, write_to_csv
from src.analytics import calculate_time_and_days


def main():
    input_path = "data/datapao_homework_2023.csv"
    output_path_part1 = "output/user_analytics.csv"

    print("Loading raw data...")
    raw_data = load_csv(input_path)

    print("Cleaning data...")
    cleaned_data = clean_data(raw_data)

    print("Calculating time, days, and rankings...")
    user_analytics = calculate_time_and_days(cleaned_data)

    print("Saving analytics results...")
    fieldnames_part1 = ['user_id', 'time', 'days', 'average_per_day', 'rank']
    write_to_csv(output_path_part1, user_analytics, fieldnames_part1)

    print(f"User analytics saved to: {output_path_part1}")

if __name__ == "__main__":
    main()