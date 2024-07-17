FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /weather_test_project

# Install dependencies
COPY requirements.txt /weather_test_project/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /weather_test_project/