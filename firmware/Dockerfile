FROM dymat/opencv:arm32v7
COPY . /app
WORKDIR /app
#RUN apt update; apt upgrade -y
#RUN apt install python3-opencv -y

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py


RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["game.py"]
