# flask_numbers

initialize database: \
`python init_db.py` \
\

build with command: \
`docker build -t gen-nums .` \
\
run with command:  \
`docker run -dp 5000:5000 -v database-db:/database.db gen-nums`
