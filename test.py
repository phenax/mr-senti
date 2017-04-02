
from libs.MrSenti import MrSenti

senti= MrSenti()

senti.load_dataset()

wasLoadedModel= senti.load_model()

if(not wasLoadedModel):
	senti.train()

prediction = senti.test([
	'This is a great product. I love this product',
	'This is a product sucks. Very bad.',
	'This product sucks balls.',
	'This is fucking great',
	'Baaad. 2 mny bugs'
], True, [ 'pos', 'neg', 'neg', 'pos', 'neg' ])

print(prediction)

if(not wasLoadedModel):
	senti.save()


