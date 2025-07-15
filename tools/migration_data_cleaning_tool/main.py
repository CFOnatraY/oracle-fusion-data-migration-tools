from clean_data import clean_data
from update_data import update_migrated_data

def main():
    # Step 1: Clean the data
    print("Cleaning data...")
    clean_data('input_file.xlsx')  # You can change this to your own input file

    # Step 2: Update the SITE_NUMBER
    print("Updating SITE_NUMBER...")
    update_migrated_data('clean_file.xlsx', 'reference_report.xlsx')

    print("Process completed successfully!")

if __name__ == "__main__":
    main()
    