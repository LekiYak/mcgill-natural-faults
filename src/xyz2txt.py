import csv 

filepath = input("Enter path: ")

f = open(filepath, 'r')

master = []
for line in f:
    master.append(line.strip())
f.close()

master = master[14:]
master = master[0:-1]

individuals = [string.split() for string in master]

result = [] 
for sublist in individuals:
    float_sublist = []
    for x in sublist:
        if x == 'No' or x == 'Data':
            continue
        else:
            float_sublist.append(float(x))
    result.append(float_sublist)

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(result)