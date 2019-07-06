FROM python:3.7-slim

WORKDIR /username

RUN apt-get update && touch /var/flag


COPY . /username

EXPOSE 80

ENV NAME debughw

CMD ["/bin/bash"]
CMD ["python", "hw.py"]
