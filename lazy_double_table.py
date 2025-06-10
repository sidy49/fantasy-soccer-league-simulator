from __future__ import annotations

from data_structures.referential_array import ArrayR
from data_structures.abstract_hash_table import HashTable
from typing import TypeVar


V = TypeVar('V')

class Sentinel:
    """
    Sentinel Class to aid in Lazy Deletion Process
    
    """
    pass

#Sentinel variable initialised to deal with deleted keys.
SENTINEL = Sentinel()

class LazyDoubleTable(HashTable[str, V]):
    """
    Lazy Double Table uses double hashing to resolve collisions, and implements lazy deletion.

    Feel free to check out the implementation of the LinearProbeTable class if you need to remind
    yourself how to implement the methods of this class.

    Type Arguments:
        - V: Value Type.
    """
    
    # No test case should exceed 1 million entries.
    TABLE_SIZES = (5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869)
    HASH_BASE = 31

    def __init__(self, sizes = None) -> None:
        """
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes

        self.__size_index = 0
        self.__array: ArrayR[tuple[str, V]] = ArrayR(self.TABLE_SIZES[self.__size_index])
        self.__length = 0
    
    @property
    def table_size(self) -> int:
        return len(self.__array)

    def __len__(self) -> int:
        """
        Returns the number of elements in the hash table
        """
        return self.__length

    def keys(self) -> ArrayR[str]:
        """
        Returns all keys in the hash table.
        complexity: O(N + S) where N is the number of items in the table and S is the table size.
        """
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None:
                res[i] = self.__array[x][0]
                i += 1
        return res

    def values(self) -> ArrayR[V]:
        """
        Returns all values in the hash table.

        complexity: O(N + S) where N is the number of items in the table and S is the table size.
        """
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None:
                res[i] = self.__array[x][1]
                i += 1
        return res

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See __getitem__.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self.__hashy_probe(key, False)
        return self.__array[position][1]
    
    def is_empty(self) -> bool:
        return self.__length == 0
    
    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        """
        result = ""
        for item in self.__array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: str) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(S) , S refers to the Table Size.

        Justification:

        Best Case:
        The best case complexity of O(1) occurs initially when the step size chosen is Co-Prime wth the table size
        and so the loop exits after one iteration and the step size is returned.

        Worst Case:

        The worst case complexity of O(s) occurs when the step values divide the table size, requiring the hash function
        to iterate through all the values < table size before 1 is returned.

        """
        # A prime number is choosen to generate a step size that's co-prime with table size and varies for each key 
        # This reduces collision and evenly distributes the keys- proving to be a good conflict resolution strategy.
        
        PRIME_NUM =  17
        # The function produces a step size based on the first character in the key.
        step = PRIME_NUM - (ord(key[0]) % PRIME_NUM)

        #Do not let the step size equal zero as this defies the purpose of the hash function.
        if step == 0:
            step = 1

        #this is done to ensure that the step size is co-prime with the table's size.
        for _ in range(step, self.table_size):

            if self.table_size % step != 0:
                return step
        
        # one is returned when all of the step sizes are invalid.   
        return 1 

    def __hashy_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Raises:
            KeyError: When the key is not in the table, but is_insert is False.
            RuntimeError: When a table is full and cannot be inserted.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(s), s refers to the table size

            Justification:

            Best Case:
            
            The best case occurs when the key we are searching for already exists or a free position is available for it
            at the first probe, resulting in constant time complexity.

            Worst Case:

            The worst case occurs when the table is nearly full or has too many SENTINELS, and s probes have to be made 
            to find an available position for the key or a matching key. However, SENTINELS allow insertions of keys into 
            the table, they still increase probing as they are ignored during lookup of the key. 
            This causes the worst case time complexity to be O(s), s refers to the table size.

        """
        # Initial position
        position = self.hash(key)
        step = self.hash2(key)

        for _ in range(self.table_size):
            
            #When the position is empty- the key is not already present in table.
            if self.__array[position] is None:
                if is_insert:
                    return position
                raise KeyError(key)
            
            #Position contains SENTINEL so it can be reused to insert a key.
            elif self.__array[position] == SENTINEL:
                if is_insert:
                    return position
            #The key-value pair already exists so the key is found- and either updated or read.  
            elif self.__array[position][0] == key:
                return position
            
            position = (position + step) % self.table_size
        
        if is_insert:
            raise RuntimeError("Table is full")
        raise KeyError(key)

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, value) pair in our hash table.

        Remember! This is where you will need to call __rehash if the table is full!
        
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N * S), where N is the number of items in the table and S is the table size.

        Justification:

        Best Case:

        The Best case occurs when the key is updated or added into the table without any 
        collisions or rehashing in the first probe.

        Worst Case:

        The worst case complexity occurs when the hash table has to be rehashed as it exceeds the
        2/3 of its capacity or when the table is full and a RunTime Error is called. So, all the 
        N items in the table have to be rehashed and reinserted into a table with a larger capacity,
        this takes upto O(S) time in worst case due to excessive probing.

        Therefore, the worst case complexity is O(N * S).

        """
        #We rehash the table if adding the key is about exceed 2/3 capacity of the table.
        if (self.__length + 1) > (2 * self.table_size) //3:
            self.__rehash()
        
        try:
            position = self.__hashy_probe(key, True)
        
        #this handles the case when the hash table is full
        except RuntimeError:
            self.__rehash()
            self.__setitem__(key,data)
            return
        #this is done to check if a new key is being added to the table. 
        if self.__array[position] is None or self.__array[position] == SENTINEL:
            self.__length += 1 
        
        #saves the key and value in the hashy table.
        self.__array[position] = (key, data)
        

    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(S), s refers to the table size

            Justification:

            Best case:
            The best case complexity is O(1) when the key that is to be deleted is located in the first
            spot probed, which requires only one operation and a constant-time deletion.

            Worst Case:
            The worst case complexity is O(1) when the key is found after we probe through most of the table, due to 
            clustering, and this requires up to s probes to locate and delete the key, which results in a worst case complexity of O(S).
        """
        index_todelete = self.__hashy_probe(key, False)

        self.__array[index_todelete] = SENTINEL
        self.__length-=1

    def __rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
            Best Case Complexity: O(N * S)
            Worst Case Complexity: O(N * S)

            N is the number of items in the table.
            S is the table size.

            Justification:

            Both the best and worst case complexities are O(N * S), as the rehash function starts off by creating a new table of size, S.
            Then, all of the N key-value items in the old table are inserted into the new table which takes N operations using double hashing.
            The reinsertion could also take up to S probes into the table, resulting in a O(S).

            Therefore, taking all these operations into account the best and worst case complexity is O(N * S).
        """
        curr_table = self.__array

        #this chooses the next table size in the predefined hash table sizes.
        self.__size_index += 1

        #this gets the next table size.
        updated_table_size = self.TABLE_SIZES[self.__size_index]

        #A new empty table is created using the new size,
        self.__array = ArrayR(updated_table_size)
        self.__length = 0

        #existing key-value pairs are re-inserted into the new table. This excludes empty positions and deleted pairs (SENTINELS).
        for pair in curr_table:
            
            if pair is not None and pair!= SENTINEL:

                key, data = pair 
                self[key] = data



