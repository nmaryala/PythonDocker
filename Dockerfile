FROM python:3.7

ADD test2.py /
EXPOSE 4555

RUN pip install pystrich
RUN pip install flask
RUN pip install torch
RUN pip install torchvision
RUN pip install opencv-python
RUN pip install Pillow

CMD [ "python", "./test2.py" ]