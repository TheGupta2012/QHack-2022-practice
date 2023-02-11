#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def binary_list(m, n):
    """Converts number m to binary encoded on a list of length n

    Args:
        - m (int): Number to convert to binary
        - n (int): Number of wires in the circuit

    Returns:
        - (list(int)): Binary stored as a list of length n
    """

    arr = []
    # QHACK #
    arr = [int(b) for b in bin(m)[2:].zfill(n)]
    # QHACK #
    return arr


def basis_states(n):
    """Given a number n, returns a list of all binary_list(m,n) for m < 2**n, thus providing all basis states
         for a circuit of n wires

    Args:
        - n(int): integer representing the number of wires in the circuit

    Returns:
        - (list(list(int))): list of basis states represented as lists of 0s and 1s.
    """

    arr = []

    # QHACK #
    for num in range(2**n):
        arr.append(binary_list(num, n))
    # QHACK #

    return arr


def is_particle_preserving(circuit, n):
    """Given a circuit and its number of wires n, returns 1 if it preserves the number of particles, and 0 if it does not

    Args:
        - circuit (qml.QNode): A QNode that has a state such as [0,0,1,0] as an input and outputs the final state after performing
        quantum operation
        - n (int): the number of wires of circuit

    Returns:
        - (bool): True / False according to whether the input circuit preserves the number of particles or not
    """

    # QHACK #
    states = basis_states(n)

    def get_hamming_weight(blist):
        weight = 0
        for b in blist:
            weight += b
        return weight

    for state in states:
        init_weight = get_hamming_weight(state)
        result = list(circuit(state))
        # okay, ONLY consider the elements having probability > 0

        # You have to measure the state and WHATEVER state you get
        # should have the same hamming weight

        # NOTE : the state which you get must be the one with a
        # probability > 0, so you only take those states!
        final_weight = 0
        for index, amp in enumerate(result):
            prob = (amp * amp.conjugate()).real
            if prob > 0:
                final_weight = get_hamming_weight(binary_list(index, n))
                
                # every possibility should have the same hamming
                # weight
                if init_weight != final_weight:
                    return False

    # if we are still here, we have succeeded!
    return True
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(";")
    gate_list = []
    wire_list = []
    param_list = []
    i = 1

    while i < len(inputs):
        gate_obj = getattr(qml, str(inputs[i]))
        gate_wires = gate_obj.num_wires
        input_wires = list(map(int, str(inputs[i + 1]).split(",")))
        gate_list.append(str(inputs[i]))
        wire_list.append(input_wires)
        if "non_parametric_ops" not in gate_obj.__module__.split("."):
            input_params = list(map(float, str(inputs[i + 2]).split(",")))
            param_list.append(input_params)
            i += 1
        i += 2

    wire_list = np.array(wire_list, dtype=object)
    param_list = np.array(param_list, dtype=object)

    n = int(inputs[0])
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circ(gate_list, wire_list, param_list, state):
        qml.BasisState(np.array(state), wires=range(n))
        j = 0
        for i in range(len(gate_list)):
            gate = getattr(qml, str(gate_list[i]))
            if "non_parametric_ops" not in gate.__module__.split("."):
                gate(*param_list[j], wires=[int(w) for w in wire_list[i]])
                j += 1
            else:
                gate(wires=[int(w) for w in wire_list[i]])
        return qml.state()

    def circuit(state):
        return circ(gate_list, wire_list, param_list, state)

    output = is_particle_preserving(circuit, n)

    print(output)
