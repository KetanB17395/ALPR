FROM python:3.11

ENV PYTHONUNBUFFERED 1

# Install system packages including libgl1-mesa-glx
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libssl-dev

WORKDIR /app

ADD . /app

COPY requirments.txt .

RUN pip install -r requirments.txt

COPY . /app

# Make any necessary migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# EXPOSE 8000

# CMD ["python3", "manage.py", "runserver"]