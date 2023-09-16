from pymongo import MongoClient, errors as pymongo_errors

class HourlyRetriever:
    def __init__(self, mongo_handler):
        self.mongo = mongo_handler

    def get_hourly_forecast(self):
        try:
            # Here, I'm providing a general-purpose aggregation pipeline. 
            # Update this according to your database's schema and requirements.
            pipeline = [
    {
        '$match': {
            'hourly': {
                '$exists': True
            }
        }
    },
    {
        '$project': {
            'hours': {
                '$zip': {
                    'inputs': [
                        '$hourly.time',
                        '$hourly.windspeed_10m',
                        '$hourly.winddirection_10m',
                        '$hourly.windgusts_10m'
                    ],
                    'useLongestLength': True
                }
            }
        }
    },
    {
        '$unwind': '$hours'
    },
    {
        '$project': {
            '_id': 0,
            'time': { '$arrayElemAt': ['$hours', 0] },
            'windspeed': { '$arrayElemAt': ['$hours', 1] },
            'winddirection': { '$arrayElemAt': ['$hours', 2] },
            'windgusts': { '$arrayElemAt': ['$hours', 3] }
        }
    }
]


            # Fetch the aggregated results
            results = list(self.mongo.collections["Forecasts"].aggregate(pipeline))

            print(results)
            return {"success": True, "data": results}

        except pymongo_errors.PyMongoError as e:
            return {"success": False, "error": str(e)}

