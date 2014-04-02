'''
Usage:
    gh-bkp.py <username> <backup-dir>
'''
import os
import requests
import subprocess
from docopt import docopt


arguments = docopt(__doc__)


def get_repo_list():
    url = 'https://api.github.com/users/%s/repos' % arguments['<username>']
    r = requests.get(url)
    repos = []
    for i in r.json():
        single_repo = []
        single_repo.append(i['name'])
        single_repo.append(i['clone_url'])
        repos.append(single_repo)

    return repos


def pull_or_clone(name, url):
    repo_name = name
    backup_dir = os.path.abspath(arguments['<backup-dir>'])

    if not os.path.exists(backup_dir + '/' + repo_name):
        proc = subprocess.Popen(['git', 'clone', url, backup_dir + '/' + name],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        proc.wait()
        with open(backup_dir + '/' + name + '.log', 'w') as f:
            for i in proc.stdout:
                f.write(i.decode('utf-8'))

        if proc.returncode == 0:
            return 'OK'
        else:
            return 'FAIL'

    elif os.path.exists(backup_dir + '/' + repo_name):
        proc = subprocess.Popen(['git', '--work-tree=' + backup_dir + '/' +
                                name, '--git-dir=' + backup_dir + '/' + name +
                                '/' + '.git', 'pull', 'origin'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        proc.wait()
        with open(backup_dir + '/' + name + '.log', 'w') as f:
            for i in proc.stdout:
                f.write(i.decode('utf-8'))

        if proc.returncode == 0:
            return 'OK'
        else:
            return 'FAIL'


def main():
    repos = get_repo_list()
    for i, j in repos:
        print('back up %s: %s' % (i, pull_or_clone(i, j)))


if __name__ == '__main__':
    main()
