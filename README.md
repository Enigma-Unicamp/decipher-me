# Decipher Me

<p align="center">
        <img src=img/sphinx_logo.png height=100px>
</p>

Decipher Me is a free and open web framework to host Jeopardy-style Capture The
Flag contests.

[![pipeline status](https://gitlab.com/enigmaster/decipher-me/badges/master/pipeline.svg)](https://gitlab.com/enigmaster/decipher-me/commits/master)

---

## What is a _Capture The Flag_?

CTF is a information security and hacking competition. Among the common types,
there is the Jeopardy style, where teams must solve tasks in a
range of categories, earning points for different tasks. The categories
mostly include Web Exploitation, Cryptography, Reverse Engineering and
Forensic. More info [here](https://ctftime.org/ctf-wtf/).

## Installing

### Requirements

- Python 3.x, Pip and Virtualenv

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
$ # if using bash
$ source env/bin/activate
$ # if using fish
$ . env/bin/activate.fish
```

Next, upgrade pip

```shell
$ pip3 install --upgrade pip
```

Then, install [Django](https://www.djangoproject.com/), a Python framework to
create and manage a webserver.

```shell
$ pip3 install -U -r requirements.txt
```

If you want to contribute with the project, also install those dependencies:

```shell
$ pip3 install -U -r requirements-dev.txt
```

Now, we need to create a fresh `SECRET_KEY` for your instance, which will be
saved in the file `decipher-me/decipher/secretkey.txt`. This key will be used by
Django to perform a [lot ot stuff](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
Also, `secret.key` is covered by `.gitignore`, so you won't have to worry about
accidentally pushing your key to your own Git repository.

```shell
$ cd decipher/
$ python3 scripts/generate_secret_key.py secretkey.txt
```

**Warning!** Don't replace your `SECRET_KEY` once the app is deployed, it can
cause usability issues.

## Using

### Sequential or non sequential challenges

Sequential means that the second challenge will be unlocked only after the first
one is complete. In no sequential mode, all challenges are unlocked.  By default,
we have <b>non sequential challenges</b>. If you want to change that, simply
edit `decipher-me/decipher/decipher/settings.py`, replacing
`SEQUENTIAL_CHALLENGES = False` with `SEQUENTIAL_CHALLENGES = True`, if you want
to have <b>sequential challenges</b>.

### Password recovery module

First of all, create a new Gmail user. Then, navigate to
`decipher-me/decipher/decipher/settings.py` and replace <b>EMAIL_HOST_USER</b>
and <b>EMAIL_HOST_PASSWORD</b> with your new email info. Also, you could use
another email provider, but then you'll have to change <b>EMAIL_HOST</b> and
<b>EMAIL_PORT</b>.

```
# Email settings (needed by reset password module)
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'test@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
```

**Warning!** Don't push this changes to any repository after setup the password
recovery module, because your email password is stored unencrypted.

### Adding your challenges

First of all, edit the file `scripts/settings.csv`. For each one of your
challenges, you must add a new line like this:

```
challenge_title,content_type,challenge_flag,challenge_description,challenge_points
```

* `challenge_title`: title of the challenge
* `content_type`: must be "no_files", download", "image", "link" or "page"
* `challenge_flag`: is the flag and must be in the following shape: `decipher{something}`
* `challenge_description`: challenge body text
* `challenge_points`: how many points a user receives for solving this challenge
(if you have `SEQUENTIAL_CHALLENGES = True`, please set it to "1")

**Atention!** The order of the challenges in this file is the one that will be
used.

To examplify, we have four challenges (`Baby Steps`, `Test Challenge`,
`Another Test` and `Try Me`), so our file stays like this:

```
"Baby Steps","image","decipher{f1rstfl4g}","First challenge, named Baby Steps and the flag is decipher{f1rstfl4g}","1"
"Test Challenge","link","decipher{cr4z1fl4g}","Another challenge, just to examplify and the flag is decipher{cr4z1fl4g}","1"
"Another Test","page","decipher{n3wfl4g}","Another challenge, just to examplify and the flag is decipher{n3wfl4g}","1"
"Try Me","no_files","decipher{br4ndn3w}","This challenge has no associated files and the flag is decipher{br4ndn3w}","1"
```

After that, create the folder `decipher-me/decipher/scripts/challenges_files`
and create folders with the **same titles of each one of the
challenges**. Inside this folders, we must add the content files. If the
`content_type` is a <b>image</b> or a <b>downloadable file</b>, you should just
drop it inside the folder. If it's a <b>link</b>, you should add a `.txt` file
containing the link. If it's a <b>page</b>, you should add the `.html`
file (and others that may be necessary, like `.js` files). The name of these
files doesn't matter to us, it can be whatever you want. Finally, if the
`content type` is <b>no_files</b>, just don't create the folder.

After adding all the challenges, navigate to the folder
`decipher-me/decipher` and run the following commands:


```shell
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py shell < scripts/create_challenges.py
$ ./manage.py runserver 0:8000
```

### Deploying

You will need to configure a web sever (e.g. `nginx`) to host your
**Decipher-me**. We recommend
[this](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
tutorial from Digital Ocean to deploying. You can skip the step of Postgres
since we use SQLite here.

## How to contribute

Please check [this page](https://gitlab.com/enigmaster/decipher-me/blob/master/CONTRIBUTING.md).


## License

This project is licensed under the
[GNU General Public License v3.0](https://gitlab.com/enigmaster/decipher-me/blob/master/LICENSE)

Sphinx image is licensed under
[Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/) by
[SVG Repo](https://www.svgrepo.com)
