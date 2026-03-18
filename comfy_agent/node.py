class Node:
    """Logical DAG node"""

    def __init__(self, node_id, class_type, inputs, alias=None):
        self.node_id = str(node_id)
        self.class_type = class_type
        self.inputs = inputs
        self.alias = alias
