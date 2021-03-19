FROM python:3

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install --default-timeout=100 future 
RUN pip install opencv_python
RUN pip install --no-cache-dir -r requirements.txt 
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

ENTRYPOINT [ "python", "read_file_multiprocess.py" ]


# docker run -it -v /home/bao/Desktop/Coding/Python/IMAGES:/app/data/images  mask_face:2.0 /bin/bash

# docker run -d -v /home/bao/Desktop/Coding/Python/IMAGES:/app/data/images -v /home/bao/Desktop/Coding/Python/ARCHIVE:/app/data/archive mask_face:2.0 