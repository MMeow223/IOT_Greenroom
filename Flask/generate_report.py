#
# This script generates a PDF report with Anvil
# 
# Read more: https://anvil.works/blog/genrate-pdf-with-python
#

#
# If you are following along with your own app, you will want
# to replace the uplink key on line 32 with your own.
#

# Load and process data with Pandas

import pandas as pd

this_month = pd.read_csv("this_month.csv")
last_month = pd.read_csv("last_month.csv")

combined = this_month.join(last_month.set_index("category"),
                           on="category", rsuffix="_last_month")

print(combined)

records = combined.to_dict('records')

# Connect to Anvil, and render a PDF by passing `records` to
# the `ReportForm` form.

import anvil.server

#### TODO: Replace this uplink key with the key for your own app ####
anvil.server.connect("OINKPQWPR5EEAE3VSWGV2WVE-622WBZDH4QYVBCM6")

import anvil.pdf
import anvil.media

pdf = anvil.pdf.render_form("ReportForm", records)

anvil.media.write_to_file(pdf, "report.pdf")
