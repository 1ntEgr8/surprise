import maketree
from surprise import db
from surprise.models import Creator, Recepient
import threading

""" This script will be run alongside the server
	It will check the database for new request every 30 min 
	and will then process those requests
	Once the request has been processed, it will send an email to
	recepients and creators notifying them of the completion 
	of their order  
"""

def get_recepient_orders():
	pending_orders = Recepient.query.filter_by(image_created=False)

	# def init_session(creator_name, recepients, id1=1, id2=[1])
	orders = []
	creators=[]

	for recepient in pending_orders:
		item = ()
		creator = recepient.sender
		recepient_list=[]
		recepient_ids=[]

		if creator not in creators:
			creators.append(creator)

			creator_orders = Recepient.query.filter_by(creator_id=creator.id)

			for order in creator_orders:
				recepient_list.append(order.recepient_name)
				recepient_ids.append(order.id)

			item = (creator.first_name, recepient_list, creator.id, recepient_ids)

			orders.append(item)

	return orders

def no_order():
	print("NO ORDER. CHECKING AGAIN")


def get_work_started():
	counter = 0
	while True:
		orders = get_recepient_orders()
		counter2 = 0
		if orders:
			print(f"BATCH {counter+1}")
			print(f"NO OF CREATOR_ORDERS {len(orders)}")
			for order in orders:
				maketree.init_session(*order)
				print(f"BATCH {counter+1}: ORDER {counter2+1} COMPLETE")
				counter2+=1

				counter3 = 0

				for recepient in order[1]:
					complete = Recepient.query.filter_by(id=order[3][counter3]).first()
					complete.image_created=True
					print(complete)
					counter3+=1
					print(f"SUB ORDER {counter3} COMPLETE")
				db.session.commit()

			print(f"BATCH {counter+1} COMPLETE")
		else:
			threading.Timer(60,no_order)

get_work_started()
