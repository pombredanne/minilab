from shared_memory import SharedMemory
from printing import print_session

SharedMemory.modify('nome', 'Ivan')
SharedMemory.modify('nome', 'Juan')
SharedMemory.modify('nome', 'John')
print_session('nome')