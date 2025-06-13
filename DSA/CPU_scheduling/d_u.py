import sys
from collections import deque
import math

# Global Constants
TRACE = "trace"
SHOW_STATISTICS = "stats"
ALGORITHMS = ["", "FCFS", "RR-", "SPN", "SRT", "HRRN", "FB-1", "FB-2i", "Aging"]

# Global Variables
processes = []
algorithms = []
process_to_index = {}
timeline = []
finish_time = []
turn_around_time = []
norm_turn = []
operation = ""
last_instant = 0
process_count = 0

def parse_algorithms(algorithm_chunk):
    """Parse the algorithm string and populate algorithms list."""
    global algorithms
    algorithm_parts = algorithm_chunk.split(',')
    for part in algorithm_parts:
        if '-' in part:
            algorithm_id = part[0]
            quantum_str = part.split('-')[1]
            quantum = int(quantum_str) if quantum_str else -1
        else:
            algorithm_id = part[0]
            quantum = -1
        algorithms.append((algorithm_id, quantum))

def parse_processes():
    """Parse process information from input."""
    global processes, process_to_index
    for i in range(process_count):
        process_chunk = input().strip()
        parts = process_chunk.split(',')
        process_name = parts[0]
        process_arrival_time = int(parts[1])
        process_service_time = int(parts[2])
        
        processes.append((process_name, process_arrival_time, process_service_time))
        process_to_index[process_name] = i

def parse():
    """Parse all input data."""
    global operation, last_instant, process_count, finish_time, turn_around_time, norm_turn, timeline
    
    line = input().strip().split()
    operation = line[0]
    algorithm_chunk = line[1]
    last_instant = int(line[2])
    process_count = int(line[3])
    
    parse_algorithms(algorithm_chunk)
    parse_processes()
    
    finish_time = [0] * process_count
    turn_around_time = [0] * process_count
    norm_turn = [0.0] * process_count
    timeline = [[' ' for _ in range(process_count)] for _ in range(last_instant)]

def clear_timeline():
    """Clear the timeline for next algorithm execution."""
    global timeline
    for i in range(last_instant):
        for j in range(process_count):
            timeline[i][j] = ' '

def print_finish_time():
    """Print finish times for all processes."""
    for i in range(process_count):
        print(f"Process {processes[i][0]} finished at time {finish_time[i]}")

def print_turn_around_time():
    """Print turnaround times for all processes."""
    for i in range(process_count):
        print(f"Process {processes[i][0]} turnaround time is {turn_around_time[i]}")

def print_norm_turn():
    """Print normalized turnaround times for all processes."""
    for i in range(process_count):
        print(f"Process {processes[i][0]} normalized turnaround time is {norm_turn[i]}")

def print_timeline(algorithm_index):
    """Print the execution timeline."""
    # Print time header
    for i in range(last_instant + 1):
        print(i % 10, end=" ")
    print()
    print("-" * 48)
    
    # Print process timelines
    for i in range(process_count):
        print(f"{processes[i][0]}     |", end="")
        for j in range(last_instant):
            print(f"{timeline[j][i]}|", end="")
        print(" ")
    print("-" * 48)

def print_stats(algorithm_index):
    """Print statistics for the algorithm."""
    print_finish_time()
    print_turn_around_time()
    print_norm_turn()

def first_come_first_serve():
    """Implement First Come First Serve scheduling algorithm."""
    current_time = 0
    for i in range(process_count):
        arrival = processes[i][1]
        service = processes[i][2]
        current_time = max(current_time, arrival)
        
        for j in range(service):
            timeline[current_time][i] = '*'
            current_time += 1
        
        finish_time[i] = current_time
        turn_around_time[i] = finish_time[i] - arrival
        norm_turn[i] = float(turn_around_time[i]) / service

