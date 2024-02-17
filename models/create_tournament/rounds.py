class TournamentScheduler:
    def __init__(self, pairings):
        self.pairings = pairings

    def distribute_into_rounds(self):
        round_data = []
        pairings = self.pairings.copy()  # Work on a copy to preserve original pairings
        while pairings:
            round_matches = []
            players_in_round = set()

            for pairing in pairings[:]:  # Iterate over a shallow copy to remove items safely
                if pairing[0] not in players_in_round and pairing[1] not in players_in_round:
                    round_matches.append({"players": list(pairing), "completed": False, "winner": None})
                    players_in_round.update(pairing)
                    pairings.remove(pairing)

            if round_matches:
                round_data.append(round_matches)

        return round_data
