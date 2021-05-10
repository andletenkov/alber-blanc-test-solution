FROM python:3.7-slim

COPY ./Pipfile .
RUN pip install pipenv && \
    pipenv install --deploy --ignore-pipfile
COPY ./ .
CMD ["pipenv", "run", "pytest", "tests/"]