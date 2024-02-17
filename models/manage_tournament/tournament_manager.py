# tournament_manager.py
from tournament_util import TournamentUtility
import os


class TournamentManager:
    def __init__(self):
        self.tournaments_directory = "/Users/waltercueva/Downloads/Chess-Club-Application-master 3/data/tournaments"

    def manage_tournament(self):
        tournament_files = TournamentUtility.list_tournament_files(self.tournaments_directory)
        for index, file in enumerate(tournament_files, start=1):
            print(f"{index}. {file}")

        selected_index = int(input("Select a tournament by number: ")) - 1
        selected_file = tournament_files[selected_index]
        selected_file_path = os.path.join(self.tournaments_directory, selected_file)
        tournament = TournamentUtility.load_tournament_data(selected_file_path)

        while True:
            round_index, match_index = TournamentUtility.display_and_select_matches(tournament)
            if round_index is not None and match_index is not None:
                TournamentUtility.modify_match(tournament, round_index, match_index, selected_file_path)
            update_round = input("Do you want to update the current round? (yes/no): ").lower()
            if update_round == 'yes':
                TournamentUtility.update_current_round(tournament)
            TournamentUtility.save_tournament_data(selected_file_path, tournament)
            if tournament["completed"]:
                break
            if input("Do you want to continue modifying this tournament? (yes/no): ").lower() != "yes":
                break


if __name__ == "__main__":
    manager = TournamentManager()
    manager.manage_tournament()
