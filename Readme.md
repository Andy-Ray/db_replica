[First](https://aliceh75.github.io/testing-postgresql-cluster-using-docker)

[Second](https://prudnitskiy.pro/2018/01/05/pgsql-replica/)

[Third](https://docs.jelastic.com/postgresql-database-replication/)

for Postgres 11-13

[12](https://docs.jelastic.com/postgresql-database-replication/)

[12](https://therishabh.in/setting-up-master-slave-replication-in-postgresql-using-dockers-and-external-volumes/)

[13](https://programmer.group/docker-configures-the-master-slave-environment-of-postgresql13.html)

[latest?](https://www.optimadata.nl/blogs/1/nlm8ci-how-to-run-postgres-on-docker-part-3)

Master

1. Copy postgresql.conf and pg_hba.conf from container
2. Change next lines in postgresql.conf:

   # need to chose correct or combine, here goes all i find, soon will be one correct conf settings"

   ```
   wal_level = hot_standby
   max_wal_senders = 10
   archive_mode = on
   archive_command = 'cd .'
   ```

   or

   ```
   wal_level = replica
   max_wal_senders = 3 # max number of walsender processes
   wal_keep_segments = 64 # in logfile segments, 16MB each; 0 disables
   listen_addresses = '*'
   # or listen_address = ‘IP_OF_SERVER’
   archive_mode = on
   archive_command = 'cp %p /var/lib/postgresql/12/main/archive/%f'
   synchronous_commit = local
   synchronous_standby_names = 'some_name'
   ```

   or

   ```
   archive_mode = on				# Enable Archive Mode
   archive_command = '/bin/date'	# Set archiving behavior
   # The sum of the number of concurrent connections from the slave to the host
   max_wal_senders = 10
   # Specifies that if the backup server needs to obtain log segment files for stream replication, pg_ The minimum size of past log file segments that can be retained in the wal directory
   wal_keep_size = 16
   # Specify a list of backup servers that support synchronous replication
   synchronous_standby_names = '*'
   ```

   or

   ```
   wal_level = hot_standby
   archive_mode = on
   archive_command = 'cd .'
   max_wal_senders = 8
   wal_keep_segments = 8
   hot_standby = on

   ```

3. Change next lines in pg_hba.conf:

   ```
   host replication all {standby_IP_address}/32 trust
   ```

   or

   ```
    # Localhost
    host    replication     replica          127.0.0.1/32             md5
    # PostgreSQL Master IP address
    host    replication     replica          10.0.15.10/32            md5
    # PostgreSQL SLave IP address
    host    replication     replica          10.0.15.11/32            md5
   ```

   or

   ```
    #add this line if created user preduser
    host replication repuser 172.18.0.102/24 md5
   ```

   or

   ```
    host replication all 0.0.0.0/0 md5
   ```

Slave:

1. same as Master
2. Change next lines in postgresql.conf:

   ```
   hot_standby = on

   # There is a primary_conninfo parameter that specifies the connection string which the standby server will use to connect to the sending #server. The connection string must indicate the host name (or address) of the sending server, as well as the port number. The username #corresponding to the role with the appropriate privileges on the sending server is also provided. The password must also be specified in #the primary_conninfo or in a separate ~/.pgpass file on the backup server if the sender requires password authentication.

   primary_conninfo = 'host=10.0.15.10 port=5432 user=replica'

   trigger_file = '/tmp/touch_me_to_promote_to_me_master'

   # The last option that makes database server as slave is standby.signal file availability, which indicates the server should start up as a hot standby. File must be located in the PostgreSQL data directory and it can be empty or contain any information. Once a slave is promoted to master this file will be deleted.
   ```
