def search(file_location):
    dummy = []
    with open(file_location,"r") as file:
        cond = False
        for line in file:
            if line.split() == []:
                continue
            if ("ttyACM" in line) or (cond):
                if cond:
                    if "(CDC ACM)" in line:
                        dev_type = line
                        dummy.append(dev_type[26:])
                        #dummy.append('')
                        cond = False
                else:
                    dev_check = line.split()[1].split('/')
                    dummy.append((dev_check[4],dev_check[5],dev_check[-1]))
                    cond = True
    if dummy == []:
        print("No Device is connected !")
    else:
        for d in dummy:
            print(d)


file_location = input("Enter file location: ")

search(file_location)