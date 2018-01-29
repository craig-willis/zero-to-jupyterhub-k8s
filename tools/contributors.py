#!/usr/bin/env python3
"""
Script to list *all* contributors to a given set of repos,
between a set of dates.
"""

import os
from github import Github
import dateutil
from dateutil.parser import parse

gh = Github(login_or_token=os.environ['GITHUB_API_TOKEN'])


def get_all_contributors(repo, from_date, to_date):
    def include(date):
        return from_date < date.replace(tzinfo=dateutil.tz.tzlocal()) < to_date
    repo = gh.get_repo(repo)
    issues = repo.get_issues()
    pulls = repo.get_pulls()

    users = set()


    for i in issues:
        if include(i.created_at):
            users.add((i.user.login, i.user.name))
        for c in i.get_comments():
            if include(c.created_at):
                users.add((c.user.login, c.user.name))


    for p in pulls:
        if include(p.created_at):
            users.add((p.user.login, p.user.name))

        for c in p.get_comments():
            if include(c.created_at):
                users.add((c.user.login, c.user.name))

        for rc in p.get_review_comments():
            if include(rc.created_at):
                users.add((rc.user.login, rc.user.name))
    return users


if __name__ == '__main__':
    users = get_all_contributors('jupyterhub/zero-to-jupyterhub', parse('Wed Dec 13 10:23:01 2017 -0800'), parse('Mon Jan 29 13:37:51 2018 -0800'))
    users |= get_all_contributors('jupyterhub/kubespawner', parse('Tue Nov 28 13:28:24 2017 -0800'), parse('Wed Jan 24 13:31:03 2018 +0100'))


    for login, name in sorted(users, key=lambda u: u[1].casefold() if u[1] else u[0].casefold()):
        if name is None:
            name = login
        print("[{name}](https://github.com/{login})".format(name=name, login=login))