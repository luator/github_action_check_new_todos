
# Container image that runs your code
FROM python:3.8

RUN pip install gitpython

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY git-diff-todos.py /git-diff-todos.py
COPY git-diff-todos-problem-matcher.json /git-diff-todos-problem-matcher.json

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
