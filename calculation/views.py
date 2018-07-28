from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import numpy as np
from django.views import View
import json
from calculation.formulas import ExcelFormulas
# Create your views here.

def calculate(request):
    try:
        # return HttpResponse('Test')
        return render(request,'calculate.html', {})
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
                emi = float(request.POST['emi'])
                loan_amnt = float(request.POST['loan_amnt'])
                intrest_rate = float(request.POST['intrest_rate'])
                loan_months = int(request.POST['loan_months'])

                ammotization = []
                update_loan = loan_amnt
                for cnt in range(1,loan_months+1):
                    principle = abs(round(((intrest_rate/100)/12 * update_loan) - emi ,0))
                    intrest = round(emi - principle, 0)
                    # update_loan = update_loan - emi
                    if round(update_loan,0) < emi:
                        ammotization.append([cnt,round(update_loan,0), emi, intrest, principle, 0])
                    else:
                        ammotization.append([cnt,round(update_loan,0), emi, intrest, principle, update_loan-principle])
                    update_loan = update_loan - principle

                response = {'status':200, 'data': ammotization}
                return HttpResponse(json.dumps(response))

        elif request.method =='GET':
            return render(request, 'header.html', {})
            # return HttpResponse(json.dumps({'status':232, "msg": 456}))
    except Exception as e:
        print (e, "Error at ajax_request_data")



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
