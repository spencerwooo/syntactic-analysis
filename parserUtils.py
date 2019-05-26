#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LL1 语法分析器工具库：parserUtils.py
包含：
- 读文法
- 处理终结与非终结符号
- 获得 First 和 Follow 集合
上级：main.py
"""

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
          # 遇到终结符就可以停啦
          if eachPostGrammarItem in terminalSymbols:
            if not eachPostGrammarItem in firstSet[eachGrammar]:
              firstSet[eachGrammar].append(eachPostGrammarItem)
            break
          # 遇到 First 集合中含有空串的还要继续哦
          elif 'ε' in firstSet[eachPostGrammarItem]:
            for item in firstSet[eachPostGrammarItem]:
              if not item in firstSet[eachGrammar]:
                firstSet[eachGrammar].append(item)
          # 但是如果 First 集合没有空串就可以停下来啦
          else:
            for item in firstSet[eachPostGrammarItem]:
              if not item in firstSet[eachGrammar]:
                firstSet[eachGrammar].append(item)
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
          lastItemIndex = len(eachPostGrammar) - 1
          # 1. 产生式形如：S->aX，将集合 Follow(S) 中的所有元素加入 Follow(X) 中
          if index == lastItemIndex:
            for item in followSet[eachGrammar]:
              if not item in followSet[eachGrammarStartSymbols]:
                followSet[eachGrammarStartSymbols].append(item)
          # 2. 产生式形如：S->aXb
          else:
            # 2.1 b 为终结符：将 b 加入 Follow(X) 中
            if eachPostGrammar[index + 1] in terminalSymbols:
              if not eachPostGrammar[index + 1] in followSet[eachGrammarStartSymbols]:
                followSet[eachGrammarStartSymbols].append(
                    eachPostGrammar[index + 1])
            # 2.2 b 为非终结符
            else:
              # 从 b 开始往后扫描
              for i in range(index + 1, lastItemIndex + 1):
                # 遇到终结符就可以停下来啦
                if eachPostGrammar[i] in terminalSymbols:
                  if not eachPostGrammar[i] in followSet[eachGrammarStartSymbols]:
                    followSet[eachGrammarStartSymbols].append(
                        eachPostGrammar[i])
                  break
                # 要看看 First 集合里面有没有空串，有的话就可以加入 Follow 啦
                elif 'ε' in firstSet[eachPostGrammar[i]]:
                  for item in firstSet[eachPostGrammar[i]]:
                    if not item in followSet[eachGrammarStartSymbols] and item != 'ε':
                      followSet[eachGrammarStartSymbols].append(item)
                  # 如果扫描到最后一项，First 集合里面还有空串，就要把集合 Follow(S) 中的所有元素加入 Follow(X) 中哦
                  if i == lastItemIndex:
                    for item in followSet[eachGrammar]:
                      if not item in followSet[eachGrammarStartSymbols]:
                        followSet[eachGrammarStartSymbols].append(item)
                # 如果没有空串，把这一项的 First 集合里除了空串以为的内容加入 Follow 集合就可以停下来啦
                else:
                  for item in firstSet[eachPostGrammar[i]]:
                    if not item in followSet[eachGrammarStartSymbols] and item != 'ε':
                      followSet[eachGrammarStartSymbols].append(item)
                  break

  return followSet
