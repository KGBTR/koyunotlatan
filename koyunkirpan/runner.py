from __future__ import unicode_literals
import json
import os
from pathlib import Path
import secrets
from typing import TYPE_CHECKING, Iterator, List, Optional, Dict, Any
import warnings
import logging

import numpy as np
from praw import Reddit
from praw.models import Subreddit, Submission, Comment
from psaw import PushshiftAPI

from koyunkirpan.binary_comb import BinaryComb
from koyunkirpan.constants import NO_REPLY
import koyunkirpan.logger

warnings.filterwarnings('ignore')

logger = logging.getLogger('koyunkirpan')

class Runner:
  reddit             : Reddit
  submissions        : List[Submission]
  comments           : List[Comment]
  commented_on       : List[str]
  flairs             : List[str]
  keywords           : List[str]
  replies            : Dict[str, Any]
  subreddit          : Subreddit
  forbidden_comments : List[str | None]
  path               : Path
  search_limit       : int
  post_limit         : int
  alike_value        : float
  reply_comment      : str

  def __init__(self, reddit: Reddit):
    self.reddit             = reddit
    self.submissions        = []
    self.comments           = []
    self.commented_on       = []
    self.flairs             = []
    self.keywords           = []
    self.replies            = {}
    self.subreddit          = reddit.subreddit('KGBTR')
    self.forbidden_comments = ['[removed]', '[deleted]', '', ' ', None]
    self.path               = Path(__file__).parent
    self.search_limit       = 20
    self.post_limit         = 50
    self.alike_value        = 1.35
    self.reply_comment      = """
{comment}

^(If you have **any comments or suggestions** about the bot, please mention **Asim-Abi** by replying to **the bot comment**)

^(This comment was automatically picked by **the koyunkırpan algorithm**)"""
    self.load_replies()
    self.load_commented_on()

  def load_replies(self):
    with open(self.path.joinpath('data/replies.json'), 'r') as f:
      self.replies = json.load(f)
    if len(self.replies.keys()) == 0:
      self.load_flairs()

  def load_commented_on(self):
    with open(self.path.joinpath('data/savedata.json'), 'r') as f:
      self.commented_on = json.load(f)

  def on_comment(self, post_id):
    if post_id:
      self.commented_on['ids'].append(post_id)
    with open(self.path.joinpath('data/savedata.json'), 'w') as json_file:
      json.dump(self.commented_on, json_file, indent=4, sort_keys=True)

  def load_flairs(self):
    for flair in self.subreddit.flair.link_templates:
      if flair['id'] not in self.flairs:
        self.replies[flair['id']] = {'text':flair['text'], 'replies':[]}
    with open(self.path.joinpath('data/replies.json'), 'w') as json_file:
      json.dump(self.replies, json_file, indent=4, sort_keys=True)

  def check_posts(self):
    for submission in self.subreddit.new(limit=self.post_limit):
      if submission not in self.submissions and submission.id not in self.commented_on['ids'] and submission.link_flair_text != 'Ciddi :snoo_disapproval:':
        self.submissions.append(submission)
    for submission in self.subreddit.hot(limit=self.post_limit):
      if submission not in self.submissions and submission.id not in self.commented_on['ids'] and submission.link_flair_text != 'Ciddi :snoo_disapproval:':
        self.submissions.append(submission)
    logger.info(f'Collected: {len(self.submissions)} posts')

  def select_post(self) -> Submission | None:
    for i in range(0, 5):
      p = self.submissions[secrets.randbelow(len(self.submissions))]
      if len(p.comments) < 5:
        continue
      else:
        return p
    return None

  def post_keywords(self, p: Submission) -> None:
    for word in p.title.split(' '):
      if word not in self.keywords:
        self.keywords.append(word.lower())
    p.comment_sort = 'best'
    for top_level_comment in p.comments[0:5]:
      if top_level_comment.body not in self.forbidden_comments:
        for word in top_level_comment.body.splitlines()[0].split(' '):
          if word not in self.keywords:
            self.keywords.append(word.lower())
    # Limit Keywors
    self.keywords = self.keywords[0:20]
    logger.debug('KEYWORDS:', self.keywords)

  def find_similar(self, title: str, nsfw: bool) -> Iterator[Submission]:
    try:
      keywords = title.split(' ')
      return self.subreddit.search('%s nsfw:%s' %(' OR '.join(keywords), 'yes' if nsfw else 'no'), limit=self.search_limit)
    except Exception:
      logger.exception('Error occured while find similar\n')
      return None

  def comment_fit(self, search_data: Iterator[Submission], id: str):
    try:
      comments: List[str] = []
      for p in search_data:
        if p.id == id:
          continue
        p.comment_sort = 'best'
        for top_level_comment in p.comments[0:5]:
          if TYPE_CHECKING:
            top_level_comment: Comment
          top_level_comment_body = top_level_comment.body.splitlines()[0].lower()
          if top_level_comment_body not in self.forbidden_comments and len(top_level_comment_body) > 0:
            self.comments.append(top_level_comment)
      logger.info('Collected: %s comments' %(len(self.comments)))
    except Exception:
      logger.exception('Error occured while comment fitting\n')

  def compare_sentences(self, s1: str | List[str], s2: str | List[str]):
    # Take sentences and split into words
    if type(s1) == list:
      words_1 = s1
    else:
      words_1 = s1.split(' ')
    if type(s2) == list:
      words_2 = s2
    else:
      words_2 = s2.split(' ')
    # Select the sentence with fewer words as words_1
    if len(words_1) >= len(words_2):
      words_3 = words_1
      words_1 = words_2
      words_2 = words_3
    w_ij = np.zeros((len(words_1),len(words_2)), float)
    e_ij = np.zeros((len(words_1),len(words_2)), float)
    for i in range(0, len(words_1)):
      for j in range(0, len(words_2)):
        # compare word lengths
        w_ij[i][j] += abs(len(words_1[i]) - len(words_2[j]))
        # compare word similarities
        word_1 = words_1[i]
        word_2 = words_2[j]
        if len(word_1) >= len(word_2):
          word_3 = word_1
          word_1 = word_2
          word_2 = word_3
        for letter in range(0, len(word_1)):
          if word_1[letter] != word_2[letter]:
            e_ij[i][j] += 1
    total   = np.add(w_ij, e_ij)
    result  = 0
    results = []
    alpha   = len(words_2)/len(words_1)

    # ZERO CHECK
    while np.count_nonzero(total==0) > 0:
      for i in range(0, len(words_1)):
        for j in range(0, len(words_2)):
          if total[i][j] == 0:
            results.append((words_1[i], words_2[j], total[i][j]))
            result += total[i][j]
            total[i] = np.Inf
            total[0][j] = np.Inf

    # REST CHECK
    for i in range(0, len(words_1)):
      if total[i][0] == np.Inf:
          continue
      row_min = 0
      for j in range(0, len(words_2)):
        if total[i][j] < total[i][row_min]:
          row_min = j
      results.append((words_1[i], words_2[row_min], total[i][row_min]))
      result += total[i][row_min]
      total[i] = np.Inf
      total[0][j] = np.Inf
    return result + abs(len(s1)-len(s2))

  def find_best_fit(self, post: Submission) -> Comment | None:
    try:
      if len(self.comments) > 0:
        z = np.full((len(self.comments)), np.inf)
        for i in range(0, len(self.comments)):
          z[i] = self.compare_sentences(
            self.comments[i].body.splitlines()[0].lower(),
            self.keywords
          )

        row_mins = []
        row_min = 0
        for i in range(0, len(self.comments)):
          if z[i] < z[row_min]:
            row_min = i

        for i in range(0, len(self.comments)):
          if z[i] == z[row_min] or z[i] <= round(z[row_min]*self.alike_value):
            row_mins.append(i)

        row_min = row_mins[secrets.randbelow(len(row_mins))]
        comment = self.comments[row_min]
        logger.info(f'Best fit found as "{comment.body}" at https://reddit.com{comment.permalink}')

        return comment
      else:
        if post.link_flair_text != None:
          if (
            post.link_flair_template_id in self.replies and
            not self.replies[post.link_flair_template_id] and
            'replies' in self.replies[post.link_flair_template_id] and
            self.replies[post.link_flair_template_id]['replies'] and
            len(self.replies[post.link_flair_template_id]['replies']) > 0
          ):
            comment = self.replies[post.link_flair_template_id]['replies'][secrets.randbelow(len(self.replies[post.link_flair_template_id]['replies']))]
            logger.warn(f'Best fit in predefined replies: {comment}')

            return comment
          else:
            logger.warn(f'No fits for the post titled "{post.title}" at https://reddit.com{post.permalink} :(')

            return None
    except Exception:
      logger.exception('Error occured while finding best fit\n')

  def reply_post(self, post: Submission, comment: Comment):
    if comment and isinstance(comment, Comment) and comment.body:
      logger.info(f'"{comment.body}" will be replied')

      if not NO_REPLY:
        reply_cmt = post.reply(self.reply_comment.format(comment=comment.body))
        self.on_comment(post.id)
        logger.info(f'Replied as "{comment.body}" at https://reddit.com{reply_cmt.permalink}')

  def do_comment(self, post_id: Optional[str]=None, post_url: Optional[str]=None):
    self.check_posts()

    if post_id:
      post = self.reddit.submission(id=post_id)
    elif post_url:
      post = self.reddit.submission(url=post_url)
    else:
      post = self.select_post()

    if not post:
      logger.warn('Couldn\'t find a suitable post :(')
      return
    
    logger.info(f'Selected post titled "{post.title}" at https://reddit.com{post.permalink}')
    self.post_keywords(post)

    logger.info('Searching similar posts...')
    similars = self.find_similar(post.title, post.over_18)
    if similars:
      self.comment_fit(similars, post.id)

    cmt = self.find_best_fit(post)

    self.reply_post(post, cmt)

  def reply_on_comment(self, id: str):
    # Function to Find Possible Replies To a Comment
    api                       = PushshiftAPI(self.reddit)
    original_comment: Comment = self.reddit.comment(id)

    all_comments              = []
    comments                  = []
    keywords: list[str]       = original_comment.body.split()
    bincomb                   = BinaryComb(keywords)
    searches                  = bincomb.get_combinations()

    logger.info("Comment:", original_comment.body)
    logger.info("Searches:", len(searches))

    #SEARCHING AND COLLECTING COMMENTS
    for search in searches:
      logger.info("Starting search %s:" %(searches.index(search)+1))
      comments.append([])

      gen   = api.search_comments(q=search, subreddit='KGBTR')
      cache = []

      for comment in gen:
        if len(cache) > 500:
          break
        if comment.body in self.forbidden_comments:
          continue
        if len(comment.body.split()) >= len(keywords)*3:
          continue
        if comment.id == original_comment.id:
          continue
        if comment not in all_comments:
          cache.append(comment)

      comments[searches.index(search)] += cache
      all_comments += cache
      if len(cache) > 2:
        break

    logger.debug("\nENDED.")

    for result in comments:
      logger.debug("Length:", len(result))
      c = None
      if len(result) > 0:
        tries = 0
        while True:
          if len(result) == 0:
            break
          c = result[secrets.randbelow(len(result))]
          c.refresh()
          if len(c.replies) >= 1:
            break
          else:
            result.remove(c)
            c = None
      if c:
        break

    if c:
      logger.debug(f'COMMENT URL: https://www.reddit.com{c.permalink}')
      logger.debug(f'COMMENT REPLIES: {len(c.replies)}')

      to_comment = []

      for reply in c.replies:
        if reply.body not in self.forbidden_comments:
          to_comment.append(reply.body)

      logger.debug(f'"{to_comment[secrets.randbelow(len(to_comment))]}" will be replied')

      if not NO_REPLY:
        reply_cmt = original_comment.reply(
          self.reply_comment.format(
            comment=to_comment[secrets.randbelow(len(to_comment))]
          )
        )
        logger.info(f'Replied as "{to_comment[secrets.randbelow(len(to_comment))]}" at https://reddit.com{reply_cmt.permalink}')
    else:
      logger.warn("No comment found :(")