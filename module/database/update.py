import schedule, time
import db, test

schedule.every(5).seconds.do(test.testprint)

while True:
    schedule.run_pending()
    time.sleep(1)