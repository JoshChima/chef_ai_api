FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

# Install ffmpeg
# RUN apt update && apt install -y ffmpeg

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
# COPY src ./src
# EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
# RUN useradd app
# USER app
# CMD ["conda" "init"]
CMD ["pip" "install" "--no-cache-dir" "-r" "requirements.txt"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]