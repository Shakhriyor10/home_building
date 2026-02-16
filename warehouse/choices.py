WAREHOUSE_STATUS = (
    ('active', 'Активный'),
    ('unactive', 'Неактивный'),
)

WAREHOUSE_TYPE = (
    ('wholesale', 'Оптовый'),
    ('production', 'Производство'),
    ('spares', 'Запчасти'),
)

ORDER_STATUS = (
    ('not_confirmed', "не подтверждено"),
    ('confirmed', "подтверждено"),
    ('denied', "отказано"),
    ('закрыто', "отказано"),
)

INCOME_STATUS = (
    (0, 'Открыто'),
    (1, 'Закрыто'),
    (2, 'Завершенный'),
    (3, 'Удалено')
)

M_PART = (
    ('created', 'Создан'),
    ('in_warehouse', 'В Складе'),
    ('sold', 'Продан')
)

PART_TYPE = (
    ('broken', 'Сломан'),
    ('defective', 'Бракован'),
    ('ready', 'Готовая'),
    ('unfinished', 'Незавершенная'),
)
