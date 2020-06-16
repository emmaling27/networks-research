"""Helper functions for getting data and plots into latex formatting"""

def get_plots_into_latex(string1, string2):
    for congress in range(97, 109):
        print(string1 + str(congress) + string2)