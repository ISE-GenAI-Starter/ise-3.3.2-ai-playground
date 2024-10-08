
FROM python:3.11-alpine

# Create and set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install Shapely
RUN apk add --no-cache \
gcc \
libc-dev \
geos-dev \
&& pip install shapely

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose the port your application will run on
EXPOSE 8080

# Specify the command to run on container start
CMD ["gunicorn"  , "-b", ":8080", "app:app"]