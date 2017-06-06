db.earnings_call_NAS_ALL.aggregate( 
   {$group : {_id : "$tradingSymbol"} }, 
   {$group: {_id:1, count: {$sum : 1 }}});