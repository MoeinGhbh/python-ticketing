from eventbrite import Eventbrite


eventbrite  = Eventbrite('TK2XUY5IOE3LWJZKHVZG')

user = eventbrite.get_user()

print(user['id'])

print(user['name'])