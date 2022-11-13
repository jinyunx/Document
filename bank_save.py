# -*- coding: UTF-8 -*-
import math

def bank_borrow(rate, month, borrow):
    tmp =  math.pow(1 + rate, month)
    pay = borrow * rate *tmp / (tmp - 1)
    total_pay = pay * month
    return (pay, total_pay)

def bank_save(benjin, month, bank_rate_month):
    return benjin*math.pow(1+bank_rate_month, month)

borrow_rate_month = 4.3/100/12
borrow_month = 336
borrow_total = 300000
bank_save_rate_month = 3/100/12

borrow_pay_month, borrow_pay_total = bank_borrow(borrow_rate_month,borrow_month,borrow_total)
print("已知向银行借了年利率为%.1f的银行贷款%d万元共%d年" %(borrow_rate_month*100*12, borrow_total/10000, borrow_month/12))
print("每月应还:%.1f, 总共应还:%.1f" %(borrow_pay_month, borrow_pay_total))

print("现在有30万该不该还呢？假设存银行年利率是%.1f" %(bank_save_rate_month*12*100))

bank_save_total = borrow_total * math.pow(1+bank_save_rate_month,borrow_month)
print("如果%d万直接存银行，%d年得到的本息和是%.1f" %(borrow_total/10000, borrow_month/12, bank_save_total))

bank_pay_save_total = 0
for i in range(borrow_month-1,-1,-1):
    save = bank_save(borrow_pay_month, i, bank_save_rate_month)
    #print(save)
    bank_pay_save_total += save

print("如果提前还了贷款，把每个月应还%.1f元存到银行，%d年后的本息和是%.1f" %(borrow_pay_month, borrow_month/12, bank_pay_save_total))
if (bank_save_total > bank_pay_save_total):
    print("建议 不提前 还款，这样最终可多赚", bank_save_total - bank_pay_save_total)
elif (bank_save_total < bank_pay_save_total):
    print("建议 提前 还款，这样最终可多赚", bank_pay_save_total - bank_save_total)
else:
    print("都行，一样受益")