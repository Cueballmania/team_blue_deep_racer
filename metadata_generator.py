# Packages
import itertools
import json
import os

# Information
print('---------------------------')
print('Metadata Creation Helper')
print('---------------------------')
print('')
print('This tool will create the metadata JSON file for offline DeepRacer V1 Training')

# Args
max_steering = abs(int(input('Max Steering (between 1 and 30): ')))
steering_granularity = abs(int(input('Steering Granularity (3, 5, or 7): ')))
max_speed = abs(int(input('Max Speed (between 0.1 and 12): ')))
speed_granularity = abs(int(input('Speed Granularity (1, 2, or 3): ')))

# Validation
max_steering_ok = (max_steering >=1) & (max_steering<=30)
steering_granularity_ok = steering_granularity in [3,5,7]
max_speed_ok = (max_speed >= 0.1) & (max_speed <= 12) # 12 is the max speed for Version 1 DeepRacer
speed_granularity_ok = speed_granularity in [1,2,3]

params_ok = (max_steering_ok) & (steering_granularity_ok) & (max_speed_ok) & (max_steering_ok)

# Create output json if params are ok
if params_ok:

	# Create steering angles
	steering_groups = [-max_steering + (2*max_steering/(steering_granularity-1))*i for i in range(steering_granularity)]

	# Create speed groups
	speed_unit = max_speed/speed_granularity
	speed_groups = [speed_unit*i for i in range(1,speed_granularity+1)]

	# Set up all combinations so as to zip the two lists
	combos = len(steering_groups) * len(speed_groups)

	steering_groups = list(itertools.chain.from_iterable(itertools.repeat(i,len(speed_groups)) for i in steering_groups))
	speed_groups = speed_groups*combos

	# Action space as a list of dictionaries
	action_space = []
	for steering, speed in zip(steering_groups, speed_groups):
		action_space.append({"steering_angle":steering, "speed":speed})

	# Add indices
	for i in range(len(action_space)):
		action_space[i]['index'] = i

	# Output
	output = {"action_space":action_space}

	if os.path.isfile("model_files/model_metadata.json"):
		proceed = input("File already exits, overwrite? y/n: ")

		if proceed == 'y':
			with open('model_files/model_metadata.json', 'w') as f:
				json.dump(output, f, indent=4)
			print("File saved in model_files/model_metadata.json")

		else:
			print('JSON creation canceled by user. Exiting.')

	else:
		with open('model_files/model_metadata.json', 'w') as f:
			json.dump(output, f, indent=4)

		print("File saved in model_files/model_metadata.json")

else:
	print("Invalid in put in one or more param(s). Please adjust.")