def round_robin(quantum):
    """Implement Round Robin scheduling algorithm."""
    remaining_service_time = [processes[i][2] for i in range(process_count)]
    ready_queue = deque()
    current_time = 0
    processed_count = 0
    
    while processed_count < process_count:
        # Add arriving processes to ready queue
        for i in range(process_count):
            if processes[i][1] == current_time:
                ready_queue.append(i)
        
        if ready_queue:
            index = ready_queue.popleft()
            execution_time = min(quantum, remaining_service_time[index])
            
            for j in range(execution_time):
                timeline[current_time][index] = '*'
                current_time += 1
            
            remaining_service_time[index] -= execution_time
            
            if remaining_service_time[index] > 0:
                ready_queue.append(index)
            else:
                finish_time[index] = current_time
                turn_around_time[index] = finish_time[index] - processes[index][1]
                norm_turn[index] = float(turn_around_time[index]) / processes[index][2]
                processed_count += 1
        else:
            current_time += 1

def shortest_process_next():
    """Implement Shortest Process Next scheduling algorithm."""
    remaining_service_time = [processes[i][2] for i in range(process_count)]
    current_time = 0
    processed_count = 0
    
    while processed_count < process_count:
        min_service_time = float('inf')
        index = -1
        
        for i in range(process_count):
            if (processes[i][1] <= current_time and 
                remaining_service_time[i] > 0 and 
                remaining_service_time[i] < min_service_time):
                min_service_time = remaining_service_time[i]
                index = i
        
        if index != -1:
            for j in range(remaining_service_time[index]):
                timeline[current_time][index] = '*'
                current_time += 1
            
            finish_time[index] = current_time
            turn_around_time[index] = finish_time[index] - processes[index][1]
            norm_turn[index] = float(turn_around_time[index]) / processes[index][2]
            remaining_service_time[index] = 0
            processed_count += 1
        else:
            current_time += 1

def shortest_remaining_time():
    """Implement Shortest Remaining Time scheduling algorithm."""
    remaining_service_time = [processes[i][2] for i in range(process_count)]
    current_time = 0
    processed_count = 0
    
    while processed_count < process_count:
        min_service_time = float('inf')
        index = -1
        
        for i in range(process_count):
            if (processes[i][1] <= current_time and 
                remaining_service_time[i] > 0 and 
                remaining_service_time[i] < min_service_time):
                min_service_time = remaining_service_time[i]
                index = i
        
        if index != -1:
            timeline[current_time][index] = '*'
            current_time += 1
            remaining_service_time[index] -= 1
            
            if remaining_service_time[index] == 0:
                finish_time[index] = current_time
                turn_around_time[index] = finish_time[index] - processes[index][1]
                norm_turn[index] = float(turn_around_time[index]) / processes[index][2]
                processed_count += 1
        else:
            current_time += 1

def highest_response_ratio_next():
    """Implement Highest Response Ratio Next scheduling algorithm."""
    remaining_service_time = [processes[i][2] for i in range(process_count)]
    current_time = 0
    processed_count = 0
    
    while processed_count < process_count:
        max_response_ratio = -1
        index = -1
        
        for i in range(process_count):
            if processes[i][1] <= current_time and remaining_service_time[i] > 0:
                response_ratio = float(current_time - processes[i][1] + remaining_service_time[i]) / remaining_service_time[i]
                if response_ratio > max_response_ratio:
                    max_response_ratio = response_ratio
                    index = i
        
        if index != -1:
            for j in range(remaining_service_time[index]):
                timeline[current_time][index] = '*'
                current_time += 1
            
            finish_time[index] = current_time
            turn_around_time[index] = finish_time[index] - processes[index][1]
            norm_turn[index] = float(turn_around_time[index]) / processes[index][2]
            remaining_service_time[index] = 0
            processed_count += 1
        else:
            current_time += 1

def feedback_q1():
    """Implement Feedback Queue with quantum 1 scheduling algorithm."""
    ready_queue = deque()
    remaining_service_time = [processes[i][2] for i in range(process_count)]
    current_time = 0
    processed_count = 0
    
    while processed_count < process_count:
        # Add arriving processes to ready queue
        for i in range(process_count):
            if processes[i][1] == current_time:
                ready_queue.append(i)
        
        if ready_queue:
            index = ready_queue.popleft()
            timeline[current_time][index] = '*'
            current_time += 1
            remaining_service_time[index] -= 1
            
            if remaining_service_time[index] > 0:
                ready_queue.append(index)
            else:
                finish_time[index] = current_time
                turn_around_time[index] = finish_time[index] - processes[index][1]
                norm_turn[index] = float(turn_around_time[index]) / processes[index][2]
                processed_count += 1
        else:
            current_time += 1

