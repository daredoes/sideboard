#!/bin/bash
DATE=$(date +backup_%m_%d_%y_%H_%M)
pg_dump -d cms -U cms --host localhost > $DATE.sql
