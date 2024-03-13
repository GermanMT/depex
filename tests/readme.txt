To generate Test Workbenches for experimentation you need to follow the following steps, from the root of the project:

1. Launch the tool with the command "docker compose up --build".

2. Load the vulnerability database with the command "seeds/vulndb_seeder.sh".

3. Run the tests with the command "python3 tests/test.py". The first run will take longer because it has to generate the graphs in the database.