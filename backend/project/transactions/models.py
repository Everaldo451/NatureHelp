from django.db import models
from api.models import User, Company

class Offert(models.Model):

	company = models.OneToOneField(Company, on_delete=models.CASCADE, null=False)
	coin = models.CharField(null=False, choices={
		"USD": "Dólar",
		"BTC": "Bitcoin",
		"EUR": "Euro"
	}, max_length=10)
	value = models.FloatField()
	index_variable= models.CharField(max_length=100)  ####Variaveis como IPCA e Selic
	fees = models.FloatField() ###Juros


class Transaction(models.Model):
	
	buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bought_transactions")
	seller = models.ForeignKey(User, on_delete=models.PROTECT)
	offert = models.ForeignKey(
		Offert, 
		on_delete=models.PROTECT, 
		limit_choices_to={"company.user":seller}
	)

# Create your models here.