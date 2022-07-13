# battstats

## How to Use

The directory must include both a config.json and an .env file.

The config.json is used for passing paramters to battstats. It should take the following form:
```
{
    "source_path": "../data/",
    "source_file": "sample_arbin_export.csv",
    "target_file" : "sample_stream.csv", 
    "segment_size" : 100,
    "write_frequency" : 0.5
}
```

The .env file is used to pass credientials for connecting to the database. It contain the following fields:
```
DB_TARGET = "your_database_name_here"
DB_USERNAME = "your_db_username_here"
DB_PASSWORD = "your_db_password_here"
DB_HOSTNAME = "your_hostname_here" ("localhost)
DB_PORT = "your_db_port here" ("5432")
```
