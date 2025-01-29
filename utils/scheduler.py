from flask_apscheduler import APScheduler
from update_temporary_db.update_temporary_db import update_temporary_db
from insert_precip_db.insert_precip_long_db import insert_precip_long_db
from insert_precip_db.insert_precip_db import insert_precip_db
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
from time import sleep

# Set up logging for the scheduler
LOG_FILENAME = 'logs/scheduler.log'
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Keep 3 backup log files

# Create a rotating file handler
rotating_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Set up the root logger
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(rotating_handler)

def start_scheduler():
    scheduler = APScheduler()

    # Add the update_temporary_db task to run every minute
    scheduler.add_job(id='update_temporary_db', func=update_temporary_db, trigger='interval', minutes=1)

    # Add the insert_precip_long_db task to run every minute
    scheduler.add_job(id='insert_precip_long_db', func=insert_precip_long_db, trigger='interval', minutes=4)

    # Add the insert_precip_db task to run every minute
    scheduler.add_job(id='insert_precip_db', func=insert_precip_db, trigger='interval', minutes=5)
    
    # Add listeners for job execution and errors
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # Start the scheduler
    scheduler.start()

    # Keep the scheduler running in the background
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

# Scheduler setup and logging
def job_listener(event):
    """Listener function to log job execution events"""
    if event.exception:
        logging.error(f'Job {event.job_id} failed with exception: {event.exception}')
    else:
        logging.info(f'Job {event.job_id} completed successfully.')

if __name__ == '__main__':
    can_run = False
    try:
        logging.debug(f'Try ბლოკში წარმატებით შევიდა პროგრამა')
        while True:
            logging.debug(f'While ბლოკში წარმატებით შევიდა პროგრამა')
            current_time = datetime.now()

            if current_time.minute % 10 in [0,5] and current_time.second < 45:
                can_run = True
                logging.debug(f'')
                break
            else:
                logging.debug(f'1 წამიანი პაუზა')
                sleep(1)
    except:
        logging.debug(f'Except ბლოკში შევიდა პროგრამა')
        can_run = True

    if can_run:
        logging.debug(f'Scheduler წარმატებით გაეშვა, დაწყების დრო: {datetime.now()+timedelta(hours=4)}')
        start_scheduler()
