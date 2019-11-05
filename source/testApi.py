# -*- coding: utf-8 -*-
from __future__ import division
import pythoncom
import win32com.client as winAPI
import datetime
import win32com.client
import pythoncom
import os, sys

SERVER_PORT = 20001
SHOW_CERTIFICATE_ERROR_DIALOG = False
REPEATED_DATA_QUERY = 1
TRANSACTION_REQUEST_EXCESS = -21
TODAY = datetime.datetime.now().strftime('%Y%m%d')


import os,sys,inspect
import pathlib
import inspect
from time import sleep
from pandas import DataFrame, Series, Panel
import pandas as pd

from util.StockManager import *

STAND_BY = 0
RECEIVED = 1

today_list = ['032350', '014820', '012630', '033180', '005690', '002990', '002210', '019170', '016580', '006490']
id = ""
password = ""
certificate_password = ""

class XASessionEvents:
    login_state = STAND_BY

    def OnLogin(self, code, msg):
        XASessionEvents.login_state = RECEIVED
        print(msg)
        if code == "0000":
            print("로그인 성공")
            XASessionEvents.login_state = 1
        else:
            print("로그인 실패")

    def OnDisconnect(self, code, msg):
       pass


class XAQueryEvents:
    query_state = STAND_BY

    def OnReceiveData(self, code):
        XAQueryEvents.query_state = RECEIVED

    def OnReceiveMessage(self, error, nMessageCode, szMessage):
        print(szMessage)

class XAQueryEvents:
    상태 = False

    def OnReceiveData(self, szTrCode):
        print("OnReceiveData : %s" % szTrCode)
        XAQueryEvents.상태 = True

    def OnReceiveMessage(self, systemError, messageCode, message):
        print("OnReceiveMessage : ", systemError, messageCode, message)


