db.earnings_call_NAS_ALL.aggregate( 
   {$group : {_id : "$tradingSymbol"} });