from src.data_process import load_csv, clean_data

DATA_FILE = "data/datapao_homework_2023.csv"

def main():
    raw_data = load_csv(DATA_FILE)
    cleaned_data = clean_data(raw_data)
    print(cleaned_data)

if __name__ == "__main__":
    main()