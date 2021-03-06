import requests
import smtplib
import time

# send email
def sendEmail(emailObj, emailText, emailTo) :

  TO = emailTo
  SUBJECT = '%s' % emailObj
  TEXT = emailText
  
  # Gmail Sign In
  try:
    gmail_sender = 'YourEmail@gmail.com' #Your email login
    gmail_passwd = 'emailPassword' # Your email password

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
  except:
    print('Error Login gmail')

  BODY = '\r\n'.join(['To: %s' % TO,
                      'From: %s' % gmail_sender,
                      'Subject: %s' % SUBJECT,
                      '', TEXT])

  try:
      server.sendmail(gmail_sender, [TO], BODY)
      print ('email sent')
      return True
  except:
      print ('error sending mail')
      return False
  server.quit()

def main():

    emailTo = 'alertEmailTobeSentTo' #Email alert to send to
    error = 0

    while (True):

        try:
            try:
                # Get public IP address
                publicIP = requests.get('http://ip.42.pl/raw').text
                print(f'Actual public IP: {publicIP}')
            except:
                publicIP = requests.get('https://api.ipify.org').text
                print(f'Actual public IP: {publicIP}')
            
            # Create file if it doesn't exist
            try:
                f= open("publicIP.txt","x")
                f.close()
            except:
                pass
            
            # Open file to read old IP and compare it
            try:
                f=open("publicIP.txt", "r")
                oldIP = f.read()
                print(f'Old IP: {oldIP}')
            except Exception as e:
                error += 1
                sendEmail('Error in open file for read', f'Error: {e}', emailTo)
            
            try:
                if (oldIP != publicIP):
                    print(f'IP changed ! New IP: {publicIP}')
                    # write the new ip in the file
                    f= open("publicIP.txt","w")
                    f.write(str(publicIP))
                    f.close()
                    emailError = 0
                    while (emailError < 80):
                        # send an alert email
                        emailSent = sendEmail('Public IP changed !', f'The new IP is: {publicIP}', emailTo)
                        if (emailSent == True):
                            break
                        emailError += 1
                        time.sleep(5)
                else:
                    print('IP ok')
            except:
                pass
            
            error = 0
        except Exception as e:
            error += 1
            sendEmail('Error in while loop', f'Error: {e}', emailTo)
            
        if (error > 7):
            break
            
        time.sleep(60)
    
main()