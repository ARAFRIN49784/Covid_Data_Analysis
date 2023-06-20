
import psycopg2
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



conn = psycopg2.connect(database="UsaDeath",
                        host="localhost",
                        user="postgres",
                        password= "Tori49784",
                        port="5432")
                        
cursor = conn.cursor()
cursor.execute("DROP TABLE usa_death")
cursor.execute(
     """
    CREATE TABLE IF NOT EXISTS usa_death (
         id SERIAL NOT NULL PRIMARY KEY,
         province_state VARCHAR(100),
         country VARCHAR(10),
         lat FLOAT,
         lon FLOAT,
         date DATE,
         confirmed INT,
         deaths INT
     )
     """
 )

with open ('usa_county_wise.csv', 'r') as f :
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute (
            "INSERT INTO usa_death VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            row
        )
    show_all_death=cursor.execute("SELECT * FROM usa_death")
    one = cursor.fetchone()
    all=cursor.fetchall()

    cursor.execute("SELECT confirmed, deaths FROM usa_death")
    data = cursor.fetchall()

    # Extract the confirmed and deaths counts into separate lists
    confirmed_counts = [row[0] for row in data]
    deaths_counts = [row[1] for row in data]
    
     # Plot the data
    bar_width = 6
    plt.figure(figsize=(8, 6))
    plt.bar(np.arange(len(confirmed_counts)), confirmed_counts,width=bar_width, label='Confirmed')
    plt.bar(np.arange(len(deaths_counts))+ bar_width, deaths_counts,width=bar_width, label='Deaths')
    plt.xlabel('Record')
    plt.ylabel('Count')
    plt.title('COVID-19 Confirmed and Deaths Counts in USA')
    plt.legend()
    plt.savefig('Figure_1.png')  # Save the plot as an image file
    plt.show()
    
    

    # Define the send_email function
    def send_email(subject, body, sender, recipients, bcc_recipients, password, attachment_path):
    # Create the email message
      msg = MIMEMultipart()
      msg["From"] = sender
      msg["To"] = ", ".join(recipients)
      msg["Subject"] = subject

    # Add the email body
      msg.attach(MIMEText(body, "plain"))

    # Add the attachment
      with open(attachment_path, "rb") as attachment:
          part = MIMEBase("application", "octet-stream")
          part.set_payload(attachment.read())
          encoders.encode_base64(part)
          part.add_header("Content-Disposition", f"attachment; filename= {attachment_path}")
          msg.attach(part)

    # Create the SMTP connection and send the email
      with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients + bcc_recipients, msg.as_string())

        print("Message sent!")



# Specify the email details
    subject = "COVID-19 Counts Plot"
    body = "Please find attached the plot of COVID-19 confirmed and deaths counts in USA.\n\nBest regards,\nSadia Afrin\nData Analyst"
    sender = "afrinsadia682@gmail.com"
    recipients = ["almehady@gmail.com", "1810892@iub.edu.bd"]
    bcc_recipients = ["1810892@iub.edu.bd"]
    password = "bhtoagjabbogluun"
    attachment_path = "Figure_1.png"  # Update with the correct path to the plot image file

# Call the send_email function to send the email
    send_email(subject, body, sender, recipients, bcc_recipients, password, attachment_path)

    conn.commit()

    conn.close()
   

    #x = np.arange(0, 5, 0.1);
    #y = np.sin(x)
    #plt.plot(x, y)
    #plt.show(block=True)
    






