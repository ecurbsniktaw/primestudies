import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
import io
import os
from   matplotlib.backends.backend_pdf import PdfPages

#----------------------------------------------------------------
# is_prime
#	Given an integer n, return True if n is prime, else False.
#
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# end: is_prime
#----------------------------------------------------------------

@st.dialog("No Gaps to Plot", width="medium")
def plot_dialog(a, b, num_primes):
    if num_primes==0:
        st.write(f"There are no primes from {a} to {b}")
    else:
        st.write(f"There is only 1 prime from {a} to {b}")
    
# End of plot_dialog
#---------------------------------------------------------------

#----------------------------------------------------------------
# primes_to_plot
#
# Generate and display a plot showing the size of gaps between
# consecutive prime numbers.
#
def primes_to_plot(params):

    a = params[0]
    b = params[1]

    gap      = 1
    max_gap  = 1
    n_primes = 0
    n_twins  = 0

    gaps = []
    ndxs = []

    # Build 2 lists: 
    #   number (index) of prime found
    #   gaps between consecutive primes.
    # Also determine maximum gap.
    for n in range(a, b + 1):

        if is_prime(n):
            n_primes = n_primes+1
            gaps.append(gap)
            ndxs.append(n_primes)

            if gap == 2:
                n_twins = n_twins + 1
            if gap > max_gap:
                max_gap = gap
            gap = 1

        else:
            gap = gap + 1

    #
    # If n_primes <= 2 then issue a modal message instead
    # of generating and displaying a plot. Otherwise 
    # generate the plot, display it, and provide a
    # button for downloading it to a PDF file.
    #
    if n_primes <= 1:
        plot_dialog(a, b, n_primes)

    else:
        if len(gaps) > 0:
            avg_gap = round(sum(gaps)/len(gaps), 2)
        else:
            avg_gap = 0

        # Create the plot.
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(ndxs, gaps, linestyle="-", color="#2b8cbe")
        ax.set_xlabel("prime number count", fontsize=8)
        ax.set_ylabel("gap", fontsize=8)
        p_title = f"Prime Number Gaps in the range {a:,} - {b:,}\n{n_primes:,} primes, max gap {max_gap:,}, {n_twins:,} twin prime pairs"
        ax.set_title(p_title, fontsize=8)
        ax.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        # Display the plot.
        st.pyplot(fig)

        # Save the plot to a BytesIO object as PDF
        pdf_buffer = io.BytesIO()
        plt.savefig(pdf_buffer, format="pdf", bbox_inches="tight")
        pdf_buffer.seek(0)

        # Provide a download button for the PDF
        st.download_button(
            label="Download Plot as PDF",
            data=pdf_buffer,
            file_name="matplotlib_plot.pdf",
            mime="application/pdf"
        )

        # Close the Matplotlib figure to free up memory
        plt.close()

# end: primes_to_plot
#----------------------------------------------------------------

