ORDER_STATUS = (
    (0, 'В процессе'),
    (1, 'Закрытый'),
    (2, 'Оплаченный/Долговой'),
    (3, 'Завершенный'),
    (4, 'Удален'),
)

ORDER_RETURN_STATUS = (
    ('open', 'Открито'),
    ('conducted', 'Проведен'),
    ('canceled', 'Отменен'),
)

ORDER_ITEM = (
    (0, 'Активный'),
    (4, 'Удален'),
)

SERVICE_UNIT_TYPE = (
    ('pieces', '(шт)'),
    ('pieces_count', 'шт'),
    ('m_area', 'метр кв'),
    ('sm_area', 'см. кв'),
    ('sm', 'см.'),
    ('m', 'метр'),
    ('mm', 'мм'),
)

M_ORDER_STATUS = (
    ('accepted', 'Принято'),
    ('confirmed', 'Обработано'),
    ('in_progress', 'В процессе'),
    ('completed', 'Завершенный'),
    ('remote', 'Удаленный')
)
M_ORDER_IMPORTANCE = (
    ('custom', 'Обычный'),
    ('important', 'Важный'),
    ('extremely_important', 'Крайне важный'),
    ('vip', 'V.I.P.'),
)
M_ORDER_TYPE = (
    ('full', 'Полный'),
    ('only_service', 'Только сервис')
)
M_ORDER_DETAIL_STATUS = (
    ('created', 'Создан'),
    ('in_progress', 'В процессе'),
    ('defective', 'Бракованный')
)
M_ORDER_DETAIL_IMPORTANCE = (
    ('custom', 'Обычный'),
    ('important', 'Важный'),
    ('extremely_important', 'Важный'),
    ('vip', 'V.I.P.'),
)
M_ORDER_DETAIL_TYPE = (
    ('door', 'Дверь'),
    ('door_l', 'Дверь (Л)'),
    ('door_r', 'Дверь (П)'),
    ('transom', 'Фрамуга'),
    ('side_l', 'Бакавой (Л)'),
    ('side_r', 'Бакавой (П)'),
    ('custom', 'Глухой проем'),
    ('custom_with_window', 'Проем с форточкой'),
)
M_DETAIL_TEMPLATE_TYPES = (
    ('double_doors', '2x Дверный'),
    ('door', '1x Дверный'),
    ('double_doors_out_sides', '2x Дверный без бакавой'),
    ('double_doors_out_transom', '2x Дверный без фрамуги'),
    ('custom', 'Глухой проем'),
    ('custom_with_window', 'Проем с форточкой'),
)
MACHINE = (
    ('working', 'Работает'),
    ('in_repair', 'В ремонте'),
    ('suspended', 'Приостановленный')
)
M_ORDER_DETAIL_SERVICE_STATUS = (
    ('created', 'Создан'),
    ('in_progress', 'В процессе'),
    ('done', 'Готово')
)
MACHINES_PLAN_STATUS = (
    ('created', 'Создан'),
    ('confirmed', 'Подтверждено'),
    ('in_progress', 'В процессе'),
    ('done', 'Сделано')
)
