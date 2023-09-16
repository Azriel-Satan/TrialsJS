import os
import time

# Function to count occurrences of a string in a file
def count_occurrences(file_path, search_string):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            occurrences = content.count(search_string)
        return occurrences
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return 0

# Function to calculate the depth of a file relative to the input directory
def calculate_depth(input_directory, file_path):
    relative_path = os.path.relpath(file_path, input_directory)
    return len(relative_path.split(os.path.sep))

# Input directory containing files
input_directory = '\\content\\'

# Output file path
output_file_path = 'Extras\\ExtractFunctionsCount.txt'

# Read search strings from a file, skipping lines starting with '#' and removing leading/trailing spaces
search_strings_file_path = 'Extras\\Search_Strings.txt'
search_strings = []

try:
    with open(search_strings_file_path, 'r', encoding='utf-8') as search_strings_file:
        for line in search_strings_file:
            line = line.strip()  # Remove leading and trailing spaces
            if not line.startswith('#') and line != '':
                search_strings.append(line)
except FileNotFoundError:
    print(f"File '{search_strings_file_path}' not found.")

# Dictionary to store counts for each search string
counts = {}

# Start the timer
start_time = time.time()

# Iterate over all files in the input directory
for root, _, files in os.walk(input_directory):
    for filename in files:
        file_path = os.path.join(root, filename)
        
        # Count occurrences for each search string in the current file
        file_counts = {}
        for search_string in search_strings:
            non_exclamation_mark_count = count_occurrences(file_path, search_string)
            exclamation_mark_count = count_occurrences(file_path, '!' + search_string)

            # Subtract exclamation mark count from non-exclamation mark count
            result_count = non_exclamation_mark_count - exclamation_mark_count

            # Only store and output counts greater than zero
            if result_count > 0:
                file_counts[search_string] = result_count

        # Calculate the depth of the current file
        depth = calculate_depth(input_directory, file_path)

        # Store the counts for the current file in the dictionary
        counts[(depth, filename)] = file_counts

# Calculate the script execution time
end_time = time.time()
execution_time = end_time - start_time

# Write all counts to the output file with appropriate indentation
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for (depth, filename), file_counts in sorted(counts.items()):
        indentation = '    ' * depth
        output_file.write(f"{indentation}File: {filename}\n")
        for search_string, count in file_counts.items():
            output_file.write(f"{indentation}    '{search_string}' count: {count}\n")
        output_file.write("\n")

    # Append the execution time to the end of the output file
    output_file.write(f"Script execution time: {execution_time:.2f} seconds\n")

print(f"Counts written to '{output_file_path}'")
