import csv

test_string = [(16777219, 'Administrator', 'TEST', 'Microsoft Windows NT Advanced Server 10.0'), 
(16777220, 'administrator', 'TEST2', 'Microsoft Windows NT Server 10.0')]

rist = list(test_string)

#-----------------

#with open('export.csv', 'w', encoding='utf-8', newline='') as f:
#    fields = ['Resource_id', 'Username', 'Hostname', 'OS']
#    writer = csv.DictWriter(f, fields, delimiter=',')
#    writer.writeheader()
#    for pc in rist:
#        writer.writerow(pc)


with open('export.csv','wb') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Resource_id', 'Username', 'Hostname', 'OS'])
    for row in test_string:
        csv_out.writerow(row)