import numpy as np
from main import ages_dict_men, ages_dict_women

def calculate_average_risk_by_age(ages_dict):
    average_risk_by_age = {}
    for age, year_values in ages_dict.items():
        values = list(year_values.values())
        average_risk_by_age[age] = np.mean(values)
    return average_risk_by_age


print("Average risk of death per thousand by age for men:")
average_risk_by_age_men = calculate_average_risk_by_age(ages_dict_men)
for age, average_risk in average_risk_by_age_men.items():
    print(f"Age {age}: {average_risk:.3f}")

print("\nAverage risk of death per thousand by age for women:")
average_risk_by_age_women = calculate_average_risk_by_age(ages_dict_women)
for age, average_risk in average_risk_by_age_women.items():
    print(f"Age {age}: {average_risk:.3f}")

import matplotlib.pyplot as plt

ages = list(average_risk_by_age_men.keys())

# Calculate the Difference in Risk
difference_in_risk = {age: average_risk_by_age_men[age] - average_risk_by_age_women[age] for age in ages}

# Visualize the Difference in Risk
plt.figure(figsize=(10, 6))
plt.bar(ages, list(difference_in_risk.values()))
plt.title('Difference in Average Risk of Death per Thousand between Men and Women by Age')
plt.xlabel('Age')
plt.ylabel('Difference in Average Risk of Death per Thousand')
plt.grid(True)
plt.show()

# Extract the maximum difference and its corresponding age
max_age = max(difference_in_risk, key=difference_in_risk.get)
max_difference = difference_in_risk[max_age]

print("Maximum Difference in Average Risk of Death per Thousand:")
print(f"Age: {max_age}, Difference: {max_difference:.3f}")

# Initialize a dictionary to store the difference in risk for each decade
difference_in_decades = {}

# Calculate the difference in risk for each decade
for decade in range(0, 91, 10):
    start_age = decade
    end_age = decade + 9
    # Calculate the average difference in risk for the current decade
    decade_difference = np.mean([difference_in_risk[age] for age in range(start_age, end_age + 1)])
    difference_in_decades[decade] = decade_difference

# Print the difference in risk for each decade
print("Difference in Average Risk of Death per Thousand for Each Decade:")
for decade, difference in difference_in_decades.items():
    print(f"Decade {decade}-{decade + 9}: {difference:.3f}")
