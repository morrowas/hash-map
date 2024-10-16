# HashMap Portfolio Project
In this project, I implemented two HashMap classes using Python. The two HashMap classes use different methods for collision resolution; the hash_map_oa.py file uses the open addressing with quadratic probing method, while the hash_map_sc.py file implements the chaining method. This project was completed as part of my coursework in Data Structures at Oregon State University. 

## Methods included in open addressing with quadratic probing HashMap class
- **put()**: This method updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value.If the given key is not in the hash map, a new key/value pair must be added.
  - For this hash map implementation, the table must be resized to double its current capacity when this method is called and the current load factor of the table is greater than or equal to 0.5.
- **get()**: This method returns the value associated with the given key. If the key is not in the hash map, the method returns None.
- **remove()**: This method removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exception needs to be raised).
- **contains_key()**: This method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.
- **clear()**: This method clears the contents of the hash map. It does not change the underlying hash table capacity.
- **empty_buckets()**: This method returns the number of empty buckets in the hash table.
- **resize_table()**: This method changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map, and all hash table links must be rehashed.
  - First check that new_capacity is not less than the current number of elements in the hash map; if so, the method does nothing.
  - If new_capacity is valid, make sure it is a prime number; if not, change it to the next highest prime number. You may use the methods _is_prime() and _next_prime() from the skeleton code.
- **table_load()**: This method returns the current hash table load factor.
- **get_keys_and_values()**: This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.
- **__iter__()**:  This method enables the hash map to iterate across itself. You **ARE** permitted (and will need to) initialize a variable to track the iterator’s progress through the hash map’s contents.
- **__next__()**: This method will return the next item in the hash map, based on the current location of the iterator. It will need to only iterate over active items.
  
## Methods included in chaining method HashMap class
- **put()**: This method updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value.If the given key is not in the hash map, a new key/value pair must be added.
  - For this hash map implementation, the table must be resized to double its current capacity when this method is called and the current load factor of the table is greater than or equal to 1.0.
- **get()**: This method returns the value associated with the given key. If the key is not in the hash map, the method returns None.
- **remove()**: This method removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exception needs to be raised).
- **contains_key()**: This method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.
- **clear()**: This method clears the contents of the hash map.It does not change the underlying hash table capacity.
- **empty_buckets()**: This method returns the number of empty buckets in the hash table.
- **resize_table()**:  This method changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map, and all hash table links must be rehashed.
  - First check that new_capacity is not less than 1; if so, the method does nothing.
  - If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next highest prime number. You may use the methods _is_prime() and _next_prime() from the skeleton code.
- **table_load()**: This method returns the current hash table load factor.
- **get_keys_and_values()**: This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.
- **find_mode()**:  Write a standalone function outside of the HashMap class that receives a dynamic array (that is not guaranteed to be sorted). This function will return a tuple containing, in this order, a dynamic array comprising the mode (most occurring) value/s of the array, and an integer that represents the highest frequency (how many times the mode value(s) appear).
  - If there is more than one value with the highest frequency, all values at that frequency should be included in the array being returned (the order does not matter). If there is only one mode, the dynamic array will only contain that value.
  - You may assume that the input array will contain at least one element, and that all values stored in the array will be strings. You do not need to write checks for these conditions.
  - For full credit, the function must be implemented with **O(N) time complexity**.
