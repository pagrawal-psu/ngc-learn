"""
Copyright (C) 2021 Alexander G. Ororbia II - All Rights Reserved
You may use, distribute and modify this code under the
terms of the BSD 3-clause license.

You should have received a copy of the BSD 3-clause license with
this file. If not, please write to: ago@cs.rit.edu
"""

import tensorflow as tf
import sys
import numpy as np
import copy
from ngclearn.utils import transform_utils

class Cable:
    """
    Base cable element (class from which other cable types inherit basic properties from)

    Args:
        cable_type: the string concretely denoting this cable's type

        inp: 2-Tuple defining the nodal points that this cable will connect.
            The value types inside each slot of the tuple are specified below:

            :input_node (Tuple[0]): the source/input Node object that this cable will carry
                signal information from

            :input_compartment (Tuple[1]): the compartment within the source/input Node that
                signals will extracted and transmitted from

        out: 2-Tuple defining the nodal points that this cable will connect.
            The value types inside each slot of the tuple are specified below:

            :input_node (Tuple[0]): the destination/output Node object that this cable will
                carry signal information to

            :input_compartment (Tuple[1]):  the compartment within the destination/output Node that
                signals transmitted and deposited into

        name: the string name of this cable (Default = None which creates an auto-name)

        seed: integer seed to control determinism of any underlying synapses
            associated with this cable

        coeff: a scalar float to control any signal scaling associated with this cable
    """
    def __init__(self, cable_type, inp, out, name=None, seed=69, coeff=1.0):
        self.cable_type = cable_type
        self.seed = seed
        self.name = name
        self.is_learnable = False
        self.coeff = coeff
        self.W = None
        self.b = None
        self.gamma = 1.0
        self.use_mod_factor = False # does the weight update use weight modulation?

        inp_node, inp_var = inp
        out_node, out_var = out
        self.inp_node = inp_node
        self.inp_var = inp_var
        self.out_node = out_node
        self.out_var = out_var

        if name == None:
            self.name = "{0}-to-{1}_{2}".format(inp_node.name, out_node.name, self.cable_type)

        self.preact_node = None
        self.preact_comp = None
        self.postact_node = None
        self.postact_comp = None
        self.deriv_node = None
        self.deriv_comp = None

    def propagate(self, node):
        pass

    def set_update_rule(self, preact, postact, deriv_node=None, gamma=1.0, use_mod_factor=False):
        self.gamma = gamma
        self.use_mod_factor = use_mod_factor
        self.is_learnable = True
        preact_node, preact_comp = preact
        self.preact_node = preact_node
        self.preact_comp = preact_comp
        postact_node, postact_comp = postact
        self.postact_node = postact_node
        self.postact_comp = postact_comp
        if deriv_node is not None:
            deriv_node, deriv_comp = deriv_node
            self.deriv_node = deriv_node
            self.deriv_comp = deriv_comp

    def calc_update(self, update_radius=-1.0):
        return []

    def clear(self):
        pass
