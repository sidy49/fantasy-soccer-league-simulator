from __future__ import annotations
from data_structures.array_set import ArraySet
from data_structures.referential_array import ArrayR
from data_structures.array_list import ArrayList
from enums import TeamGameResult
from game_simulator import GameSimulator, GameSimulationOutcome
from dataclasses import dataclass
from team import Team
from data_structures import ArraySortedList


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html

    Do not make any changes to this class.
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game] | ArrayList[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        self.games = games
        self.week: int = week

    def __iter__(self):
        """
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Justification:
            This method sets the internal index to 0 and it returns it self, both these statements 
            are performed in constant time in both best and worst case- resulting in an O(1).

        """
        self._index = 0 
        return self

    def __next__(self):
        """
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            
            Justification:
            This method access the index of self.games in constant time and increments the internal counter
            to move to the next to the game. Therefore, both best and worst case complexities are O(1) for the 
            method.
        """
        if self._index < len(self.games):
            game = self.games[self._index]
            self._index +=1
            return game 
        else:
            raise StopIteration 


class Season:

    def __init__(self, teams: ArrayR[Team] | ArrayList[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity: O(N^2)
            Worst Case Complexity: O(N^2), 

            N refers to the number of teams in the season.

            Justification:

            Best Case:
            The best case complexity is O(N^2), as regardless of the best case of the add function being O(log N) and 
            the insert function for ArrayList being O(1), these are dominated by the generate_schedule function
            which always performs nested loops across all teams in the season, resulting in a best case complexity of 
            O(N^2).

            Worst Case:
            The worst case complexity is O(N^2), as regardless of the worst case of the add function in ArraySortedList
            being O(N) and the insert function for ArrayList being O(N), these are dominated by the generate_schedule function
            which always performs nested loops across all teams in the season, resulting in a worst case complexity of 
            O(N^2).
        """
        self.teams = teams
        self.leaderboard = ArraySortedList()
        for team in teams:
            self.leaderboard.add(team)

        self.schedule = ArrayList()
        populated_schedule = self._generate_schedule()
        
        #schedule is updated for each week.
        week_count = 1
        for weekly_games in populated_schedule:
            self.schedule.insert(len(self.schedule), WeekOfGames(week_count,weekly_games))
            week_count +=1 

    def _generate_schedule(self) -> ArrayList[ArrayList[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayList[ArrayList[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        
        Do not make any changes to this function.
        """
        num_teams: int = len(self.teams)
        weekly_games: ArrayList[ArrayList[Game]] = ArrayList()
        flipped_weeks: ArrayList[ArrayList[Game]] = ArrayList()
        games: ArrayList[Game] = ArrayList()

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: ArrayList[Game] = ArrayList()
            flipped_week: ArrayList[Game] = ArrayList()
            used_teams: ArraySet = ArraySet(len(self.teams))

            week_game_no: int = 0
            for game in games:
                if game.home_team.name not in used_teams and game.away_team.name not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.name)
                    used_teams.add(game.away_team.name)

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(current_week)
            flipped_weeks.append(flipped_week)
            week += 1

        for flipped_week in flipped_weeks:
            weekly_games.append(flipped_week)
        
        return weekly_games

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume GameSimulator.simulate() is O(1)
            Remember to define your variables in your complexity.

            Best Case Complexity: O(G log N)
            Worst Case Complexity: O(G * N)

            G is the total number of games played in the season.
            N is the number of teams in the season.

            Justification:

            Best Case:
            The best case for this function is O(G log N). We assume that calling the simulate() function would cost
            constant time and adding the result using the add_result() function in best case and player updates from 
            LazyDoubleTable is also done in constant time. The updation of the leaderboard is done in O(log N) time 
            using the index (O(1)) and delete_at_index (O(log N)) functions in best case. However, all this work is being done for
            one game, so to find the overall best case complexity we multiply O(log N) by the total number of games 
            in the season- O(G log N).

            Worst Case:
            The worst case for this function is O(G * N). We assume that calling the simulate() function would cost
            constant time and adding the result using the add_result() function in worst case and player updates from 
            LazyDoubleTable is also done in constant time. The updation of the leaderboard is done in O(N) time using the 
            index (O(log N)) and delete_at_index (O(N)) functions in worst case. However, all this work is being done 
            for one game, so to find the overall worst case complexity we multiply O(N) by the total number of games 
            in the season- O(G log N).
        """
        for week in self.schedule:
            for game in week:
                # simulates the game between the home and away team.
                game_simulate = GameSimulator.simulate(game.home_team, game.away_team)

                # Process's game result for home and away team.
                if game_simulate.home_goals > game_simulate.away_goals:
                    result_home_team = TeamGameResult.WIN
                    result_away_team = TeamGameResult.LOSS
                
                elif game_simulate.home_goals < game_simulate.away_goals:
                    result_home_team = TeamGameResult.LOSS 
                    result_away_team = TeamGameResult.WIN

                else:
                    result_home_team = result_away_team = TeamGameResult.DRAW

                #add_result function to add the result to team's history.
                game.home_team.add_result(result_home_team)
                game.away_team.add_result(result_away_team)
                
                #add the home/away team's results to the leaderboard.
                if game.home_team in self.leaderboard:
                    self.leaderboard.delete_at_index(self.leaderboard.index(game.home_team))
                self.leaderboard.add(game.home_team)
                
                if game.away_team in self.leaderboard:
                    self.leaderboard.delete_at_index(self.leaderboard.index(game.away_team))
                self.leaderboard.add(game.away_team)

                #This is done to list out the players who scored goals.
                for name in game_simulate.goal_scorers:
                    if name in game.home_team.player_search:
                        game.home_team.player_search[name].goals += 1
                    elif name in game.away_team.player_search:
                        game.away_team.player_search[name].goals += 1


    def delay_week_of_games(self, orig_week: int, new_week: int | None = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (int or None): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(W)

            W refers to the number of weeks in a season.

            Justification:

            Best Case:
            The best case occurs in O(1) for this function, when new_week is None so we delete the index and insert the week
            to the end of the list- all these operations are done in constant time.

            Worst Case:
            The worst case of O(W) occurs when the new_week index is at the start of the list, and this cause all the other
            "W" weeks to be moved one index to the right, resulting in an overall worst case complexity of O(W).
        """
        # find the index of the week to delay.
        orig_week_index = orig_week - 1

        delay_week = self.schedule.delete_at_index(orig_week_index)

        #If the new week isn't specified, move the week of games to the end of the ArrayList.
        if new_week is None:
            self.schedule.insert(len(self.schedule),delay_week)
        #Move the original week of games to the specified index of new week given.
        else:
            new_week_index = new_week - 1
            self.schedule.insert(new_week_index, delay_week)


    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Justification:
            Both the best and worst complexities are O(1), as the len function is applied on the ArrayR storing
            the teams, and this is done in constant time.
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
