#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parserUtils


def closure():
  pass


def goto():
  pass


def printAnalysisTable():
  pass


def main():
  # 日志级别
  logLevel = 'verbose'

  print('[INFO] Start parsing...')

  # 文法文件路径
  grammarFilePath = 'grammar.txt'

  # 读入文法
  grammar = parserUtils.readGrammar(grammarFilePath)
  print('[Grammar]:')
  print(grammar)

  # 划分终结符与非终结符
  terminalSymbols, nonTerminalSymbols = parserUtils.differentiateSymbols(grammar)
  if (logLevel == 'verbose'):
    print('[Terminal Symbols]:   ', terminalSymbols)
    print('[Nonterminal Symbols]:', nonTerminalSymbols)

  itemSet = parserUtils.getItemSet(grammar)
  if (logLevel == 'verbose'):
    print(itemSet)


if __name__ == "__main__":
  main()
