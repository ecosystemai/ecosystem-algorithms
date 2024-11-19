import os

mypath = "apis/"
all_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

for file_name in all_files:
	print(file_name)
	f = open(mypath + file_name, "r")
	all_lines = f.readlines()
	for line in all_lines:
		if line[:3] == "def":
			new_line = line[4:-2]
			print(new_line)
	print()