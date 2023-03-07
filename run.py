import os


import argparse
import os


def run_server():
    cmd = 'python manage.py runserver 0.0.0.0:80'
    os.system(cmd)


def run_celery():
    cmd = 'celery -A core worker -l info --pool solo'
    os.system(cmd)

def run_celery_beat():
    cmd = "celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
    os.system(cmd)

def run_bot():
    cmd = 'python bot/main.py'
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser(description='ReklamaBot')
    parser.add_argument('-s', '--server', help='server',
                        action='store_true')
    parser.add_argument('-c', '--celery', help='celery',
                        action='store_true')
    parser.add_argument('-b', '--bot', help='bot',
                        action='store_true')
    parser.add_argument('-cb', '--celerybeat', help='celery-beat',
                        action='store_true')

    args = parser.parse_args()
    if args.server:
        run_server()

    if args.celery:
        run_celery()
    
    if args.celerybeat:
        run_celery_beat()

    if args.bot:
        run_bot()


if __name__ == "__main__":
    main()