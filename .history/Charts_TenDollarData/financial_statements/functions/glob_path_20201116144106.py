import glob
print(glob.glob("D:\\Cloud\\rclone\\OneDrive\\Web\\TenDollarData\\Charts_TenDollarData\\financial_statements\\data\\Historical Financial Statements\\*"))
print(glob.glob("D:\\Cloud\\rclone\\OneDrive\\Web\\TenDollarData\\Charts_TenDollarData\\financial_statements\\data\\Historical Financial Statements\\*\\year\\{}\\*_{}_*".format(subject,symbol))[-1])