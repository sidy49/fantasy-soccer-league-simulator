from __future__ import annotations

from data_structures.hash_table_linear_probing import LinearProbeTable

from data_structures.referential_array import ArrayR

import datetime

class HashyDateTable(LinearProbeTable[str]):
    """
    HashyDateTable assumed the keys are strings representing dates, and therefore tries to
    produce a balanced, uniform distribution of keys across the table.

    Conflicts are resolved using Linear Probing.
    
    All values will also be strings.
    """
    def __init__(self) -> None:
        """
        Initialise the Hash Table with with increments of 366 as the table size.
        This means, initially we will have 366 slots, once they are full, we will have 4 * 366 slots, and so on.

        No complexity is required for this function.
        Do not make any changes to this function.
        """
        LinearProbeTable.__init__(self, [366, 4 * 366, 16 * 366])

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        The key will always be exactly 10 characters long and can be any of these formats, but nothing else:
        - DD/MM/YYYY
        - DD-MM-YYYY
        - YYYY/MM/DD
        - YYYY-MM-DD

        The function assumes the dates will always be valid i.e. the input will never be something like 66/14/2020.
        
        Complexity: 
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)

        Justification:

        Let k = the input key of the date of length- 10 characters.

        Both the best and worst case complexities are O(1) as the function performs a fixed number of operations.
        The function uses string slicing to extract the contents of the input key's date, uses the datetime
        module to format the sliced data and performs arithmetic operations to find the hash value. All these
        operations take constant time as none of them depend on the size of the input.

        Therefore, both the best and worst case time complexities are O(1).
        
        """

        # String slicing to find the day, month and year in the input key. : YYYY/MM/DD and YYYY-MM-DD
        if key[4] in ("-", "/"):

            year = int(key[0:4])
            month = int(key[5:7])
            day = int(key[8:10])
        
        # DD/MM/YY and DD-MM-YY
        elif key[2] in ("-", "/"):

            year = int(key[6:10])
            month = int(key[3:5])
            day = int(key[0:2])

       #this converts the data inserted as the key into a properly formatted date using datetime.

        date_formatted = datetime.date(year, month, day)
        
        #this is used to calculate the number of days off from the key date to the start of the year.
        first_day_year = datetime.date(year,1,1)
        day_index = (date_formatted-first_day_year).days

        # Calculates the year offset from 1970- start of valid date input.
        years_from_start = year - 1970

        return (day_index + years_from_start * 366) % self.table_size


            