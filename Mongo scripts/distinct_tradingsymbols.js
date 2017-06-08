db.earnings_transcript.aggregate( 
   {$group : {_id : "$tradingSymbol"} },
   {$project: {'Symbol': '$_id', '_id':0}});