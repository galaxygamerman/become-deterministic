import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

class FiniteStateMachineApp:
    root : tk
    states : list
    transitions : dict
    num_states_frame : tk.Frame
    num_states_entry : tk.Entry
    state_names_frame : tk.Frame
    transitions_frame : tk.Frame
    
    def __init__(self, root):
        self.root = root
        self.root.title("Finite State Machine App")
        self.states = []
        self.transitions = {}

        # Create input frame for number of states
        self.num_states_frame = tk.Frame(self.root)
        self.num_states_frame.pack()
        tk.Label(self.num_states_frame, text="Enter number of states (dead states can be excluded from this number):").pack(side=tk.LEFT)
        self.num_states_entry = tk.Entry(self.num_states_frame)
        self.num_states_entry.pack(side=tk.LEFT)
        tk.Button(self.num_states_frame, text="Submit", command=self.get_num_states).pack(side=tk.LEFT)

        # Create input frame for state names
        self.state_names_frame = tk.Frame(self.root)
        self.state_names_frame.pack()

        # Create input frame for transitions
        self.transitions_frame = tk.Frame(self.root)
        self.transitions_frame.pack()

    def get_num_states(self):
        try:
            num_states = int(self.num_states_entry.get())
            if num_states <= 0:
                messagebox.showerror("Error", "Number of states must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a positive integer.")
            return

        # Create input fields for state names
        self.state_names_frame.pack_forget()
        self.state_names_frame = tk.Frame(self.root)
        self.state_names_frame.pack()
        for i in range(num_states):
            tk.Label(self.state_names_frame, text=f"State {i+1} name:").pack(side=tk.LEFT)
            entry = tk.Entry(self.state_names_frame)
            entry.pack(side=tk.LEFT)
            self.states.append(entry)

        # Create button to submit state names
        tk.Button(self.state_names_frame, text="Submit", command=self.get_state_names).pack(side=tk.LEFT)

    def get_state_names(self):
        state_names = [state.get() for state in self.states]
        if len(set(state_names)) != len(state_names):
            messagebox.showerror("Error", "State names must be unique.")
            return

        # Create input fields for transitions
        self.transitions_frame.pack_forget()
        self.transitions_frame = tk.Frame(self.root)
        self.transitions_frame.pack()
        for i, state in enumerate(state_names):
            tk.Label(self.transitions_frame, text=f"Transitions for {state}:").pack(side=tk.LEFT)
            entry = tk.Entry(self.transitions_frame)
            entry.pack(side=tk.LEFT)
            self.transitions[state] = entry

        # Create button to submit transitions
        tk.Button(self.transitions_frame, text="Submit", command=self.get_transitions).pack(side=tk.LEFT)

    def get_transitions(self):
        transitions = {}
        for state, entry in self.transitions.items():
            transitions[state] = entry.get().split(",")

        # Print the finite state machine
        print("Finite State Machine:")
        print("States:", list(self.transitions.keys()))
        print("Transitions:")
        for state, transition in transitions.items():
            print(f"{state}: {transition}")

        # Create DFA digraph
        G = nx.DiGraph()
        for state, transition in transitions.items():
            for t in transition:
                G.add_edge(state, t)

        # Draw DFA digraph
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color='lightblue')
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edge_color='gray')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FiniteStateMachineApp(root)
    root.mainloop()