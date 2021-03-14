import itertools


def rhs_to_lhs_mapping(cfg):
    ret = dict()
    for key, rules in cfg.production_rules.items():
        for rule in rules:
            rhs_tuple = tuple(rule.rhs)
            exists = ret.get(rhs_tuple)
            if exists is None:
                ret.update({rhs_tuple: {rule.lhs}})
            else:
                exists.add(rule.lhs)
    return ret


def cyk_parser(cfg, word):
    rhs_mapping = rhs_to_lhs_mapping(cfg)
    subword_mapping = dict()
    length = len(word)
    for term in word:
        exists = subword_mapping.get(term)
        if exists is None:
            subword_mapping.update({tuple([term]): rhs_mapping.get(tuple([term]), set())})

    for i in range(2, length+1):
        for j in range(length - (i - 1)):
            subword = word[j:j+i]
            subword_tuple = tuple(subword)
            exists = subword_mapping.get(subword_tuple)
            if exists is None:
                prod_rules = set()
                for k in range(1, i):
                    lhs = subword_mapping.get(tuple(subword[:k]))
                    rhs = subword_mapping.get(tuple(subword[k:]))
                    if lhs is not None and rhs is not None:
                        for prod in itertools.product(lhs, rhs):
                            rule = rhs_mapping.get(prod)
                            if rule:
                                prod_rules = prod_rules.union(rule)
                subword_mapping.update({subword_tuple: prod_rules})

    return cfg.start_var in subword_mapping.get(tuple(word), {})
