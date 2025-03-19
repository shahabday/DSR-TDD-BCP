import pytest
import allure
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import base64  # Import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@allure.feature("Telegram Tests")
@allure.title("Test of Static Telegrams Count")
@allure.description("This test verifies that static telegrams are received exactly once per hour.")
@pytest.mark.parametrize("duration_minutes", [60, 120, 600, 100000])  # More varied durations
def test_static_telegrams_count(duration_minutes):
    telegrams = record_telegrams(duration_minutes)
    static_telegrams_count = sum(1 for telegram in telegrams if "Static telegram" in telegram)
    hours = duration_minutes // 60
    if duration_minutes % 60 != 0:
        hours += 1

    # Create a failure graph (even if there are no failures)
    failure_data = []  # Store data for Plotly
    for telegram in telegrams:
        if "ERROR" in telegram:
            timestamp_str = telegram.split(" at ")[1].split(" STATUS:")[0]
            mobile_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            failure_data.append({"Time": mobile_time, "Status": "Failed"})

    if failure_data:
        df = pd.DataFrame(failure_data)
        fig = px.scatter(df, x="Time", y="Status", title="Telegram Failures Over Time")
        fig.update_yaxes(categoryorder='array', categoryarray= ['Failed']) #For having the correct order.
        fig_html = fig.to_html(full_html=False)  # Convert to HTML
        allure.attach(fig_html, name="Failure Graph (Plotly)", attachment_type=allure.attachment_type.HTML)
    else:
         # If no failures, attach a simple message
        allure.attach("No Failures Detected", name="Failure Status", attachment_type=allure.attachment_type.TEXT)


    # --- Attachments ---
    allure.attach(str(duration_minutes), name="Test Duration (minutes)", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(telegrams), name="Recorded Telegrams", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(static_telegrams_count), name="Static Telegrams Count",
                  attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(hours), name="Expected Static Telegram Count (hours)",
                  attachment_type=allure.attachment_type.TEXT)

    assert static_telegrams_count == hours, f"Expected {hours} static telegrams, but got {static_telegrams_count}"