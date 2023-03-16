import numpy as np
import numpy_financial as npf
import ipywidgets as widgets
import matplotlib.pyplot as plt
from pathlib import Path

class Investment:
    def __init__(self, rc, cc, l, g, b, y):
        self.rc = rc
        self.cc = cc
        self.l = l
        self.g = g
        self.b = b
        self.y = y
        self.contributions = [0] * (l + 1)
        self.distributions = [0] * (l + 1)
        self.navs = [0] * (l + 1)

    def compute(self):
        # Compute the contributions, distributions, and NAV for each year
        for t in range(self.l + 1):
            if t == 0:
                # Compute the initial contribution and NAV
                self.contributions[t] = self.rc * self.cc
                self.navs[t] = self.contributions[t]
            elif t == self.l:
                # No contribution is made in the final year
                self.contributions[t] = 0
            else:
                # Compute the contribution and distribution for the current year
                self.contributions[t] = self.rc * (self.cc - sum(self.contributions[:t]))
                self.distributions[t] = self.navs[t - 1] * min(max(self.y, (t / self.l) ** self.b), 1) * (1 + self.g)
                # Compute the NAV for the current year
                self.navs[t] = self.navs[t - 1] * (1 + self.g) + self.contributions[t] - self.distributions[t]

        # Compute the IRR using the cash flows of contributions and distributions
        cash_flows = np.array(self.contributions) * -1 + np.array(self.distributions)
        irr = npf.irr(cash_flows) * 100

        # Print the results
        print(f"Contributions: {[round(c, 1) for c in self.contributions]}")
        print(f"Distributions: {[round(d, 1) for d in self.distributions]}")
        print(f"NAV: {[round(n, 1) for n in self.navs]}")
        print(f"IRR: {round(irr, 2)}%")
        res = {
            'Contributions': [round(c, 1) for c in self.contributions],
            'Distributions': [round(d, 1) for d in self.distributions],
            'NAV': [round(n, 1) for n in self.navs],
            'IRR': round(irr, 2),
        }
        # Plot the results
        fig, axs = plt.subplots(1, 3, figsize=(20, 4), sharex=False)
        axs[0].bar(range(self.l + 1), self.contributions)
        axs[0].set_title('Contributions')
        axs[0].set_xlabel('Year')
        axs[1].bar(range(self.l + 1), self.distributions)
        axs[1].set_title('Distributions')
        axs[1].set_xlabel('Year')
        axs[2].bar(range(self.l + 1), self.navs)
        axs[2].set_title('NAV')
        axs[2].set_xlabel('Year')
        plt.tight_layout()

        THIS_FOLDER = Path(__file__).parent.parent.resolve()
        my_file = THIS_FOLDER / "media/ic.jpg"
        plt.savefig(my_file)
        # plt.show()
        return res


# Create the widgets for the input parameters
rc_slider = widgets.FloatSlider(min=0, max=1, step=0.01, value=0.25, description='Contr. Shape')
cc_slider = widgets.FloatSlider(min=1000, max=50000, step=100, value=10000, description='Total Invest')
l_slider = widgets.IntSlider(min=1, max=20, step=1, value=12, description='Inv. horizon')
g_slider = widgets.FloatSlider(min=-0.5, max=0.5, step=0.01, value=0.10, description='p.a growth')
b_slider = widgets.FloatSlider(min=0, max=10, step=1, value=0.5, description='Dist.Shape')
y_slider = widgets.FloatSlider(min=0, max=1, step=0.01, value=0.05, description='Distr. rate')
output = widgets.Output()


# Define a function to create an instance of the Investment class and compute the results
def calculate_results(rc, cc, l, g, b, y):
    investment = Investment(rc=rc, cc=cc, l=l, g=g, b=b, y=y)
    # output.clear_output(wait=True)
    # with output:
    res = investment.compute()
    return res


# Create a button widget and attach the calculate_results function to it
calculate_button = widgets.Button(description='Calculate')


def on_calculate_button_clicked(b):
    calculate_results(
        rc_slider.value,
        cc_slider.value,
        l_slider.value,
        g_slider.value,
        b_slider.value,
        y_slider.value
    )


# calculate_button.on_click(on_calculate_button_clicked)

# Display the widgets
# widgets.VBox([
#     rc_slider,
#     cc_slider,
#     l_slider,
#     g_slider,
#     b_slider,
#     y_slider,
#     calculate_button,
#     output
# ])

# calculate_results(0.5, 10000, 10, 0.12, 5, 0.3)
