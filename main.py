import sys
from collections import defaultdict


class GhostDB:
    def __init__(self):
        self.db = {}
        self.value_counts = defaultdict(int)
        self.transactions = []

    def _set(self, key, value):
        old_value = self.db.get(key)
        if old_value:
            self.value_counts[old_value] -= 1
        self.db[key] = value
        self.value_counts[value] += 1

    def _unset(self, key):
        if key in self.db:
            old_value = self.db[key]
            self.value_counts[old_value] -= 1
            del self.db[key]

    def set(self, key, value):
        if self.transactions:
            # Сохраняем текущее состояние ключа в транзакции
            if key not in self.transactions[-1]:
                self.transactions[-1][key] = self.db.get(key)
        self._set(key, value)

    def get(self, key):
        return self.db.get(key, "NULL")

    def unset(self, key):
        if self.transactions:
            if key not in self.transactions[-1]:
                self.transactions[-1][key] = self.db.get(key)
        self._unset(key)

    def counts(self, value):
        return self.value_counts[value]

    def find(self, value):
        return [k for k, v in self.db.items() if v == value]

    def begin(self):
        self.transactions.append({})

    def rollback(self):
        if not self.transactions:
            print("NO TRANSACTION")
            return
        changes = self.transactions.pop()
        for key, old_value in changes.items():
            if old_value is None:
                self._unset(key)
            else:
                self._set(key, old_value)

    def commit(self):
        if not self.transactions:
            print("NO TRANSACTION")
            return
        self.transactions.clear()

    def process(self, line):
        parts = line.strip().split()
        print(parts)
        if not parts:
            return False

        cmd = parts[0].upper()

        if cmd == 'END':
            return True
        elif cmd == 'SET' and len(parts) == 3:
            self.set(parts[1], parts[2])
        elif cmd == 'GET' and len(parts) == 2:
            print(self.get(parts[1]))
        elif cmd == 'UNSET' and len(parts) == 2:
            self.unset(parts[1])
        elif cmd == 'COUNTS' and len(parts) == 2:
            print(self.counts(parts[1]))
        elif cmd == 'FIND' and len(parts) == 2:
            print(" ".join(self.find(parts[1])) or "NULL")
        elif cmd == 'BEGIN':
            self.begin()
        elif cmd == 'ROLLBACK':
            self.rollback()
        elif cmd == 'COMMIT':
            self.commit()
        else:
            print("INVALID COMMAND")
        return False


def main():
    db = GhostDB()
    for line in sys.stdin:
        if db.process(line):
            break


if __name__ == '__main__':
    main()
