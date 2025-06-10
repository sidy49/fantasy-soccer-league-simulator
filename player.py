from __future__ import annotations
from enums import PlayerPosition
from data_structures import ArrayList
from lazy_double_table import LazyDoubleTable

# Do not change the import statement below
# If you need more modules and classes from datetime, do not use
# separate import statements. Use them from datetime like this:
# datetime.datetime, or datetime.date, etc.
import datetime


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Justification:

            The best and worst case complexity of the init function is O(1) since all operations are perfomed in constant time, i.e, 
            just intialisation of variables and object instantiation. 
                    
         """
        self.name = name
        self.position = position
        self.age_current = datetime.datetime.now().year - age 
        self.goals = 0

        self.stats = LazyDoubleTable()

    def reset_stats(self) -> None:
        """
        Reset the stats of the player.
        
        This doesn't delete the existing stats, but resets them to 0.
        I.e. all stats that were previously set should still be available, with a value of 0.

        Complexity:
            Best Case Complexity: O(N)
            Worst Case Complexity: O(N * S)

            N is the number of stats 
            S is the table size.

            Justification:

            Best Case:
            The best case complexity of O(N), occurs when all the keys are retrieved seamlessly and each statistic is reset
            without any collisions.

            Worst Case:
            The Worst Case complexity of O(N * S) occurs when the keys() method in HashyDoubleTable is called and it iterates
            through several empty positions/SENTINELS costing O(N+S), and each reset causes a full probe of the table 
            which costs O(S). Therefore, the worst case complexity simplifies to O(N*S).
        """
        for key in self.stats.keys():
            self.stats[key] = 0

    def __setitem__(self, statistic: str, value: int) -> None:
        """
        Set the given value for the given statistic for the player.

        Args:
            statistic (string): The key of the stat
            value (int): The value of the stat

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(S), S refers to the table size.

            Justification:

            Best Case:
            The best case happens when the value for the statistic (key) lands in an empty position or if it's already 
            in the table and the statistic's value has to updated.

            Worst Case:
            The Worst case happens when the value for the statistic (key) requires probing through the most of the table 
            due to collisions/SENTINELS, which results in S probes and an overall worst case complexity of O(S).
        """
        self.stats[statistic] = value


    def __getitem__(self, statistic: str) -> int:
        """
        Get the value of the player's stat based on the passed key.

        Args:
            statistic (str): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(S), S refers to the table size.

            Justification:

            Best Case:
            The Best case occurs when the key is found on the first probe, so only one operation is done in constant time.

            Worst Case:
            The Worst case occurs when multiple positions must be probed through due to collisions/SENTINELS, which
            requires S probes resulting in an overall worst case complexity of O(S).
        """
        return self.stats[statistic]

    def get_age(self) -> int:
        """
        Get the age of the player

        Returns:
            int: The age of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

            Justification:

            Both the best and worst case complexities are O(1), as only basic arithmetic operations 
            are perfomed and each call to the functions of the datetime module is O(1).
        """
        return datetime.datetime.now().year - self.age_current

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity Analysis not required.
        """
        return f"{self.name} {self.position.name} Goals: {self.goals} Age: {self.get_age()}"

    def __repr__(self) -> str:
        """ String representation of the Player object.
        Useful for debugging or when the Player is held in another data structure.
        """
        return str(self)
