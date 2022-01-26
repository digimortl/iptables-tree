#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from collections import defaultdict
import re
import sys
from typing import Dict, List, NamedTuple, NoReturn, Optional, Sequence, Tuple


class Counters(NamedTuple):
    pcnt: int = 0
    bcnt: int = 0

    def __str__(self):
        return f'[{self.pcnt}:{self.bcnt}]'


class Policy(NamedTuple):
    verdict: str
    counters: Counters = Counters()


class Target(NamedTuple):
    jump: 'Chain'
    goto: Optional['Chain'] = None
    perTargetOptions: Optional[str] = None


class RuleSpec(NamedTuple):
    matches: str = ''
    target: Optional[Target] = None
    counters: Optional[Counters] = None


class Chain(NamedTuple):
    name: str
    ruleSpecs: List[RuleSpec]
    policy: Optional[Policy] = None

    @classmethod
    def of(cls, chainName: str, policy: Optional[Policy] = None) -> 'Chain':
        return cls(chainName, [], policy)

    @property
    def hasNoRules(self) -> bool:
        return not self.ruleSpecs


# [counters] -A chain rule-specification
# rule-specification = [matches...] [target]
# match = -m matchname [per-match-options]
# target = {-j|-g} targetname [per-target-options]
RULE_RE = re.compile(r'''
    ^
    (?:
      \[(?P<pcnt>\d+):(?P<bcnt>\d+)\]\s+              # counters
    )?
    -A\s*(?P<chain>[\w\\'"-]+)                        # chain
    (?P<matches>.*?)                                  # matches
    (?:
      \s+(?P<action>-[jg])\s*(?P<target>[\w\\'"-]+)   # target
         (?P<perTargetOptions>.+)?                    # per-target -options
    )?
    $
''', re.VERBOSE)


class ParseError(Exception):
    pass


def parsePolicy(line: str) -> Tuple[str, Optional[Policy]]:
    chainName, verdict, counters = line.strip(': ').split()
    if verdict == '-':
        return chainName, None

    pcnt, _, bcnt = counters.strip('][ ').partition(':')
    return chainName, Policy(verdict, Counters(int(pcnt), int(bcnt)))


def parseRule(line: str) -> Dict[str, Optional[str]]:

    def strip(x: Optional[str]) -> str:
        return (x or '').strip()

    match = RULE_RE.match(line)
    if match is None:
        raise ParseError('cannot parse rule')

    rv = {}
    rv['chainName'] = strip(match.group('chain'))
    rv['matches'] = strip(match.group('matches'))
    rv['targetName'] = strip(match.group('target'))
    rv['perTargetOptions'] = strip(match.group('perTargetOptions'))
    rv['action'] = strip(match.group('action'))
    rv['pcnt'] = strip(match.group('pcnt'))
    rv['bcnt'] = strip(match.group('bcnt'))
    return rv


def parseTablesFromStream(stream):
    tables = defaultdict(dict)

    currentTable = None
    for lino, line in enumerate(map(str.strip, stream), start=1):
        if not line or line.startswith('#'):
            continue

        if line.startswith('*'):
            currentTable = tables[line.strip('* ')]  # Open table.
            continue

        if line.startswith('COMMIT'):
            currentTable = None  # Close table.
            continue

        if currentTable is None:
            raise ParseError(f'Line {lino}: {line!r}: table was not specified')

        #
        # Parse policy:
        #
        if line.startswith(':'):
            chainName, policy = parsePolicy(line)
            if policy is None:
                continue

            currentTable.setdefault(
                chainName, Chain.of(chainName, policy))
            continue

        #
        # Parse the rule:
        #
        try:
            ruleDict = parseRule(line)
        except ParseError as exc:
            raise ParseError(f'Line {lino}: {line!r}: {exc!s}')

        if not ruleDict['chainName']:
            raise ParseError(f'Line {lino}: {line!r}: chain not found')

        chain = currentTable.setdefault(
            ruleDict['chainName'], Chain.of(ruleDict['chainName']))

        pcnt, bcnt = ruleDict['pcnt'], ruleDict['bcnt']
        counters = Counters(int(pcnt), int(bcnt)) if pcnt and bcnt else None

        if ruleDict['targetName']:
            jumpTo = currentTable.setdefault(
                ruleDict['targetName'], Chain.of(ruleDict['targetName']))
            goTo = jumpTo if ruleDict['action'] in ['-g', '--goto'] else None

            ruleSpec = RuleSpec(
                ruleDict['matches'],
                Target(jumpTo, goTo, ruleDict['perTargetOptions']),
                counters,
            )
        else:
            ruleSpec = RuleSpec(
                ruleDict['matches'], None, counters)

        chain.ruleSpecs.append(ruleSpec)

    return tables


