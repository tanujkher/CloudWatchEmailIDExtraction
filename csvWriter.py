import csv 

def writeFile(fileName, fileHeader, fileContent):
    with open(fileName, 'w', newline='', encoding='utf-8') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fileHeader) 
        csvwriter.writerows(fileContent)