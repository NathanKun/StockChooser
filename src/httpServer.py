from genIndicator import plotIndicator

'''
import http.server
import socketserver

PORT = 8000

#Handler = http.server.SimpleHTTPRequestHandler
Handler = http.server.CGIHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.server_name = "test"
httpd.server_port = PORT

print("serving at port", PORT)
httpd.serve_forever()
'''

from flask import Flask, url_for, redirect, render_template, request
app = Flask(__name__, root_path = '/home/wwwroot/catprogrammer.com/stockchooser')

app.debug = True

@app.route('/')
def index():
    return render_template('index.html')
#    return 'a'

@app.route('/stockchooser')
def sc():
#    return render_template('index.html')
    return 'b'


@app.route('/submit', methods=['POST', 'GET'])
def submit(name=None):
    if request.method == 'POST':
        name = request.form['stockName']
        
        import genIndicator as gi
        df = gi.readDataFromNet(name)
        gi.genAll(df)
        
        import matplotlib.pyplot as plt, mpld3  # 2D plotting library
        plotIndicator(df, 'RS')
        rs = mpld3.fig_to_html(plt.gcf())
        plotIndicator(df, 'Bollinger')
        bollinger= mpld3.fig_to_html(plt.gcf())
        plotIndicator(df, 'MA')
        ma = mpld3.fig_to_html(plt.gcf())
        plotIndicator(df, 'MACD')
        macd = mpld3.fig_to_html(plt.gcf())
        plotIndicator(df, 'RSI')
        rsi = mpld3.fig_to_html(plt.gcf())
        plotIndicator(df, 'Stoschastic')
        stoschastic = mpld3.fig_to_html(plt.gcf())
        fig = [rs, bollinger, ma, macd, rsi, stoschastic]
    return render_template('stock.html', name = name, fig = fig)

if __name__ == '__main__':
    app.run(debug=True)
