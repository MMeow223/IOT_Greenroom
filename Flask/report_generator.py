import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF

data = [
{"type":"header","version":"5.2.1","comment":"Export to JSON plugin for PHPMyAdmin"},
{"type":"database","name":"iot_greenroom"},
{"type":"table","name":"air_moisture_actuator_activity","database":"iot_greenroom","data":
[
{"id":"1","action":"1","timestamp":"2023-11-05 15:05:42","greenroom_id":"1"},
{"id":"2","action":"1","timestamp":"2023-11-05 15:05:45","greenroom_id":"1"},
{"id":"3","action":"1","timestamp":"2023-11-05 15:05:46","greenroom_id":"1"},
{"id":"4","action":"1","timestamp":"2023-11-05 15:05:46","greenroom_id":"1"},
{"id":"5","action":"1","timestamp":"2023-11-05 15:05:46","greenroom_id":"1"},
{"id":"6","action":"1","timestamp":"2023-11-05 15:05:46","greenroom_id":"1"},
{"id":"7","action":"1","timestamp":"2023-11-05 15:05:46","greenroom_id":"1"},
{"id":"8","action":"1","timestamp":"2023-11-05 15:05:47","greenroom_id":"1"},
{"id":"9","action":"1","timestamp":"2023-11-05 15:05:47","greenroom_id":"1"},
{"id":"10","action":"1","timestamp":"2023-11-05 15:05:47","greenroom_id":"1"},
{"id":"11","action":"1","timestamp":"2023-11-05 15:05:47","greenroom_id":"1"},
{"id":"12","action":"1","timestamp":"2023-11-05 15:05:47","greenroom_id":"1"},
{"id":"13","action":"1","timestamp":"2023-11-05 15:05:47","greenroom_id":"1"},
{"id":"14","action":"1","timestamp":"2023-11-05 15:05:49","greenroom_id":"2"},
{"id":"15","action":"1","timestamp":"2023-11-05 15:05:49","greenroom_id":"2"},
{"id":"16","action":"1","timestamp":"2023-11-05 15:05:49","greenroom_id":"2"},
{"id":"17","action":"1","timestamp":"2023-11-05 15:05:50","greenroom_id":"2"},
{"id":"18","action":"1","timestamp":"2023-11-05 15:05:50","greenroom_id":"2"},
{"id":"19","action":"1","timestamp":"2023-11-05 15:05:50","greenroom_id":"2"},
{"id":"20","action":"1","timestamp":"2023-11-05 15:05:50","greenroom_id":"2"},
{"id":"21","action":"1","timestamp":"2023-11-05 15:05:50","greenroom_id":"2"},
{"id":"22","action":"1","timestamp":"2023-11-05 15:05:50","greenroom_id":"2"},
{"id":"23","action":"1","timestamp":"2023-11-05 15:05:51","greenroom_id":"2"},
{"id":"24","action":"1","timestamp":"2023-11-05 15:05:51","greenroom_id":"2"}
]
}
,{"type":"table","name":"air_moisture_sensor","database":"iot_greenroom","data":
[
{"id":"1","value":"10.00","timestamp":"2023-11-05 15:05:23","greenroom_id":"1"},
{"id":"2","value":"10.00","timestamp":"2023-11-05 15:05:25","greenroom_id":"1"},
{"id":"3","value":"10.00","timestamp":"2023-11-05 15:05:28","greenroom_id":"1"},
{"id":"4","value":"10.00","timestamp":"2023-11-05 15:05:28","greenroom_id":"1"},
{"id":"5","value":"10.00","timestamp":"2023-11-05 15:05:29","greenroom_id":"1"},
{"id":"6","value":"10.00","timestamp":"2023-11-05 15:05:29","greenroom_id":"1"},
{"id":"7","value":"10.00","timestamp":"2023-11-05 15:05:29","greenroom_id":"1"},
{"id":"8","value":"10.00","timestamp":"2023-11-05 15:05:29","greenroom_id":"1"},
{"id":"9","value":"10.00","timestamp":"2023-11-05 15:05:29","greenroom_id":"1"},
{"id":"10","value":"10.00","timestamp":"2023-11-05 15:05:29","greenroom_id":"1"},
{"id":"11","value":"10.00","timestamp":"2023-11-05 15:05:30","greenroom_id":"1"},
{"id":"12","value":"10.00","timestamp":"2023-11-05 15:05:30","greenroom_id":"1"},
{"id":"13","value":"10.00","timestamp":"2023-11-05 15:05:32","greenroom_id":"2"},
{"id":"14","value":"10.00","timestamp":"2023-11-05 15:05:32","greenroom_id":"2"},
{"id":"15","value":"10.00","timestamp":"2023-11-05 15:05:32","greenroom_id":"2"},
{"id":"16","value":"10.00","timestamp":"2023-11-05 15:05:32","greenroom_id":"2"},
{"id":"17","value":"10.00","timestamp":"2023-11-05 15:05:32","greenroom_id":"2"},
{"id":"18","value":"10.00","timestamp":"2023-11-05 15:05:32","greenroom_id":"2"},
{"id":"19","value":"10.00","timestamp":"2023-11-05 15:05:33","greenroom_id":"2"},
{"id":"20","value":"10.00","timestamp":"2023-11-05 15:05:33","greenroom_id":"2"},
{"id":"21","value":"10.00","timestamp":"2023-11-05 15:05:33","greenroom_id":"2"},
{"id":"22","value":"10.00","timestamp":"2023-11-05 15:05:33","greenroom_id":"2"},
{"id":"23","value":"10.00","timestamp":"2023-11-05 15:05:33","greenroom_id":"2"}
]
}
,{"type":"table","name":"greenroom","database":"iot_greenroom","data":
[
{"greenroom_id":"1","name":"GreenRoom1","location":"Lab","description":"This is greenroom 1","image":"default.png"},
{"greenroom_id":"2","name":"Greenroom2","location":"House","description":"This is Greenroom 2","image":"default.png"}
]
}
,{"type":"table","name":"light_actuator_activity","database":"iot_greenroom","data":
[
{"id":"1","action":"1","timestamp":"2023-11-05 15:05:06","greenroom_id":"1"},
{"id":"2","action":"1","timestamp":"2023-11-05 15:05:09","greenroom_id":"1"},
{"id":"3","action":"1","timestamp":"2023-11-05 15:05:10","greenroom_id":"1"},
{"id":"4","action":"1","timestamp":"2023-11-05 15:05:10","greenroom_id":"1"},
{"id":"5","action":"1","timestamp":"2023-11-05 15:05:10","greenroom_id":"1"},
{"id":"6","action":"1","timestamp":"2023-11-05 15:05:10","greenroom_id":"1"},
{"id":"7","action":"1","timestamp":"2023-11-05 15:05:10","greenroom_id":"1"},
{"id":"8","action":"1","timestamp":"2023-11-05 15:05:11","greenroom_id":"1"},
{"id":"9","action":"1","timestamp":"2023-11-05 15:05:11","greenroom_id":"1"},
{"id":"10","action":"1","timestamp":"2023-11-05 15:05:11","greenroom_id":"1"},
{"id":"11","action":"1","timestamp":"2023-11-05 15:05:11","greenroom_id":"1"},
{"id":"12","action":"1","timestamp":"2023-11-05 15:05:13","greenroom_id":"2"},
{"id":"13","action":"1","timestamp":"2023-11-05 15:05:13","greenroom_id":"2"},
{"id":"14","action":"1","timestamp":"2023-11-05 15:05:14","greenroom_id":"2"},
{"id":"15","action":"1","timestamp":"2023-11-05 15:05:14","greenroom_id":"2"},
{"id":"16","action":"1","timestamp":"2023-11-05 15:05:14","greenroom_id":"2"},
{"id":"17","action":"1","timestamp":"2023-11-05 15:05:14","greenroom_id":"2"},
{"id":"18","action":"1","timestamp":"2023-11-05 15:05:14","greenroom_id":"2"},
{"id":"19","action":"1","timestamp":"2023-11-05 15:05:14","greenroom_id":"2"},
{"id":"20","action":"1","timestamp":"2023-11-05 15:05:15","greenroom_id":"2"}
]
}
,{"type":"table","name":"light_sensor","database":"iot_greenroom","data":
[
{"id":"1","value":"41.00","timestamp":"2023-10-26 02:00:16","greenroom_id":"2"},
{"id":"2","value":"41.00","timestamp":"2023-10-26 02:00:19","greenroom_id":"2"},
{"id":"3","value":"41.00","timestamp":"2023-10-26 02:00:25","greenroom_id":"2"},
{"id":"4","value":"41.00","timestamp":"2023-10-26 02:00:25","greenroom_id":"2"},
{"id":"5","value":"41.00","timestamp":"2023-10-26 02:00:25","greenroom_id":"2"},
{"id":"6","value":"41.00","timestamp":"2023-10-26 02:00:25","greenroom_id":"2"},
{"id":"7","value":"41.00","timestamp":"2023-10-26 02:00:26","greenroom_id":"2"},
{"id":"8","value":"41.00","timestamp":"2023-10-26 02:00:26","greenroom_id":"2"},
{"id":"9","value":"41.00","timestamp":"2023-10-26 02:00:26","greenroom_id":"2"},
{"id":"10","value":"41.00","timestamp":"2023-10-26 02:00:26","greenroom_id":"2"},
{"id":"11","value":"41.00","timestamp":"2023-10-26 02:00:26","greenroom_id":"2"},
{"id":"12","value":"41.00","timestamp":"2023-10-26 02:00:26","greenroom_id":"2"},
{"id":"13","value":"41.00","timestamp":"2023-10-26 02:00:27","greenroom_id":"2"}
]
}
,{"type":"table","name":"soil_moisture_actuator_activity","database":"iot_greenroom","data":
[
{"id":"1","action":"1","timestamp":"2023-11-05 15:01:54","greenroom_id":"1"},
{"id":"2","action":"1","timestamp":"2023-11-05 15:02:08","greenroom_id":"1"},
{"id":"3","action":"1","timestamp":"2023-11-05 15:02:09","greenroom_id":"1"},
{"id":"4","action":"1","timestamp":"2023-11-05 15:02:10","greenroom_id":"1"},
{"id":"5","action":"1","timestamp":"2023-11-05 15:02:10","greenroom_id":"1"},
{"id":"6","action":"1","timestamp":"2023-11-05 15:02:10","greenroom_id":"1"},
{"id":"7","action":"1","timestamp":"2023-11-05 15:02:10","greenroom_id":"1"},
{"id":"8","action":"1","timestamp":"2023-11-05 15:04:54","greenroom_id":"1"}
]
}
,{"type":"table","name":"soil_moisture_sensor","database":"iot_greenroom","data":
[
{"id":"1","value":"10.00","timestamp":"2023-10-23 17:20:33","greenroom_id":"1"},
{"id":"2","value":"21.00","timestamp":"2023-10-24 20:51:58","greenroom_id":"1"},
{"id":"3","value":"21.00","timestamp":"2023-10-24 20:52:02","greenroom_id":"1"},
{"id":"4","value":"21.00","timestamp":"2023-10-24 20:52:10","greenroom_id":"1"},
{"id":"5","value":"21.00","timestamp":"2023-10-24 20:52:11","greenroom_id":"1"},
{"id":"6","value":"21.00","timestamp":"2023-10-24 20:52:12","greenroom_id":"1"},
{"id":"7","value":"33.00","timestamp":"2023-10-24 20:52:27","greenroom_id":"1"},
{"id":"8","value":"21.00","timestamp":"2023-10-24 20:52:12","greenroom_id":"1"},
{"id":"9","value":"21.00","timestamp":"2023-10-24 20:52:12","greenroom_id":"1"},
{"id":"10","value":"21.00","timestamp":"2023-10-24 20:52:12","greenroom_id":"1"},
{"id":"11","value":"55.00","timestamp":"2023-10-24 20:52:31","greenroom_id":"1"},
{"id":"12","value":"21.00","timestamp":"2023-10-24 20:52:13","greenroom_id":"1"},
{"id":"13","value":"21.00","timestamp":"2023-10-24 20:52:13","greenroom_id":"1"},
{"id":"14","value":"21.00","timestamp":"2023-10-24 20:52:13","greenroom_id":"1"},
{"id":"15","value":"21.00","timestamp":"2023-10-24 20:52:13","greenroom_id":"1"},
{"id":"16","value":"21.00","timestamp":"2023-10-24 20:52:14","greenroom_id":"1"},
{"id":"17","value":"21.00","timestamp":"2023-10-24 20:52:14","greenroom_id":"1"},
{"id":"18","value":"21.00","timestamp":"2023-10-24 20:52:14","greenroom_id":"1"},
{"id":"19","value":"21.00","timestamp":"2023-10-24 20:52:14","greenroom_id":"1"},
{"id":"20","value":"21.00","timestamp":"2023-10-24 20:52:14","greenroom_id":"1"},
{"id":"21","value":"21.00","timestamp":"2023-10-24 20:52:14","greenroom_id":"1"},
{"id":"22","value":"21.00","timestamp":"2023-10-24 20:52:15","greenroom_id":"1"},
{"id":"23","value":"21.00","timestamp":"2023-10-24 20:52:15","greenroom_id":"1"},
{"id":"24","value":"21.00","timestamp":"2023-10-24 20:52:15","greenroom_id":"1"},
{"id":"25","value":"21.00","timestamp":"2023-10-24 20:52:15","greenroom_id":"1"},
{"id":"26","value":"21.00","timestamp":"2023-10-24 20:52:15","greenroom_id":"1"},
{"id":"27","value":"21.00","timestamp":"2023-10-24 20:52:15","greenroom_id":"1"},
{"id":"28","value":"21.00","timestamp":"2023-10-26 02:16:14","greenroom_id":"1"},
{"id":"29","value":"21.00","timestamp":"2023-10-26 02:16:27","greenroom_id":"2"},
{"id":"30","value":"21.00","timestamp":"2023-10-26 02:16:30","greenroom_id":"1"},
{"id":"31","value":"21.00","timestamp":"2023-10-26 02:16:22","greenroom_id":"2"},
{"id":"32","value":"21.00","timestamp":"2023-10-26 02:16:24","greenroom_id":"1"},
{"id":"33","value":"21.00","timestamp":"2023-10-26 02:16:17","greenroom_id":"1"},
{"id":"34","value":"21.00","timestamp":"2023-10-26 02:16:20","greenroom_id":"2"}
]
}
,{"type":"table","name":"temperature_actuator_activity","database":"iot_greenroom","data":
[
{"id":"1","action":"1","timestamp":"2023-11-05 15:00:23","greenroom_id":"1"},
{"id":"2","action":"1","timestamp":"2023-11-05 15:00:31","greenroom_id":"1"},
{"id":"3","action":"1","timestamp":"2023-11-05 15:00:32","greenroom_id":"1"},
{"id":"4","action":"1","timestamp":"2023-11-05 15:00:33","greenroom_id":"1"},
{"id":"5","action":"1","timestamp":"2023-11-05 15:00:33","greenroom_id":"1"},
{"id":"6","action":"1","timestamp":"2023-11-05 15:00:34","greenroom_id":"1"},
{"id":"7","action":"1","timestamp":"2023-11-05 15:00:34","greenroom_id":"1"},
{"id":"8","action":"1","timestamp":"2023-11-05 15:00:36","greenroom_id":"2"},
{"id":"9","action":"1","timestamp":"2023-11-05 15:00:37","greenroom_id":"2"},
{"id":"10","action":"1","timestamp":"2023-11-05 15:00:37","greenroom_id":"2"},
{"id":"11","action":"1","timestamp":"2023-11-05 15:00:37","greenroom_id":"2"},
{"id":"12","action":"1","timestamp":"2023-11-05 15:00:37","greenroom_id":"2"},
{"id":"13","action":"1","timestamp":"2023-11-05 15:00:37","greenroom_id":"2"},
{"id":"14","action":"1","timestamp":"2023-11-05 15:00:37","greenroom_id":"2"},
{"id":"15","action":"1","timestamp":"2023-11-05 15:00:38","greenroom_id":"2"}
]
}
,{"type":"table","name":"temperature_sensor","database":"iot_greenroom","data":
[
{"id":"1","value":"41.00","timestamp":"2023-11-05 15:00:57","greenroom_id":"1"},
{"id":"2","value":"41.00","timestamp":"2023-11-05 15:01:02","greenroom_id":"1"},
{"id":"3","value":"41.00","timestamp":"2023-11-05 15:01:03","greenroom_id":"1"},
{"id":"4","value":"41.00","timestamp":"2023-11-05 15:01:03","greenroom_id":"1"},
{"id":"5","value":"41.00","timestamp":"2023-11-05 15:01:03","greenroom_id":"1"},
{"id":"6","value":"41.00","timestamp":"2023-11-05 15:01:03","greenroom_id":"1"},
{"id":"7","value":"41.00","timestamp":"2023-11-05 15:01:03","greenroom_id":"1"},
{"id":"8","value":"41.00","timestamp":"2023-11-05 15:01:04","greenroom_id":"1"},
{"id":"9","value":"41.00","timestamp":"2023-11-05 15:01:04","greenroom_id":"1"},
{"id":"10","value":"41.00","timestamp":"2023-11-05 15:01:04","greenroom_id":"1"},
{"id":"11","value":"41.00","timestamp":"2023-11-05 15:01:04","greenroom_id":"1"},
{"id":"12","value":"41.00","timestamp":"2023-11-05 15:01:06","greenroom_id":"2"},
{"id":"13","value":"41.00","timestamp":"2023-11-05 15:01:06","greenroom_id":"2"},
{"id":"14","value":"41.00","timestamp":"2023-11-05 15:01:06","greenroom_id":"2"},
{"id":"15","value":"41.00","timestamp":"2023-11-05 15:01:06","greenroom_id":"2"},
{"id":"16","value":"41.00","timestamp":"2023-11-05 15:01:07","greenroom_id":"2"},
{"id":"17","value":"41.00","timestamp":"2023-11-05 15:01:07","greenroom_id":"2"},
{"id":"18","value":"41.00","timestamp":"2023-11-05 15:01:07","greenroom_id":"2"},
{"id":"19","value":"41.00","timestamp":"2023-11-05 15:01:07","greenroom_id":"2"},
{"id":"20","value":"41.00","timestamp":"2023-11-05 15:01:07","greenroom_id":"2"}
]
}
,{"type":"table","name":"water_level_actuator_activity","database":"iot_greenroom","data":
[
{"id":"1","action":"1","timestamp":"2023-11-05 15:01:14","greenroom_id":"1"},
{"id":"2","action":"1","timestamp":"2023-11-05 15:01:16","greenroom_id":"1"},
{"id":"3","action":"1","timestamp":"2023-11-05 15:01:17","greenroom_id":"1"},
{"id":"4","action":"1","timestamp":"2023-11-05 15:01:17","greenroom_id":"1"},
{"id":"5","action":"1","timestamp":"2023-11-05 15:01:18","greenroom_id":"1"},
{"id":"6","action":"1","timestamp":"2023-11-05 15:01:18","greenroom_id":"1"},
{"id":"7","action":"1","timestamp":"2023-11-05 15:01:18","greenroom_id":"1"},
{"id":"8","action":"1","timestamp":"2023-11-05 15:01:18","greenroom_id":"1"},
{"id":"9","action":"1","timestamp":"2023-11-05 15:01:18","greenroom_id":"1"},
{"id":"10","action":"1","timestamp":"2023-11-05 15:01:18","greenroom_id":"1"},
{"id":"11","action":"1","timestamp":"2023-11-05 15:01:19","greenroom_id":"1"},
{"id":"12","action":"1","timestamp":"2023-11-05 15:01:19","greenroom_id":"1"},
{"id":"13","action":"1","timestamp":"2023-11-05 15:01:24","greenroom_id":"2"},
{"id":"14","action":"1","timestamp":"2023-11-05 15:01:24","greenroom_id":"2"},
{"id":"15","action":"1","timestamp":"2023-11-05 15:01:24","greenroom_id":"2"},
{"id":"16","action":"1","timestamp":"2023-11-05 15:01:24","greenroom_id":"2"},
{"id":"17","action":"1","timestamp":"2023-11-05 15:01:24","greenroom_id":"2"},
{"id":"18","action":"1","timestamp":"2023-11-05 15:01:25","greenroom_id":"2"},
{"id":"19","action":"1","timestamp":"2023-11-05 15:01:25","greenroom_id":"2"},
{"id":"20","action":"1","timestamp":"2023-11-05 15:01:25","greenroom_id":"2"},
{"id":"21","action":"1","timestamp":"2023-11-05 15:01:25","greenroom_id":"2"},
{"id":"22","action":"1","timestamp":"2023-11-05 15:01:25","greenroom_id":"2"}
]
}
,{"type":"table","name":"water_level_sensor","database":"iot_greenroom","data":
[
{"id":"1","value":"21.00","timestamp":"2023-11-05 15:01:33","greenroom_id":"2"},
{"id":"2","value":"21.00","timestamp":"2023-11-05 15:01:36","greenroom_id":"2"},
{"id":"3","value":"21.00","timestamp":"2023-11-05 15:01:37","greenroom_id":"2"},
{"id":"4","value":"21.00","timestamp":"2023-11-05 15:01:37","greenroom_id":"2"},
{"id":"5","value":"21.00","timestamp":"2023-11-05 15:01:37","greenroom_id":"2"},
{"id":"6","value":"21.00","timestamp":"2023-11-05 15:01:37","greenroom_id":"2"},
{"id":"7","value":"21.00","timestamp":"2023-11-05 15:01:37","greenroom_id":"2"},
{"id":"8","value":"21.00","timestamp":"2023-11-05 15:01:38","greenroom_id":"2"},
{"id":"9","value":"21.00","timestamp":"2023-11-05 15:01:38","greenroom_id":"2"},
{"id":"10","value":"21.00","timestamp":"2023-11-05 15:01:38","greenroom_id":"2"},
{"id":"11","value":"21.00","timestamp":"2023-11-05 15:01:38","greenroom_id":"2"},
{"id":"12","value":"21.00","timestamp":"2023-11-05 15:01:40","greenroom_id":"1"},
{"id":"13","value":"21.00","timestamp":"2023-11-05 15:01:40","greenroom_id":"1"},
{"id":"14","value":"21.00","timestamp":"2023-11-05 15:01:40","greenroom_id":"1"},
{"id":"15","value":"21.00","timestamp":"2023-11-05 15:01:40","greenroom_id":"1"},
{"id":"16","value":"21.00","timestamp":"2023-11-05 15:01:40","greenroom_id":"1"},
{"id":"17","value":"21.00","timestamp":"2023-11-05 15:01:41","greenroom_id":"1"},
{"id":"18","value":"21.00","timestamp":"2023-11-05 15:01:41","greenroom_id":"1"},
{"id":"19","value":"21.00","timestamp":"2023-11-05 15:01:41","greenroom_id":"1"},
{"id":"20","value":"21.00","timestamp":"2023-11-05 15:01:41","greenroom_id":"1"},
{"id":"21","value":"21.00","timestamp":"2023-11-05 15:01:41","greenroom_id":"1"},
{"id":"22","value":"21.00","timestamp":"2023-11-05 15:01:42","greenroom_id":"1"},
{"id":"23","value":"21.00","timestamp":"2023-11-05 15:01:42","greenroom_id":"1"}
]
}
]


