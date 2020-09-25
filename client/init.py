import daemon 
import time 
from client import main

with daemon.DaemonContext():
    main()