# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables for Django
ENV DJANGO_SETTINGS_MODULE=SMARTROLL.settings
ENV SECRET=django-insecure-%2%pce8*3&4x-plp)vyxlk^lfuwcq=%88=pzxx8dwsnv%y+_9j
ENV DB_NAME=smartroll
ENV DB_USER=manav1011
ENV DB_PASS=Manav@1011
ENV DB_HOST=postgres
ENV DB_PORT=5432

# RUN chmod +x /app/run.sh

# # Run Django application
# RUN /app/run.sh

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "SMARTROLL.asgi:application"]