from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import ccxt
import pandas as pd
import ta

class CryptoBotLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        self.title_label = Label(text="BTC/USDT RSI Bot", font_size='24sp', bold=True)
        self.price_label = Label(text="Price: Loading...", font_size='20sp')
        self.rsi_label = Label(text="RSI: Loading...", font_size='20sp')
        self.signal_label = Label(text="Signal: Waiting...", font_size='22sp', bold=True)
        
        self.add_widget(self.title_label)
        self.add_widget(self.price_label)
        self.add_widget(self.rsi_label)
        self.add_widget(self.signal_label)
        
        self.exchange = ccxt.binance({'options': {'defaultType': 'spot'}})
        
        Clock.schedule_interval(self.update_data, 30)
        self.update_data(0)

    def update_data(self, dt):
        try:
            bars = self.exchange.fetch_ohlcv('BTC/USDT', timeframe='15m', limit=100)
            df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
            
            price = df['close'].iloc[-1]
            rsi = df['rsi'].iloc[-1]
            
            self.price_label.text = f"Price: ${price:.2f}"
            self.rsi_label.text = f"RSI: {rsi:.2f}"
            
            if rsi < 30:
                self.signal_label.text = "Signal: BUY"
                self.signal_label.color = (0, 1, 0, 1)
            elif rsi > 70:
                self.signal_label.text = "Signal: SELL"
                self.signal_label.color = (1, 0, 0, 1)
            else:
                self.signal_label.text = "Signal: HOLD"
                self.signal_label.color = (1, 1, 1, 1)
        except Exception as e:
            self.signal_label.text = f"Error: {e}"

class CryptoBotApp(App):
    def build(self):
        return CryptoBotLayout()

if __name__ == "__main__":
    CryptoBotApp().run()
