from mongoengine import *
from datetime import datetime, timedelta
from random import randint
import uuid


class GarbageStatus(Document):
    garbage_can_id = StringField(required=True)
    company_id = StringField(required=True)
    completion = FloatField(required=True)
    location = PointField()
    volume_filled = DecimalField()
    volume = DecimalField()
    created_at = DateTimeField(default=datetime.now())
    is_full = BooleanField(default=False)
    predict_full = BooleanField(default=False)

    @staticmethod
    def create(can_id, company_id, completion, location, volume_filled, volume, isFull, created_at=datetime.now()):
        can = GarbageStatus()
        can.garbage_can_id = can_id
        can.company_id = company_id
        can.completion = completion
        can.location = location
        can.volume_filled = volume_filled
        can.volume = volume
        can.is_full = isFull
        can.created_at = created_at
        can.save()
        return can

    @staticmethod
    def get_recent_bins(company_id):
        ids = GarbageStatus.objects().only('garbage_can_id').distinct('garbage_can_id')
        print(ids)

        bins = []
        for id in ids:
            bin = GarbageStatus.objects(garbage_can_id=id, company_id=company_id).order_by('-created_by')
            if bin:
                bins.append(bin[len(bin) -1].show_attributes())

        return bins

    def show_attributes(self):
        return {
            'name': str(self.garbage_can_id),
            'completion': str(self.completion),
            'volume': str(self.volume),
            'predict_full': self.predict_full,
            'is_full': self.is_full,
            'created_at': str(self.created_at)
        }


    @staticmethod
    def get_consumption_graph_by_year(company_id):
        return GarbageStatus.objects.exec_js("""
        db.garbage_status.aggregate(
   [
   {
            $match :
                {$and: [{ is_full : true },{company_id: options.company_id }]}
            },

     {
       $group:
         {
           _id: { year: { $year: "$created_at" } },
           totalAmount: { $sum: "$volume"}
         }
     }
   ])
""", **{'company_id': company_id})

    @staticmethod
    def get_consumption_graph_by_month(company_id):
        # GarbageStatus.create(str(randint(0,1000)), company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        # GarbageStatus.create(str(randint(0,1000)), company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        # GarbageStatus.create(str(randint(0,1000)), company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        # GarbageStatus.create(str(randint(0,1000)), company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        # GarbageStatus.create(str(randint(0,1000)), company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        # GarbageStatus.create(str(randint(0,1000)), company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        # GarbageStatus.create(str(randint(0,1000)), company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        return GarbageStatus.objects.exec_js("""
            db.garbage_status.aggregate(
       [
       {
                $match :
                    {$and: [{ is_full : true },{company_id: options.company_id }]}
                },

         {
           $group:
             {
               _id: {
               year: { $year: "$created_at" },
               month: { $month: "$created_at" },
               },
               totalAmount: { $sum: "$volume"}
             }
         },{
         $sort:{"_id.year":-1, "_id.month":-1}
         }

       ])
    """, **{'company_id': company_id})


    @staticmethod
    def get_consumption_graph_by_month_pr(company_id):
        # GarbageStatus.create("1", company_id, 0.8, [33.4, 33.2], 50, 50, True, datetime.now() - timedelta(randint(0,1000)))
        return GarbageStatus.objects.exec_js("""
            db.garbage_status.aggregate(
       [
       {
                $match :
                    {$and: [{ is_full : true },{company_id: options.company_id }]}
                },

        {
            $project: {

            }
        }
         {
           $group:
             {
               _id: {
               month: { $month: "$created_at" },
               },
               totalAmount: { $sum: "$volume"}
             }
         }

       ])
    """, **{'company_id': company_id})

    @staticmethod
    def get_consumption_graph_by_day(company_id):
        return GarbageStatus.objects.exec_js("""
            db.garbage_status.aggregate(
       [
       {
                $match :
                    {$and: [{ is_full : true },{company_id: options.company_id }]}
                },

         {
           $group:
             {
               _id: { day: { $dayOfMonth: "$created_at" } },
               totalAmount: { $sum: "$volume"}
             }
         }
       ])
    """, **{'company_id': company_id})

    @staticmethod
    def get_filled_stats_by_year(company_id):
        return GarbageStatus.objects.exec_js("""
                db.garbage_status.aggregate(
       [ {
            $match :
                {$and: [{ is_full : true },{company_id: options.company_id }]}
            },
         {
           $group:
             {
               _id: {  year: { $year: "$created_at" },
                       month: { $month: "$created_at" },

                    },
                    'totalAmount': {$sum: 1}
             }
         },{
         $sort:{"_id.year":-1, "_id.month":-1}
         }
         ])""",  **{'company_id': company_id})


    @staticmethod
    def get_filled_stats_by_month(company_id):
        return GarbageStatus.objects.exec_js("""
                        db.garbage_status.aggregate(
               [ {
                    $match :
                        {$and: [{ is_full : true },{company_id: options.company_id }]}
                    },
                 {
                   $group:
                     {
                       _id: {  month: { $month: "$created_at" },

                            },
                            'count': {$sum: 1}
                     }
                 }    ])""", **{'company_id': company_id})

    @staticmethod
    def get_filled_stats_by_day(company_id):
        return GarbageStatus.objects.exec_js("""
                            db.garbage_status.aggregate(
                   [ {
                        $match :
                            {$and: [{ is_full : true },{company_id: options.company_id }]}
                        },
                     {
                       $group:
                         {
                           _id: {  day: { $dayOfMonth: "$created_at" },

                                },
                                'count': {$sum: 1}
                         }
                     }    ])""", **{'company_id': company_id})