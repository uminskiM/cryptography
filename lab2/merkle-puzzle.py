from merklepuzzlesender import MerklePuzzleSender
from merklepuzzlereceiver import MerklePuzzleReceiver
import time

if __name__ == '__main__':
    start = time.time()
    merkle_puzzle_sender = MerklePuzzleSender(20)
    encrypted_messages = merkle_puzzle_sender.generate_public_keys()
    merkle_puzzle_receiver = MerklePuzzleReceiver(20, encrypted_messages)
    identifier, response = merkle_puzzle_receiver.respond()
    # print(identifier, response)
    merkle_puzzle_sender.decode_message(identifier, response)
    end = time.time()
    duration = end - start
    print(duration)
