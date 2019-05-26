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
  print(parseStack, input[i])
  while True:
    if parseStack[-1] in terminalSymbols and input[i] in terminalSymbols:
      if parseStack[-1] == '#' and input[i] == '#':
        print('Success!')
        break
      elif parseStack[-1] == input[i] and input[i] != '#':
        parseStack.pop()
        print(parseStack, input[i])
        i = i + 1
      else:
        print('Failed!')
        break
    elif parseStack[-1] in nonTerminalSymbols:
      row = analyzeTable[parseStack[-1]]
      if input[i] in row.keys():
        parseStack.pop()
        for item in reversed(row[input[i]]):
          if item != 'ε':
            parseStack.append(item)
      else:
        print('Parse failed.')
        break
      print(parseStack, input[i])
