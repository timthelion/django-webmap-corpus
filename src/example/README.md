Running the example app
-----------------------

Step 0: Check out and setup repo
--------------------------------

    $ git clone https://github.com/timthelion/django-webmap-corpus.git
    $ git checkout unbranded
    $ cd django-webmap-corpus

Step 2: Setup and launch postgis
--------------------------------

    $ sudo docker volume create webmap-pgdata
    $ sudo docker run -v webmap-pgdata:/var/lib/postgresql/data --hostname dpnk-postgres --name webmap-postgres -e POSTGRES_PASSWORD=foobar -e POSTGRES_USER=corpus -e PGDATA=/var/lib/postgresql/data/pgdata mdillon/postgis:9.6

Relaunching the container:

    $ docker start -a webmap-postgres

Note: By using multiple container names you can have multiple postgres containers and dbs and switch between the dbs for testing purposes. Perhaps have one db per git branch.

Step 3: Running the example webserver
-------------------------------------

In a new terminal...

    $ sudo docker run -it --rm --link webmap-postgres:postgres --name webmap-test --volume=<PATH_TO_SOURCE_DIR>/django-webmap-corpus:/webmap-v:rw --workdir=/webmap-v --entrypoint=/bin/bash --user=1000 -p 8000:8000 timthelion/webmap-corpus

    $ # The first time you launch you need to do migrations and install static files...
    $ npm install
    $ pip3 install -r test_requirements.txt
    $ cd src/example
    $ python3 manage.py migrate
    $ python3 manage.py createsuperuser
    $ python3 manage.py collectstatic

    $ python3 manage.py runserver 0.0.0.0:8000


Setting up the server for the first time
----------------------------------------

On your first visit you should go to the URL: <http://localhost:8000/admin/>

Log in.

Create some base layers, presets, markers, and POIs.

(An example tileserver is here: https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png

Go to <http://localhost:8000/map/>
