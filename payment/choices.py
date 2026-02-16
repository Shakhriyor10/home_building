OUTLAY_TYPE_CHOICES = (
    ('car', 'Машина'),
    ('worker', 'Сотрудники'),
    ('machine', 'Станки'),
)


AMOUNT_TYPE_CHOICES = (
    ('income', 'Приход'),
    ('outcome', 'Расход'),
)


PAYMENT_LOG_OUTLAY = (
    (1, 'Оплата за приход'),    # income
    (2, 'Оплата за заказ'),     # order
    (3, 'Оплата за расход'),    # outlay
    (4, 'Пополнение баланса'),    # outlay
    (5, 'Оплата за доставку'),    # outlay
)


PAYMENT_METHOD_CHOICES = (
    ('cash', 'Наличные'),
    ('transfer', 'Перечисление'),
    ('card', 'Безналичные'),
    ('-', '-'),
)


PAYMENT_TYPE_CHOICES = (
    ('uzs', 'Сум'),
    ('usd', 'Доллар'),
)

EXPENSE_PAYMENT_TYPE_CHOICES = (
    ('uzs', 'Сум'),
    ('usd', 'Доллар'),
)

