import csv
import os
from typing import Dict, List


class VoteManager:
    """
    handles vote storage and counting in a CSV file.
    """

    def __init__(self, filename: str = "votes.csv") -> None:
        """
        makes sure the CSV exists and has a header row.
        Ags:
            filename: path to the vote file
        """
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["voter_id", "candidate"])

    def validate_id(self, voter_id: str) -> bool:
        """
        check if voter_id isnt empty and is alphanumeric.
        ar:
            voter_id: the id string to check
        Returns:
            True if it's ok, False otherwise
        """
        return bool(voter_id) and voter_id.isalnum()

    def has_voted(self, voter_id: str) -> bool:
        """
        see if this id is already in the CSV.
        Args:
            voter_id: the id to search for
        Returns:
            True if found, False if not
        """
        with open(self.filename, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and row[0] == voter_id:
                    return True
        return False

    def record_vote(self, voter_id: str, candidate: str) -> None:
        """
        appends a vote to the file
        Args:
            voter_id: who is voting
            candidate: who they vote for
        Raises:
            ValueError if invalid id or duplicate
            IOError if write fails
        """
        if not self.validate_id(voter_id):
            raise ValueError("ID must be alphanumeric & not empty")
        if self.has_voted(voter_id):
            raise ValueError("ID already voted")

        try:
            with open(self.filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([voter_id, candidate])
        except OSError as e:
            raise IOError("Could not save vote") from e

    def get_results(self) -> Dict[str, int]:
        """
        reads file and tallies votes
        Returns:
            dict where key=candidate, value=votes
        """
        tally: Dict[str, int] = {}
        with open(self.filename, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row:
                    tally[row[1]] = tally.get(row[1], 0) + 1
        return tally

    def get_winner(self) -> str:
        """
        picks the winner based on counts
        Returns:
            name of winner, "Tie", or "No votes yet"
        """
        results = self.get_results()
        if not results:
            return "No votes yet"
        items: List[tuple[str, int]] = sorted(results.items(), key=lambda x: x[1], reverse=True)
        top = items[0][1]
        leaders = [name for name, cnt in items if cnt == top]
        return "Tie" if len(leaders) > 1 else leaders[0]
