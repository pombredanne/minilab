from collections import defaultdict
import pickle
import mmap


class Session(object):
    """

    """
    file = '/tmp/.session'
    max_size = 1024 * 10

    @classmethod
    def modify(cls, key_id, value):
        """

        """
        try:
            mm = mmap.mmap(-1, cls.max_size)
            cls.session[key_id] = mm.readlines()
        except:
            cls.session = defaultdict(dict)

        if not session:
            cls.session = defaultdict(dict)

        cls.session[key_id] = value
        mm.write(pickle.dumps(cls.session))

    @classmethod
    def get(cls, key_id):
        """

        """
        mm = mmap.mmap(-1, cls.max_size)
        session = mm.readline()
        return cls.session[key_id]
