class Process:
    def __init__(self, id, priority):
        self.id = id
        self.priority = priority
        self.active = True

def start_election(processes, num_processes, initiating_process_id, coordinator):
    initiator = processes[initiating_process_id - 1]
    print(f"Process {initiating_process_id} initiates the election.")

    highest_priority_id = -1
    for p in processes:
        if p.id > initiating_process_id and p.active:
            highest_priority_id = max(highest_priority_id, p.id)

    if highest_priority_id != -1:
        print(f"Process {highest_priority_id} has a higher priority. Sending election message...")
        start_election(processes, num_processes, highest_priority_id, coordinator)
    else:
        coordinator[0] = initiator
        print(f"Process {coordinator[0].id} becomes the coordinator.")

def process_fails(processes, failed_process_id, coordinator):
    failed_process = processes[failed_process_id - 1]
    failed_process.active = False
    print(f"Process {failed_process_id} fails.")

    if coordinator[0] is not None and coordinator[0].id == failed_process_id:
        coordinator[0] = None
        print("Coordinator failed. Starting new election...")
        start_election(processes, len(processes), 1, coordinator)

num_processes = 7
processes = [Process(i + 1, num_processes - i) for i in range(num_processes)]
coordinator = [None]

print("Initial state:")
for p in processes:
    print(f"Process {p.id}: Priority {p.priority}, Active: {1 if p.active else 0}")

start_election(processes, num_processes, 3, coordinator)

print("\nAfter election:")
for p in processes:
    print(f"Process {p.id}: Priority {p.priority}, Active: {1 if p.active else 0}")

process_fails(processes, coordinator[0].id, coordinator)

print("\nAfter coordinator failure:")
for p in processes:
    print(f"Process {p.id}: Priority {p.priority}, Active: {1 if p.active else 0}")

# Select a new coordinator among the remaining processes
start_election(processes, num_processes, 1, coordinator)

print("\nAfter new election:")
for p in processes:
    print(f"Process {p.id}: Priority {p.priority}, Active: {1 if p.active else 0}")
