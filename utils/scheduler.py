from flask_apscheduler import APScheduler
from update_temporary_db.update_temporary_db import update_temporary_db
from insert_precip_db.insert_precip_long_db import insert_precip_long_db
from insert_precip_db.insert_precip_db import insert_precip_db
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
from logging.handlers import RotatingFileHandler

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
    start_scheduler()
