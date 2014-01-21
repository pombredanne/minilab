from collections import defaultdict


class SharedMemory(object):
    """

    """
    mem = defaultdict(dict)

    @classmethod
    def modify(cls, key_id, value):
        """

        """
        cls.mem[key_id] = value

    @classmethod
    def get(cls, key_id):
        """

        """
        return cls.mem[key_id]
