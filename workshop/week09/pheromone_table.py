from config import DECAY_FACTOR

class PheromoneTable:
    def __init__(self):
        self.table = {}  # {peer_port: pheromone_value}

    def reinforce(self, peer, value):
        self.table[peer] = self.table.get(peer, 0) + value
        print(f"[PHEROMONE] Reinforced {peer} → {self.table[peer]:.2f}")

    def decay(self):
        print("[PHEROMONE] Decaying...")
        for peer in list(self.table.keys()):
            self.table[peer] *= DECAY_FACTOR

    def get_best_candidates(self, threshold):
        return [
            peer for peer, pher in self.table.items()
            if pher >= threshold
        ]

    def debug_print(self):
        print("=== PHEROMONE TABLE ===")
        for peer, val in self.table.items():
            print(f"{peer} → {val:.2f}")
        print("========================")