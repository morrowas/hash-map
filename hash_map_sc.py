# Name: Ashley Morrow
# OSU Email: morrowas@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/09/2023
# Description: HashMap implementation with chaining for collision resolution.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Takes the key and value input as arguments and add them as a key/value pair in the hash map. If the key
        already exists in the hash map, its value will be replaced with the new value. Otherwise, a new key/value
        pair is added. The table will be resizes to at least double its current capacity (to the nearest prime number)
        if the current load factor of the table is greater than or equal to 1.0.
        """
        load_factor = self.table_load()
        if load_factor >= 1.0: #If greater than or equal to 1, resize dynamic array
            self.resize_table(self._capacity*2) #Initializes to double the original capacity

        hash_value = self._hash_function(key)
        index = hash_value % self._capacity
        #Did not create capacity variable since table could have been resized if load factor was >= 1.0

        #Pull the linked list already at the index the new key/pair value will be added to
        linked_list = self._buckets.get_at_index(index)
        linked_list_length = linked_list.length()

        #Determine if key is already in linked list - if so, replace value for key. Else, create new node with key/value
        #pair.
        if linked_list_length > 0:
            current_node = linked_list.contains(key)
            if current_node is not None: #If not None, this means the key is already included in the linked list
                current_node.value = value
            else: #This means the key is not already included in the linked list
                linked_list.insert(key, value)
                self._size += 1
        else: #If linked list is empty
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table, which in this case would be elements with empty
        linked lists in the dynamic array.
        """
        array_length = self._capacity
        empty_bucket_num = 0

        for index in range(0, array_length):
            linked_list = self._buckets.get_at_index(index)
            if linked_list.length() == 0:
                empty_bucket_num += 1

        return empty_bucket_num

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table.
        """
        num_of_elements = 0 #Counter to hold number of elements in table
        num_of_buckets = self._buckets.length() #Will also use this variable to represent length of table

        for index in range(0, num_of_buckets): #Iterating through dynamic array
            index_value = self._buckets.get_at_index(index)
            if index_value is not None:
                for value in index_value: #Iterating through linked list
                    num_of_elements += 1

        return num_of_elements / num_of_buckets

    def clear(self) -> None:
        """
        Clears the contents of the dynamic array holding the hash map without changing the underlying hash table
        capacity.
        """
        empty_list = LinkedList()

        for index in range(0, self._capacity):
            self._buckets.set_at_index(index, empty_list)

        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity as an argument and changes the capacity of the internal hash table to the prime number
        closest to the new capacity (in ascending order). If the new capacity is less than 1, this method will do
        nothing.
        """
        #If new_capacity is less than 1, the method does nothing
        if new_capacity < 1:
            return
        #If new_capacity is 1 or more, make sure it is a prime number
        else:
            is_num_prime = self._is_prime(new_capacity) #Tests to see if the new capacity is a prime number
            if is_num_prime is False: #If not prime, change new_capacity to next prime number
                new_capacity = self._next_prime(new_capacity)

            #Create new dynamic array, will become the dynamic array for the hashmap later
            new_da = DynamicArray()
            #Creates dynamic array with tuples with key and value pairs
            keys_and_values_da = self.get_keys_and_values()

            #Change capacity to new capacity - important that this is AFTER we create the keys and values da
            self._capacity = new_capacity

            # Creates new empty buckets to match new capacity in new dynamic array
            for index in range(0, new_capacity):
                new_linked_list = LinkedList()
                new_da.append(new_linked_list)

            self._buckets = new_da #Sets hashmap dynamic array to equal new dynamic array
            self._size = 0 #Reset size since we're using put method below

            #Rehash values
            keys_and_values_length = keys_and_values_da.length()
            for num in range(0, keys_and_values_length):
                current_tuple = keys_and_values_da.get_at_index(num)
                key = current_tuple[0]
                value = current_tuple[1]
                self.put(key, value)



    def get(self, key: str):
        """
        Searches the hash map for the key input as an argument and returns the value associated with that key. If the
        key is not present in the hash map, the method will return None.
        """
        #Find the index the key will be under, if in the hash table
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        linked_list = self._buckets.get_at_index(index)

        if linked_list.length() == 0:
            return None #Return None if the linked list is empty

        node_with_key = linked_list.contains(key)
        if node_with_key is None:
            return None
        else:
            return node_with_key.value

    def contains_key(self, key: str) -> bool:
        """
        Searches the hash map for the key input as an argument. Returns True if the given key is in the hash map,
        and False otherwise.
        """
        # Find the index the key will be under, if in the hash table
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        linked_list = self._buckets.get_at_index(index)

        if linked_list.length() == 0:
            return False  # Return False if the linked list is empty

        node_with_key = linked_list.contains(key)
        if node_with_key is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Removes the first node with the key entered as the argument from the hash map. If the key does not exist
        in the hash map, this method does nothing.
        """
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        linked_list = self._buckets.get_at_index(index)
        linked_list_length = linked_list.length()

        if linked_list_length > 0: #If linked list is not empty
            was_value_removed = linked_list.remove(key)
            if was_value_removed is True:
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the table.
        """
        new_da = DynamicArray()

        for index in range(0, self._capacity):
            linked_list = self._buckets.get_at_index(index)
            linked_list_length = linked_list.length()
            if linked_list_length > 0:
                for current_node in linked_list:
                    new_tuple = (current_node.key, current_node.value)
                    new_da.append(new_tuple)

        return new_da



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes a dynamic array and finds the mode value(s) of the array, as well as the frequency of the mode values.
    Returns a tuple, where the first element is a dynamic array of all the mode values, and the second element
    is the frequency of the mode values represented as an integer.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    #Get size of input dynamic array
    da_length = da.length()
    frequency_counter = 1

    #Iterate through each element and add to hashmap
    for index in range(0, da_length):
        da_value = da.get_at_index(index) #Get value from input DA, should be a string
        map_value = map.get(da_value) #Searches hashmap to see if value from DA is a key in the hashmap
        if map_value is None: #This means the string from da_value was not already in the hashmap
            map.put(da_value, 1) #Sets value in hashmap to 1, the frequency of the new string
        else:
            map_value += 1 #Increase map_value by 1 since this represents the frequency of the string in the hashmap
            map.put(da_value, map_value)

    keys_and_values_da = map.get_keys_and_values() #Returns DA with tuples of the values and their frequency
    return_da = DynamicArray() #Will be the DA we return when the method is complete
    mode_frequency = 1
    keys_values_length = keys_and_values_da.length()

    #Iterate through keys and values dynamic array to find mode and frequency of mode value(s)
    for index in range(0, keys_values_length):
        da_tuple = keys_and_values_da.get_at_index(index) #Should return tuple with string and frequency
        da_string, da_frequency = da_tuple
        if da_frequency == mode_frequency: #If frequency of string matches mode frequency, add string to return DA
            return_da.append(da_string)
        elif da_frequency > mode_frequency: #If frequency of string is > than mode frequency, reset DA, then add string
            return_da = DynamicArray()
            return_da.append(da_string)
            mode_frequency = da_frequency

    return (return_da, mode_frequency)

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
