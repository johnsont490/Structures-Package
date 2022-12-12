# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 08:43:34 2022

@author: johns
"""

import math

from pymatgen.analysis.local_env import CrystalNN


class Bond:
    """
    A bond between two atoms in a structure.
    """

    def __init__(self, parent_structure, site_index_0, atom_0, neighbor_1, bond_CNs):
        """
        Defines a bond.
        :param structure: Pymatgen IStructure object.
        :param site_indices: The two site indices within the IStructure object for the bond.
        :param atoms: THe two atoms involved in the bond, corresponding to each site index.
        """
        self.sites = (site_index_0, neighbor_1["site_index"])
        self.species = (atom_0.specie, neighbor_1["site"].specie)
        self.ENs = (atom_0.specie.X, neighbor_1["site"].specie.X)
        self.CNs = bond_CNs
        self.bond_length = math.dist(
            parent_structure[site_index_0].coords, neighbor_1["site"].coords
        )


def detect_bonds(structure):
    bonds = []
    for site_index, atom in enumerate(structure):
        # TODO: Options for other NN algorithms
        nn_object = CrystalNN()
        neighbors = nn_object.get_nn_info(structure, site_index)
        if not neighbors:
            continue
        cn1 = nn_object.get_cn(structure, site_index)
        for neighbor in neighbors:
            if neighbor["site_index"] < site_index:
                continue
            cn2 = nn_object.get_cn(structure, neighbor["site_index"])
            bond = Bond(structure, site_index, atom, neighbor, (cn1, cn2))
            bonds.append(bond)

    return bonds