import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def find_collabora_online_path(start_path):
    for root, dirs, files in os.walk(start_path):
        if 'collabora-online' in dirs:
            return os.path.join(root, 'collabora-online')
    raise NotImplementedError("Path not found")

#Each csv contains an empty cell at the end, so need exclude that value
def remove_empty_strings(string):
    return string != ""


def read_latency_performance_data(filepath):
    data = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            data.append([int(val) for val in row if remove_empty_strings(val)])
    return headers, np.array(data)


def plot_latency_performance_data(headers, data, title):

    plt.figure(figsize=(15, 7))
    for i, row in enumerate(data):
        plt.bar(headers, row, alpha=0.5, label=f'Run {i+1}')

    plt.xlabel('Response Time')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(rotation=45) #rotating the x-axis labels by 45 degrees to make them more readable
    plt.legend()
    plt.tight_layout()
    plt.show()

def read_bandwidth_data(filepath):
    incoming = []
    outgoing = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            incoming.append(int(row[0]))
            outgoing.append(int(row[1]))
    return incoming, outgoing

def read_stress_data(filepath):
    stress = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            stress.append(int(row[0]))
    return stress

def plot_bandwidth(incoming, outgoing):
    runs = range(1, len(incoming) + 1)
    plt.figure(figsize=(10, 5))
    plt.plot(runs, incoming, label='Incoming Bandwidth (kB/s)', marker='o')
    plt.plot(runs, outgoing, label='Outgoing Bandwidth (kB/s)', marker='o')
    plt.xlabel('Run Count')
    plt.ylabel('Bandwidth (kB/s)')
    plt.title('Incoming and Outgoing Bandwidth Over Runs')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_stress(stress):  #Matlab uses scientifc notation for the  larger values on the y axis
    runs = range(1, len(stress) + 1)
    plt.figure(figsize=(10, 5))
    plt.plot(runs, stress, label='Stress', marker='o')
    plt.xlabel('Run Count')
    plt.ylabel('Stress (ms) ')
    plt.title('Stress Over Runs')
    plt.legend()
    plt.tight_layout()

    plt.show()



homedir = os.path.expanduser('~')
collaboraPath = find_collabora_online_path(homedir)

performanceCSVs = ["TileLatency.csv","PingLatency.csv"]

for csvName in performanceCSVs:
    csv_path = os.path.join(collaboraPath, 'test', csvName)
    headers, data = read_latency_performance_data(csv_path)
    plot_latency_performance_data(headers, data, f'Performance Variation for {csvName}')


CPUPath = os.path.join(collaboraPath, 'test', 'CPU.csv')
NetworkPath = os.path.join(collaboraPath, 'test', 'Network.csv')

incoming, outgoing = read_bandwidth_data(NetworkPath)
plot_bandwidth(incoming, outgoing)

stress = read_stress_data(CPUPath)
plot_stress(stress)
