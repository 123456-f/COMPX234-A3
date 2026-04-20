import socket
import threading
import time

tuple_space = {}  # 元组空间
lock = threading.Lock()  # 线程安全锁

#Define statistical numbers (starting from 0)
total_clients = 0               # How many clients have been connected in total
active_clients = 0              # The client currently being connected
total_ops = 0                   # How many operations were processed in total
total_read = 0                  # Read times
total_get = 0                   # GET times
total_put = 0                   # PUT times
total_errors = 0                # Number of errors

