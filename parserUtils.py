# 从文件中读文法列表
def readGrammar(filePath):
  grammar = []
  with open(filePath, 'r') as f:
    # 按行读取，加入文法列表
    for line in f:
      line = line.rstrip('\n')
      grammar.append(line)
  # 扩展文法
  grammar.insert(0, grammar[0][0] + '` -> ' + grammar[0][0])
  return grammar

# 区分终结符与非终结符
def differentiateSymbols(grammar):
  # 终结符
  terminalSymbols = []
  # 非终结符
  nonTerminalSymbols = []

  tempSymbols = []

  for eachGrammar in grammar:
    preGrammar, postGrammar = eachGrammar.split('->')
    preGrammar = preGrammar.rstrip(' ')

    if preGrammar not in nonTerminalSymbols:
      nonTerminalSymbols.append(preGrammar)

    postGrammarList = postGrammar.lstrip(' ').split(' ')
    for eachPostGrammar in postGrammarList:
      tempSymbols.append(eachPostGrammar)

  for eachTempSymbol in tempSymbols:
    if eachTempSymbol not in nonTerminalSymbols and eachTempSymbol not in terminalSymbols:
      terminalSymbols.append(eachTempSymbol)

  terminalSymbols.append('#')
  return terminalSymbols, nonTerminalSymbols

# 项目集
def getItemSet(grammar):
  itemSet = []
  for eachGrammar in grammar:
    grammarItem = eachGrammar.split(' ')

    for i in range(2, len(grammarItem) + 1):
      itemSetItem = grammarItem[:i] + ['·'] + grammarItem[i:]
      itemSet.append(itemSetItem)

  return itemSet