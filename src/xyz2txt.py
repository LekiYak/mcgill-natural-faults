import csv
import glob

def process_xyz(filepath):
    f = open(filepath, 'r')
    print(f'Processing {filepath}')

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

    csvname = filepath.rsplit('/', 1)[-1][:-4]

    with open(f"{csvname}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(result)
        print(f'Saved as {csvname}.csv')

# Allow user to choose between directory or file input
directory_or_file = input("Directory (d) or file (f)?: ")

if directory_or_file == 'f':

    filepath = input("Enter path: ")

    # return error if file does not exist
    try:
        f = open(filepath, 'r')
        f.close()
    except FileNotFoundError:
        print("File not found")
        exit()

    process_xyz(filepath)

elif directory_or_file == 'd':

    directory_path = input("Enter directory path: ")

    # return error if directory does not exist
    try:
        file_list = glob.glob(directory_path + '/*.xyz')
    except FileNotFoundError:
        print("Directory not found")
        exit()

    file_list = glob.glob(directory_path + '/*.xyz')

    for filepath in file_list:

        process_xyz(filepath)

else:
    print('Invalid input')
