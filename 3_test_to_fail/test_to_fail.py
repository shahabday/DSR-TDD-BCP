# CERTIFICATION REQUIREMENTS

# The wireless radio meter is sending a Mobile telegram every minute (with timing accuracy tolerance 10%) with the
# volume of water that it measured that passed through it. The water is pumped under pressure only one way through the
# meter at a rate of exactly 10 dm^3 per minute, assume no problems with the pump delivering the water from the tap.
# The volume is measured from zero every time You start recording telegrams.
# Every hour a Static telegram is sent with the meter status which shall be stating OK throughout the whole meter
# operation.


# TODO Write tests that record telegrams and are checking if the meter is up the certification requirements
# TODO Report all inconsistencies with the required parameters

import pytest

# DO NOT LOOK INTO THE RECORD_TELEGRAMS FUNCTION AS IT WILL SPOIL THE MYSTERY!
from water_meter import record_telegrams

telegrams = record_telegrams(duration_minutes=60)
for telegram in telegrams:
    print(telegram)
