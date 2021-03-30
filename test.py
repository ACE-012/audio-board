import time
timestamp = int(time.time()*1000.0)
print(timestamp)
time.sleep(0.30)
timestamp1 = int(time.time()*1000.0)
print(timestamp1-timestamp)