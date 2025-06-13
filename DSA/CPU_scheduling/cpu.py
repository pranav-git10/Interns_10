import sys

# Global Constants
TRACE = "trace"
SHOW_STATISTICS = "stats"
ALGORITHMS = ["", "FCFS", "RR-", "SPN", "SRT", "HRRN", "FB-1", "FB-2i", "Aging"]

# Global Variables
processes = []
algorithms = []
processToIndex = {}
timeline = []
finishTime = []
turnAroundTime = []
normTurn = []
operation = ""
last_instant = 0
process_count = 0

# Parsing Functions
def parse_algorithms(algorithm_chunk):
    global algorithms
    for part in algorithm_chunk.split(','):
        split_parts = part.split('-')
        algorithm_id = split_parts[0][0]
        quantum = int(split_parts[1]) if len(split_parts) > 1 and split_parts[1] else -1
        algorithms.append((algorithm_id, quantum))


def parse_processes():
    global processes, processToIndex
    for i in range(process_count):
        process_chunk = input().strip()
        parts = process_chunk.split(',')
        process_name = parts[0]
        process_arrival_time = int(parts[1])
        process_service_time = int(parts[2])
        processes.append((process_name, process_arrival_time, process_service_time))
        processToIndex[process_name] = i
          
def parse():
    global operation, last_instant, process_count
    algorithm_chunk = ""
    inputs = input().strip().split()
    operation = inputs[0]
    algorithm_chunk = inputs[1]
    last_instant = int(inputs[2])
    process_count = int(inputs[3])
    
    parse_algorithms(algorithm_chunk)
    parse_processes()
    
    global finishTime, turnAroundTime, normTurn, timeline
    finishTime = [0] * process_count
    turnAroundTime = [0] * process_count
    normTurn = [0.0] * process_count
    timeline = [[' ' for _ in range(process_count)] for _ in range(last_instant)]