class ExcelFormulas():
    """docstring for ExcelFormulas."""

    def CumulativeInterestPaid(self,rate, numberOfPayments, presentValue, startPeriod, endPeriod, type):
        if (startPeriod < 1 or endPeriod < startPeriod or rate <= 0.0 or endPeriod > numberOfPayments or numberOfPayments <= 0 or presentValue <= 0.0 or (type != 0 and type != 1)):
            return None

        fRmz = self.GetRmz(rate, numberOfPayments, presentValue, 0.0, type)
        fZinsZ = 0.0
        nStart = startPeriod
        nEnd = endPeriod

        if nStart == 1:
            if type <= 0:
                fZinsZ = -presentValue
            nStart += 1


        for i in range(nStart, nEnd, 1 ):
            if type > 0:
                fZinsZ += self.GetZw(rate, i - 2, fRmz, presentValue, 1) - fRmz
            else:
                fZinsZ += self.GetZw(rate, i - 1, fRmz, presentValue, 0)

        fZinsZ *= rate

        return fZinsZ



    def GetZw(self,fZins,fZzr,fRmz,fBw,nF):
        if fZins == 0.0:
            fZw = fBw + fRmz * fZzr
        else:
            fTerm = pow(1.0 + fZins, fZzr)
            if (nF > 0):
                fZw = fBw * fTerm + fRmz * (1.0 + fZins) * (fTerm - 1.0) / fZins
            else:
                fZw = fBw * fTerm + fRmz * (fTerm - 1.0) / fZins

        return -fZw


    def GetRmz(self,fZins,fZzr,fBw,fZw,nF):
        if fZins == 0.0:
            fRmz = (fBw + fZw) / fZzr
        else:
            fTerm = pow(1.0 + fZins, fZzr)
            if (nF > 0):
                fRmz = (fZw * fZins / (fTerm - 1.0) + fBw * fZins / (1.0 - 1.0 / fTerm)) / (1.0 + fZins)
            else:
                fRmz = fZw * fZins / (fTerm - 1.0) + fBw * fZins / (1.0 - 1.0 / fTerm)

        return -fRmz




    # def CUMPRINC(self,rate, periods, value, start, end, type):
    #     rate = eval(rate)
    #     periods = eval(periods)
    #
    #     #Return error if either rate, periods, or value are lower than or equal to zero
    #     if rate <= 0 or periods <= 0 or value <= 0:
    #         return '#NUM!'
    #
    #     #Return error if start < 1, end < 1, or start > end
    #     if start < 1 or end < 1 or start > end:
    #         return '#NUM!';
    #
    #     #Return error if type is neither 0 nor 1
    #     if type !== 0 and type !== 1:
    #         return '#NUM!';
    #
    #     #Compute cumulative principal
    #     payment = getPartialPayment(rate, periods, value, 0, type)
    #     principal = 0;
    #     if start === 1:
    #         if type === 0:
    #             principal = payment + value * rate
    #         else:
    #             principal = payment
    #         start +=1
    #
    #     for i in range(start, end,1):
    #         if type > 0:
    #             principal += payment - (getFutureValue(rate, i - 2, payment, value, 1) - payment) * rate
    #         else:
    #             principal += payment - getFutureValue(rate, i - 1, payment, value, 0) * rate
    #
    #     return principal



    def CumPrinc(self, rate,periods,pV,start,end,type):
        if type == 1:
            start -= 1
            end -= 1
        monthlyPayment = ((rate * pV * pow((1 + rate), periods)) / (pow((1 + rate), periods) - 1))
        remainingBalanceAtStart = ((pow((1 + rate), start - 1) * pV) - (((pow((1 + rate), start - 1) - 1) / rate) * monthlyPayment))
        remainingBalanceAtEnd = ((pow((1 + rate), end) * pV) - (((pow((1 + rate), end) - 1) / rate) * monthlyPayment))
        return remainingBalanceAtEnd - remainingBalanceAtStart
