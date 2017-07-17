db.zacks_earnings_call_dates.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$match: {
			    nextReportDate: {
			      $gte: new Date()
			    }
			}
		},

		// Stage 2
		{
			$lookup: {
			    from: "tickers",
			    localField: "ticker",
			    foreignField: "ticker",
			    as: "matching_tickers"
			}
		},

		// Stage 3
		{
			$match: { 
			     matching_tickers: { 
			           $ne: [] 
			     } 
			}
		},

		// Stage 4
		{
			$group: {
			    _id: {day: "$nextReportDate"},
			    numb: {$sum: 1}
			}
		},

		// Stage 5
		{
			$sort: {
			_id:1
			}
		},

		// Stage 6
		{
			$project: {
			      _id:0,
			    day: "$_id.day",
			    numb:1,
			
			
			}
		},

	]

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
