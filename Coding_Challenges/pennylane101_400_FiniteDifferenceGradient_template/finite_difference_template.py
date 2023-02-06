#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=3)


def my_finite_diff_grad(params):
    """Function that returns the gradients of the cost function (defined below) with respect
    to all parameters in params.

    Args:
        - params (np.ndarray): The parameters needed to create the variational circuit.

    Returns:
        - gradients (np.ndarray): the gradient w.r.t. each parameter
    """
    delta = 1e-4
    gradients = np.zeros([len(params)])

    for i in range(len(params)):
        # QHACK #

        # NICE!

        # whichever parameter we are considering right now, perturb it
        # and get the cost

        # means -> i = 0, params_up = [p[0]+d/2, p[1], p[2]]
        # params_down = [p[0]-d/2, p[1], p[2]]

        # then we get the cost and calculate the partial derivate with respect to
        # it

        # and we go on doing this...

        shift_up_params_i = [
            params[j] if j != i else (params[j] + delta / 2) for j in range(len(params))
        ]

        shift_down_params_i = [
            params[j] if j != i else (params[j] - delta / 2) for j in range(len(params))
        ]

        cost_up = cost(shift_up_params_i)
        cost_down = cost(shift_down_params_i)

        gradients[i] = round(float((cost_up - cost_down) / delta), 9)
        # QHACK #

    return gradients


def variational_circuit(params):
    """A layered variational circuit. The first layer comprises of x, y, and z rotations on wires
    0, 1, and 2, respectively. The second layer is a ring of CNOT gates. The final layer comprises
    of x, y, and z rotations on wires 0, 1, and 2, respectively.
    """

    # DO NOT MODIFY anything in this code block
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.RZ(params[2], wires=2)

    qml.broadcast(qml.CNOT, wires=[0, 1, 2], pattern="ring")

    qml.RX(params[3], wires=0)
    qml.RY(params[4], wires=1)
    qml.RZ(params[5], wires=2)

    qml.broadcast(qml.CNOT, wires=[0, 1, 2], pattern="ring")


@qml.qnode(dev)
def cost(params):
    """A QNode that pairs the variational_circuit with an expectation value measurement.

    Args:
        - params (np.ndarray): Variational circuit parameters

    Returns:
        - (float): qml.expval(qml.PauliY(0) @ qml.PauliZ(2))
    """

    # DO NOT MODIFY anything in this code block
    variational_circuit(params)
    return qml.expval(qml.PauliY(0) @ qml.PauliZ(2))


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    params = np.array(sys.stdin.read().split(","), dtype=float)
    output = my_finite_diff_grad(params)
    print(*output, sep=",")
