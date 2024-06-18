from app import rooms
from app.models import Room

# If you want to add new rooms, write theri names in 'quotation marks'
# and separate them with commas. Just remember to sart each name
# with '/' slash symbol and do not use spaces
names = ['/main', '/memes', '/test']

if __name__ == '__main__':
    occupied = set()

    for room in rooms:
        occupied.add(room.name)

    for name in names:
        if name not in occupied:
            room = Room(name=name)
            #room.name = name
            room.save()
            print('Created new room: {}'.format(name))

