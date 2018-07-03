from __future__ import absolute_import, unicode_literals

from celery import chain


from partials import add


if __name__ == "__main__":
    result = chain(add.s(1,2), add.s(3), add.s(4))
    result = (add.s(1,2) | add.s(3) | add.si(4,3))