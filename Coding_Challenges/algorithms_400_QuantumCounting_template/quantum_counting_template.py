#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np
from pennylane.templates import QuantumPhaseEstimation


dev = qml.device("default.qubit", wires=8)


def oracle_matrix(indices):
    """Return the oracle matrix for a secret combination.

    Args:
        - indices (list(int)): A list of bit indices (e.g. [0,3]) representing the elements that are map to 1.

    Returns:
        - (np.ndarray): The matrix representation of the oracle
    """

    # QHACK #
    sign_flip = np.eye(2**4)

    for idx in indices:
        sign_flip[idx][idx] = -1.0
    # QHACK #

    return sign_flip


def diffusion_matrix():

    # DO NOT MODIFY anything in this code block

    psi_piece = (1 / 2**4) * np.ones(2**4)
    ident_piece = np.eye(2**4)
    return 2 * psi_piece - ident_piece


def grover_operator(indices):

    # DO NOT MODIFY anything in this code block

    return np.dot(diffusion_matrix(), oracle_matrix(indices))


dev = qml.device("default.qubit", wires=8)


@qml.qnode(dev)
def circuit(indices):
    """Return the probabilities of each basis state after applying QPE to the Grover operator

    Args:
        - indices (list(int)): A list of bits representing the elements that map to 1.

    Returns:
        - (np.tensor): Probabilities of measuring each computational basis state
    """

    # QHACK #

    target_wires = [0, 1, 2, 3]
    estimation_wires = [4, 5, 6, 7]

    # grover op
    unitary_matrix = grover_operator(indices)

    # Build your circuit here
    for q in target_wires:
        qml.Hadamard(wires=q)

    QuantumPhaseEstimation(
        unitary_matrix,
        target_wires=target_wires,
        estimation_wires=estimation_wires,
    )

    # QHACK #

    return qml.probs(estimation_wires)


def number_of_solutions(indices):
    """Implement the formula given in the problem statement to find the number of solutions from the output of your circuit

    Args:
        - indices (list(int)): A list of bits representing the elements that map to 1.

    Returns:
        - (float): number of elements as estimated by the quantum counting algorithm
    """

    # QHACK #
    probabilities = circuit(indices)
    max_index = np.argmax(probabilities)

    theta = max_index * np.pi * 1 / 8

    return 16 * (np.sin(theta / 2) ** 2)

    # QHACK #


def relative_error(indices):
    """Calculate the relative error of the quantum counting estimation

    Args:
        - indices (list(int)): A list of bits representing the elements that map to 1.

    Returns:
        - (float): relative error
    """

    # QHACK #
    true_num = len(indices)
    quantum_num = number_of_solutions(indices)
    rel_err = ((quantum_num - true_num) * 100) / true_num

    # QHACK #

    return rel_err


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    lst = [int(i) for i in inputs]
    output = relative_error(lst)
    print(f"{output}")
