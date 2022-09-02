FROM gitpod/workspace-full:latest

USER gitpod

RUN pyenv install 3.10.5
RUN pyenv global 3.10.5
RUN python -m pip install --upgrade pip
RUN pip install pre-commit
RUN npm i --global commitizen
