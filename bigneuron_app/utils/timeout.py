import os
from bigneuron_app import items_log
import bigneuron_app.clients.constants as c

BYTES_PER_MEGABYTE = 1000000.0

def get_timeout(file_bytes, bytes_per_sec, max_time, min_time, buffer_multiplier):
    """
    Returns estimate job item runtime w buffer between min and max
    """
    items_log.info("buffer " + str(buffer_multiplier))
    items_log.info("Filesize in MB: " + str(file_bytes/BYTES_PER_MEGABYTE))
    estimated_runtime = file_bytes / bytes_per_sec
    items_log.info("Est Runtime: " + str(int(estimated_runtime)))
    timeout = int(estimated_runtime * buffer_multiplier)
    items_log.info("Est Runtime w buffer: " + str(int(timeout)))
    return max_time
    # if timeout < min_time:
    #     return min_time
    # elif timeout > max_time:
    #     return max_time
    # return timeout

def get_timeout_from_file(file_path, bytes_per_sec=c.BASE_BYTES_PER_SEC, max_time=c.VAA3D_MAX_RUNTIME,
    min_time=c.VAA3D_MIN_RUNTIME, buffer_multiplier=c.BUFFER_MULTIPLIER):
    file_bytes = os.stat(file_path).st_size
    return get_timeout(file_bytes, bytes_per_sec, max_time, min_time, 
        buffer_multiplier)