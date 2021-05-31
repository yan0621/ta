from st_assistant.data.stock_pos import StockLevel
from st_assistant.data.stock_pos import StockPos


class StockPosLoader(object):

  DEFAULT_POS_FILE = '/Users/yanpan/Documents/stock_pos.txt'

  def __init__(self, pos_file=None):
    self._pos_file = pos_file if pos_file else self.DEFAULT_POS_FILE

  def load(self):
    f = open(self._pos_file)
    line_count = 0
    stock_pos_list = []
    while True:
      line = f.readline()
      if line and line.strip():
        if line_count == 0:
          self._parse_header(line)
        else:
          pos = StockPos()
          self._parse_line(pos, line)
          stock_pos_list.append(pos)
        line_count += 1
      else:
        break

    f.close()
    return stock_pos_list

  def _parse_header(self, header_line):
    HEADER_PARSER_DICT = {
      'level': self._parse_level,
      'code': self._parse_code,
      'name': self._parse_name,
      'rv': self._parse_rv,
      'pos': self._parse_pos,
      'pos_v': self._parse_pos_value
    }

    headers = header_line.split('\t')
    self._header_parser_funcs = []
    for header in headers:
      if header.lower().strip() not in HEADER_PARSER_DICT:
        raise Exception('Bad header found %s' % header)
      else:
        self._header_parser_funcs.append(HEADER_PARSER_DICT[header.lower().strip()])

  def _parse_line(self, stock_pos, line):
    tokens = line.split('\t')
    for i in range(len(tokens)):
      self._header_parser_funcs[i](stock_pos, tokens[i].strip())

  def _parse_level(self, stock_pos, input):
    for stockLevelValue in StockLevel:
      if input == stockLevelValue.name:
        stock_pos.level = stockLevelValue
        return
    raise Exception("Bad stock level value %s" % input)

  def _parse_code(self, stock_pos, input):
    stock_pos.stock_id = input

  def _parse_name(self, stock_pos, input):
    stock_pos.name = input

  def _parse_rv(self, stock_pos, input):
    if input == '?':
      return
    tokens = input.split(' ')
    stock_pos.rv = int(tokens[0])

  def _parse_pos(self, stock_pos, input):
    stock_pos.pos = int(input)

  def _parse_pos_value(self, stock_pos, input):
    stock_pos.pos_value = int(input)