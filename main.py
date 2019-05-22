"""
LR(1) 语法分析
"""

import parse


def closure():
  pass


def goto():
  pass


def printAnalysisTable():
  pass


def main():
  print('[INFO] Start parsing...')

  # 文法文件路径
  grammarFilePath = 'grammar.txt'

  # 读入文法
  grammar = parse.readGrammar(grammarFilePath)
  print('[Grammar]:', grammar)

  # 划分终结符与非终结符
  terminalSymbols, nonTerminalSymbols = parse.differentiateSymbols(grammar)
  print('[Terminal Symbols]:   ', terminalSymbols)
  print('[Nonterminal Symbols]:', nonTerminalSymbols)


if __name__ == "__main__":
  main()
