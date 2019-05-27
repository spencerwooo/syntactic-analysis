#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def parseInputString(input, grammar, terminalSymbols, nonTerminalSymbols, analyzeTable):
  """
  Demo 性质的函数，分析一个输入字符串，比如 "i+i*i"
  PARAM <input>: inputString = 'i+i*i'
  """
  print('[Start parsing]:', input)

  # 初始化
  parseStack = ['#']
  grammarTop = list(grammar.keys())[0]
  parseStack.append(grammarTop)

  input = input + '#'
  # 开始分析
  i = 0
  print('{0: >30}'.format(str(parseStack)), input[i])
  while True:
    if parseStack[-1] in terminalSymbols and input[i] in terminalSymbols:
      if parseStack[-1] == '#' and input[i] == '#':
        print('[INFO] Parse Success!')
        break
      elif parseStack[-1] == input[i] and input[i] != '#':
        parseStack.pop()
        i = i + 1
        print('{0: >30}'.format(str(parseStack)), '-')
      else:
        print('[ERROR] Parse Failed!')
        break
    elif parseStack[-1] in nonTerminalSymbols:
      row = analyzeTable[parseStack[-1]]
      if input[i] in row.keys():
        parseStack.pop()
        for item in reversed(row[input[i]]):
          if item != 'ε':
            parseStack.append(item)
      else:
        print('[ERROR] Parse failed.')
        break
      print('{0: >30}'.format(str(parseStack)), input[i], row[input[i]])


def createParserTree(inputToken, grammar, terminalSymbols, nonTerminalSymbols, analyzeTable):
  """
  开始了！分析树！
  """
  parseStack = ['#']
  grammarTop = list(grammar.keys())[0]
  parseStack.append(grammarTop)

  i = 0
  print(parseStack, inputToken[i][1].text)
  while True:
    if parseStack[-1] in terminalSymbols and (inputToken[i][1].text in terminalSymbols or inputToken[i][2].text in terminalSymbols):
      if parseStack[-1] == '#' and inputToken[i][1].text == '#':
        print('[INFO] Parse success!')
        break
      elif (parseStack[-1] == inputToken[i][1].text or parseStack[-1] == inputToken[i][2].text) and inputToken[i][1].text != '#':
        parseStack.pop()
        i = i + 1
        print(parseStack, inputToken[i][1].text)
      else:
        print('[ERROR] Parse failed!')
        break

    elif parseStack[-1] in nonTerminalSymbols:
      row = analyzeTable[parseStack[-1]]
      if inputToken[i][1].text in row.keys():
        parseStack.pop()
        for item in reversed(row[inputToken[i][1].text]):
          if item != 'ε':
            parseStack.append(item)
        print(parseStack, inputToken[i][1].text, row[inputToken[i][1].text])
      elif inputToken[i][2].text in row.keys():
        parseStack.pop()
        for item in reversed(row[inputToken[i][2].text]):
          if item != 'ε':
            parseStack.append(item)
        print(parseStack, inputToken[i][1].text, row[inputToken[i][2].text])
      else:
        print('[ERROR] Parse failed!')
        break
