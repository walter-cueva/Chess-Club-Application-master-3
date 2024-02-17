import json
import os
from models.player import list_club_files, get_player_ids_from_club
from matches import MatchGenerator
from rounds import TournamentScheduler


class TournamentCreator:
    def __init__(self):
        self.clubs_directory = '/Users/waltercueva/Downloads/Chess-Club-Application-master 3/data/clubs'
        self.save_directory = '/Users/waltercueva/Downloads/Chess-Club-Application-master 3/data/tournaments'

    def select_club(self):
        club_files = list_club_files(self.clubs_directory)
        for index, file in enumerate(club_files, start=1):
            print(f"{index}. {file}")

        while True:
            try:
                selected_index = int(input("Select a club by number: ")) - 1
                if selected_index < 0 or selected_index >= len(club_files):
                    print("Invalid number. Please select a valid club number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        return club_files[selected_index]

    @staticmethod
    def collect_tournament_info():
        return {
            "name": input("Enter tournament name: "),
            "dates": {"from": input("Enter start date (DD-MM-YYYY): "), "to": input("Enter end date (DD-MM-YYYY): ")},
            "venue": input("Enter venue: "),
            "number_of_rounds": int(input("Enter number of rounds: ")),
            "current_round": 1,
            "completed": False,
            "players": [],  # This will be filled later
            "rounds": []
        }

    @staticmethod
    def generate_pairings_and_schedule(player_ids):
        match_generator = MatchGenerator(player_ids)
        pairings = match_generator.generate_pairings()
        scheduler = TournamentScheduler(pairings)
        return scheduler.distribute_into_rounds()

    def save_tournament_data(self, tournament_data):
        filename = (f"{tournament_data['name'].replace(' ', '_').lower()}-"
                    f"{'completed' if tournament_data['completed'] else 'in-progress'}.json")
        os.makedirs(self.save_directory, exist_ok=True)
        file_path = os.path.join(self.save_directory, filename)
        with open(file_path, 'w') as json_file:
            json.dump(tournament_data, json_file, indent=4)
        print(f"JSON file created: {file_path}")

    def create_tournament(self):
        selected_club_file = self.select_club()
        player_ids = get_player_ids_from_club(os.path.join(self.clubs_directory, selected_club_file))
        tournament_data = self.collect_tournament_info()  # Collect basic info first
        tournament_data["players"] = player_ids  # Now add player IDs
        tournament_data["rounds"] = TournamentCreator.generate_pairings_and_schedule(player_ids)  # Generate rounds
        self.save_tournament_data(tournament_data)


if __name__ == "__main__":
    tournament_creator = TournamentCreator()
    tournament_creator.create_tournament()
