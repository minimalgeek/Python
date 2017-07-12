var cursor = db.zacks_earnings_call_dates.aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$project: {
			 ab: {$cmp: ['$nextReportDate','$previousReportDate']},
			 ticker: 1,
			 nextReportDate: 1,
			 previousReportDate: 1
			}
		},

		// Stage 2
		{
			$match: {ab:{$eq:0}}
		},

		// Stage 3
		{
			$sort: {
				ticker:1,
				nextReportDate:1
			}
		},

	]

);

cursor.forEach(function (doc){
    db.zacks_earnings_call_dates.remove({"_id": doc._id});
});