#----------------------------------------------------------------
def primes_to_html(params):

    a       = params[0] # start of range
    b       = params[1] # end of range
    columns = params[2] # number of columns in the table
    which   = params[3] # 1=show all values, 2=just primes and gaps

    log_b = round(math.log(b), 2)

    html_top = [
        "<html>",
        "<head>",
        "<style>",
        "table { border-collapse: collapse; font-family: Arial; font-size: 14pt; }",
        "td { width: 50px; height: 30px; text-align: right; padding: 4px; }",
        ".prime { color: blue; font-weight: normal; }",
        ".twin { color: blue; font-style: italic; font-weight: normal}",
        "h5,h4,h3 {margin: 0; padding: 0;}",
        "</style>",
        "</head>",
        "<body>",
        ]

    html_body =[]

    # row will hold the td tags for a row as the table is
    # being generated.
    row      = []

    gap      = 1
    max_gap  = 1
    n_primes = 0
    n_twins  = 0

    gaps = []

    was_twin    = False
    found_prime = False

    #------------------------------------------------------------
    # Walk through the range, counting primes and gaps, 
    # and building rows for the output html table.
    for n in range(a, b + 1):

        if is_prime(n):

            n_primes = n_primes+1
            found_prime = True

            # If the previous prime was the first of a twin
            # prime pair, then this one is the second of that pair.
            if was_twin:
                css_class = "twin"
                was_twin   = False

            # This N is a prime, so if N+2 is also prime, then N
            # is the first member of a twin prime pair.
            ###### DO WE WANT TO CONFIRM THAT N+2 IS IN THE RANGE(?)
            if is_prime(n+2):
                css_class = "twin"
                was_twin   = True
            else:
                css_class = "prime"

            if (gap > max_gap) & (n_primes > 0):
                max_gap = gap

            if gap == 2:
                n_twins = n_twins + 1
                css_class = "twin"

            was_gap = gap
            gaps.append(was_gap)
            gap = 1

        else:
            css_class = ""
            if found_prime:
                gap = gap + 1

        if which == 1: # showing all values in the range
            row.append(f"<td class='{css_class}'>{n:,}</td>")

        else: # just showing primes and gaps
            if css_class == 'twin' or css_class == 'prime':
                row.append(f"<td>{was_gap:,}</td>")
                if len(row) == columns:
                	html_body.append("<tr>" + "".join(row) + "</tr>")
                	row = []
                row.append(f"<td class='{css_class}'>{n:,}</td>")

        if len(row) == columns:
            html_body.append("<tr>" + "".join(row) + "</tr>")
            row = []

    # End of walk through the range.
    #------------------------------------------------------------

    # Add remaining cells if not a full row
    if row:
        html_body.append("<tr>" + "".join(row) + "</tr>")

    html_body.extend(["</table></center>", "</body>", "</html>"])

    if len(gaps) > 0:
        avg_gap = round(sum(gaps)/len(gaps), 2)
    else:
        avg_gap = 0

    numInt = b-a+1

    if n_primes > 1:
        gap_stat_txt  = f" avg {avg_gap:,}, ln({b:,})={log_b:,}"
        gap_stat_max  = f" Gaps: max {max_gap:,} "
    else:
        gap_stat_txt = ""
        gap_stat_max = ""

    html_heading = [
        f"<center><h5>{a:,} - {b:,}: primes in blue, twin primes in italics<br>",
        f"{n_primes:,} prime{'s' if n_primes!=1 else ''},",
        f"{n_twins:,} twin prime pair{'s,' if n_twins!=1 else ','}",
        gap_stat_max,
        gap_stat_txt,
        "</h5><center><table>"
        ]

    html = html_top + html_heading + html_body

    htmlToWrite = "\n".join(html)

    st.markdown(htmlToWrite, unsafe_allow_html=True)

# end: primes_to_html
#----------------------------------------------------------------

#----------------------------------------------------------------
#   update_display
#       Respond to a change in the radio button state:
#       Change the text of the application state 
#       variable named display_text.
#
def update_display(option_name):
    selected_option = st.session_state.my_setting_radio

# end: update_display
#----------------------------------------------------------------

#
# MAIN
#

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .stNumberInput > label p {
        font-size: 1rem;
        font-weight: normal; 
    }
    .block-container {
        padding-top: 2.8rem; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

no_errors = True
type_display = "Table: all numbers"
which = 1

#---------------------------------------------------------------
# Sidebar content
with st.sidebar:

    #-----------------------------------------------------------
    # Radio button for type of output: 
    #   - table of all numbers in the range, primes highlighted
    #   - table of primes and size of gaps between them
    #   - line plot of the gaps
    type_display = st.radio(
        " ",
        ["Table: all numbers", 
        "Table: primes & gaps",
        "Plot: gaps"],
        key="my_setting_radio",
        on_change=update_display,
        args=("my_setting_radio",),
        index=0
    )

    #-----------------------------------------------------------
    # Three input fields:
    #   - Start of range of integers
    #   - End of range
    #   - Number of columns in the table
    #       not visible for plot output option
    a     = st.number_input("Start At:", min_value=1, value=1,   step=1, width=100)
    b     = st.number_input("Go Thru:", min_value=1, value=100, step=1, width=100)
    if type_display != "Plot: gaps":
        cols = st.number_input("Num columns:", min_value=1, value=10, step=1, width=100)

# End of sidebat
#---------------------------------------------------------------

@st.dialog("Invalid Input", width="medium")
def my_dialog(a, b, are_equal):
    if are_equal:
        which = "equal to"
    else:
        which = "greater than"
    st.write(f"First value must be less than the last, but {a} is {which} {b}")

# End of my_dialog
#---------------------------------------------------------------

# Determine which type of display the user has chosen.
if type_display == "Table: all numbers":
    which = 1
else:
    if type_display == "Table: primes & gaps":
        which = 2
    else:
        which = 3

if 'display_text' not in st.session_state:
    st.session_state.display_text = "No option selected yet."

no_errors = True
if b <= a:
    no_errors = False
    my_dialog(a, b, a==b)

#---------------------------------------------------------------
# Additional sidebar content
with st.sidebar:

    ok_to_table = False
    ok_to_plot  = False
    if st.button("Submit") & no_errors:
        if type_display != "Plot: gaps":
            ok_to_table = True
        else:
            ok_to_plot = True

# End of sidebat
#---------------------------------------------------------------

if ok_to_table:
    primes_to_html([a, b, cols, which])
else:
    if ok_to_plot:
        primes_to_plot([a, b])

