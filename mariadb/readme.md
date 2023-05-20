**Configuring the MariaDB x64 server for working with Kaspersky Security Center 14.2**
Enable support of InnoDB and MEMORY storage and of UTF-8 and UCS-2 encodings

Windows: 
1. Open the my.ini file in a text editor
2. Adding the following lines code in my.ini file into into the [mysqld] section. 

Linux: 
1. Open the my.cnf file in a text editor.
2. Adding the following lines code my.cnf in my.cnf file.

innodb_buffer_pool_size - size of the memory buffer used for caching InnoDB data and indexes
innodb_buffer_pool_size should be set to a value that is at least 80 percent of the expected size of the KAV database. If the database size is smaller than the specified buffer size, only the required memory is allocated. If you use MariaDB 10.4.3 or older, the actual size of allocated memory is approximately 10 percent greater than the specified buffer size.

By default, the optimizer add-ons join_cache_incremental, join_cache_hashed, join_cache_bka are enabled. If these add-ons are not enabled, you must enable them.

To check whether optimizer add-ons are enabled:

1. In the MariaDB client console, execute the command:
```
SELECT @@optimizer_switch;
```
2. Make sure that its output contains the following lines:
```
join_cache_incremental=on
join_cache_hashed=on
join_cache_bka=on
```
If these lines are present and have the values on, then optimizer add-ons are enabled.
--------------------------------------------------------------------------------------
If these lines are missing or have off values, you need to do the following:

Windows:
1. Open the my.ini file in a text editor.
2. Add the following lines into the [mysqld] section of the my.ini file:
```
optimizer_switch='join_cache_incremental=on'
optimizer_switch='join_cache_hashed=on'
optimizer_switch='join_cache_bka=on'
```
Linux:
1. Open the my.cnf file in a text editor.
2. Add the following lines into the my.cnf file:
```
optimizer_switch='join_cache_incremental=on'
optimizer_switch='join_cache_hashed=on'
optimizer_switch='join_cache_bka=on'
```
The add-ons join_cache_incremental, join_cache_hash, and join_cache_bka are enabled.

