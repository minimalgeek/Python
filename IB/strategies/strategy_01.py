from .strategy import Strategy
from .trade_signal import *

class Strategy01(Strategy):
    def __init__(self, *args, **kwargs):
        super(Strategy01, self).__init__(*args, **kwargs)

    def run(self):
        """
        Check h_tone of current and previous transcript
            increase: long
            decrease: short
        Check portfolio
            signal: long   short
            long    T      LCSO
            short   SCLO   T
        """
        self.info('Run %s', self.name)
        for transcript in self.data:
            symbol = transcript['tradingSymbol']
            self.info('Check %s signal', symbol)
            prev_transcript = transcript['previous']
            if prev_transcript is None:
                self.warning('Previous transcript does not exist for %s', symbol)
                continue

            prev_ratio, ratio = self.calc_ratios(prev_transcript, transcript)
            self.info('%s[Ratio (%f), previous ratio(%f)]', symbol, ratio, prev_ratio)

            if ratio > prev_ratio:
                signal = Buy(ticker=symbol)
            else:
                signal = Sell(ticker=symbol)

            in_portfolio = self.portfolio.get(symbol)
            if in_portfolio is not None:
                self.info('%s exist in portfolio', symbol)
                prev_signal = in_portfolio.get('signal')
                if prev_signal.direction != signal.direction:
                    self.info('Adding signal to queue: %s', str(signal))
                    self.signals.put(Close(ticker=symbol))
                else:
                    signal = None

            if signal is not None:
                self.info('Adding signal to queue: %s', str(signal))
                self.signals.put(signal)


    def calc_ratios(self, prev_transcript, transcript):
        tone = transcript['h_tone']
        ratio = tone['positiveCount'] / tone['negativeCount']
        prev_tone = prev_transcript['h_tone']
        prev_ratio = prev_tone['positiveCount'] / prev_tone['negativeCount']
        return prev_ratio, ratio

    def calc_value(self):
        return 0