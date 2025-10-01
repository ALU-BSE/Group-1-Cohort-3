import json
import time

# Load and extract SMS transactions
with open("database/xml_to_json.json", "r") as f:
    data = json.load(f)
    transactions = data["smses"]["sms"]

target_id = input("Enter the transaction ID to search for: ")

# Linear search function
def linear_search(transactions, target_id):
    for transaction in transactions:
        if int(transaction["date"]) == target_id:
            return transaction
    return None

# Dictionary lookup function
def dictionary_lookup(transactions_dict, target_id):
    return transactions_dict.get(target_id, None)

# Build dictionary for lookup
transactions_dict = {int(t["date"]): t for t in transactions}

# Time linear search
start_time = time.time()
result_linear = linear_search(transactions, target_id)
end_time = time.time()
linear_search_time = end_time - start_time

# Time dictionary lookup
start_time = time.time()
result_dict = dictionary_lookup(transactions_dict, target_id)
end_time = time.time()
dictionary_lookup_time = end_time - start_time

# Print results
if result_linear:
    print("Linear Search: Transaction found!")
else:
    print("Linear Search: Transaction not found.")

if result_dict:
    print("Dictionary Lookup: Transaction found!")
else:
    print("Dictionary Lookup: Transaction not found.")

if result_dict:
    print("Transaction Details:")
    print(json.dumps(result_dict, indent=4))

print(f"Linear Search Time: {linear_search_time:.10f} seconds")
print(f"Dictionary Lookup Time: {dictionary_lookup_time:.10f} seconds")
