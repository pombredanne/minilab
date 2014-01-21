from shared_memory import SharedMemory


def print_session(key_id):
    #memory = SharedMemory
    print(SharedMemory.get(key_id))