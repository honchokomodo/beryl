# Database Setup for Beryl

## PostgreSQL 

DisQuest requires PostgreSQL first. The easiest way to do so is to use PostgreSQL on Docker. You can find instructions on how to do this [here](https://hub.docker.com/_/postgres). In short, when you are going to run it, input these 2 env variables: `POSTGRES_PASSWORD`, `POSTGRES_USER`. `POSTGRES_USER` should be named `Beryl` ideally, but you could change it. Make sure to keep note of it some secure. When making the password, please don't include anything with `@` in it. Asyncpg will complain about it and not connect to the database. Now use psql and login into the Postgres server with the password and username that you just created. Once you are in, create a database called `beryl_disquest`. Next, cd into the bot folder, and create an `.env` file. This is where you are going to store all of the credentials. The file should look like this:

```
# Bot/.env
Beryl_Keys = "Discord Bot Tokens"
Postgres_Password = "Password for Postgres"
Postgres_IP = 127.0.0.1 # if localhost doesn't work, use your ipv4 address instead
Postgres_User = "Beryl"
Postgres_Database = "beryl_disquest"
Postgres_Port = 5432
```

Now run `Scripts/databaseInit.py`. This will create the table within the database that will store all of the data. From there on out, run Beryl, and that's all. DisQuest is the alternative to the XP cog, which saves all of it into a JSON file (that's a very very bad practice, since running on production with that wouldn't scale well).

## MongoDB

Beryl's Events system uses MongoDB under the hood to handle persistence data storage. The easiest way to get started is with MongoDB on Docker. You can find instructions on how to do this [here](https://hub.docker.com/_/mongo). In short, when you are going to run it, input these 2 env variables: `MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD`. `MONGO_INITDB_ROOT_USERNAME` should be named `Beryl` ideally, but you could change it. Make sure to keep note of it some secure. When making the password, please don't include anything with `@` in it. Beanie and in turn Pymongo, will complain about it and not connect to the database (Blame MongoDB for that). Now use mongo and login into the Mongo server with the password and username that you just created. You can use MongoDBCompass or Mongosh to create the database on the next step. Once you are in, create a database called `beryl_events`. Assuming that you already have created the `.env` file from earlier, add these lines in. The file should look like this:

```
# Bot/.env
Beryl_Keys = "Discord Bot Tokens"
MongoDB_Password = "MongoDB password"
MongoDB_IP = 127.0.0.1 # if localhost doesn't work, use your ipv4 address instead
MongoDB_User = "Beryl"
```

Collections will already be handled by Beanie, so there is no need to worry about creating collections. Now run Beryl, and that's it.