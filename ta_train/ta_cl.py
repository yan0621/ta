import click
import pprint

from flask import Flask, g
from flask.cli import with_appcontext

from config import ta_config
from simulated import controller as st_controller


@click.command('ta-cl')
@with_appcontext
def cl_command():
  """Command line training assistant."""
  vtype = raw_input('Please input variety type [FT/st]: ')
  if not vtype:
    vtype = 'FT'
  if vtype not in ta_config.TA_CONFIG:
    click.echo('Bad variety type: %s, not found in config' % vtype)
    return
  vconfig= ta_config.TA_CONFIG[vtype]
  
  variety = raw_input('Please input variety code: ')
  if variety not in vconfig:
    click.echo('Bad variety:%s, not found in config' % variety)
    return
  
  pp = pprint.PrettyPrinter()
  click.echo('Training assistant starts running.')
  controller = st_controller.STController(vconfig[variety])
  pp.pprint(controller.get_statistics())

  while True:
    # check burst
    if controller.get_statistics().get('profit_rate') <= -1:
      click.echo('You burst!')
      break
    cmd = raw_input('Input next action:')
    if not cmd:
      continue
    try:
      if cmd == 'exit' or cmd == 'e':
        pp.pprint(controller.get_statistics())
        break
      elif cmd == 'show' or cmd == 'sh':
        pp.pprint(controller.get_statistics())
      elif cmd.startswith('risk') or cmd.startswith('r '):
        # risk [percent] [price] [sl]
        tokens = cmd.split(' ')
        if len(tokens) != 4:
          click.echo('usage: risk [percent] [price] [sl]')
          continue
        click.echo(controller.get_risk_capacity(float(tokens[1]), abs(float(tokens[2]) - float(tokens[3]))))
      elif cmd.startswith('long') or cmd.startswith('l '):
        # long [price] [volume] [sl]
        tokens = cmd.split(' ')
        if len(tokens) != 4:
          click.echo('usage: long [price] [volume] [sl]')
          continue
        res = controller.long(
            price=float(tokens[1]),
            hands=int(tokens[2]),
            sl=float(tokens[3]))
        if not res:
          click.echo('Failed to create long position.')
      elif cmd.startswith('short') or cmd.startswith('s '):
        # short [price] [volume] [sl]
        tokens = cmd.split(' ')
        if len(tokens) != 4:
          click.echo('usage: short [price] [volume] [sl]')
          continue
        res = controller.short(
            price=float(tokens[1]),
            hands=int(tokens[2]),
            sl=float(tokens[3]))
        if not res:
          click.echo('Failed to create short position')
      elif cmd.startswith('update') or cmd.startswith('u '):
        # update [price] ...
        tokens = cmd.split(' ')
        if len(tokens) != 2:
          click.echo('usage: update [price] ...')
          continue
        for i in range(1, len(tokens)):
          pp.pprint(controller.update(float(tokens[i])))
      elif cmd.startswith('sl'):
        # sl [value] [postion_id]
        tokens = cmd.split(' ')
        if len(tokens) not in (2, 3):
          click.echo('usage: sl [value] [position_id]')
          continue
        if len(tokens) == 2:
          controller.set_sl(float(tokens[1]))
        elif len(tokens) == 3:
          controller,set_sl(float(tokens[1]), int(tokens[2]))
      else:
        click.echo('Unknown action!')
    except Exception as e:
      print(str(e))
      continue


def init_app(app):
  app.cli.add_command(cl_command)