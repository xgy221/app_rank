import analysis.tool as tool
import matplotlib.pyplot as plt

session_list = tool.get_leading_session('36400')
y = tool.y

plt.figure()
plt.plot(range(1, 731), y)
plt.ylim(0, 300)
plt.gca().invert_yaxis()
plt.show()

a = 1
