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

import parserUtils
import parserGeneral


def main():
  """
  日志级别：
  - 10: Verbose
  -  5: Essential
  -  1: None
  """
  logLevel = 10

  print('[INFO] Start parsing...')

  # 文法文件路径
  grammarFilePath = 'firstsetgrammar.txt'

  # 读入文法
  grammar = parserUtils.readGrammar(grammarFilePath)
  if (logLevel > 1):
    print('[Grammar]:')
    for grammaritem in grammar.items():
      print(' ', grammaritem)

  # 划分终结符与非终结符
  terminalSymbols, nonTerminalSymbols = parserUtils.differentiateSymbols(
      grammar)
  if (logLevel > 9):
    print('[Terminal Symbols]:\n ', terminalSymbols)
    print('[Nonterminal Symbols]:\n ', nonTerminalSymbols)

  # 递归求 FIRST 集
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

  # 递归求 FOLLOW 集
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

  parserGeneral.hello('World')

if __name__ == "__main__":
  main()
