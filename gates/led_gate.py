from gates.gate_item import GateItem


class LEDGate(GateItem):
    def __init__(self, x, y, w=80, h=50):
        super().__init__(x, y, 1, 0, w, h)

    def eval(self):
        result = super().eval()

        if len(result) == 0:
            return False
        elif len(result) == 1:
            return result[0]
        else:
            raise RuntimeError('Unsupported operation')



