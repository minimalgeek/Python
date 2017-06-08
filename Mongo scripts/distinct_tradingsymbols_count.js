db.earnings_transcript.aggregate( 
   {$group : {_id : "$tradingSymbol"} }, 
   {$group: {_id:1, count: {$sum : 1 }}});