import sys
import json
import time
import pandas as pd


def read_json(file_path):
    try:
        data = pd.read_json(file_path)

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Invalid JSON format in file: {file_path}")

    return data


def compute_sales(price_catalogue, sales_record):
    total_cost = 0.0
    price_list = price_catalogue[["title", "price"]].set_index("title")
    sales_record = sales_record.merge(
            price_list, how="left", left_on="Product", right_index=True
        )
    sales_record["import"] = sales_record["Quantity"]*sales_record["price"]
    total_cost = sales_record["import"].sum()

    return total_cost


if __name__ == "__main__":
    try:
        time_start = time.time()

        if len(sys.argv) < 3:
            raise ValueError(
                    "Error: Invalid number of arguments." +
                    "Please provide price catalogue and sales record files."
                )

        price_catalogue_path = sys.argv[1]
        sales_record_path = sys.argv[2]

        price_catalogue = read_json(price_catalogue_path)
        sales_record = read_json(sales_record_path)

        total_cost = compute_sales(price_catalogue, sales_record)

        # Show in screen
        print(f"Total Sales Cost: ${total_cost:.2f}")
        elapsed_time = time.time() - time_start
        print(f"Time elapsed: {elapsed_time} s")

        # Save in file
        with open('SalesResults.txt', 'w') as results_file:
            results_file.write(f"Total Sales Cost: ${total_cost:.2f}\n")
            results_file.write(f"Time elapsed: {elapsed_time} s")

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
