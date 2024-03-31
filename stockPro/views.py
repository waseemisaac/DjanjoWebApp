from django.shortcuts import render
from .models import StockData  # Import if you're using the StockData model
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def enter_stock_data(request):
    # This view will display the form
    return render(request, 'form.html')

def fetch_stock_data(request):
    if request.method == 'POST':
        ticker = request.POST.get('ticker')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Fetch the stock data using yfinance
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
        except (yf.DownloadError, Exception) as e:  # Handle potential errors
            error_message = f"Error fetching data: {str(e)}"
            context = {'error_message': error_message}
            return render(request, 'results.html', context)

        # Prepare data for bar chart (assuming you want to plot closing prices)
        dates = stock_data.index.to_pydatetime()
        closing_prices = stock_data['Close'].tolist()
        opening_prices = stock_data['Open'].tolist()

        # Create the bar chart
        plt.figure(figsize=(10, 5))
        plt.bar(dates, closing_prices, label='Close Price',color='black')
        plt.bar(dates, opening_prices, label='Open Price',color='blue')
        plt.xticks(rotation=45)  # Rotate x-axis labels
        plt.title(f'Open and Close Prices for {ticker}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.legend()
        # Convert plot to PNG image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode('utf-8')
        context = {'graphic': graphic, 'ticker': ticker}  # Include ticker for results

        return render(request, 'results.html', context)

    else:
        # Handle non-POST requests (e.g., initial page load)
        return render(request, 'form.html')
