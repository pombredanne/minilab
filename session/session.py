from collections import defaultdict
import pickle


class Session(object):
    """

    """
    file = '/tmp/.session'

    @classmethod
    def modify(cls, key_id, value):
        """

        """
        try:
            f = open(cls.file, 'rb')
            session = pickle.load(f)
            f.close()
        except:
            session = defaultdict(dict)

        if not session:
            session = defaultdict(dict)

        session[key_id] = value
        f = open(cls.file, 'wb')
        pickle.dump(session, f)
        f.close()

    @classmethod
    def get(cls, key_id):
        """

        """
        f = open(cls.file, 'rb')
        session = pickle.load(f)
        print(session)
        f.close()
        return session[key_id]
