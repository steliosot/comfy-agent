class DataRef:
    """Reference to a node output"""

    def __init__(self, node_id, output_index):
        self.node_id = str(node_id)
        self.output_index = int(output_index)

    def as_tuple(self):
        return (self.node_id, self.output_index)

    def __repr__(self):
        return f"DataRef(node_id={self.node_id!r}, output_index={self.output_index})"


class NodeResult:
    """Node outputs that support tuple unpacking and named access."""

    def __init__(self, refs, output_names):
        self._refs = tuple(refs)
        self._output_names = tuple(output_names)

        for name, ref in zip(self._output_names, self._refs):
            setattr(self, name, ref)

    def __iter__(self):
        return iter(self._refs)

    def __len__(self):
        return len(self._refs)

    def __getitem__(self, index):
        return self._refs[index]

    def __repr__(self):
        names = ", ".join(self._output_names)
        return f"NodeResult(outputs=[{names}])"

    def primary(self):
        if len(self._refs) != 1:
            raise ValueError(
                "NodeResult has multiple outputs; use a named output like "
                ".MODEL or unpack the result."
            )
        return self._refs[0]
