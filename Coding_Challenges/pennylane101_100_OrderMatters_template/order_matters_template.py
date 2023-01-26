#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


def compare_circuits(angles):
    """Given two angles, compare two circuit outputs that have their order of operations flipped: RX then RY VERSUS RY then RX.

    Args:
        - angles (np.ndarray): Two angles

    Returns:
        - (float): | < \sigma^x >_1 - < \sigma^x >_2 |
    """

    # QHACK #
    # define a device and quantum functions/circuits here
    num_shots = 60000000
    device1 = qml.device(name="default.qubit", wires=1, shots=num_shots)
    device2 = qml.device(name="default.qubit", wires=1, shots=num_shots)

    # okay, pennylane uses decorators in python

    @qml.qnode(device1)
    def circuit1_exp(angles):
        qml.RX(angles[0], wires=0)
        qml.RY(angles[1], wires=0)

        return qml.sample(qml.PauliX(wires=0))

    @qml.qnode(device2)
    def circuit2_exp(angles):
        qml.RY(angles[1], wires=0)
        qml.RX(angles[0], wires=0)

        return qml.sample(qml.PauliX(wires=0))

    value_1 = np.average(circuit1_exp(angles))
    value_2 = np.average(circuit2_exp(angles))

    return abs(value_1 - value_2)
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    angles = np.array(sys.stdin.read().split(","), dtype=float)
    output = compare_circuits(angles)
    print(f"{output:.6f}")
