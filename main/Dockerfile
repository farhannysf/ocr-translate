FROM registry1.dso.mil/ironbank/opensource/python/python38:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "./entrypoint" ] 
