# file for a constants storaging

# Pizza sizes

SMALL = 'small'
MEDIUM = 'medium'
LARGE = 'large'

PIZZA_SIZES = (
    (SMALL, SMALL),
    (MEDIUM, MEDIUM),
    (LARGE,LARGE),
)

# Order statuses

NEW = 0
CONFIRMED = 1

SENT_TO_DELIVERY = 2
ON_THE_WAY = 3
DELIVERED = 4

DECLINED = 10

ORDER_STATUSES = (
    (NEW, 'NEW'),
    (CONFIRMED, 'CONFIRMED'),
    (SENT_TO_DELIVERY, 'SENT_TO_DELIVERY'),
    (ON_THE_WAY, 'ON_THE_WAY'),
    (DELIVERED, 'DELIVERED'),
    (DECLINED, 'DECLINED'),
)

