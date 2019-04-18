# Contributing

First of all, thank you for contributing to our project :)

There are several ways to do so:

- [Reporting a bug or requesting a feature](https://gitlab.com/enigmaster/decipher-me/issues/new)
- [Solving an existent issue](https://gitlab.com/enigmaster/decipher-me/issues)
(issues marked with "Good first issue" are a good starting point).
- Enhancing our code quality, adding unit test or improving our documentation.

Please, read all the
[ReadMe](https://gitlab.com/enigmaster/decipher-me/blob/master/README.md)
before starting, there you can find important and useful information about the
project and also how to get started if the project setup.

## Coding requirements

This project isn't really complex, but it will help you to have a basic
knowledge in Python and Git. Also, make sure you have an account in
[gitlab.com](https://gitlab.com/users/sign_in)
and be respectful in your communication and interaction with other contributors.

### Django

[Django](https://www.djangoproject.com/) is a Python web framework, focused on
simplicity, security and scalability. If you are new to Django, we recommend
this two tutorials:

- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Django Project Tutorial](https://www.djangoproject.com/start/)

### Git

If you are new to Git or open source development, this is the simplified
workflow:

- Fork the [repository](https://gitlab.com/enigmaster/decipher-me/forks/new)
(you need to be logged to do that)
- Make your modification
- Test your code and make sure it passes tests
- Commit then and push to your repository
- Check the result of the Continuous Integration pipeline
- Open a merge request from your repository to our master branch
- Wait to receive a feedback

Also, is good to open an issue so other developers can know on what you are
working on.

More information:
- [Git Guide](http://rogerdudler.github.io/git-guide/): most common commands
with examples
- [GitHub introduction](https://guides.github.com/introduction/git-handbook/):
you can have a look on how Git works and what are the main concepts behind it,
followed by the main commands
- A good guide on how to
[write a good commit message](https://chris.beams.io/posts/git-commit/)

Get in touch with us if you have a question and don't be afraid of the open
source world!


### Continuous integration

Our repository have a CI pipeline to ensure every patch is working properly. If
you have forked our GitLab project, it should be possible to you run the
pipeline on your repository (check the Pipeline section on CI/CD menu).

Run this on the repository to check the results of tests on your code (make
sure you have prepared your environment as described on README):

```shell
$ ./manage.py check
...
$ pylint --load-plugins pylint_django --rcfile=.pylint.cfg decipher/challenge/
...
$ pylint --load-plugins pylint_django --rcfile=.pylint.cfg decipher/scripts/

```

## About us and contact

This project is maintained by Enigma, a study group about privacy,
cybersecurity and cryptography, based on Unicamp - Brazil. You
can get in touch with us in our [Telegram channel](https://t.me/enigmaunicamp).
