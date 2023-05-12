class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = list()
    
    def __str__(self):
        lines = str()
        sum = float()

        title = self.name
        title = title.center(30, '*')

        for operation in self.ledger:
            lines += operation['description'][:23].ljust(23) + format(operation['amount'], '.2f')[:7].rjust(7) + '\n'
            sum += operation['amount']

        total = 'Total: ' + format(sum, '.2f')
        text = '\n'.join([title, lines[:-1], total])

        return text

    def deposit(self, amount, description=str()):
        self.ledger.append({
            'amount': amount,
            'description': description
        })

    def withdraw(self, amount, description=str()):
        enough_funds = bool(self.check_funds(amount))

        if enough_funds:
            self.ledger.append({
                'amount': -amount,
                'description': description
            })
        
        return enough_funds

    def get_balance(self):
        balance = float()

        for operation in self.ledger:
            balance += operation['amount']

        return balance

    def transfer(self, amount, destination):
        enough_funds = bool(self.check_funds(amount))
        
        if enough_funds:
            self.withdraw(amount, 'Transfer to ' + destination.name)
            destination.deposit(amount, 'Transfer from ' + self.name)
        
        return enough_funds

    def check_funds(self, amount):
        return True if amount <= self.get_balance() else False

def create_spend_chart(categories):
    chart = 'Percentage spent by category\n'
    label = 100
    bars, expenses, percentages, names = [list() for i in range(4)]

    while label >= 0:
        bars.append([str(label).rjust(3) + '|'])
        label -= 10

    for i, category in enumerate(categories):
        expenses.append(0)
        names.append(category.name)
        
        for operation in category.ledger:
            if operation['amount'] < 0:
                expenses[i] += operation['amount'] * (-1)
    
    total = sum(expenses)

    for i, category in enumerate(categories):
        percentage = (100 * expenses[i]) / total
        rounded = (percentage // 10) * 10

        percentages.append(rounded)

        for j, label in enumerate(bars):
            if percentages[i] >= int(label[0][:-1]):
                bars[j].append(' o ')
            else:
                bars[j].append(' ' * 3)
    
    for label in bars:
        chart += ''.join(label) + ' \n'
    
    chart += (' ' * 4) + ('-' * 3 * len(categories)) + '-\n'

    for i in range(len(max(names, key=len))):
        chart += ' ' * 4

        for name in names:
            try:
                chart += name[i].center(3, ' ')
            except:
                chart += ' ' * 3
        
        chart += ' \n'

    return chart[:-1]