def feedback_q2i():
    """Implement Feedback Queue with increasing quantum scheduling algorithm."""
    ready_queues = [deque() for _ in range(32)]
    remaining_service_time = [processes[i][2] for i in range(process_count)]
    current_time = 0
    processed_count = 0
    quantum = 1
    
    while processed_count < process_count:
        # Add arriving processes to first queue
        for i in range(process_count):
            if processes[i][1] == current_time:
                ready_queues[0].append(i)
        
        # Find first non-empty queue
        queue_level = -1
        for i in range(32):
            if ready_queues[i]:
                queue_level = i
                break
        
        if queue_level != -1:
            index = ready_queues[queue_level].popleft()
            execution_time = min(quantum, remaining_service_time[index])
            
            for j in range(execution_time):
                timeline[current_time][index] = '*'
                current_time += 1
            
            remaining_service_time[index] -= execution_time
            
            if remaining_service_time[index] > 0:
                if queue_level + 1 < 32:
                    ready_queues[queue_level + 1].append(index)
                else:
                    ready_queues[queue_level].append(index)
            else:
                finish_time[index] = current_time
                turn_around_time[index] = finish_time[index] - processes[index][1]
                norm_turn[index] = float(turn_around_time[index]) / processes[index][2]
                processed_count += 1
            
            quantum = 1 << (queue_level + 1)
        else:
            current_time += 1

def aging(quantum):
    """Implement Aging scheduling algorithm."""
    remaining_service_time = [processes[i][2] for i in range(process_count)]
    priority = [0] * process_count
    current_time = 0
    processed_count = 0
    
    while processed_count < process_count:
        max_priority = float('-inf')
        index = -1
        
        for i in range(process_count):
            if (processes[i][1] <= current_time and 
                remaining_service_time[i] > 0 and 
                priority[i] > max_priority):
                max_priority = priority[i]
                index = i
        
        if index != -1:
            execution_time = min(quantum, remaining_service_time[index])
            for j in range(execution_time):
                timeline[current_time][index] = '*'
                current_time += 1
            
            remaining_service_time[index] -= execution_time
            
            if remaining_service_time[index] <= 0:
                finish_time[index] = current_time
                turn_around_time[index] = finish_time[index] - processes[index][1]
                norm_turn[index] = float(turn_around_time[index]) / processes[index][2]
                processed_count += 1
        else:
            current_time += 1
        
        # Age all waiting processes
        for i in range(process_count):
            if processes[i][1] <= current_time and remaining_service_time[i] > 0:
                priority[i] += 1

def execute_algorithm(algorithm_id, quantum, operation):
    """Execute the specified scheduling algorithm."""
    if algorithm_id == '1':
        if operation == TRACE:
            print("FCFS  ", end="")
        first_come_first_serve()
    elif algorithm_id == '2':
        if operation == TRACE:
            print(f"RR-{quantum}  ", end="")
        round_robin(quantum)
    elif algorithm_id == '3':
        if operation == TRACE:
            print("SPN   ", end="")
        shortest_process_next()
    elif algorithm_id == '4':
        if operation == TRACE:
            print("SRT   ", end="")
        shortest_remaining_time()
    elif algorithm_id == '5':
        if operation == TRACE:
            print("HRRN  ", end="")
        highest_response_ratio_next()
    elif algorithm_id == '6':
        if operation == TRACE:
            print("FB-1  ", end="")
        feedback_q1()
    elif algorithm_id == '7':
        if operation == TRACE:
            print("FB-2i ", end="")
        feedback_q2i()
    elif algorithm_id == '8':
        if operation == TRACE:
            print("Aging ", end="")
        aging(quantum)

def main():
    """Main function to run the scheduler simulator."""
    parse()
    
    for idx, (algorithm_id, quantum) in enumerate(algorithms):
        clear_timeline()
        execute_algorithm(algorithm_id, quantum, operation)
        
        if operation == TRACE:
            print_timeline(idx)
        elif operation == SHOW_STATISTICS:
            print_stats(idx)
        
        print()

if __name__ == "__main__":
    main()