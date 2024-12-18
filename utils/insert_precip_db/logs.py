from datetime import datetime
import os



log_filename = "log"
script_path = os.path.dirname(os.path.realpath(__file__))

"""
ფუნქცია, რომელიც გადაცემულ message - ს ჩაწერს  მითტითებულ log ფაილში
ან დაბეჭდავს ტერმინალში
""" 
def log(message, empty_line=False):
    log_file_path = script_path + "/" + log_filename
    pid  = os.getpid()
    with open(log_file_path, "a") as log_file:
        if not empty_line:
            log_file.write("[" + datetime.now().strftime('%Y-%m-%d %T') + "] [" + str(pid) + "] " + message + "\n")
        else:
            log_file.write("\n")
