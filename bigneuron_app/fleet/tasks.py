import time
import traceback
from bigneuron_app import tasks_log
from bigneuron_app.fleet import fleet_manager

FLEET_UPDATE_SLEEP=60
FLEET_UPDATE_MAX_RUNS=20

def update_fleet():
	count = 0
	while count < FLEET_UPDATE_MAX_RUNS:
		try:
			tasks_log.info("Update Jobs and JobItems Fleets. Attempt " + str(count))
			fleet_manager.update_fleet_capacity()
		except Exception, err:
			tasks_log.error(traceback.format_exc())
		finally:
			count += 1
			time.sleep(FLEET_UPDATE_SLEEP)