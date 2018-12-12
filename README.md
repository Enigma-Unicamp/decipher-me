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

First of all, clone the repo, create and activate a Python virtual environment:

```shell
$ git clone https://gitlab.com/enigmaster/decipher-me.git
$ cd decipher-me/
$ python3 -m venv env
$ source env/bin/activate
```

Then, install Django:

```shell
$ pip3 install django
$ pip3 install django-generate-secret-key
```

Now, let's get a fresh `SECRET_KEY` for your instance.

```shell
$ cd decipher/
$ ./manage.py generate_secret_key --replace
```

**Warning!** Don't replace your `SECRET_KEY` once the app is deployed, it can
cause usability issues.

Create the database and you are ready to run:

```shell
$ ./manage.py migrate
$ ./manage.py runserver 0:8000
```

## Using

TODO

## Contributing

TODO

## License

This project is licensed under the 
[GNU General Public License v3.0](https://gitlab.com/enigmaster/decipher-me/blob/master/LICENSE)

Sphinx image is licensed under 
[Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/) by
[SVG Repo](https://www.svgrepo.com)
