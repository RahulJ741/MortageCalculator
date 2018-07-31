from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import numpy as np
from django.views import View
import json, sys
from calculation.formulas import ExcelFormulas
from calculation.forms import MortageForm
# Create your views here.

def calculate(request):
    try:
        mortage = MortageForm()
        # return HttpResponse('Test')
        return render(request,'calculate.html', {'form': mortage})
    except Exception as e:
        print (e, "LLLLLLLLLLLLLL")


def ajax_request_data(request):
    try:
        if request.method == 'POST':
            if request.POST['initial'] == '0':
                loan_amnt = float(request.POST['loan_amnt'])
                interst_rate = float(request.POST['intrest_rate'])
                loan_months = float(request.POST['loan_months'])
                emi_amount = np.pmt((interst_rate/100)/12, loan_months, loan_amnt)
                print (emi_amount,"emi ammount")
                intrest_total = abs((abs(emi_amount)*loan_months) - loan_amnt)
                response = {'status': 200, 'count': round(abs(emi_amount), 2),'intrest': round(intrest_total,2)}
                excel_formula = ExcelFormulas()
                print(excel_formula.CumulativeInterestPaid(.12/12,300,10000000,1,84,0) ,"LLLLLLLLLLLLLLL")
                print (excel_formula.CumPrinc(.12/12,300,10000000,1,84,0), 'Cummalative price')
                return HttpResponse(json.dumps(response))
            elif request.POST['initial'] == '1':
                emi = round(float(request.POST['emi']),0)
                loan_amnt = float(request.POST['loan_amnt'])
                intrest_rate = float(request.POST['intrest_rate'])
                loan_months = int(request.POST['loan_months'])
                installment_paid = int(request.POST['installment_paid'])
                cal_type = int(request.POST['cal_type'])
                number_of_months = int(request.POST['number_of_months'])
                new_roi = float(request.POST['new_roi'])


                new_anno =  return_ammotization(loan_amnt,intrest_rate, new_roi, loan_months, installment_paid, cal_type,number_of_months)
                return HttpResponse(json.dumps(new_anno))
                # ammotization = []
                # update_loan = loan_amnt
                # for cnt in range(1,loan_months+1):
                #     principle = round(emi - ((intrest_rate/100)/12 * update_loan) ,0)
                #     intrest = round(emi - principle, 0)
                #     # update_loan = update_loan - emi
                #     if round(update_loan,0) < emi:
                #         ammotization.append([cnt,round(update_loan,0), emi, intrest, principle, 0])
                #     else:
                #         ammotization.append([cnt,round(update_loan,0), emi, intrest, principle, update_loan-principle])
                #     update_loan = update_loan - principle
                #
                # response = {'status':200, 'data': ammotization}
                # return HttpResponse(json.dumps(response))

    except Exception as e:
        print (e, "Error at ajax_request_data")


def return_ammotization(loan_amount,old_roi, new_roi, old_months, paid_months, case_opt,cust_month):
    try:
        new_rate = (old_roi/100)/12
        new_emi_rate = (new_roi/100)/12
        emi_amount = np.pmt(new_rate, old_months, loan_amount)
        old_intrest_total = abs((abs(emi_amount)*old_months) - loan_amount)
        remaining_principle = get_annotized_ammount(new_rate,loan_amount, old_months, paid_months)
        print (remaining_principle, "Remaining principle")
        if case_opt == 1:
            emi = round(abs(np.pmt(new_emi_rate, old_months-paid_months, remaining_principle)),0)
            new_intrest_total = abs((abs(emi)*old_months-paid_months) - remaining_principle)
            intrest_saved = old_intrest_total - new_intrest_total
            print (emi ,"EMI in case 1",new_intrest_total, "::::::", intrest_saved)
            return_list = get_annotized_list(new_emi_rate, remaining_principle, emi, old_months-paid_months)
            return_list['intrest_saved'] = round(intrest_saved,2)
            return return_list
        elif case_opt == 2:
            emi = round(abs(np.pmt(new_emi_rate, cust_month, remaining_principle)),0)
            new_intrest_total = abs((abs(emi)*cust_month) - remaining_principle)
            intrest_saved = old_intrest_total - new_intrest_total
            print (emi, "EMI in case 2", new_intrest_total, "::::::", intrest_saved)
            return_list = get_annotized_list(new_emi_rate, remaining_principle, emi, cust_month)
            return_list['intrest_saved'] = round(intrest_saved,2)
            return return_list
    except Exception as emp:
        print ('Error occured at the return_ammotization_function', emp)
        print ("line number of error {}".format(sys.exc_info()[-1].tb_lineno))


def get_annotized_ammount(rate, amount, months, months_paid):
    print (rate, amount, months, months_paid, ":::::::::::::::::::OOOOOOOOOOOO")
    monthly_emi = abs(round(np.pmt(rate,months, amount),0))
    print(monthly_emi, "EMI")
    update_amount = amount
    for i in range(1,months_paid+1):
        principle = round(monthly_emi-(rate*update_amount),0)
        print (principle, "::::")
        update_amount -= principle
        print (update_amount, ":P:P:P:P:P:P:P:P:P")

    print (update_amount, "<<<<<<<< Update Amount")
    return update_amount


def get_annotized_list(intrest_rate, loan_amnt, emi,loan_months):
    ammotization = []
    update_loan = loan_amnt
    for cnt in range(1,loan_months+1):
        principle = abs(emi - round(intrest_rate * update_loan ,0))
        intrest = round(emi - principle, 0)
        # update_loan = update_loan - emi
        if round(update_loan,0) < emi:
            ammotization.append([cnt,round(update_loan,0), emi, intrest, principle, 0])
        else:
            ammotization.append([cnt,round(update_loan,0), emi, intrest, principle, update_loan-principle])
        update_loan = update_loan - principle

    response = {'status':200, 'data': ammotization}
    return response
# class Classbased(View):
#     """docstring for Classbased."""
#     def __init__(self):
#         pass
#
#     def get(self, request, *args, **kwargs):
#         pass
#
#     def post(self, request,*arg, **kwargs):
#         pass
