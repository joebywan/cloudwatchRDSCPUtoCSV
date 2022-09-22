from subprocess import getoutput
from datetime import datetime
from datetime import timedelta
from json import loads
from csv import writer

LatestTime = "2022-09-21T01:00:00"
dbInstanceIdentifier = "dbidentifier"
daysToRetrieve = 31
csvOutput = [["Identifier","Timestamp","CPU Usage"]]
statistics = "Average"

for day in range(0, daysToRetrieve):
  endTime = datetime.isoformat(datetime.strptime(LatestTime, "%Y-%m-%dT%H:%M:%S") - timedelta(days=day))
  startTime = datetime.isoformat(datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S") - timedelta(days=1))
  cwOutput = getoutput(f'aws cloudwatch get-metric-statistics --namespace "AWS/RDS" --metric-name "CPUUtilization" --start-time {startTime}Z --end-time {endTime}Z --period 300 --statistics {statistics} --dimensions Name=DBInstanceIdentifier,Value={dbInstanceIdentifier}')
  daysOutput = {}
  daysOutput = loads(cwOutput)

  for dataPoint in range(0, len(daysOutput['Datapoints'])):
    Timestamp = daysOutput['Datapoints'][dataPoint]['Timestamp']
    cpuUsage = daysOutput['Datapoints'][dataPoint][statistics]
    csvOutput.append([dbInstanceIdentifier,Timestamp,cpuUsage])

with open('output.csv', 'w', newline='') as file:  # Open the file, write the data.
  writer = writer(file)
  writer.writerows(csvOutput)
