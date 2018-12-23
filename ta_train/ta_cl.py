import click

from flask import Flask, g
from flask.cli import with_appcontext

from config import ta_config


@click.command('ta-cl')
@with_appcontext
def cl_command():
  """Command line training assistant."""
  click.echo('Training assistant starts running.')
  config = {}
  
  vtype = raw_input('Please input variety type [FT/st]: ')
  if not vtype:
    vtype = 'FT'
  if vtype not in ta_config.TA_CONFIG:
    click.echo('Bad variety type: %s, not found in config' % vtype)
    return
  vconfig= ta_config.TA_CONFIG[vtype]
  config['vtype'] = vtype
  
  variety = raw_input('Please input variety code: ')
  if variety not in vconfig:
    click.echo('Bad variety:%s, not found in config' % variety)
    return
  config['variety'] = variety
  
  click.echo(config)
  

def init_app(app):
  app.cli.add_command(cl_command)