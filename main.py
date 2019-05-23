#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自上而下的 LL(1) 分析器
Top down: LL(1) parser
"""

import parserUtils


def main():
  # 日志级别
  logLevel = 'verbose'

  print('[INFO] Start parsing...')

  # 文法文件路径
  grammarFilePath = 'grammar.txt'

  # 读入文法
  grammar = parserUtils.readGrammar(grammarFilePath)
  if (logLevel == 'verbose'):
    print('[Grammar]:')
    for grammaritem in grammar.items():
      print(' ', grammaritem)

  # 划分终结符与非终结符
  terminalSymbols, nonTerminalSymbols = parserUtils.differentiateSymbols(
      grammar)
  if (logLevel == 'verbose'):
    print('[Terminal Symbols]:\n ', terminalSymbols)
    print('[Nonterminal Symbols]:\n ', nonTerminalSymbols)


if __name__ == "__main__":
  main()
