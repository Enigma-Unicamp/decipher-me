# Decipher Me

<p align="center">
        <img src=img/sphinx_logo.png height=100px>
</p>

Decipher Me is a free and open web framework to host Jeopardy-style Capture The
Flag contests.

## What is a _Capture The Flag_?

CTF is a information security and hacking competition. Among the common types,
there is the Jeopardy style, where teams must solve tasks in a
range of categories, earning points for different tasks. The categories
mostly include Web Exploitation, Cryptography, Reverse Engineering and
Forensic. More info [here](https://ctftime.org/ctf-wtf/).

## Installing

### Requirements

- Python 3.x

### Setup

First of all, clone the repo and create a Python virtual environment. This way
you won't have to install the dependencies in your system, only under the repo
folder.

```shell
$ git clone https://gitlab.com/enigmaster/decipher-me.git
$ cd decipher-me/
$ python3 -m venv env
```

Now, enter the Python virtual environment.

```shell
$ source env/bin/activate
```

Next, upgrade pip

```shell
$ pip3 install --upgrade pip
```

Then, install [Django](https://www.djangoproject.com/), a Python framework to
create and manage a webserver.

```shell
$ pip3 install django
```

Now, we need to create a fresh `SECRET_KEY` for your instance, which will be
saved in the file `decipher/secretkey.txt`. This key will be used by Django to
perform a
[lot ot stuff](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
Also, `secret.key` is covered by `.gitignore`, so you
won't have to worry about accidentally pushing your key to your own Git
repository.

```shell
$ python3 scripts/generate_secret_key.py decipher/secretkey.txt
```

**Warning!** Don't replace your `SECRET_KEY` once the app is deployed, it can
cause usability issues.

Create the database and you are ready to run:

```shell
$ cd decipher/
$ ./manage.py migrate
$ ./manage.py runserver 0:8000
```

## Using

To add your own challenges, go to `decipher/challenge/static/challenges_files`
and create folders to each one of the challenges. We have a place holder called
`Baby Steps` to examplify it. Inside the folder, you must create a file named
`settings.csv`. Inside this file, you must add the following information
(respecting this order):

```
content_type,challenge_name,challenge_flag,challenge_description
```

* `content_type` must be "download", "image", "link" or "page"
* `challenge_name` is the name of the challenge
* `challenge_flag` is the flag and must be in the following shape: `decipher{something}`
* `challenge_description` is the challenge description

For the `Baby Steps` example, we have:

```
"download","Baby Steps","decipher{fl4g}","First challenge, named Baby Steps"
```

Inside the same folder, we also add the downloadable file. If the `content_type`
is a <b>image</b>, you should add the image file. If it's a <b>link</b>, you
should add a .txt file containing the link. Finally, if it's a <b>page</b>, you
should add the html file (and others that may be necessary).

After adding all the challenges, you must navigate to the folder
`decipher-me/decipher` and run the following command:

```
python3 manage.py shell < scripts/create_challenges.py
```


## Contributing

TODO

## License

This project is licensed under the
[GNU General Public License v3.0](https://gitlab.com/enigmaster/decipher-me/blob/master/LICENSE)

Sphinx image is licensed under
[Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/) by
[SVG Repo](https://www.svgrepo.com)
