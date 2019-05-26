#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import copy


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


def getFIRST(firstSet, grammar, terminalSymbols, nonTerminalSymbols):
  """
  获取文法的 FIRST 集合
  参考：https://blog.csdn.net/Cielyic/article/details/82941014
  """
  for eachGrammar in grammar:
    for eachPostGrammar in grammar[eachGrammar]:
      # 例子中大写字母表示非终结符，小写字母表示终结符：
      # 1. 遇到了终结符、产生式右侧子式首符号是终结符，直接加入（比如：A -> g D B）
      if eachPostGrammar[0] in terminalSymbols:
        if not eachPostGrammar[0] in firstSet[eachGrammar]:
          firstSet[eachGrammar].append(eachPostGrammar[0])
      # 2. 产生式右侧子式首符号，递归（比如：A -> B C c）
      else:
        for eachPostGrammarItem in eachPostGrammar:
          if eachPostGrammarItem in terminalSymbols:
            if not eachPostGrammarItem in firstSet[eachGrammar]:
              firstSet[eachGrammar].append(eachPostGrammarItem)
            break
          elif 'ε' in firstSet[eachPostGrammarItem]:
            for item in firstSet[eachPostGrammarItem]:
              if not item in firstSet[eachGrammar]:
                firstSet[eachGrammar].append(item)
          else:
            break

  return firstSet


def getFOLLOW(firstSet, followSet, grammar, terminalSymbols, nonTerminalSymbols):
  """
  获取文法的 FOLLOW 集合
  """

  for eachGrammarStartSymbols in grammar.keys():
    for eachGrammar in grammar:
      for eachPostGrammar in grammar[eachGrammar]:
        if eachGrammarStartSymbols in eachPostGrammar:
            index = eachPostGrammar.index(eachGrammarStartSymbols)
            # 1. 产生式形如：S->aX，将集合 Follow(S) 中的所有元素加入 Follow(X) 中
            if index == len(eachPostGrammar) - 1:
              for item in followSet[eachGrammar]:
                if not item in followSet[eachGrammarStartSymbols]:
                  followSet[eachGrammarStartSymbols].append(item)
            # 2. 产生式形如：S->aXb
            else:
              # 2.1 b 为终结符：将 b 加入 Follow(x) 中
              if eachPostGrammar[index + 1] in terminalSymbols:
                if not eachPostGrammar[index + 1] in followSet[eachGrammarStartSymbols]:
                  followSet[eachGrammarStartSymbols].append(eachPostGrammar[index + 1])
              # 2.2 b 为非终结符，First(b) 中包含 ε：将集合 Follow(S) 中的所有元素加入 Follow(X) 中
              elif 'ε' in firstSet[eachPostGrammar[index + 1]]:
                for item in followSet[eachGrammar]:
                  if not item in followSet[eachGrammarStartSymbols]:
                    followSet[eachGrammarStartSymbols].append(item)
              # 2.3 b 为非终结符，First(b) 中没有 ε：将集合 First(b) 中除了 ε 的所有元素加入 Follow(X) 中
              else:
                for item in firstSet[eachPostGrammar[index + 1]]:
                  if not item in followSet[eachGrammarStartSymbols] and item != 'ε':
                    followSet[eachGrammarStartSymbols].append(item)

            # # LOG: 每次分析后 Follow 集合的变化
            # print('Follow:')
            # for item in followSet.items():
            #   print(' ', item)

  return followSet
