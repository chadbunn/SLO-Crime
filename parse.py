import os, datetime, csv

infile = r'reports.txt'
outfile = r'reports_parsed.csv'

#Create an list aggregator to hold all csv values
csv_data = []

with open(infile) as f:
    for line in f.readlines():  ##read through each line in the file

        #Look for keywords in a line and extract the data that follows it
        if "Received:" in line:
            record = {}  ##create a dictionary to hold incident-level data
            record["incident"] = line[0:9].strip()
            record["date"] = line[10:18].strip()
            record["dayofweek"] = datetime.datetime.strptime(record["date"],'%m/%d/%y').strftime('%A')
            record["received"] = line[28:33].strip()
            record["dispatched"] = line[45:50].strip()
            record["arrived"] = line[59:64].strip()
            record["cleared"] = line[73:80].strip()

        elif "Type:" in line:
            record["type"] = line[6:20].strip()
            record["location"] = line[71:80].strip()

        elif "Addr:" in line:
            parseaddress = line[6:49].partition(";")[0].strip().split(",")
            record["addr"] = parseaddress[0]
            record["city"] = "San Luis Obispo"
            record["state"] = "CA"
            record["clearcode"] = line[64:80].strip()

        elif "Responsible Officer:" in line:
            record["officer"] = line[21:80].strip()

        elif "Units:" in line:
            record["units"] = line[6:80].strip()

        elif "Des:" in line:
            ##This line appears to terminate an incident record
            csv_data.append(record)


if os.path.exists(outfile):  ##check to see if the output exists already
    os.remove(outfile)

#Write the data to a CSV file
with open (outfile, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')

    #create the header row
    csvwriter.writerow(["Incident","Address", "City", "State", "Type", "Location", "Date", "Day of Week", "Time Received", "Time Dispatched", "Time Arrived", "Time Cleared"])

    #Add individual records to the CSV
    for record in csv_data:
        csvwriter.writerow([ record["incident"], record["addr"], record["city"], record["state"], record["type"], record["location"], record["date"], record["dayofweek"], record["received"], record["dispatched"], record["arrived"], record["cleared"] ])

print "Data converted to :" + str(outfile)
