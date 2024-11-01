from queue import Queue
from threading import Event

shared_queue = Queue()
update_event = Event()
