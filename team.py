from __future__ import annotations

from data_structures.referential_array import ArrayR
from enums import TeamGameResult, PlayerPosition
from player import Player
from typing import Collection, TypeVar

from data_structures import *
from hashy_date_table import HashyDateTable
from lazy_double_table import LazyDoubleTable

T = TypeVar("T")


class Team:
    def __init__(self, team_name: str, initial_players: ArrayR[Player], history_length: int) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            initial_players (ArrayR[Player]): The players the team starts with initially
            history_length (int): The number of `GameResult`s to store in the history

        Returns:
            None

        Complexity:
            Best Case Complexity: O(P)
            Worst Case Complexity: O(P) , P refers to the number of players in "initial_players".

            Justification:

            Both best and worst case complexities are O(P) for the init function. Most of the operations
            in the init function are performed in constant time, except the part where the initial players are 
            added into the Array of Linked Lists. We do this by calling the add_player() method which takes O(1)
            time in both best and worst case. However, since we are meant to store all the player it takes O(P) * O(1)
            time, simplfying the best and worst case complexity for the function to O(P), where P is the number of initial players.
        """
        self.name = team_name
        self.points = 0
        self.history_length = history_length

        #An array of len 4 is created, where each slot in the array stores a LinkedList- which corresponds to different Player Positions.
        NUM_POSITIONS = 4
        self.players = ArrayR(4)
        for i in range(NUM_POSITIONS):
            self.players[i] = LinkedList()
        
        #used to aid process of lookup and deletion of players.
        self.player_search = LazyDoubleTable()

        for player in initial_players:
            self.add_player(player)

        self.history = CircularQueue(history_length)
        self.posts = HashyDateTable()

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(S), S is the size of the hash table

            Justification:
            
            Best Case:
            Best case happens when the correct linked list is appended to directly (based on the position enum value) and the
            player's name is inserted into the hash table without collisions — all in constant time.
           
            Worst Case:
            Worst case occurs if the hash table("player_search") needs to rehash due to hitting the load factor limit,
            requiring re-insertion of all entries, which takes O(S) time.
        """
        if player.position == PlayerPosition.GOALKEEPER:
            position_index = 0
        
        elif player.position == PlayerPosition.DEFENDER:
            position_index = 1
        
        elif player.position == PlayerPosition.MIDFIELDER:
            position_index = 2
        
        elif player.position == PlayerPosition.STRIKER:
            position_index = 3

        else:
            raise ValueError("Please enter a valid Player Position!")

        self.players[position_index].append(player)
        self.player_search[player.name] = player 

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(P), P refers to the number of players at a particular position.

            Justification:

            Best Case:
            The best case occurs when the player that is to be removed from the team is in the head of the LinkedList- so finding the index and deleting the 
            player all happens in constant time, along with player deletion from hash table which costs O(1)- resulting in an O(1) best case time complexity.

            Worst Case:
            The worst case occurs when the player is found at the end of the LinkedList, requiring N traversals through the LinkedList. The deletion
            of the player from the hash table costs O(1), which brings the overall worst case complexity to O(N).
        """
        #The index in the LinkedList is found based on  the player's position.
        if player.position == PlayerPosition.GOALKEEPER:
            position_index = 0
        
        elif player.position == PlayerPosition.DEFENDER:
            position_index = 1
        
        elif player.position == PlayerPosition.MIDFIELDER:
            position_index = 2
        
        elif player.position == PlayerPosition.STRIKER:
            position_index = 3

        else:
            raise ValueError("Please enter a valid Player Position!")
        
        #The player is deleted and removed from the LinkedList and the HashTable("player_search")- which will be used in future code.
        if player in self.players[position_index]:
            index_delete = self.players[position_index].index(player)
            self.players[position_index].delete_at_index(index_delete)
            self.player_search.__delitem__(player.name)
        else:
            raise ValueError("Player is not in the team")

    def get_players(self, position: PlayerPosition | None = None) -> Collection[Player]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (PlayerPosition or None): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder.
            
            This includes the ArrayR, which was previously prohibited.

        Complexity:
            Best Case Complexity: O(P), P is the number of players in a particular position.
            Worst Case Complexity: O(N), N is the total number of players in the team.

            Justification:
            
            Best Case:
            The best case occurs when the position of the player is given, and so we only traverse through
            that particular position's linked list instead of all the positions linked list, so the best 
            case complexity is O(P), where P is the number of players in a particular position of the team

            Worst Case:
            The Wort case occurs when the position of the player is given as None, which would require us to 
            traverse through all the 4 LinkedLists for all the positions to return all the players in the team,
            this results in a worst case complexity of O(N), where N is the total number of player in the team
            across all positions.
        """
        players_at_position = ArrayList()

        if position is not None:
            if position == PlayerPosition.GOALKEEPER:
                position_index = 0
        
            elif position == PlayerPosition.DEFENDER:
                position_index = 1
        
            elif position == PlayerPosition.MIDFIELDER:
                position_index = 2
        
            elif position == PlayerPosition.STRIKER:
                position_index = 3

            else:
                raise ValueError("Please enter a valid Player Position!")
            
            for player in self.players[position_index]:
                players_at_position.append(player)

        else:
            NUM_POSITIONS = 4
            for i in range(NUM_POSITIONS):
                for player in self.players[i]:
                    players_at_position.append(player)
        
        return players_at_position
        
    def add_result(self, result: TeamGameResult) -> None:
        """
        Add the `result` to this `Team`'s history

        Args:
            result (GameResult): The result to add
            
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Justification:
            Both best and worst case complexities are O(1), as the CircularQueue functions- is_full(), serve() and append() 
            and updation of points(by accessing the enum value: TeamGameResult) are all performed in constant time complexity. 
        """
        if not self.history.is_full():
            self.history.append(result)
        # if the history is full, the oldest result is removed and the new result is added into the Team's result
        else:
            self.history.serve()
            self.history.append(result)

        #The points are updated for the team based on the result and the value in the enum class.
        self.points+= result.value

    def get_history(self) -> Collection[TeamGameResult] | None:
        """
        Returns the `GameResult` history of the team.
        If the team has played less than this team's `history_length`,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the result should be a container with 4 objects in this order:
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        If this method is called before the team has played any games,
        return None the reason for this is explained in the specification.

        Returns:
            Collection[GameResult]: The most recent `GameResult`s for this team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(H), H is the history length.

            Justification:

            Best Case:
            The best case complexity of O(1) is when the CircularQueue is empty,
            and the history is returned as None in constant time complexity.

            Worst Case:
            The worst case complexity is O(H) when the history queue is full when the history length is met, and
            we have to serve the oldest result and re-add all the other resutls to a list -> this takes linear time
            dependant on the history length.
        """
        if self.history.is_empty():
            return None 
        
        team_results = ArrayList()

        for _ in range(len(self.history)):
            result = self.history.serve()
            team_results.append(result)
            self.history.append(result)

        return team_results
    
    def make_post(self, post_date: str, post_content: str) -> None:
        """
        Publish a team blog `post` for a particular `post_date`.
       
        A `Team` can have one published post per day. Any duplicate
        posts should overwrite the original post for that day.
        
        Args:
            `post_date` (`str`) - The date of the post
            `post_content` (`str`) - The content of the post
        
        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(S), S refers to the size of the hash table

            Justification:

            Best Case:
            The best case is O(1) when we insert the date into the Hash Table (HashyDateTable) without meeting many collisions,
            as insertion is done in constant time in a hash table.

            Worst Case:
            The worst case is O(S) when the hashtable performs linear probing and probes through the table that is full and has deleted positions,
            before finding an spot for the key. This happens due to primary clustering from linear probing, resulting in a worst case complexity
            of O(S), where S is the table size.
        """
        self.posts[post_date] = post_content

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Justification:
            Finding the length of the hash table, gives us the number of players in the team
            in constant time, as the hash table ensures all the players are distinct/unique.
        """
        num_players = len(self.player_search)
        return num_players

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity analysis not required.
        """
        return f"Team({self.name})"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure.
        """
        return str(self)

    def __lt__(self, other: Team) -> bool:

        """
        Check if this team should rank higher than another team on the leaderboard.

        Args:
            other (Team): The other team to compare to.

        Returns:
            bool: True if this team ranks higher than the other team, False otherwise.

        Complexity:
            Best Case: O(1)
            Worst Case: O(1)

            Justification:
            This method involves simple comparisons between integers (points) and strings (names).
            Integer and string comparisons both take constant time. So, the time complexity
            is constant in both best and worst cases.
        
        """
        
        if self.points != other.points:
            return self.points > other.points        
        return self.name < other.name 
    
    def __eq__(self, other: Team) -> bool:

        """
        Check if this team is equal to another team based on name.

        Args:
            other (Team): The other team to compare to.

        Returns:
            bool: True if both teams have the same name, False otherwise.

        Complexity:
            Best Case: O(1)
            Worst Case: O(1)

            Justification:
            This method only compares the team names (strings), which is a constant time operation.
            So, the time complexity is constant in both best and worst case.
        
        """
        return self.name == other.name