from collections import defaultdict


class Session(object):
    """

    """
    session = defaultdict(dict)

    @classmethod
    def modify(cls, key_id, value):
        """

        """
        cls.session[key_id] = value

    @classmethod
    def get(cls, key_id):
        """

        """
        return cls.session[key_id]
