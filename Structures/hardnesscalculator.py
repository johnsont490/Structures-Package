# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 08:36:43 2022

@author: johns
"""

#module created by Salil Bavdekar for calculating hardness from Cheenady Model

import logging
import math


def calculate_hardness(structure, bonds, model):
    """
    Calculate intrinsic hardness as per the specified model.
    :param structure: Pymatgen IStructure object.
    :param bonds: List of Bond objects including every bond in the structure.
    :param model: Hardness model for the calculations.
    :return: Intrinsic hardness of the structure.
    """
    n = len(bonds)

    if n == 0:
        logging.warning("No bonds detected in structure.")
        hardness = 0
    else:
        volume = structure.volume
        prod = 1
        for bond in bonds:
            if model == "CAS":
                fi = ((bond.ENs[0] - bond.ENs[1]) / (bond.ENs[0] + bond.ENs[1])) ** 2
                z = (bond.ENs[0] / bond.CNs[0]) * (bond.ENs[1] / bond.CNs[1])
                prod = (
                    prod
                    * (z**0.006)
                    * (bond.bond_length**-3.18)
                    * math.exp(-2.44 * fi)
                )
            elif model == "EN":
                fi = (
                    0.25
                    * abs((bond.ENs[0] - bond.ENs[1]))
                    / (bond.ENs[0] * bond.ENs[1]) ** 0.5
                )
                xi = ((bond.ENs[0] / bond.CNs[0]) * (bond.ENs[1] / bond.CNs[1])) ** 0.5
                prod = prod * (xi * math.exp(-2.7 * fi))
            elif model == "BS":
                fi = ((bond.ENs[0] - bond.ENs[1]) / (bond.ENs[0] + bond.ENs[1])) ** 2
                s = (
                    (1 / bond.CNs[0] / bond.CNs[1])
                    * (bond.ENs[0] / 0.481 * bond.ENs[1] / 0.481) ** 0.5
                    / bond.bond_length
                )
                prod = prod * s * math.exp(-2.8 * fi)
            else:
                logging.error(f"Invalid hardness model: {model}")
                prod = 0

        if model == "CAS":
            hardness = (986 * (n / volume) ** 0.844) * prod ** (1 / n)
        elif model == "EN":
            hardness = 469.27 * (n / volume) * prod ** (1 / n) - 7.24
        elif model == "BS":
            hardness = (1450 * n / volume) * prod ** (1 / n)
        else:
            logging.error(f"Invalid hardness model: {model}")
            hardness = 0

    return hardness