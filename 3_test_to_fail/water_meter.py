from datetime import datetime, timedelta
import random
from typing import List


def record_telegrams(duration_minutes: int) -> List[str]:
    """
    NO PEAKING DURING CLASS!!!!!!!



















    I'M SERIOUS!!!!!!!!!!
































    I WILL SEE YOU SCROLLING THAT FAR!
























    LAST WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!










    OK. YOu are a patient one.

    FULL SCENARIO:
    The meter works generally well, but the testing environment is not optimal.

    Finding 1:
    The telegram receiver gateway has a rare bug occurrence where the static telegram is received twice.
    This has to be reported to the developers of the gateway firmware (FW) to be corrected.

    Finding 2:
    Generally only 70% of static telegrams are received from the meter. The issue could be related again to the gateway,
    but connecting this to a real life scenario telegrams are usually lost because of high traffic of telegrams
    from multiple meters. This could be solved by isolating the meter from others to test its communication in a closed
    environment. This is usually achieved by putting the meter in a shield-box. A Faraday cage, so a metal box, that
    keeps any outside signals from disrupting communication with the tested meter. Such a situation can happen when
    a new batch of meters is completed and hundreds or even thousands are tested at the same freshly of the production
    line.

    Finding 3:
    Exactly at 13 the meter gets an ERROR status. (bonus points for coming up with the reason) as it is caused by the
    lunch break and too many people leaving the lab at once and disturbing its operation.

    Finding 4:
    There is a disruption in electricity every day after midnight, as the IT department is resetting infrastructure
    automatically at the time. This cuts the power to the gateway and telegrams are lot for 5-10 minutes before it
    boots up again.

    Finding 5:
    There is a leakage of 0.1dm^3 per minute which is somewhere in the water installation after the meter.
    Solutions would be to make the testing system a closed on so that the meter itself would detect the leak by some air
    being detected in the pipe. Also a secondary meter later in the pipe could catch that there is less water flowing
    in the system.

    :param duration_minutes:
    :return: telegrams
    """

    volume = 0.0
    telegrams = []
    current_time = datetime.now()
    current_hour = current_time.hour

    for i in range(duration_minutes):

        # Generate static telegram every hour, with only 70% chance for it to actually appear
        if current_hour != current_time.hour:
            current_hour = current_time.hour
            roll_of_dice = random.random()
            if current_time.hour != 13 and roll_of_dice <= 0.7:
                static_telegram = f"Static telegram at {current_time.strftime('%Y-%m-%d %H:%M:%S')} STATUS: OK"
                telegrams.append(static_telegram)
            elif roll_of_dice > 0.9:
                static_telegram = f"Static telegram at {current_time.strftime('%Y-%m-%d %H:%M:%S')} STATUS: OK"
                telegrams.append(static_telegram)
                telegrams.append(static_telegram)
            elif current_time.hour == 13:
                static_telegram = f"Static telegram at {current_time.strftime('%Y-%m-%d %H:%M:%S')} STATUS: ERROR"
                telegrams.append(static_telegram)

        # Generate mobile telegram every minute, excluding 5-10 minutes after midnight
        # Flow is 9.9 dm^3/min as there as a 0.1 dm^3/min leak in the pipe system
        minutes_missed_after_midnight = random.randint(5, 10)
        if not (current_time.hour == 0 and 0 <= current_time.minute <= minutes_missed_after_midnight):
            volume += 9.9

            mobile_telegram = f"Mobile telegram at {current_time.strftime('%Y-%m-%d %H:%M:%S')} Volume: {volume:.1f}"
            telegrams.append(mobile_telegram)

        # some randomness between mobile telegrams, as they never arrive precisely due to many possible resons
        seconds_to_next_correct_mobile = random.randint(54, 66)
        current_time += timedelta(seconds=seconds_to_next_correct_mobile)

    return telegrams

if __name__ == "__main__":
    # Example usage:
    duration_minutes = 1200
    telegrams = record_telegrams(duration_minutes)
    for telegram in telegrams:
        print(telegram)
