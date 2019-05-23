#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自上而下的 LL(1) 分析器
Top down: LL(1) parser
"""

import parserUtils


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

  grammarFirstSet = parserUtils.getFIRST(
      grammar, terminalSymbols, nonTerminalSymbols)
  if (logLevel > 9):
    print('[FIRST SET]:')
    print(' ', grammarFirstSet)

  grammarFollowSet = parserUtils.getFOLLOW(
      grammar, terminalSymbols, nonTerminalSymbols)
  if (logLevel > 9):
    print('[FOLLOW SET]:')
    print(' ', grammarFollowSet)


if __name__ == "__main__":
  main()
