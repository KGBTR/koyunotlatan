#!/usr/bin/python3
#-*- encoding:utf-8 -*-

from argparse import ArgumentParser
import logging
from typing import TYPE_CHECKING

from praw import Reddit
from praw.models import Message, Comment

from koyunkirpan.runner import Runner
import koyunkirpan.logger
from koyunkirpan.constants import (
  NO_REPLY,
  BOT_CLIENT_ID,
  BOT_CLIENT_SECRET,
  BOT_USERNAME,
  BOT_PASSWORD,
)

logger = logging.getLogger('koyunkirpan')
logger.setLevel(logging.INFO)

def main():
    try:
      if (BOT_CLIENT_ID and BOT_CLIENT_SECRET and BOT_USERNAME and BOT_PASSWORD):
        reddit = Reddit(
          client_id=BOT_CLIENT_ID,
          client_secret=BOT_CLIENT_SECRET,
          username=BOT_USERNAME,
          password=BOT_PASSWORD,
          user_agent=False,
        )
      else:
        reddit = Reddit(
          "koyunkirpan",
          user_agent=False,
          config_interpolation="basic",
        )

      logger.info(f'Started in "{"NO_REPLY" if NO_REPLY else "REPLY"}" mode as u/{reddit.user.me()}')
    except Exception:
      logger.exception('Error occured while login reddit\n')

    runner = Runner(reddit)

    argparser = ArgumentParser(description='Ak koyun ak bacağından, kara koyun kara bacağından asılır.')

    argparser.add_argument('-i', '--id', type=str, dest="post_id",  help='Post/Submission ID')
    argparser.add_argument('-u', '--url', type=str, dest="post_url", help='Post/Submission URL')

    args = argparser.parse_args()

    try:
      if args.post_url is not None:
        runner.do_comment(post_id=args.post_id)
      elif args.post_id is not None:
        runner.do_comment(post_url=args.post_url)
      else:
          # Select a Random Submission and Comment
          runner.do_comment(None)

      exit(1)
    except Exception:
      logger.exception('Exception occurred while do comment\n')

    # Replying to Comment Replies
    for message in reddit.inbox.unread(limit=10):
      if TYPE_CHECKING:
        message: Message | Comment

      try:
        if message.type == "comment_reply":
          runner.reply_on_comment(message.id)
        message.mark_read()
      except Exception:
        logger.exception('Exception occurred while reply to inbox comment\n')

if __name__ == '__main__':
  main()
