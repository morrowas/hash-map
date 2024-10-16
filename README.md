# HashMap Portfolio Project
In this project, I implemented two HashMap classes using Python. The two HashMap classes use different methods for collision resolution; the hash_map_oa.py file uses the open addressing with quadratic probing method, while the hash_map_sc.py file implements the chaining method. This project was completed as part of my coursework in Data Structures at Oregon State University. 

## Methods included in open addressing with quadratic probing HashMap class
- put()
- get()
- remove()
- contains_key()
- clear()
- empty_buckets()
- resize_table()
- table_load()
- get_keys()
- __iter__(), __next__()

## Methods included in chaining method HashMap class
- **put()**: This method updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value.If the given key is not in the hash map, a new key/value pair must be added. For this hash map implementation, the table must be resized to double its current capacity when this method is called and the current load factor of the table is greater than or equal to 1.0.
- get()
- remove()
- contains_key()
- **clear()**: This method clears the contents of the hash map.It does not change the underlying hash table capacity.
- **empty_buckets()**: This method returns the number of empty buckets in the hash table.
- resize_table()
- **table_load()**: This method returns the current hash table load factor.
- get_keys()
- find_mode()
