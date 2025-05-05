from collections import defaultdict
import copy

class CFGtoCNFConverter:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.VN = set(variables)
        self.VT = set(terminals)
        self.P = defaultdict(set)
        for head, bodies in productions.items():
            for body in bodies:
                self.P[head].add(tuple(body))
        self.S = start_symbol

    def print_step(self, step_name):
        print(f"\n{step_name}")
        print("G = (VN, VT, P, S)")
        print(f"VN = {self.VN}")
        print(f"VT = {self.VT}")
        print(f"S = {self.S}")
        print("P = {")
        for head in self.P:
            for body in self.P[head]:
                print(f"  {head} -> {' '.join(body) if body else 'ε'}")
        print("}")

    def eliminate_epsilon(self):
        nullable = {var for var in self.VN if () in self.P[var]}
        while True:
            changed = False
            for head in self.VN:
                for body in list(self.P[head]):
                    if any(sym in nullable for sym in body):
                        new_bodies = self._generate_nullable_combinations(body, nullable)
                        for new_body in new_bodies:
                            if new_body != body and new_body not in self.P[head]:
                                self.P[head].add(new_body)
                                changed = True
            if not changed:
                break
        for var in self.VN:
            self.P[var] = {body for body in self.P[var] if body != () or var == self.S}
        self.print_step("Step 1: Eliminate ε productions")

    def _generate_nullable_combinations(self, body, nullable):
        results = set()
        n = len(body)
        for mask in range(1 << n):
            new_body = tuple(body[i] for i in range(n) if not ((1 << i) & mask) or body[i] not in nullable)
            results.add(new_body)
        return results

    def eliminate_unit_productions(self):
        unit_pairs = set((A, A) for A in self.VN)
        while True:
            new_pairs = unit_pairs.copy()
            for A, B in unit_pairs:
                for body in self.P[B]:
                    if len(body) == 1 and body[0] in self.VN:
                        new_pairs.add((A, body[0]))
            if new_pairs == unit_pairs:
                break
            unit_pairs = new_pairs

        new_P = defaultdict(set)
        for A, B in unit_pairs:
            for body in self.P[B]:
                if len(body) != 1 or body[0] not in self.VN:
                    new_P[A].add(body)
        self.P = new_P
        self.print_step("Step 2: Eliminate renaming")

    def eliminate_nonproductive_symbols(self):
        productive = set()
        while True:
            updated = False
            for A in self.VN:
                for body in self.P[A]:
                    if all(sym in self.VT or sym in productive for sym in body):
                        if A not in productive:
                            productive.add(A)
                            updated = True
            if not updated:
                break
        self.VN = {A for A in self.VN if A in productive}
        self.P = {A: {body for body in self.P[A] if all(sym in self.VT or sym in self.VN for sym in body)} for A in self.VN}
        self.print_step("Step 3: Eliminate nonproductive symbols")

    def eliminate_inaccessible_symbols(self):
        reachable = {self.S}
        changed = True
        while changed:
            changed = False
            new_reachable = reachable.copy()
            for A in reachable:
                for body in self.P.get(A, []):
                    for sym in body:
                        if sym in self.VN and sym not in new_reachable:
                            new_reachable.add(sym)
                            changed = True
            reachable = new_reachable
        self.VN = reachable
        self.P = {A: self.P[A] for A in self.VN}
        self.print_step("Step 4: Eliminate inaccessible symbols")

    def convert_to_cnf(self):
        new_P = defaultdict(set)
        term_map = {}

        def get_term_var(term):
            if term not in term_map:
                var = f"X_{term}"
                while var in self.VN:
                    var += "_"
                term_map[term] = var
                self.VN.add(var)
                new_P[var].add((term,))
            return term_map[term]

        for A in list(self.VN):  # Use a copy of self.VN to avoid modifying it during iteration
            for body in self.P[A]:
                if len(body) == 1 and body[0] in self.VT:
                    new_P[A].add(body)
                else:
                    new_body = []
                    for sym in body:
                        if sym in self.VT:
                            new_body.append(get_term_var(sym))
                        else:
                            new_body.append(sym)

                    while len(new_body) > 2:
                        new_var = f"Y_{len(new_P)}"
                        while new_var in self.VN:
                            new_var += "_"
                        self.VN.add(new_var)
                        new_P[new_var].add((new_body[0], new_body[1]))
                        new_body = [new_var] + new_body[2:]
                    new_P[A].add(tuple(new_body))

        for var, rules in term_map.items():
            new_P[rules].add((var,))
        self.P = new_P
        self.print_step("Step 5: Convert to CNF")

    def to_cnf(self):
        print("Variant20")
        self.print_step("Original Grammar")
        self.eliminate_epsilon()
        self.eliminate_unit_productions()
        self.eliminate_nonproductive_symbols()
        self.eliminate_inaccessible_symbols()
        self.convert_to_cnf()


# Example usage:
variables = {'S', 'A', 'B', 'C', 'D'}
terminals = {'a', 'b'}
productions = {
    'S': [('a', 'B'), ('b', 'A'), ('A',)],
    'A': [('B',), ('S', 'a'), ('b', 'B', 'A'), ('b',)],
    'B': [('b',), ('b', 'S'), ('a', 'D'), ()],  # ε as ()
    'D': [('A', 'A')],
    'C': [('B', 'a')],
}
start_symbol = 'S'

converter = CFGtoCNFConverter(variables, terminals, productions, start_symbol)
converter.to_cnf()