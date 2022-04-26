#!/bin/sh
cp -f /db_conf/*.signal /var/lib/postgresql/data/ > /dev/null
cp -f /db_conf/*.conf /var/lib/postgresql/data/
