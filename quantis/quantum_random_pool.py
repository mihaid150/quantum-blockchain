# quantum_random_pool.py
import os


class QuantumRandomPool:
    def __init__(self):
        """
        Initialize the Quantum Random Pool with the path to the file containing the quantum random bytes. The file is
        read once and stored in memory.
        """
        self.file_path = os.path.join(os.path.dirname(__file__), 'qrandom1MB_0.dat')
        self.random_pool = None
        self.offset = 0
        self.load_random_pool()

    def load_random_pool(self):
        """
        Reads the random data file once and stores its content in the random pool.
        """
        with open(self.file_path, 'rb') as f:
            self.random_pool = f.read()

    def get_random_bytes(self):
        """
        Extract the next random 32 bytes from the pool when requested
        """
        if self.random_pool is None:
            raise Exception("Random pool not loaded.")

        if self.offset + 32 > len(self.random_pool):
            raise Exception("Random pool exhausted. No more 256-bit numbers available.")

        # Extract 32 bytes from the pool
        random_bytes = self.random_pool[self.offset:self.offset + 32]
        self.offset += 32

        return random_bytes

    def total_numbers_available(self):
        """
        Returns the total number of 2560-bit random numbers  available in the pool.
        """
        if self.random_pool is None:
            return 0
        return len(self.random_pool) // 32

    def reset_pool(self):
        """
        Resets the index pointer to the beginning of the pool, allowing the numbers to be reused.
        """
        self.offset = 0

