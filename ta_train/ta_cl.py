import click
import pprint

from flask import Flask, g
from flask.cli import with_appcontext

from auto import auto_main
from config import ta_config
from simulated import controller as st_controller


@click.command('ta-auto')
@with_appcontext
def auto_command():
  """Command line auto training."""
  click.echo('Auto training starts running.')
  auto_main.run(['tlt', 'spy'], '2016-05-01', '2019-05-01', 'day', trade_strategy='balance', agent_type='ST')
  #auto_main.run(['cf', 'ma', 'sr', 'v', 'c', 'a', 'y', 'ag'], '2015-01-01', '2019-05-01', 'day')
  #auto_main.run(['a', 'y'], '2016-01-01', '2016-05-01', 'day')


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
      elif cmd.startswith('set'):
        tokens = cmd.split(' ')
        # set risk [risk]
        if len(tokens) == 3 and tokens[1] == 'risk':
          controller.set_default_risk(float(tokens[2]))
        continue
      elif cmd.startswith('risk') or cmd.startswith('r '):
        # risk [percent] [price] [sl]
        tokens = cmd.split(' ')
        if len(tokens) != 4:
          click.echo('usage: risk [percent] [price] [sl]')
          continue
        click.echo(controller.get_risk_capacity(float(tokens[1]), abs(float(tokens[2]) - float(tokens[3]))))
      elif cmd.startswith('long') or cmd.startswith('l '):
        # long [volume] [price] [sl]
        # long [price] [sl]
        tokens = cmd.split(' ')
        if len(tokens) != 4:
          click.echo('usage: long [price] [volume] [sl]')
          continue
        res = controller.long(
            price=float(tokens[2]),
            hands=int(tokens[1]),
            sl=float(tokens[3]))
        if not res:
          click.echo('Failed to create long position.')
      elif cmd.startswith('lr '):
        tokens = cmd.split(' ')
        # lr [risk] [price] [sl]
        if len(tokens) == 4:
          res = controller.long_by_risk(
              risk=float(tokens[1]),
              price=float(tokens[2]),
              sl=float(tokens[3])
          )
          if not res:
            click.echo('Failed to create long position by risk.')
        # lr [price] [sl]
        elif len(tokens) == 3:
          res = controller.long_by_default_risk(
              price=float(tokens[1]),
              sl=float(tokens[2])
          )
          if not res:
            click.echo('Failed to create long position by default risk.')
        else:
          click.echo('usage: risk <risk> [price] [sl]')
      elif cmd.startswith('short') or cmd.startswith('s '):
        # short [volume] [price] [sl]
        tokens = cmd.split(' ')
        if len(tokens) != 4:
          click.echo('usage: short [price] [volume] [sl]')
          continue
        res = controller.short(
            price=float(tokens[2]),
            hands=int(tokens[1]),
            sl=float(tokens[3])
        )
        if not res:
          click.echo('Failed to create short position')
      elif cmd.startswith('sr '):
        tokens = cmd.split(' ')
        # sr [risk] [price] [sl]
        if len(tokens) == 4:
          res = controller.short_by_risk(
              risk=float(tokens[1]),
              price=float(tokens[2]),
              sl=float(tokens[3])
          )
          if not res:
            click.echo('Failed to create short position by risk.')
        # sr [price] [sl]
        elif len(tokens) == 3:
          res = controller.short_by_default_risk(
              price=float(tokens[1]),
              sl=float(tokens[2])
          )
          if not res:
            click.echo('Failed to create short position by defualt risk.')
        else:
          click.echo('Usage: sr <risk> [price] [sl]')
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
          controller.set_sl(float(tokens[1]), int(tokens[2]))
      elif cmd.startswith('close'):
        # close [position_id] [price] [hands=0]
        tokens = cmd.split(' ')
        if len(tokens) not in (3, 4):
          click.echo('usage: close [position_id] [price] [hands=0]')
        if len(tokens) == 3:
          if not controller.close(int(tokens[1]), float(tokens[2])):
            click.echo('Failed to close position %s' % tokens[1])
        else:
          if not controller.close(int(tokens[1]), float(tokens[2]), int(tokens[3])):
            click.echo('Failed to close position %s' % tokens[1])
      else:
        click.echo('Unknown action!')
    except Exception as e:
      print(str(e))
      continue


def init_app(app):
  app.cli.add_command(cl_command)
  app.cli.add_command(auto_command)