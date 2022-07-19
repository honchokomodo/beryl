# Contributing

These are mainly just instructions on getting set up.

# Installing Dependencies

## Windows 

1. Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/). Pick your distro of choice. In this example, we will use Ubuntu 22.04
2. Install the suggested build dependencies for pyenv. 

    ```sh
    sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev python3.10-dev git
    ```

3. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

4. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

5. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/beryl.git && cd beryl
    ```


6. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

## Linux
    
### Ubuntu

1. Install the suggested build dependencies for pyenv. 

    ```sh
    sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev python3.10-dev git
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/beryl.git && cd beryl
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

### OpenSUSE

1. Install the suggested build dependencies for pyenv.

    ```sh
    sudo zypper install gcc automake bzip2 libbz2-devel xz xz-devel openssl-devel ncurses-devel \
    readline-devel zlib-devel tk-devel libffi-devel sqlite3-devel python310-devel
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/beryl.git && cd beryl
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

### Fedora/CentOS

1. Install the suggested build dependencies for pyenv

    Fedora 22 and above:

    ```sh
    sudo dnf install make gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel python-devel git curl
    ```

    CentOS or Fedora 22 and below:

    ```sh
    sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel python-devel git curl
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/beryl.git && cd beryl
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```
### Arch/Manjaro

1. Install the suggested build dependencies for pyenv

    ```sh
    sudo pacman -S --needed base-devel openssl zlib xz tk python libffi
    ```

2. Install Pyenv. Also make sure to follow the instructions [here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

    ```sh
    curl https://pyenv.run | bash
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

3. Restart your shell (make sure you have added it to your path and configured it either in your `.zshrc`, or `.bashrc` files)
    
    ```sh
    exec "$SHELL"
    ```

4. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/beryl.git && cd beryl
    ```

5. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

## MacOS

1. Install Xcode Command Line Tools (`xcode-select --install`) and [Homebrew](https://brew.sh/)

2. Install the suggested build dependencies for pyenv

    ```sh
    brew install openssl readline sqlite3 xz zlib tcl-tk git curl make
    ```
3. Install Pyenv via Homebrew

    ```sh
    brew update
    brew install pyenv
    ```

4. Install Python

    ```sh
    pyenv update
    pyenv install 3.10.5
    pyenv global 3.10.5
    pyenv rehash
    ```

5. Follow the rest of the steps, starting on [Set Up Your shell Environment For Pyenv](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

5. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/beryl.git && cd beryl
    ```

6. Run Make to create the venv and install dependencies

    ```sh
    make dev-setup
    ```

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