 from ubuntu
 RUN apt-get update
 RUN dpkg --configure -a
 RUN apt-get install -y wget
 RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
 RUN apt-get -y install software-properties-common
 RUN add-apt-repository -y ppa:deadsnakes/ppa
 RUN apt-get install -y python3.8 python3.8-distutils libpython3.8-dev
 RUN cd /tmp && wget https://bootstrap.pypa.io/get-pip.py
 RUN python3.8 /tmp/get-pip.py
 RUN ln -s /usr/bin/python3.8 /usr/bin/python
 RUN ln -s /usr/local/bin/pip3 /usr/bin/pip
 RUN  apt-get install -y postgresql-server-dev-all gcc telnet curl
 COPY Webgen/ /app/
 RUN pip3 install pipreqs 
 WORKDIR /app
 RUN pipreqs
 ENV FLASK_APP=app.py
 RUN pip3 install -r requirements.txt
 ENTRYPOINT  ["/usr/local/bin/flask","run","--host=0.0.0.0","--port=5000"]