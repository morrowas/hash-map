# Name: Ashley Morrow
# OSU Email: morrowas@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/09/2023
# Description: HashMap implementation with open addressing for collision resolution.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Places the key/value pair in the hash map. If the key is already in the hash map, the value will be replaced
        with the new value. Otherwise, a new key/value pair will be added. If the current load factor of the table
        is greater than or equal to 0.5, the table will be resized before adding the new key/value pair.
        """
        load_factor = self.table_load()
        if load_factor >= 0.5:  # If greater than or equal to 0.5, resize dynamic array
            self.resize_table(self._capacity * 2)  # Initializes to double the original capacity

        #First, test to see if the key is already in the hash map
        index = 0
        dup_key_index = None
        hash_entry = None

        #Only runs the below while loop if the list is not empty
        if self._size != 0:
            while dup_key_index is None and index != self._capacity:
                hash_entry = self._buckets.get_at_index(index)
                if hash_entry is not None:
                    hash_key = hash_entry.key
                    if hash_key == key:
                        dup_key_index = index
                    else:
                        index += 1
                else:
                    index += 1

        #If key found, change the value for that key to the new value
        if dup_key_index is not None:
            hash_entry.value = value
            if hash_entry.is_tombstone is True: #If key found but element is a tombstone, remove tombstone status
                hash_entry.is_tombstone = False
                self._size += 1
        #If key not found, add a new hash entry to the dynamic array
        else:
            #Get index through hash function
            hash_value = self._hash_function(key)
            index = hash_value % self._capacity
            initial_index = index
            probing_val = 1 #Will use in probing scheme if array is not empty at index

            #If array is not empty and not a tombstone, use quadratic probing until one of these conditions is met
            current_entry = self._buckets.get_at_index(index)
            while current_entry is not None and current_entry.is_tombstone is False:
                index = (initial_index + (probing_val)**2) % self._capacity #Added modulo operator
                probing_val += 1
                current_entry = self._buckets.get_at_index(index)

            new_hash_entry = HashEntry(key, value)
            self._buckets.set_at_index(index, new_hash_entry)
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table.
        """
        num_of_elements = 0  # Counter to hold number of elements in table
        num_of_buckets = self._buckets.length()  # Will also use this variable to represent length of table

        for index in range(0, num_of_buckets):  # Iterating through dynamic array
            index_value = self._buckets.get_at_index(index) # Should return a hash entry or None
            if index_value is not None:
                num_of_elements += 1

        return num_of_elements / num_of_buckets

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table, which in this case would be an empty dynamic array
        element, or an element with a tombstone hash entry.
        """
        counter = 0 #Counter variable for number of empty buckets
        current_element = None

        for index in range(0, self._capacity):
            current_element = self._buckets.get_at_index(index)
            if current_element is None:
                counter += 1
            else: #If get_at_index returns a hash entry
                if current_element.is_tombstone is True:
                    counter += 1

        return counter

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table to the integer input into the method as an argument. All
        existing key/value pairs are preserved, and all hash table links are rehashed.
        """
        #Save old capacity - will use later to add None entries to the new dynamic array
        old_capacity = self._capacity

        # If new_capacity is less than current number of elements, the method does nothing
        if new_capacity < self._size:
            return
        # If new_capacity is a valid number, make sure it is a prime number
        else:
            is_num_prime = self._is_prime(new_capacity)  # Tests to see if the new capacity is a prime number
            if is_num_prime is False:  # If not prime, change new_capacity to next prime number
                new_capacity = self._next_prime(new_capacity)

        # Create new dynamic array with key/value pairs
        keys_values_da = self.get_keys_and_values()
        self.clear() #Clear contents of hash map
        self._capacity = new_capacity
        self._size = 0 #Reset size to zero since we'll be using the put method below, which will add to the size

        #If new capacity more than old, add "blank" elements to the new dynamic array
        if new_capacity > old_capacity:
            for num in range(old_capacity, new_capacity):
                self._buckets.append(None)
        #If new capacity less than old, remove elements from the dynamic array
        elif new_capacity < old_capacity:
            while self._buckets.length() != self._capacity:
                self._buckets.pop()

        # Iterate through dynamic array with tuples containing all keys and values
        keys_length = keys_values_da.length()
        for index in range(0, keys_length):
            current_tuple = keys_values_da.get_at_index(index)
            current_key = current_tuple[0]
            current_value = current_tuple[1]
            self.put(current_key, current_value) #Put method will add new hash entry with key and value

    def get(self, key: str) -> object:
        """
        Searches the hash map for the key input as an argument and returns the value associated with that key. If the
        key is not present in the hash map, the method will return None.
        """

        index = 0
        dup_key_index = None
        hash_entry = None

        while dup_key_index is None and index != self._capacity:
            hash_entry = self._buckets.get_at_index(index)
            if hash_entry is not None: #Checks to make sure the entry is not empty before performing more operations
                hash_key = hash_entry.key
                if hash_key == key and hash_entry.is_tombstone is False:
                    dup_key_index = index
                    return hash_entry.value
                else:
                    index += 1
            else:
                index += 1

        return None # Return none if we reach an empty element


    def contains_key(self, key: str) -> bool:
        """
        Searches the hash map for the key input as an argument. Returns True if the given key is in the hash map,
        and False otherwise.
        """
        if self._size == 0: #If list has no elements, return False
            return False
        else:
            index = 0
            dup_key_index = None
            hash_entry = None

            while dup_key_index is None and index != self._capacity:
                hash_entry = self._buckets.get_at_index(index)
                if hash_entry is not None:
                    hash_key = hash_entry.key
                    if hash_key == key and hash_entry.is_tombstone is False:
                        dup_key_index = index
                    else:
                        index += 1
                else:
                    index += 1

            if dup_key_index is not None:
                return True
            else:
                return False

    def remove(self, key: str) -> None:
        """
        Removes the input key and its associated value from the hash map. To maintain search functionality for
        other methods, this method adds a tombstone marker at the index instead of leaving it completely empty.
        """
        if self._size == 0:
            return

        index = 0
        dup_key_index = None #If key found, will hold index where the key is found
        hash_entry = None

        while dup_key_index is None and index != self._capacity:
            hash_entry = self._buckets.get_at_index(index)
            if hash_entry is not None:
                hash_key = hash_entry.key
                if hash_key == key and hash_entry.is_tombstone is False:
                    dup_key_index = index #Stops while loop
                    hash_entry.is_tombstone = True #Setting tombstone to True removes the value from the hash map
                    self._size -= 1
                    return
                else:
                    index += 1
            else:
                index += 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying table capacity.
        """
        for index in range(0, self._capacity):
            self._buckets.set_at_index(index, None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the table.
        """
        new_da = DynamicArray()

        for index in range(0, self._capacity):
            hash_entry = self._buckets.get_at_index(index)
            if hash_entry is not None and hash_entry.is_tombstone is False:
                new_tuple = (hash_entry.key, hash_entry.value)
                new_da.append(new_tuple)

        return new_da

    def __iter__(self):
        """
        Creates an iterator for loops.
        """
        initial_index = 0
        hash_entry = self._buckets.get_at_index(initial_index)

        while hash_entry is None or hash_entry.is_tombstone is True:
            initial_index += 1
            hash_entry = self._buckets.get_at_index(initial_index)

        self._index = initial_index
        return self

    def __next__(self):
        """
        Collects next value, then advances iterator.
        """
        try:
            hash_entry = self._buckets.get_at_index(self._index)
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        if hash_entry is not None and hash_entry.is_tombstone is False:
            return hash_entry
        else:
            raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
