# Pulled directly from Rin
FROM ubuntu:22.04 as install_python
RUN apt-get update
RUN apt-get install -y --no-install-recommends make build-essential 
RUN apt-get install libssl-dev zlib1g-dev libbz2-dev libreadline-dev  -y --no-install-recommends
RUN apt-get install libsqlite3-dev wget ca-certificates curl  -y --no-install-recommends
RUN apt-get install llvm libncurses5-dev  -y --no-install-recommends
RUN apt-get install xz-utils  -y --no-install-recommends
RUN apt-get install tk-dev -y --no-install-recommends
RUN apt-get install libxml2-dev libxmlsec1-dev libffi-dev  -y --no-install-recommends
RUN apt-get install liblzma-dev mecab-ipadic-utf8 git python3.10-dev -y --no-install-recommends
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN set -ex \
  && curl https://pyenv.run | bash \
  && pyenv update \
  && pyenv install 3.10.4 \
  && pyenv global 3.10.4 \
  && pyenv rehash

FROM install_python as install_node
RUN mkdir -p /usr/local/nvm
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update \
  && apt-get install -y curl \
  && apt-get -y autoclean
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION lts
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN source $NVM_DIR/nvm.sh \
  && nvm install $NODE_VERSION \
  && nvm alias default $NODE_VERSION \
  && nvm use default
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
RUN npm install -g npm pm2@latest

FROM install_node AS install_poetry
RUN python -m pip install --upgrade pipx
RUN python -m pipx ensurepath
RUN python -m pipx install poetry

FROM install_poetry AS prod_deployment
WORKDIR /
RUN mkdir /Beryl/ 
COPY /pyproject.toml /Beryl/
COPY /poetry.lock /Beryl/
COPY /Bot/beryl.py /Beryl/Bot/
COPY /Bot/.env /Beryl/Bot
RUN mkdir /Beryl/Bot/Cogs
COPY /Bot/Cogs/ /Beryl/Bot/Cogs
RUN cd /Beryl/ && poetry install
ARG PM2_PUBLIC_KEY_INGEST
ARG PM2_SECRET_KEY_INGEST
ENV PM2_PUBLIC_KEY=${PM2_PUBLIC_KEY_INGEST}
ENV PM2_SECRET_KEY=${PM2_SECRET_KEY_INGEST}
CMD ["pm2-runtime", "cd /Beryl/ && poetry install && poetry run python /Beryl/Bot/beryl.py", "--name", "Beryl"]
