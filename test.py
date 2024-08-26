# Dictionary with keys and values
person_info = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "occupation": "Engineer"
}

# Loop through the dictionary using a for loop
for key in person_info:
    print(key)
    # Access the value corresponding to the current key
    value = person_info[key]
    # Print the key and its corresponding value
    print(f"{key}: {value}")
