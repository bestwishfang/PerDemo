import time
import warnings


warnings.filterwarnings('ignore', category=RuntimeWarning,
                        module='qiskit')

create_time = 1620821370762
local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(create_time * 1e-3))

print(local_time)