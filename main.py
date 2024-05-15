import json
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_ages(data):
    ages = []
    for entry in data:
        nombre = entry['Nombre']
        age = int(re.findall(r'\d+', nombre)[0])
        ages.append(age)
    return ages

def extract_values(data, start, end):
    values = []
    for i in range(start, end):
        for j in range(20):
            value = data[i]['Data'][j]['Valor']
            values.append(value)
    return values

def create_dict(years, values):
    # Split values into chunks of 20 elements
    value_chunks = [values[i:i+20] for i in range(0, len(values), 20)]
    
    # Create a list of dictionaries containing pairs of years and values for each chunk
    return [{year: val for year, val in zip(years, chunk)} for chunk in value_chunks]

def create_dicts_with_indices(dict_list):
    return {idx: value for idx, value in enumerate(dict_list)}

def combine_dicts(dict1, dict2):
    combined_dict = {}
    for idx in set(dict1) | set(dict2):
        combined_dict[idx] = (dict1.get(idx), dict2.get(idx))
    return combined_dict

# Load JSON data from file
data = load_data('tdmort.txt')

# Extract ages
ages = extract_ages(data)

# Extract values for men and women
half_len = len(data) // 2
men_values = extract_values(data, 0, half_len)
women_values = extract_values(data, half_len, len(data))

# Create list of years
years = list(range(2002, 2023))
years.reverse()

# Create dictionaries for men and women
men_dict = create_dict(years, men_values)
women_dict = create_dict(years, women_values)

# Create dictionaries with indices for men and women
ages_dict_men = create_dicts_with_indices(men_dict)
ages_dict_women = create_dicts_with_indices(women_dict)

# Combine the dictionaries into a single dictionary
combined_dict = combine_dicts(ages_dict_men, ages_dict_women)

# Create a function to animate the plot
def animate(year):
    plt.clf()
    plt.title(f'Risk of Death per Thousand by Age in {year}')
    plt.xlabel('Age')
    plt.ylabel('Risk of Death per Thousand')

    handles = []
    labels = []

    for idx, (men_vals, women_vals) in combined_dict.items():
        men_value = men_vals.get(year, None)
        women_value = women_vals.get(year, None)

        if men_value is not None and women_value is not None:
            men_handle = plt.scatter(idx, men_value, label='Men', color='blue', marker='o')
            women_handle = plt.scatter(idx, women_value, label='Women', color='red', marker='x')

            if 'Men' not in labels:
                handles.append(men_handle)
                labels.append('Men')
            if 'Women' not in labels:
                handles.append(women_handle)
                labels.append('Women')

    plt.legend(handles, labels)
    plt.xticks(np.arange(0, 101, 10))
    plt.yticks(np.arange(0, 1001, 100))
    plt.grid(True)

# Create animation
ani = animation.FuncAnimation(plt.figure(), animate, frames=range(2003, 2023), repeat=False)

# Save animation as a GIF file
ani.save('transition.gif', writer='pillow', fps=2)
plt.show()
