FROM ros:humble 

WORKDIR /home/Documents/Manipulator/ 

RUN apt-get update && apt-get install -y \ 
    python3-pip \
    python3-dev \ 
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libxi-dev \
    libxmu-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt . 
RUN pip3 install --no-cache-dir -r requirements.txt 

CMD ["python3, bash"]