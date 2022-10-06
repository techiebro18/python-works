import csv

""" with open('Newsletter sign up interest fashion_Leads_2021-04-06_2021-04-12.csv', newline='', encoding='utf-16') as f:
    reader = csv.reader(f, delimiter='\t')
    reader = list(reader)
    for row in reader:
        print(row[12]) """
        

""" with open('19058153_5e0a90ab-0bc5-4dd0-8fbb-b6d156cac85b.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    reader = list(reader)
    for row in reader:
        print(row[0]) """

#Open files
fb_csv = open('Newsletter sign up interest fashion_Leads_2021-04-06_2021-04-12.csv', newline='', encoding='utf-16')
sendgrid_csv  = open('19058153_5e0a90ab-0bc5-4dd0-8fbb-b6d156cac85b.csv', newline='', encoding='utf-8')
result_csv    = open('results2.csv', 'w', newline='')

fb_reader       = csv.reader(fb_csv, delimiter='\t')
sendgrid_reader = csv.reader(sendgrid_csv, delimiter=',')
result_writer   = csv.writer(result_csv)

#Row Header
result_writer.writerow(['ad_id', 'ad_name', 'adset_id', 'adset_name', 'campaign_id', 'campaign_name', 'form_id', 'form_name', 'email'])


fb_reader = list(fb_reader)
# Exclude row header
fb_reader = fb_reader[1:]
sendgrid_reader = list(sendgrid_reader)
# Exclude row header
sendgrid_reader = sendgrid_reader[1:]
print(len(fb_reader))
print(len(sendgrid_reader))
for row in fb_reader:
    fb_email = row[12]
    found = False
    for srow in sendgrid_reader:
        sendgrid_email = srow[0]
        if fb_email.strip() == sendgrid_email.strip():
            found = True
            break

    if found == False:
        ad_id       = row[2]
        ad_name     = row[3]
        adset_id    = row[4]
        adset_name  = row[5]
        campaign_id = row[6]
        campaign_name = row[7]
        form_id     = row[8]
        form_name   = row[9]

        result_writer.writerow([ad_id, ad_name, adset_id, adset_name, campaign_id, campaign_name, form_id, form_name, fb_email])

#Close files
fb_csv.close()
sendgrid_csv.close()
result_csv.close()

print("------- Finished --------")