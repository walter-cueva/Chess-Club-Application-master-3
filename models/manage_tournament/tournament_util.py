# tournament_util.py
import json
import os


class TournamentUtility:
    @staticmethod
    def list_tournament_files(directory):
        """List all tournament JSON files in the specified directory, excluding point system files."""
        return [file for file in os.listdir(directory) if file.endswith('.json')
                and not file.endswith('_point_system.json')]

    @staticmethod
    def update_current_round(tournament):
        """Prompt the user to update the current round number of the tournament."""
        new_round_number = input("Enter the new current round number: ").strip()
        if new_round_number.isdigit():
            tournament["current_round"] = int(new_round_number)
            print(f"Current round updated to: {tournament['current_round']}")
        else:
            print("Invalid input. Current round not updated.")

    @staticmethod
    def load_tournament_data(file_path):
        """Load tournament data from a JSON file."""
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_tournament_data(file_path, data):
        """Save tournament data to a JSON file, updating the filename based on tournament status."""
        directory, filename = os.path.split(file_path)
        name_part, ext = os.path.splitext(filename)

        if data["completed"]:
            if "-in-progress" in name_part:
                name_part = name_part.replace("-in-progress", "-completed")
            elif not name_part.endswith("-completed"):
                name_part += "-completed"
        else:
            if not name_part.endswith("-in-progress") and not name_part.endswith("-completed"):
                name_part += "-in-progress"

        new_file_path = os.path.join(directory, f"{name_part}{ext}")
        with open(new_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Remove the old file if the name has changed and the old file exists
        if new_file_path != file_path and os.path.exists(file_path):
            os.remove(file_path)

        print(f"Tournament file updated: {os.path.basename(new_file_path)}")
        return new_file_path  # Returning the new path can be useful

    @staticmethod
    def calculate_player_points(tournament):
        """Calculate points for each player based on matches completed."""
        player_points = {}
        for rounds in tournament["rounds"]:
            for match in rounds:
                if not match['completed']:
                    continue
                p1, p2 = match["players"]
                winner = match.get("winner")
                player_points.setdefault(p1, 0)
                player_points.setdefault(p2, 0)
                if winner:
                    player_points[winner] += 1
                else:
                    player_points[p1] += 0.5
                    player_points[p2] += 0.5
        return player_points

    @staticmethod
    def save_player_points(tournament, directory):
        """Save player points and tournament details to a separate JSON file."""
        tournament_name = tournament["name"].replace(" ", "_")
        points_file_name = f"{tournament_name}_point_system.json"
        points_file_path = os.path.join(directory, points_file_name)

        player_points = TournamentUtility.calculate_player_points(tournament)
        sorted_points = sorted(player_points.items(), key=lambda item: item[1], reverse=True)
        ranked_players = [{"Player": player, "Points": points} for player, points in sorted_points]

        point_system_data = {
            "Tournament Name": tournament["name"],
            "Dates": tournament["dates"],
            "Rounds": tournament["rounds"],
            "Player Points": ranked_players
        }

        try:
            print("Attempting to save player points and tournament details...")
            with open(points_file_path, 'w') as file:
                json.dump(point_system_data, file, indent=4)
            print(f"Point system file updated successfully: {points_file_path}")
        except Exception as e:
            print(f"Error saving point system file: {e}")

    @staticmethod
    def modify_match(tournament, round_index, match_index, selected_file_path):
        """Allow modification of a match's outcome, marking it as completed and updating the winner."""
        match = tournament["rounds"][round_index][match_index]
        match["completed"] = True
        winner = input(f"Enter the winner's ID ({match['players'][0]} "
                       f"or {match['players'][1]}, or leave blank for draw): ").strip()
        match["winner"] = winner if winner in match["players"] else None
        if tournament["current_round"] == tournament["number_of_rounds"]:
            tournament["completed"] = True

        TournamentUtility.save_player_points(tournament,
                       '/Users/waltercueva/Downloads/Chess-Club-Application-master 3/data/tournament_point_system')


        if tournament["completed"]:
            print(f"Tournament {tournament['name']} is completed.")

    @staticmethod
    def display_and_select_matches(tournament):
        """Display all matches for the current round and allow the user to select one for modification."""
        current_round_num = tournament["current_round"]
        print(f"Current Round {current_round_num}:")
        match_counter = 1
        for rounds in tournament["rounds"]:
            for match in rounds:
                print(f"{match_counter}: {match['players'][0]} vs "
                      f"{match['players'][1]} - Completed: {match['completed']}"
                      f" - Winner: {match.get('winner', 'N/A')}")
                match_counter += 1
        while True:
            try:
                match_index = int(input("Enter match number to modify: ")) - 1
                break
            except ValueError:
                print("Please enter a valid match number.")
        total_matches = 0
        for round_index, rounds in enumerate(tournament["rounds"]):
            total_matches += len(rounds)
            if match_index < total_matches:
                match_index_within_round = match_index - (total_matches - len(rounds))
                return round_index, match_index_within_round
        return None, None
