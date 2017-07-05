Some queries
```
db.opositores.aggregate([{$match:{"tribunal.ntribunal":3, "prueba1": {$gt:0}}}, {$sort:{"prueba1":-1}}, {$project:{"_id":0, "apellidos":1, "nombre":1, "prueba1":1}}])
```
