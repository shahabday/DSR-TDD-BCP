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
import allure

# DO NOT LOOK INTO THE RECORD_TELEGRAMS FUNCTION AS IT WILL SPOIL THE MYSTERY!
from water_meter import record_telegrams
from datetime import datetime, timedelta


telegrams = record_telegrams(duration_minutes=60)
for telegram in telegrams:
    print(telegram)

print (telegrams)




@allure.feature("Static Telegrame Test")
@allure.title("Test of Telegram functoin ")
@allure.description("Import the function calculation the mean value from a list of ints from SciPy library.")
@pytest.mark.parametrize("duration_minutes", [7000])
def test_static_telegrams_status_second_alternative(duration_minutes):
    telegrams = record_telegrams(duration_minutes)

    failures = [telegram for telegram in telegrams if "Static telegram" in telegram and "STATUS: OK" not in telegram]

    assert not failures, f"Static telegram status check failed for: \n" + "\n".join(failures)


@pytest.mark.parametrize("duration_minutes", [180000])  # Test for 600 minutes
def test_mobile_telegrams_distance(duration_minutes):
    telegrams = record_telegrams(duration_minutes)
    mobile_times = []

    # Extract timestamps of mobile telegrams
    for telegram in telegrams:
        if "Mobile telegram" in telegram:
            timestamp_str = telegram.split(" at ")[1].split(" Volume:")[0]

            mobile_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            mobile_times.append([mobile_time , timestamp_str])
    
    errors = []
    # Check distance between mobile telegrams
    for i in range(1, len(mobile_times)):
        time_difference = mobile_times[i][0] - mobile_times[i-1][0]
        maximum_difference = timedelta(minutes=1.1)
        minimum_difference = timedelta(minutes=0.9)
        if not  minimum_difference <= time_difference <= maximum_difference:
            errors.append(f"Time difference between {mobile_times[i-1][1]} and {mobile_times[i][1]} is {time_difference}")

    assert not errors, f"Mobile telegram distance check failed for: \n" + "\n".join(errors)



@pytest.mark.parametrize("duration_minutes, volume_increase_per_min", [(6000, 10)])  # Test for 600 minutes
def test_volume_accu(duration_minutes, volume_increase_per_min):
    telegrams = record_telegrams(duration_minutes)
    volume = 0

    # Check if volume increases by volume_increase_per_min at every mobile telegram
    errors = [] 
    for telegram in telegrams:
        if "Mobile telegram" in telegram:
            volume_str = telegram.split("Volume: ")[1]
            current_volume = float(volume_str)
            current_volume = round(current_volume, 0)
            if current_volume != round(volume + volume_increase_per_min, 0):
                errors.append(f"Volume increase is not correct at {telegram}")
                allure.attach(str(current_volume), name="Volume")
            volume = current_volume
            
            
    assert not errors, f"Volume accuracy check failed for: \n" + "\n".join(errors)
