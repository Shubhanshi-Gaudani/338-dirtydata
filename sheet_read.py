from src import csvToMatrix, file_path

pth = file_path()
print(pth)

with open(pth, 'r', encoding = 'utf-8-sig') as sheet:
    for line in sheet:
        print(line.replace('\n', '').split(','))

for row in csvToMatrix(pth):
    print(row)

