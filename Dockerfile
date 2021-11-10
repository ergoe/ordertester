FROM python:3.8.0
FROM ubuntu:20.04

WORKDIR /opt/app

COPY . /opt/app

EXPOSE 5000

RUN apt-get update
RUN apt-get --assume-yes install python3-dev
RUN apt-get update && apt-get install -y curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-9 && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/19.10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"




RUN apt-get update && apt-get install -y python3-pip python-dev python-setuptools --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
#RUN . /opt/venv/bin/activate && pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3" ]


CMD [ "./app.py" ]

#RUN python3 app.py