FROM python:3.12.11-bullseye@sha256:7cc929040c5e8cf6036c5099d62a83708427c131fb7a7c965b5ba51e995eea1c

LABEL version="1.0"
LABEL ver_date="28Jul2025"
LABEL description="Python image for application. Will be used for both commands in \
        compose file."

RUN curl -LsSf https://astral.sh/uv/0.8.3/install.sh | sh
ENV PATH="/root/.local/bin/:$PATH"
COPY ./docker_files/python-app-container/.bashrc /root/.bashrc

# Copying just those files before running uv sync to avoid resyncing when pyproject does not change. This will create a layer, which will only change when packages added or deleted from the project.
COPY ./python-app/pyproject.toml /python-app/pyproject.toml
COPY ./python-app/uv.lock /python-app/uv.lock
WORKDIR /python-app
RUN uv sync --locked

COPY ./python-app /python-app
# Removing unnecessary for deployment files.
# In new (unstable syntax there is --exclude option of COPY command), but before it becomes available RUN rm is the option
RUN rm -r /python-app/.venv
RUN rm -r /python-app/test
RUN rm /python-app/.env
# Add - find ./**/*.pyc -delete
#       find ./**/__pycache__ -delete

CMD [ "/bin/bash" ]


