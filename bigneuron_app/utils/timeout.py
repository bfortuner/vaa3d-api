import os
from bigneuron_app import items_log
from bigneuron_app.clients.constants import VAA3D_MIN_RUNTIME, VAA3D_MAX_RUNTIME
from bigneuron_app.clients.constants import SECONDS_PER_BYTE, BUFFER_MULTIPLIER

BYTES_PER_MEGABYTE = 1000000.0

def get_timeout(file_bytes, sec_per_byte, max_time, min_time, buffer_multiplier):
    """
    Returns estimate job item runtime w buffer between min and max
    """
    items_log.info("buffer " + str(buffer_multiplier))
    items_log.info("Filesize in MB: " + str(file_bytes/BYTES_PER_MEGABYTE))
    estimated_runtime = sec_per_byte * file_bytes
    items_log.info("Est Runtime: " + str(int(estimated_runtime)))
    timeout = int(estimated_runtime * buffer_multiplier)
    items_log.info("Est Runtime w buffer: " + str(int(timeout)))
    if timeout < min_time:
        return min_time
    elif timeout > max_time:
        return max_time
    return timeout

def get_timeout_from_file(file_path, sec_per_byte=SECONDS_PER_BYTE, max_time=VAA3D_MAX_RUNTIME,
    min_time=VAA3D_MIN_RUNTIME, buffer_multiplier=BUFFER_MULTIPLIER):
    file_bytes = os.stat(file_path).st_size
    return get_timeout(file_bytes, sec_per_byte, max_time, min_time, 
        buffer_multiplier)