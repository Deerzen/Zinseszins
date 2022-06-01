# Streamlit is used as dashboard to simplify data input
# The library Matplotlib is used to visualize the calculation
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Zinseszins", page_icon="📈", layout="centered")

#CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title
st.title("Zinseszins")

# Definition of number inputs
i1 = st.number_input("Enter value of current portfolio", min_value=0, value=1000, key="1")
i2 = st.number_input("Enter monthly investment", min_value=0, value=500, key="2")
i3 = st.number_input("Enter expected yearly return in percent", min_value=0, value=10, key="3")
i4 = st.number_input("Enter duration in months", min_value=1, value=60, key="4")


# This function calculates and adds monthly values of total wealth,
# total profit from the investment and the expected monthly income
# from the investment for the chosen amount of months to arrays.
# The arrays are then transformed into Pandas DataFrames
# and into downloadable data which are returned by the function.
def calculate():
    values = {"m_inv": 0, "total_inv": 0, "months": 0, "p_return": 0, "profit": 0}
    arrays = {"total_inv_ar": [], "months_ar": [], "profit_ar": [], "monthly_profit_ar": []}

    values["total_inv"] = i1
    values["m_inv"] = i2
    values["p_return"] = i3
    values["months"] = i4

    for i in range(values["months"]):
        former_balance = values["total_inv"]
        values["total_inv"] = values["total_inv"] / 100 * (100 + values["p_return"] / 12)
        m_profit = values["total_inv"] - former_balance
        values["profit"] += m_profit
        values["total_inv"] += values["m_inv"]
        arrays["profit_ar"].append(int(values["profit"]))
        arrays["total_inv_ar"].append(int(values["total_inv"]))
        arrays["months_ar"].append(int(i + 1))
        arrays["monthly_profit_ar"].append(int(m_profit))

    chart_dict = {"Profit": arrays["profit_ar"], "Wealth": arrays["total_inv_ar"]}
    chart_data = pd.DataFrame(chart_dict, index=arrays["months_ar"])
    frame_dict = {"Total Wealth": arrays["total_inv_ar"], "Total Profit": arrays["profit_ar"], "Monthly Profit": arrays["monthly_profit_ar"]}
    frame_data = pd.DataFrame(frame_dict, index=arrays["months_ar"])
    csv = frame_data.to_csv().encode('utf-8')

    return [chart_data, frame_data, csv]


# Calculates the difference between the value of the current month
# and the previous month in percent
def delta(data, slider_value, column):
    if slider_value > 1:
        difference = data.loc[slider_value, column] - data.loc[slider_value - 1, column]
        percentage_dif = difference * 100 / data.loc[slider_value, column]
        return str(round(percentage_dif, 2)) + "%"
    else:
        return "0.00%"


# Updates the displayed data
def update_display_data():
    display_data = calculate()
    st.line_chart(display_data[0])
    sv = st.slider("Select month for detailed data and percentage changes compared to the previous month",
        min_value=1,
        max_value=i4,
        value=1,
        step=1
        )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Wealth", display_data[1].loc[sv,"Total Wealth"], delta(display_data[1], sv, "Total Wealth"))
    col2.metric("Total Profit", display_data[1].loc[sv,"Total Profit"], delta(display_data[1], sv, "Total Profit"))
    col3.metric("Monthly Profit", display_data[1].loc[sv,"Monthly Profit"], delta(display_data[1], sv, "Monthly Profit"))
    st.table(display_data[1])
    st.download_button("Download CSV", display_data[2], "Zinseszins.csv", "text/csv")


if __name__ == '__main__':
    update_display_data()
