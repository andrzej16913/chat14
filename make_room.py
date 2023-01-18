from app import db, rooms
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
            room = Room()
            room.name = name
            db.session.add(room)
            db.session.commit()
            print('Created new room: {}'.format(name))

