class Scheduler:
    def __init__(self, schedule):
        # Schedule: (ops, trans_num, data_item)
        # Lock table: data_item => (lock_type, trans_list)
        self.schedule = schedule

        self.lock_table = dict()
        self.final_schedule = []

    def has_lock(self, trans_num, data):
        return data in self.lock_table.keys() and trans_num in self.lock_table[data][1]

    def upgrade_lock(self, trans_num, data):
        if self.lock_table[data][0] == "X":
            return
        elif len(self.lock_table[data][1]) == 1:
            self.lock_table[data] = ("X", self.lock_table[data][1])
            self.final_schedule.append(("XL", trans_num, data))
        else:
            raise Exception("Lock is not available")

    def commit_transaction(self, transaction):
        self.final_schedule.append(transaction)

        for data in list(self.lock_table):
            try:
                self.lock_table[data][1].remove(transaction[1])
                self.final_schedule.append(("UL", transaction[1], data))
            except Exception:
                pass

            if len(self.lock_table[data][1]) == 0:
                del self.lock_table[data]

    def grant_lock(self, trans_num, data, lock):
        if not data in self.lock_table.keys():
            self.lock_table[data] = (
                lock,
                [
                    trans_num,
                ],
            )
            self.final_schedule.append((f"{lock}L", trans_num, data))
        elif self.lock_table[data][0] == "S" and lock == "S":
            self.lock_table[data][1].append(trans_num)
            self.final_schedule.append(("SL", trans_num, data))
        else:
            raise Exception("Lock is not available")

    def add_to_final(self, transaction):
        lock = ""
        if transaction[0] == "R":
            lock = "S"
        elif transaction[0] == "W":
            lock = "W"

        if lock != "" and not self.has_lock(transaction[1], transaction[2]):
            try:
                self.grant_lock(transaction[1], transaction[2], lock)
                self.final_schedule.append(transaction)
            except Exception as e:
                raise e
        elif lock == "S":
            self.final_schedule.append(transaction)
        elif lock == "W":
            try:
                self.upgrade_lock(transaction[1], transaction[2])
                self.final_schedule.append(transaction)
            except Exception as e:
                raise e
        else:
            self.commit_transaction(transaction)

    def generate_schedule(self):
        queue = []

        while len(self.schedule) > 0 or len(queue) > 0:
            sche_len = len(self.schedule)
            queue_len = len(queue)

            # Get the current schedule and queue
            transaction = self.schedule[0] if sche_len > 0 else None

            # Try to add the current transaction in queue
            try:
                while len(queue) > 0:
                    if queue[0] is not None:
                        self.add_to_final(queue[0])
                        queue = queue[1:]
            except Exception:
                pass

            # Try to add the current transaction
            try:
                if transaction is not None:
                    self.add_to_final(transaction)
                    self.schedule = self.schedule[1:]

            except Exception as e:
                remaining_schedule = []
                for i in range(len(self.schedule)):
                    if self.schedule[i][1] == transaction[1]:
                        queue.append(self.schedule[i])
                    else:
                        remaining_schedule.append(self.schedule[i])

                self.schedule = remaining_schedule

            # If the schedule length and queue length doesnt change,
            # a deadlock has occured
            if len(self.schedule) == sche_len and len(queue) == queue_len:
                raise Exception("Deadlock")

    def print_final_schedule(self):
        for transaction in self.final_schedule:
            print(f"{transaction[0]}{transaction[1]}({transaction[2]})", end="; ")
        print()
        
    @staticmethod
    def from_file(file_path):
        with open(file_path, mode="r") as f:
            file_str = f.read()
            operations = map(lambda x: x.strip() ,file_str.split(";"))
            
            schedule = [(ops[0], int(ops[1]), ops[3]) for ops in list(operations)]
            return Scheduler(schedule)