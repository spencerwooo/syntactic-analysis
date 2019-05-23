#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections

# 从文件中读文法列表
def readGrammar(filePath):
  grammar = collections.defaultdict(list)
  with open(filePath, 'r') as f:
    # 按行读取，加入文法字典
    for line in f:
      preGrammar, postGrammar = line.rstrip('\n').split('->')
      preGrammar = preGrammar.rstrip(' ')
      postGrammar = postGrammar.lstrip(' ').split('|')

      for eachPostGrammar in postGrammar:
        eachPostGrammar = eachPostGrammar.strip(' ').split(' ')
        grammar[preGrammar].append(eachPostGrammar)

  return grammar

# 区分终结符与非终结符
def differentiateSymbols(grammar):
  # 终结符
  terminalSymbols = []
  # 非终结符
  nonTerminalSymbols = []

  tempSymbols = []

  for eachPreGrammar in grammar:
    if eachPreGrammar not in nonTerminalSymbols:
      nonTerminalSymbols.append(eachPreGrammar)

    postGrammarList = grammar[eachPreGrammar]
    for eachPostGrammar in postGrammarList:
      for eachPostGrammarItem in eachPostGrammar:
        tempSymbols.append(eachPostGrammarItem)

  for eachTempSymbol in tempSymbols:
    if eachTempSymbol not in nonTerminalSymbols and eachTempSymbol not in terminalSymbols:
      terminalSymbols.append(eachTempSymbol)

  terminalSymbols.append('#')
  return terminalSymbols, nonTerminalSymbols

# 获取文法的 FIRST 集合
def getFIRST(grammar, terminalSymbols, nonTerminalSymbols):
  pass

# 获取文法的 FOLLOW 集合
def getFOLLOW(grammar, terminalSymbols, nonTerminalSymbols):
  pass
