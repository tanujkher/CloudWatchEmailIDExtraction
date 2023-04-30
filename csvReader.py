import csv
from logGroupCsvExport import logGroupResultForEmail
from csvWriter import writeFile

log_group = '/aws/lambda/DataPassFunction'
fileName = 'EmailIDList.csv'

with open(fileName, mode ='r')as file:
   
  csvFile = csv.reader(file)

  emails = []
  headerArr = ['Email ID', 'JSON Body']
  counter = False

  for line in csvFile:
        if counter:
          emails.append(line)
        else:
           if(not (headerArr == line)):
              break
        counter = True
  
  if counter:
    for line in emails:
       line[1] = logGroupResultForEmail(line[0], log_group)
    # print(emails)
    writeFile(fileName, headerArr, emails)
  else:
     print('csv file header should be of the following format ' + str(headerArr))