df = pd.DataFrame()
df['Question'] = ["Q1", "Q2", "Q3", "Q4"]
df['Charles'] = [3, 4, 5, 3]
df['Mike'] = [3, 3, 4, 4]

title("Professor Criss's Ratings by Users")
xlabel('Question Number')
ylabel('Score')

c = [2.0, 4.0, 6.0, 8.0]
m = [x - 0.5 for x in c]

xticks(c, df['Question'])

bar(m, df['Mike'], width=0.5, color="#91eb87", label="Mike")
bar(c, df['Charles'], width=0.5, color="#eb879c", label="Charles")

legend()
axis([0, 10, 0, 8])
savefig('barchart.png')

pdf = FPDF()
pdf.add_page()
pdf.set_xy(0, 0)
pdf.set_font('arial', 'B', 12)
pdf.cell(60)
pdf.cell(75, 10, "A Tabular and Graphical Report of Professor Criss's Ratings by Users Charles and Mike", 0, 2, 'C')
pdf.cell(90, 10, " ", 0, 2, 'C')
pdf.cell(-40)
pdf.cell(50, 10, 'Question', 1, 0, 'C')
pdf.cell(40, 10, 'Charles', 1, 0, 'C')
pdf.cell(40, 10, 'Mike', 1, 2, 'C')
pdf.cell(-90)
pdf.set_font('arial', '', 12)
for i in range(0, len(df)):
    pdf.cell(50, 10, '%s' % (df['Question'].iloc[i]), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df.Mike.iloc[i])), 1, 0, 'C')
    pdf.cell(40, 10, '%s' % (str(df.Charles.iloc[i])), 1, 2, 'C')
    pdf.cell(-90)
pdf.cell(90, 10, " ", 0, 2, 'C')
pdf.cell(-30)
pdf.image('barchart.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
pdf.output('test.pdf', 'F')