class Trade():
    def __init__(self, debug):
        if debug:
            return
        print('init')

        self.instXASession = winAPI.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
        if self.instXASession.IsConnected() is True:
            self.instXASession.DisconnectServer()

        # demo.ebestsec.co.kr => 모의투자
        # hts.ebestsec.co.kr => 실투자
        self.instXASession.ConnectServer("hts.ebestsec.co.kr", SERVER_PORT)
        self.instXASession.Login(id, password, certificate_password, SERVER_PORT, SHOW_CERTIFICATE_ERROR_DIALOG)

        while XASessionEvents.login_state is STAND_BY:
            pythoncom.PumpWaitingMessages()
        XASessionEvents.login_state = STAND_BY

    def check_realTime_stoks(self):
        print('check_realTime_stoks')

        today = datetime.date.today()
        startTime = datetime.datetime(today.year, today.month, today.day, 9, 0, 0)
        endTime = datetime.datetime(today.year, today.month, today.day, 15, 30, 0)

        while True:
            if ( datetime.datetime.now() < startTime):
                print('Before[%s]' %( datetime.datetime.now()))
                sleep(5)  # 10 -> 1분
                continue
            if ( datetime.datetime.now() > endTime):
                break

            log_folder = ('log/%s' % (TODAY))
            if not os.path.exists(log_folder):
                pathlib.Path(log_folder).mkdir(parents=True, exist_ok=True)

            for code in today_list:
                # self.get_status_code(code)
                df0, df = self.t1302(단축코드=code, 작업구분='1', 시간='1', 건수='1')
                df.to_csv('log/%s/%s_%s.csv' % (TODAY, TODAY, code), mode='a', index=False, header=False)
                sleep(3) # 1초

    def t1302(self, 단축코드='', 작업구분='1', 시간='1', 건수='1'):
        '''
        주식분별주가조회
        '''
        query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        pathname = os.path.dirname(sys.argv[0])
        RESDIR = os.path.abspath(pathname)

        MYNAME = inspect.currentframe().f_code.co_name
        INBLOCK = "%sInBlock" % MYNAME
        OUTBLOCK = "%sOutBlock" % MYNAME
        OUTBLOCK1 = "%sOutBlock1" % MYNAME
        RESFILE = "%s\\Res\\%s.res" % (RESDIR, MYNAME)

        query.LoadFromResFile(RESFILE)
        query.SetFieldData(INBLOCK, "shcode", 0, 단축코드)
        query.SetFieldData(INBLOCK, "gubun", 0, 작업구분)
        query.SetFieldData(INBLOCK, "time", 0, 시간)
        query.SetFieldData(INBLOCK, "cnt", 0, 건수)
        query.Request(0)

        while XAQueryEvents.상태 == False:
            pythoncom.PumpWaitingMessages()

        result = []
        nCount = query.GetBlockCount(OUTBLOCK)
        for i in range(nCount):
            시간CTS = query.GetFieldData(OUTBLOCK, "cts_time", i).strip()

            lst = [시간CTS]
            result.append(lst)

        df = DataFrame(data=result, columns=['시간CTS'])

        result = []
        nCount = query.GetBlockCount(OUTBLOCK1)
        for i in range(nCount):
            시간 = query.GetFieldData(OUTBLOCK1, "chetime", i).strip()
            종가 = int(query.GetFieldData(OUTBLOCK1, "close", i).strip())
            전일대비구분 = query.GetFieldData(OUTBLOCK1, "sign", i).strip()
            전일대비 = int(query.GetFieldData(OUTBLOCK1, "change", i).strip())
            등락율 = float(query.GetFieldData(OUTBLOCK1, "diff", i).strip())
            체결강도 = float(query.GetFieldData(OUTBLOCK1, "chdegree", i).strip())
            매도체결수량 = int(query.GetFieldData(OUTBLOCK1, "mdvolume", i).strip())
            매수체결수량 = int(query.GetFieldData(OUTBLOCK1, "msvolume", i).strip())
            순매수체결량 = int(query.GetFieldData(OUTBLOCK1, "revolume", i).strip())
            매도체결건수 = int(query.GetFieldData(OUTBLOCK1, "mdchecnt", i).strip())
            매수체결건수 = int(query.GetFieldData(OUTBLOCK1, "mschecnt", i).strip())
            순체결건수 = int(query.GetFieldData(OUTBLOCK1, "rechecnt", i).strip())
            거래량 = int(query.GetFieldData(OUTBLOCK1, "volume", i).strip())
            시가 = int(query.GetFieldData(OUTBLOCK1, "open", i).strip())
            고가 = int(query.GetFieldData(OUTBLOCK1, "high", i).strip())
            저가 = int(query.GetFieldData(OUTBLOCK1, "low", i).strip())
            체결량 = int(query.GetFieldData(OUTBLOCK1, "cvolume", i).strip())
            매도체결건수시간 = int(query.GetFieldData(OUTBLOCK1, "mdchecnttm", i).strip())
            매수체결건수시간 = int(query.GetFieldData(OUTBLOCK1, "mschecnttm", i).strip())
            매도잔량 = int(query.GetFieldData(OUTBLOCK1, "totofferrem", i).strip())
            매수잔량 = int(query.GetFieldData(OUTBLOCK1, "totbidrem", i).strip())
            시간별매도체결량 = int(query.GetFieldData(OUTBLOCK1, "mdvolumetm", i).strip())
            시간별매수체결량 = int(query.GetFieldData(OUTBLOCK1, "msvolumetm", i).strip())

            lst = [시간, 단축코드, 종가, 전일대비구분, 전일대비, 등락율, 체결강도, 매도체결수량, 매수체결수량, 순매수체결량, 매도체결건수, 매수체결건수, 순체결건수, 거래량, 시가, 고가, 저가, 체결량,
                   매도체결건수시간, 매수체결건수시간, 매도잔량, 매수잔량, 시간별매도체결량, 시간별매수체결량]
            result.append(lst)

        df1 = DataFrame(data=result,
                        columns=[시간, 단축코드, 종가, 전일대비구분, 전일대비, 등락율, 체결강도, 매도체결수량, 매수체결수량, 순매수체결량, 매도체결건수, 매수체결건수, 순체결건수, 거래량, 시가, 고가, 저가, 체결량,
                   매도체결건수시간, 매수체결건수시간, 매도잔량, 매수잔량, 시간별매도체결량, 시간별매수체결량])

        XAQueryEvents.상태 = False

        return (df, df1)

    def file_test(self):
        for code in today_list:
            df = pd.read_csv('log/%s/%s_%s.csv' % (TODAY, TODAY, code),
                             names=['시간', '단축코드', '종가', '전일대비구분', '전일대비', '등락율', '체결강도', '매도체결수량', '매수체결수량', '순매수체결량',
                                    '매도체결건수',
                                    '매수체결건수', '순체결건수', '거래량', '시가', '고가', '저가', '체결량', '매도체결건수시간', '매수체결건수시간', '매도잔량',
                                    '매수잔량', '시간별매도체결량', '시간별매수체결량'])

            fig, axs = plt.subplots(2)
            ax = axs[0]
            ax.plot(df['종가'])
            ax.grid(True)

            ax = axs[1]
            ax.plot(df['거래량'])
            ax.plot(df['체결량'])
            ax.grid(True)

            plt.show()

if __name__ == "__main__":
    debug_mode = False
    Trade = Trade(debug=debug_mode)
    if debug_mode:
        Trade.file_test()
    else:
        Trade.check_realTime_stoks()