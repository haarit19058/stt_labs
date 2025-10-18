// File: scheduler_rr.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_PROCESSES 10
#define TIME_QUANTUM 4 // The time slice for each process

// A structure to represent a process
// Using a struct makes managing process data much cleaner.
struct Process {
    int pid;                // Process ID
    int burst_time;         // CPU time required by the process
    int remaining_time;     // Remaining CPU time
    int arrival_time;       // Time when the process arrives in the ready queue
    int waiting_time;       // Total time spent waiting in the ready queue
    int turnaround_time;    // Time from arrival to completion
    int in_ready_queue;     // Flag to check if it's in the queue
    int completion_time;    // Time when the process finishes execution
};


int main() {
    // --- Variable Declarations ---
    int i, n_processes;
    struct Process processes[MAX_PROCESSES];
    int ready_queue[MAX_PROCESSES];
    int front = -1, rear = -1;
    int current_time = 0;
    int completed_processes = 0;
    float total_waiting_time = 0.0;
    float total_turnaround_time = 0.0;
    int active_process_pid = -1;
    int current_quantum_slice = 0;

    // Seed the random number generator for variability
    srand(time(NULL));

    // --- User Input for Number of Processes ---
    printf("--- Round Robin CPU Scheduler Simulator ---\n");
    printf("Enter the number of processes to simulate (1 to %d): ", MAX_PROCESSES);
    scanf("%d", &n_processes);

    if (n_processes < 1 || n_processes > MAX_PROCESSES) {
        printf("Invalid number of processes. Exiting.\n");
        return 1; // Exit with an error code
    }

    // --- Process Initialization ---
    // Initialize processes with random burst times and sequential arrival times.
    printf("\nInitializing %d processes...\n", n_processes);
    printf("--------------------------------------------------\n");
    printf("PID\tArrival Time\tBurst Time\n");
    printf("--------------------------------------------------\n");
    for (i = 0; i < n_processes; i++) {
        processes[i].pid = i + 1;
        // Assign a random burst time between 2 and 12
        processes[i].burst_time = (rand() % 10) + 3;
        processes[i].remaining_time = processes[i].burst_time; // Initially, remaining time is the full burst time
        processes[i].arrival_time = i * 2; // Staggered arrival times for a more realistic simulation
        processes[i].waiting_time = 0;
        processes[i].turnaround_time = 0;
        processes[i].in_ready_queue = 0;
        processes[i].completion_time = 0;
        printf("%d\t%d\t\t%d\n", processes[i].pid, processes[i].arrival_time, processes[i].burst_time);
    }
    printf("--------------------------------------------------\n\n");
    printf("Simulation starting... Time Quantum = %d\n\n", TIME_QUANTUM);


    // --- Main Simulation Loop ---
    // This loop continues as long as not all processes have been completed.
    // It simulates the passage of time, tick by tick.
    while (completed_processes < n_processes) {
        
        // Check for new arrivals at the current time and add them to the ready queue.
        for (i = 0; i < n_processes; i++) {
            if (processes[i].arrival_time == current_time) {
                // Add to ready queue (simple array-based queue)
                if (front == -1) {
                    front = 0;
                }
                rear = (rear + 1) % MAX_PROCESSES;
                ready_queue[rear] = i; // Store index of the process
                processes[i].in_ready_queue = 1;
                printf("Time %d: Process %d arrived and added to ready queue.\n", current_time, processes[i].pid);
            }
        }

        // If no process is currently running, but the ready queue is not empty,
        // dequeue the next process to run.
        if (active_process_pid == -1 && front != -1) {
            int process_index = ready_queue[front];
            front = (front + 1) % MAX_PROCESSES;
            if (front == (rear + 1) % MAX_PROCESSES) { // Queue is now empty
                front = -1;
                rear = -1;
            }
            active_process_pid = processes[process_index].pid;
            current_quantum_slice = 0; // Reset the time slice counter for the new process
            printf("Time %d: CPU is idle. Dispatching Process %d from ready queue.\n", current_time, active_process_pid);
        }

        // --- Process Execution Logic ---
        if (active_process_pid != -1) {
            int current_process_index = -1;
            // Find the index of the currently active process
            for(i = 0; i < n_processes; i++) {
                if(processes[i].pid == active_process_pid) {
                    current_process_index = i;
                    break;
                }
            }

            // Decrement the remaining time for the running process
            processes[current_process_index].remaining_time--;
            current_quantum_slice++;
            printf("Time %d: Process %d is running. (Remaining Time: %d)\n", current_time, active_process_pid, processes[current_process_index].remaining_time);

            // Check if the process has finished
            if (processes[current_process_index].remaining_time == 0) {
                processes[current_process_index].completion_time = current_time + 1;
                processes[current_process_index].turnaround_time = processes[current_process_index].completion_time - processes[current_process_index].arrival_time;
                processes[current_process_index].waiting_time = processes[current_process_index].turnaround_time - processes[current_process_index].burst_time;
                
                total_waiting_time += processes[current_process_index].waiting_time;
                total_turnaround_time += processes[current_process_index].turnaround_time;
                
                completed_processes++;
                printf("Time %d: Process %d FINISHED. Turnaround: %d, Waiting: %d\n", current_time + 1, active_process_pid, processes[current_process_index].turnaround_time, processes[current_process_index].waiting_time);
                active_process_pid = -1; // CPU is now free
                current_quantum_slice = 0;

            } 
            // Check if the time quantum has expired for the current process
            else if (current_quantum_slice == TIME_QUANTUM) {
                printf("Time %d: Time quantum expired for Process %d.\n", current_time + 1, active_process_pid);
                
                // Add the preempted process back to the end of the ready queue,
                // but only if there are other processes waiting.
                if (front != -1) {
                    if (front == -1) { // If queue was empty
                        front = 0;
                    }
                    rear = (rear + 1) % MAX_PROCESSES;
                    ready_queue[rear] = current_process_index;
                    printf("Time %d: Process %d moved to the back of the ready queue.\n", current_time + 1, active_process_pid);
                } else {
                    // If no other process is in the queue, let this one continue
                     printf("Time %d: No other processes in queue. Process %d continues.\n", current_time + 1, active_process_pid);
                }
                
                // In either case, the CPU will pick a new process in the next cycle
                active_process_pid = -1;
                current_quantum_slice = 0;
            }
        } else {
             printf("Time %d: CPU is idle, no processes in ready queue.\n", current_time);
        }

        // Increment the master simulation clock
        current_time++;
    }

    // --- Results Calculation and Display ---
    printf("\n\n--- Simulation Complete ---\n");
    printf("Final Results:\n");
    printf("------------------------------------------------------------------------------------------\n");
    printf("PID\tArrival Time\tBurst Time\tCompletion Time\tTurnaround Time\tWaiting Time\n");
    printf("------------------------------------------------------------------------------------------\n");

    for (i = 0; i < n_processes; i++) {
        printf("%d\t%d\t\t%d\t\t%d\t\t%d\t\t\t%d\n",
               processes[i].pid,
               processes[i].arrival_time,
               processes[i].burst_time,
               processes[i].completion_time,
               processes[i].turnaround_time,
               processes[i].waiting_time);
    }
    printf("------------------------------------------------------------------------------------------\n");

    // Calculate and display averages
    float avg_waiting_time = total_waiting_time / n_processes;
    float avg_turnaround_time = total_turnaround_time / n_processes;

    printf("\nAverage Waiting Time:    %.2f\n", avg_waiting_time);
    printf("Average Turnaround Time: %.2f\n", avg_turnaround_time);
    printf("Total time elapsed: %d\n", current_time);

    return 0; // Successful execution
}