# -*- coding: utf-8 -*-
from __future__ import division
from flask import Flask, render_template, request, Response, send_file
from util.services import *
from util.tomorrow_recommander import tomorrow_recommander

from common import *
import datetime
from dateutil.relativedelta import relativedelta
from util.back_tester import back_tester
from util.stationarity_tester import stationarity_tester
from util.machineLearning_tester import machine_learning_tester
from util.ta_tester import ta_tester
from util.profit_tester import profit_tester
from util.macd_tester import macd_tester

app = Flask(__name__)


def init():
    parentPath = os.path.abspath("..")
    if parentPath not in sys.path:
        sys.path.insert(0, parentPath)
    services.register('configurator', Configurator())
    # services.get('configurator').register('input_column', ['Open', 'High','Low', 'Close',  'Volume', 'kospi', 'kospi_volume'])
    # services.get('configurator').register('input_column', ['Close', 'Volume','kospi','kospi_volume'])
    # services.get('configurator').register('input_column',
    #                                       ['Open', 'High', 'Low', 'Close', 'Volume', 'kospi','kospi_volume', 'SMA', 'BBANDS_upper',
    #                                        'BBANDS_middle', 'BBANDS_lower',], )
    services.get('configurator').register('input_column',
                                          ['Open', 'High', 'Low', 'Close', 'Volume', 'kospi', 'kospi_volume', 'SMA',
                                           'BBANDS_upper', 'BBANDS_middle', 'BBANDS_lower', "MOM", "STOCH_slowk",
                                           "STOCH_slowd"
                                              , "MACD_macd", "MACD_signal", "MACD_hist"], )
    # services.get('configurator').register('input_column', ['Close', 'Volume'])

    # services.get('configurator').register('input_column', ['Close', 'Volume'])
    # services.get('configurator').register('input_column',['Close','Volume','Open'])

    """
    'SMA','BBANDS_upper','BBANDS_middle','BBANDS_lower',"MOM","STOCH_slowk","STOCH_slowd"
    ,"MACD_macd","MACD_signal","MACD_hist"
    """

    services.get('configurator').register('output_column', 'Close_Direction')



if __name__ == "__main__":
    init()
    end = datetime.datetime.today()
    start = end - relativedelta(months=6)

    # end = datetime.datetime.strptime('20170519', '%Y%m%d')
    # start = end - relativedelta(months=3)

    tomorrow_recommander = tomorrow_recommander()
    # tomorrow_recommander.tomorrow_recommand_stock(end=end, is_update_stock=True, last_month=3, window=10)
    # tomorrow_recommander.recommand_draw('2017-05-10')
    # tomorrow_recommander.recommand_draw()


    # start = datetime.datetime.strptime('20160115', '%Y%m%d')
    # end = datetime.datetime.strptime('20170515', '%Y%m%d')
    # start = end - relativedelta(months=6)

    stationarity_tester = stationarity_tester()
    # stationarity_tester.stationarity_per_day(code='023530', start=start, end=end, view_chart=True, window=10)
    # stationarity_tester.stationarity_per_day(code='036570', start=start, end=end, view_chart=False, window=10)
    # stationarity_tester.stationarity_per_day(code='012330', start=start, end=end, view_chart=False, window=10)

    back_tester = back_tester()
    # back_tester.run()
    # back_tester.run_series()

    code_list = []
    data = load_yaml('kospi100')
    for company_code, value in data.iterItems():
        code_list.append(company_code)

    machine_learning_recommander = machine_learning_tester()
    # for i in [1, 2, 5]:
    #      machine_learning_recommander.show_machine_learning(code_list, False, start, end, i)
    # machine_learning_recommander.show_machine_learning(code_list, False, start, end, 1)

    # for i in [1, 2, 3, 4, 5, 7, 10]:
    #     machine_learning_recommander.trading_machine_learning('114090', start, end, False, 4)
    # machine_learning_recommander.trading_machine_learning('047040', start, end, False, 1)
    # machine_learning_recommander.trading_machine_learning('047040', start, end, True, 10)

    ta_tester = ta_tester()
    # ta_tester.test('008770')

    macd_tester = macd_tester()
    # macd_tester.show_profit(start=start, end=end, view_chart=False, last_day_sell=True)
    # df = get_df_from_file('012330', start, end)
    # macd_tester.train_macd_vaule(df=df, last_day_sell=True)
    # macd_tester.show_profit_total_all_kospi(start, end, view_chart=False, last_day_sell=True)
    # macd_tester.show(df, 6, 29, 13, last_day_sell=True)


    profit_tester = profit_tester()
    # profit_tester.profit_print_kospi200('20160510')
    # profit_tester.profit_print_all_today()
    # profit_tester.profit_print_all_with_sell_today()
    profit_tester.profit_print_all_with_sell()
    # profit_tester.code_profit(code='128940', start='2017-05-10')


    # app.debug = True
    # app.run(host='0.0.0.0', port=services.get('configurator').get('trbs_master_port'))
