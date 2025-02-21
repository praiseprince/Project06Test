# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Set necessary environment variables (adjust as needed).
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Expose the port your Flask app runs on.
EXPOSE 5000

# Run the Flask app.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]