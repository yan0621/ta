import logging

from flask import current_app

app = current_app

class Price(object):
  def __init__(self):
    app.logger.info('Price object created!')