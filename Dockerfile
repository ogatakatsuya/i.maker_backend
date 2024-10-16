FROM public.ecr.aws/lambda/python:3.10

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --output requirements.txt

RUN pip install -r requirements.txt

COPY . ./

CMD [ "src/main.handler" ]