file1 = open("depth.txt", "r")
file2 = open("value.txt" ,"r")
while True:
    f1 = file1.read()
    f2 = file2.read()
    print(f1, "End of first file", f2)

