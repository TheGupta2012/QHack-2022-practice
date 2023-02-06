#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs, fs_daggers):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """

    # nice question

    # use the toffoli to make a controlled rotation and store the
    # results in the ancilla qubits

    # this result is then measured and if probability of |0> or |1>
    # state is 1 then all are same, else different

    # valid inputs need to be ensured as it may be that we have
    # 3 - 1 type inputs too

    # QHACK #
    device = qml.device("default.qubit", wires=7, shots=1)

    def init_dj():
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)

        qml.PauliX(wires=2)
        qml.Hadamard(wires=2)

    def init_dj_dagger():
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)

        qml.Hadamard(wires=2)
        qml.PauliX(wires=2)

    def apply_function(fn, fn_dagger, target_out):
        init_dj()
        fn(wires=[0, 1, 2])

        # controlled flip of target_out conditioned on 0 and 1 being in |0> state
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        qml.Toffoli(wires=[0, 1, target_out])
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)

        # uncompute
        fn_dagger(wires=[0, 1, 2])
        init_dj_dagger()

    @qml.qnode(device)
    def circuit():
        # build 1 by 1
        for fn, fn_dg, target in zip(fs, fs_daggers, [3, 4, 5, 6]):
            apply_function(fn, fn_dg, target)

        return qml.sample(wires=[3, 4, 5, 6])

    result = circuit()

    sum = 0
    for element in result:
        sum += element

    if sum == 0 or sum == 4:
        return "4 same"

    return "2 and 2"
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f1_dagger(wires):
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f2_dagger(wires):
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f3_dagger(wires):
        qml.PauliX(wires=wires[2])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4_dagger(wires):
        qml.PauliX(wires=wires[2])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])

    output = deutsch_jozsa(
        [f1, f2, f3, f4], [f1_dagger, f2_dagger, f3_dagger, f4_dagger]
    )
    print(f"{output}")
