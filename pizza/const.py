# file for a constants storaging

# Pizza sizes

SMALL = 'small'
MEDIUM = 'medium'
BIG = 'big'

PIZZA_SIZES = (
    (SMALL, SMALL),
    (MEDIUM, MEDIUM),
    (BIG,BIG),
)

# Order statuses

NEW = 0
CONFIRMED = 1
DECLINED = 2

SENT_TO_DELIVERY = 3
ON_THE_WAY = 4
DELIVERED = 5

ORDER_STATUSES = (
    (NEW, 'NEW'),
    (CONFIRMED, 'CONFIRMED'),
    (DECLINED, 'DECLINED'),
    (SENT_TO_DELIVERY, 'SENT_TO_DELIVERY'),
    (ON_THE_WAY, 'ON_THE_WAY'),
    (DELIVERED, 'DELIVERED'),
)

