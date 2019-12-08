FROM python:3.7

ADD test2.py /

RUN pip install pystrich
RUN pip install flask
RUN pip install torch
RUN pip install torchvision
RUN pip install opencv-python
RUN pip install Pillow
EXPOSE 5000

CMD [ "python", "./test2.py" ]