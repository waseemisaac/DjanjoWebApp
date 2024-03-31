from django.db import models

class StockData(models.Model):
  ticker = models.CharField(max_length=10)
  date = models.DateField()
  open_price = models.DecimalField(max_digits=10, decimal_places=2)
  close_price = models.DecimalField(max_digits=10, decimal_places=2)

  def _str_(self):
    return f"{self.ticker} - {self.date}"