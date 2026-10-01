from datetime import datetime
from threading import Thread, Semaphore
from typing import List, Dict, Any
import time

INITIAL_TIMESTAMP = datetime.now()
total_earnings = 0.0
vip_count = 0

sem_store_capacity = None
sem_lock = None
vip_bouncer = None
vip_lock = None
ticket_price_global = 0.0
n_vips_global = 0


def get_elapsed_seconds() -> float:
    return round((datetime.now() - INITIAL_TIMESTAMP).total_seconds(), 1)


class CustomerThread(Thread):
    def __init__(self, data):
        super().__init__(name=data["name"])
        self.data = data

    def run(self):
        global total_earnings
        global vip_count

        name = self.data["name"]
        join_delay = self.data["joinDelay"]
        time_in_store = self.data["timeInStore"]
        ticket_count = self.data["ticketCount"]
        is_vip = self.data["VIP"]

        time.sleep(join_delay)

        if not is_vip and n_vips_global > 0:
            vip_bouncer.acquire()
            vip_bouncer.release()

        sem_store_capacity.acquire()
        print(f"{get_elapsed_seconds()}s: {name} (entering)")
        time.sleep(time_in_store)
        print(f"{get_elapsed_seconds()}s: {name} (leaving)")
        sem_store_capacity.release()

        sem_lock.acquire()
        total_earnings += ticket_count * ticket_price_global
        sem_lock.release()

        if is_vip and n_vips_global > 0:
            vip_lock.acquire()
            vip_count += 1
            last = (vip_count == n_vips_global)
            vip_lock.release()
            if last:
                vip_bouncer.release()


def simulate_store(customers: List[Dict[str, Any]],
                   ticket_price: float,
                   max_occupancy: int,
                   n_vips: int) -> float:

    global total_earnings
    global vip_count
    global sem_store_capacity
    global sem_lock
    global vip_bouncer
    global vip_lock
    global ticket_price_global
    global n_vips_global

    ticket_price_global = ticket_price
    n_vips_global = n_vips

    sem_store_capacity = Semaphore(max_occupancy)
    sem_lock = Semaphore(1)
    vip_lock = Semaphore(1)
    vip_bouncer = Semaphore(0 if n_vips > 0 else 1)

    threads_list: List[Thread] = []

    for c in customers:
        t = CustomerThread(c)
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

    return total_earnings
