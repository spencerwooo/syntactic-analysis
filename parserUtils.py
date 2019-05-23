#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections


def readGrammar(filePath):
  """
  从文件中读文法列表
  """
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


def differentiateSymbols(grammar):
  """
  区分终结符与非终结符
  """
  # 终结符
  terminalSymbols = []
  # 非终结符
  nonTerminalSymbols = []
  # 中间处理符号
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


def getFIRST(grammar, terminalSymbols, nonTerminalSymbols):
  """
  获取文法的 FIRST 集合
  """
  firstSet = collections.defaultdict(list)
  allSymbols = terminalSymbols + nonTerminalSymbols

  for eachGrammar in grammar:
    for eachPostGrammarItem in grammar[eachGrammar]:
      if len(eachPostGrammarItem) == 1 and eachPostGrammarItem[0] in terminalSymbols:
        firstSet[eachGrammar] = eachPostGrammarItem

  return firstSet


def getFOLLOW(grammar, terminalSymbols, nonTerminalSymbols):
  """
  获取文法的 FOLLOW 集合
  """
  followSet = {}

  return followSet
