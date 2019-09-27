from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import csv
import datetime
import numpy as np



app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    out_arr = [1] # Start of the outbound array
    in_arr = [0] # Start of inbound array
    # Respond to the message, and save information to all_text_records.csv
    number = request.form['From']
    message_body = request.form['Body']
    
    response = "Thank you for your response. To view results of the poll, visit @Real_Datums on Twitter."
    resp = MessagingResponse()
    resp.message(response)

    in_arr.append(number)
    in_arr.append(datetime.datetime.now())
    in_arr.append(message_body)


    out_arr.append(number)
    out_arr.append(datetime.datetime.now())
    out_arr.append(response)

    with open('Iowa_Poll1.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(in_arr)
        writer.writerow(out_arr)
    csvFile.close()

    return str(resp)

if __name__ == "__main__":

    from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'xxxxxxxx'
    auth_token = 'xxxxxxxx'
    client = Client(account_sid, auth_token)
    bod = """Your number was randomly generated for an automated poll. Please answer the following question: Which quantity is larger,one quarter, or one third?
              Please reply 'A' for one quarter, or 'B' for one third."""
    base = '+1515200'
    suffix = np.random.choice(10000,1000, replace = False)
    suffix = suffix.astype(str)
    suffix = np.core.defchararray.zfill(suffix, 4)



    for suff in suffix:
        num = base + suff

        message = client.messages \
                .create(
                     body=bod,
                        to=num,
                        from_='xxxxxxx'
                 )

        print(message.sid)  
        out_arr = [1]
        out_arr.append(num)
        out_arr.append(datetime.datetime.now())
        out_arr.append(bod)

        with open('Iowa_Poll1.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(out_arr)
        csvFile.close()


    app.run(debug=True)
