# The library Matplotlib is used to visualize the calculation
import matplotlib.pyplot as plt

# Global variables
m_inv = 0
total_inv = 0
total_inv_ar = []
months = 0
months_ar = []
profit_ar = []
p_return = 0


# This function calculates and prints monthly reports on total wealth,
# total profit from the investment and the expected monthly income
# from the investment for the chosen amount of months.
def calculate():
    global m_inv
    global total_inv
    global months
    global p_return
    global total_inv_ar
    global months_ar
    global profit_ar
    profit = 0

    for i in range(months):
        former_balance = total_inv
        total_inv = total_inv / 100 * (100 + p_return / 12)
        m_profit = total_inv - former_balance
        profit += m_profit
        total_inv += m_inv
        profit_ar.append(profit)
        total_inv_ar.append(total_inv)
        months_ar.append(int(i + 1))

        print("")
        print("Month " + str(i + 1))
        print("Total wealth: " + str(round(total_inv, 2)))
        print("Total investment profit: " + str(round(profit, 2)))
        print("Monthly investment profit: " + str(round(m_profit, 2)))


# This function graphs the calculated values and illustrates how wealth and 
# investment profits are expected to develop over the chosen time frame
def graph():
    global total_inv_ar
    global months_ar
    global profit_ar

    plt.plot(months_ar, total_inv_ar, color='green', label='Wealth')
    plt.plot(months_ar, profit_ar, color='purple', label='Profit')
    plt.title('Investment growth', fontsize=14)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Money', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()


# Main loop
while True:
    total_inv = int(input("Enter current total portfolio: "))
    m_inv = int(input("Enter monthly investment: "))
    p_return = int(input("Enter expected yearly return in percent: "))
    months = int(input("Enter duration in months: "))
    if months > 0:
        calculate()
        print("")
        graph()
        total_inv = 0
        p_return = 0
        m_inv = 0
        months = 0
        months_ar = []
        total_inv_ar = []
        profit_ar = []
    else:
        print("no months")