class Sym(NamedTuple):
    V: str   # Vertical line drawing char
    VR: str  # Vertical and right
    H: str   # Horizontal
    UR: str  # Up and right


def findSym(charMap: str) -> Sym:
    ascii = Sym('|', '|', '-', '`')
    return {
        'ascii': ascii,
        'utf-8': Sym('\u2502', '\u251C', '\u2500', '\u2514'),
    }.get(charMap, ascii)


def printRuleSpecsOf(chain: Chain, sym: Sym) -> NoReturn:
    loopDetectionCache = {chain.name}

    def printRuleSpec(ruleSpec: RuleSpec, prefix: str, isLast: bool):
        print(prefix + (sym.UR if isLast else sym.VR) + sym.H, end='')

        if ruleSpec.matches:
            print(f'{ruleSpec.matches} ', end='')

        if not ruleSpec.target:
            print()
            return

        print('-g' if ruleSpec.target.goto else '-j', ruleSpec.target.jump.name, end='')

        if ruleSpec.target.perTargetOptions:
            print(f' {ruleSpec.target.perTargetOptions}', end='')

        if ruleSpec.counters:
            print(f' {ruleSpec.counters!s}', end='')

        print()

        prefix += (
            (' ' if isLast else sym.V) +
            (' ' * (len(ruleSpec.matches) + 1 if ruleSpec.matches else 0)) +
            '    ')

        if ruleSpec.target.jump.name in loopDetectionCache:
            print(prefix + sym.UR + sym.H + '[[...LOOP...]]')
            return

        loopDetectionCache.add(ruleSpec.target.jump.name)
        for targetRuleSet in ruleSpec.target.jump.ruleSpecs:
            printRuleSpec(
                targetRuleSet,
                prefix,
                targetRuleSet is ruleSpec.target.jump.ruleSpecs[-1],
            )
        loopDetectionCache.discard(ruleSpec.target.jump.name)

    print(f'-A {chain.name}')
    for chainRuleSpec in chain.ruleSpecs:
        printRuleSpec(
            chainRuleSpec,
            prefix='   ',
            isLast=chainRuleSpec is chain.ruleSpecs[-1],
        )


if __name__ == '__main__':
    parser = ArgumentParser(description='Convert iptables-save format to pstree-like view')
    parser.add_argument('-A', '--ascii', action='store_true', help='Use ASCII characters to draw the tree.')
    ns = parser.parse_args()

    try:
        tables = parseTablesFromStream(sys.stdin)
    except ParseError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    sym = findSym(sys.stdout.encoding)
    if ns.ascii:
        sym = findSym('ascii')

    for name, table in tables.items():
        print(f'*{name}')

        for _, chain in table.items():
            if chain.policy is None:
                continue
            print(f':{chain.name}'
                  f' {chain.policy.verdict}'
                  f' {chain.policy.counters}')

        for _, chain in table.items():
            if chain.policy is None or chain.hasNoRules:
                continue

            printRuleSpecsOf(chain, sym)

    sys.exit(0)
