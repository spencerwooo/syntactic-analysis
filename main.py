#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自上而下的 LL(1) 分析器
Top down: LL(1) parser
主控程序：main.py
下级程序：
- 工具库：parserUtils.py
- 输入串处理：parserGeneral.py
"""

import collections
import copy
import os
import xml.etree.ElementTree as ET

import parserUtils
import parserGeneral


def readToken(filePath):
  """
  读入 Token XML 中的内容
  """
  inputTokenList = []

  tokenRoot = ET.parse(filePath).getroot()
  tokens = tokenRoot[0]
  for i in range(0, len(tokens)):
    inputTokenList.append(tokens[i])
  return inputTokenList


def main():
  """
  日志级别：
  - 10: Verbose
  -  5: Essential
  -  1: None
  """
  logLevel = 1

  print('[INFO] Start parsing...')

  # 文法文件路径
  grammarFilePath = 'grammar.txt'

  # 1. 读入文法
  grammar = parserUtils.readGrammar(grammarFilePath)
  if (logLevel > 1):
    print('[Grammar]:')
    for grammaritem in grammar.items():
      print(' ', grammaritem)

  # 2. 划分终结符与非终结符
  terminalSymbols, nonTerminalSymbols = parserUtils.differentiateSymbols(
      grammar)
  if (logLevel > 9):
    print('[Terminal Symbols]:\n ', terminalSymbols)
    print('[Nonterminal Symbols]:\n ', nonTerminalSymbols)

  # 3-1. 递归求 FIRST 集
  grammarFirstSet = collections.defaultdict(list)
  grammarFirstSet = parserUtils.getFIRST(
      grammarFirstSet, grammar, terminalSymbols, nonTerminalSymbols)
  while True:
    originalFirstSet = copy.deepcopy(grammarFirstSet)
    # 查看递归情况的 LOG
    # print(originalFirstSet)
    grammarFirstSet = parserUtils.getFIRST(
        grammarFirstSet, grammar, terminalSymbols, nonTerminalSymbols)
    if grammarFirstSet == originalFirstSet:
      break
  if (logLevel > 9):
    print('[FIRST SET]:')
    for item in grammarFirstSet.items():
      print(' ', item)

  # 3-2. 递归求 FOLLOW 集
  grammarTop = list(grammar.keys())[0]
  grammarFollowSet = collections.defaultdict(list, {grammarTop: ['#']})

  grammarFollowSet = parserUtils.getFOLLOW(
      grammarFirstSet, grammarFollowSet, grammar, terminalSymbols, nonTerminalSymbols)
  while True:
    originalFollowSet = copy.deepcopy(grammarFollowSet)
    # print(originalFollowSet)
    grammarFollowSet = parserUtils.getFOLLOW(
        grammarFirstSet, grammarFollowSet, grammar, terminalSymbols, nonTerminalSymbols)
    if grammarFollowSet == originalFollowSet:
      break

  if (logLevel > 9):
    print('[FOLLOW SET]:')
    for item in grammarFollowSet.items():
      print(' ', item)

  # 4. 创建 LL1 分析表
  analyzeTable = parserUtils.createAnalyzeTable(
      grammar, terminalSymbols, nonTerminalSymbols, grammarFirstSet, grammarFollowSet)
  if (logLevel > 1):
    print('[ANALYZE TABLE]:')
    for item in analyzeTable.items():
      print(' ', item)

  # 5. Demo: 分析一个串 i+i*i
  # inputString = 'i+i*i'
  # parserGeneral.parseInputString(
  #     inputString, grammar, terminalSymbols, nonTerminalSymbols, analyzeTable)

  # 分析输入 Token 文件
  tokenFilePath = os.path.join('test', 'input.token.xml')
  tokenList = readToken(tokenFilePath)
  parserGeneral.createParserTree(
      tokenList, grammar, terminalSymbols, nonTerminalSymbols, analyzeTable)


if __name__ == "__main__":
  main()
