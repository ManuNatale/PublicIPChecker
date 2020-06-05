# PublicIPChecker
A script that alert you by email when your public IP change

The script use gmail server, you need a gmail account and [Allow less secure apps turned ON](https://myaccount.google.com/lesssecureapps)

**Usage:**
 - You need to enter your gmail login (email and password)
 - And enter the email address that will receive alert
 
The script check your public IP address every minute and store it in a .txt file. If the IP is not the same as the one in the file, you will receive an email alert with the new IP address, the .txt file will be updated.
