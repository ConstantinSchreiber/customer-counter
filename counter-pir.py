### packet import
import sys
import time
import datetime
import RPi.GPIO as GPIO
import mechanize


### GPIO setup
PIN = 11 # <-declare BOARD Pin that the output jumper of the PIR is connected to
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


### Mechanize setup
mech = mechanize.Browser()


### Variables setup
t=time.time() # get current time as starting point for timing

location = 'Eingang'  # <- Define for each Location the counter is set up
upload_intervall = 300 # <- Define intervall for uploading (in s)

customer_count = 0.0
customer_count_upload = 0.0



### Main loop
while True:

	if time.time()-t>upload_intervall and customer_count > 0: # Checks the time. If n seconds have passed since last check nad the customer count changed it uploads to form
		try:
			url = "https://docs.google.com/forms/d/e/1FAIpQLScCgWIKrXQVwIBOKf2OmQA2IAiE-OI7si32AMW3FRTwhfAf9g/formResponse?ifq&entry.2023070382=%s&entry.431224590=%s&submit=Submit" % (location, customer_count_upload)
			mech.open(url) 
			print "%s new customers were counted at %s. Upload complete. Time: %s" % (customer_count_upload, location, time.strftime("%H:%M:%S"))
			customer_count = 0.0
			t=time.time()
			sys.exit
		except:
			print "Error uploading to form."
			
		
	elif GPIO.input(PIN) == True:
		customer_count = customer_count + 0.5 #Adds 0.5 because each customer enters and exits the store, thus two passes = 1 customer
		customer_count_upload = str(customer_count).replace('.',',') #Converting US to GER spelling
		print "Location: %s. New Customers Detected: %s. Time: %s " % (location, customer_count, time.strftime("%H:%M:%S"))
		sys.exit
