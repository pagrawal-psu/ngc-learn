import tensorflow as tf
import sys
import numpy as np
import copy
from ngclearn.utils import transform_utils
from ngclearn.engine.cables.rules.rule import UpdateRule

class HebbRule(UpdateRule):
    """
    The Hebbian update rule.

    Args:
        name: the string name of this update rule (Default = None which creates an auto-name)
    """
    def __init__(self, name=None):
        rule_type = "hebbian"
        super().__init__(rule_type, name)

    def clone(self):
        rule = HebbRule(self.name)
        rule.terms = self.terms
        rule.cable = self.cable
        rule.param_name = self.param_name
        return rule

    def set_terms(self, terms):
        if len(terms) == 2:
            self.terms = terms
        elif len(terms) == 1:
            self.terms = [None] + terms
        else:
            print("ERROR: {} must contain 1 or 2 terms "
                  "(input.len = {}) (rule.name = {})".format(self.rule_type,
                                                             len(terms), self.name))
            sys.exit(1)

    def calc_update(self, for_bias=False):
        preact = self.terms[0]
        postact = self.terms[1]
        postact_node, postact_comp = postact
        postact_term = postact_node.extract(postact_comp)
        if preact is not None and for_bias == False: # update matrix
            preact_node, preact_comp = preact
            preact_term = preact_node.extract(preact_comp)
            # calculate the final update matrix
            update = tf.matmul(preact_term, postact_term, transpose_a=True)
        else: # vector update
            update = tf.reduce_sum(postact_term, axis=0, keepdims=True)
        return update
