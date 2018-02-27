from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///itemcatalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change ade against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create a dummy user and store in users table
User1 = User(name = "Apple Pie", email = "applepie@example.com", picture = "https://upload.wikimedia.org/wikipedia/commons/f/f4/Honeycrisp.jpg")
session.add(User1)
session.commit()


# Category Items for Air sports category
category1 = Category(user_id = 1, name = "Air")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(user_id = 1, name = "Aerobatics", description = "Aerobatics is the practice of flying maneuvers involving aircraft attitudes that are not used in normal flight. Aerobatics are performed in airplanes and gliders for training, recreation, entertainment, and sport. Additionally, some helicopters, such as the MBB Bo 105, are capable of limited aerobatic maneuvers. An example of a fully aerobatic helicopter, capable of performing loops and rolls, is the Westland Lynx. The term is sometimes referred to as acrobatics, especially when translated.", category = category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id = 1, name = "Gliding", description = "Gliding is a recreational activity and competitive air sport in which pilots fly unpowered aircraft known as gliders or sailplanes using naturally occurring currents of rising air in the atmosphere to remain airborne. The word soaring is also used for the sport. Gliding as a sport began in the 1920s.", category = category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id = 1, name = "Parachuting", description = "Parachuting, or skydiving, is a method of transiting from a high point to Earth with the aid of gravity, involving the control of speed during the descent with the use of a parachute. It may involve more or less free-falling which is a period during the parachute has not been deployed and the body gradually accelerates to terminal velocity.", category = category1)

session.add(categoryItem3)
session.commit()




# Category Items for Archery sports category
category1 = Category(user_id = 1, name = "Archery")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(user_id = 1, name = "Gakgung", description = "The Korean Bow (horn bow) is a water buffalo horn-based composite reflex bow, standardized centuries ago from a variety of similar weapons in earlier use. Due to its long use by Koreans, it is also known as Guk Gung (national bow).", category = category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id = 1, name = "Popinjay", description = "Popinjay or Papingo (signifying a painted bird), also called pole archery, is a shooting sport that can be performed with either rifles or archery equipment. The rifle form is a popular diversion in Denmark; a Scottish variant is also known.", category = category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id = 1, name = "Target Archery", description = "Target archery is the most popular form of archery, in which members shoot at stationary circular targets at varying distances. All types of bow - longbow, barebow, recurve and compound - can be used. ", category = category1)

session.add(categoryItem3)
session.commit()






# # Category Items for Ball-over-net sports category
# category1 = Category(name = "Ball-over-Net")

# session.add(category1)
# session.commit()

# categoryItem1 = CategoryItem(name = "Football Tennis", description = "Footballtennis, also known as futnet (in Czech and Slovak nohejbal) is a sport originating in the 1920s in Czechoslovakia. It is a ball game that can be played indoors or outdoors in a court divided by a low net with two opposing teams (one, two or three players) who try to score a point hitting the ball with any part of their body except for the hands and making it bounce in the opponent's area in a way that makes it difficult or impossible for the other team to return it over the net.", timestamp = timestamp, category = category1)

# session.add(categoryItem1)
# session.commit()

# categoryItem2 = CategoryItem(name = "Sepak Takraw", description = "Gliding is a recreational activity and competitive air sport in which pilots fly unpowered aircraft known as gliders or sailplanes using naturally occurring currents of rising air in the atmosphere to remain airborne. The word soaring is also used for the sport. Gliding as a sport began in the 1920s.", timestamp = timestamp, category = category1)

# session.add(categoryItem2)
# session.commit()

# categoryItem3 = CategoryItem(name = "Sipa", description = "Parachuting, or skydiving, is a method of transiting from a high point to Earth with the aid of gravity, involving the control of speed during the descent with the use of a parachute. It may involve more or less free-falling which is a period during the parachute has not been deployed and the body gradually accelerates to terminal velocity.", timestamp = timestamp, category = category1)

# session.add(categoryItem3)
# session.commit()



# Category Items for Equine sports category
# category1 = Category(name = "Equine")

# session.add(category1)
# session.commit()

# categoryItem1 = CategoryItem(name = "Horseball", description = "Aerobatics is the practice of flying maneuvers involving aircraft attitudes that are not used in normal flight. Aerobatics are performed in airplanes and gliders for training, recreation, entertainment, and sport. Additionally, some helicopters, such as the MBB Bo 105, are capable of limited aerobatic maneuvers. An example of a fully aerobatic helicopter, capable of performing loops and rolls, is the Westland Lynx. The term is sometimes referred to as acrobatics, especially when translated.", category = category1)

# session.add(categoryItem1)
# session.commit()

# categoryItem2 = CategoryItem(name = "Gymkhana", description = "Gliding is a recreational activity and competitive air sport in which pilots fly unpowered aircraft known as gliders or sailplanes using naturally occurring currents of rising air in the atmosphere to remain airborne. The word soaring is also used for the sport. Gliding as a sport began in the 1920s.", category = category1)

# session.add(categoryItem2)
# session.commit()

# categoryItem3 = CategoryItem(name = "Rodeo", description = "Parachuting, or skydiving, is a method of transiting from a high point to Earth with the aid of gravity, involving the control of speed during the descent with the use of a parachute. It may involve more or less free-falling which is a period during the parachute has not been deployed and the body gradually accelerates to terminal velocity.", category = category1)

# session.add(categoryItem3)
# session.commit()


# # Category Items for Board sports category
# category1 = Category(name = "Board")

# session.add(category1)
# session.commit()

# categoryItem1 = CategoryItem(name = "Skateboarding", description = "Aerobatics is the practice of flying maneuvers involving aircraft attitudes that are not used in normal flight. Aerobatics are performed in airplanes and gliders for training, recreation, entertainment, and sport. Additionally, some helicopters, such as the MBB Bo 105, are capable of limited aerobatic maneuvers. An example of a fully aerobatic helicopter, capable of performing loops and rolls, is the Westland Lynx. The term is sometimes referred to as acrobatics, especially when translated.", category = category1)

# session.add(categoryItem1)
# session.commit()

# categoryItem2 = CategoryItem(name = "Skysurfing", description = "Gliding is a recreational activity and competitive air sport in which pilots fly unpowered aircraft known as gliders or sailplanes using naturally occurring currents of rising air in the atmosphere to remain airborne. The word soaring is also used for the sport. Gliding as a sport began in the 1920s.", category = category1)

# session.add(categoryItem2)
# session.commit()

# categoryItem3 = CategoryItem(name = "Wakeboarding", description = "Parachuting, or skydiving, is a method of transiting from a high point to Earth with the aid of gravity, involving the control of speed during the descent with the use of a parachute. It may involve more or less free-falling which is a period during the parachute has not been deployed and the body gradually accelerates to terminal velocity.", category = category1)

# session.add(categoryItem3)
# session.commit()


# # Category Items for Climbing sports category
# category1 = Category(name = "Climbing")

# session.add(category1)
# session.commit()

# categoryItem1 = CategoryItem(name = "Abseiling", description = "Aerobatics is the practice of flying maneuvers involving aircraft attitudes that are not used in normal flight. Aerobatics are performed in airplanes and gliders for training, recreation, entertainment, and sport. Additionally, some helicopters, such as the MBB Bo 105, are capable of limited aerobatic maneuvers. An example of a fully aerobatic helicopter, capable of performing loops and rolls, is the Westland Lynx. The term is sometimes referred to as acrobatics, especially when translated.", category = category1)

# session.add(categoryItem1)
# session.commit()

# categoryItem2 = CategoryItem(name = "ice Climbing", description = "Gliding is a recreational activity and competitive air sport in which pilots fly unpowered aircraft known as gliders or sailplanes using naturally occurring currents of rising air in the atmosphere to remain airborne. The word soaring is also used for the sport. Gliding as a sport began in the 1920s.", category = category1)

# session.add(categoryItem2)
# session.commit()

# categoryItem3 = CategoryItem(name = "Mountaineering", description = "Parachuting, or skydiving, is a method of transiting from a high point to Earth with the aid of gravity, involving the control of speed during the descent with the use of a parachute. It may involve more or less free-falling which is a period during the parachute has not been deployed and the body gradually accelerates to terminal velocity.", category = category1)

# session.add(categoryItem3)
# session.commit()


# # Category Items for Cue sports category
# category1 = Category(name = "Cue")

# session.add(category1)
# session.commit()

# categoryItem1 = CategoryItem(name = "Carom Billiards", description = "Aerobatics is the practice of flying maneuvers involving aircraft attitudes that are not used in normal flight. Aerobatics are performed in airplanes and gliders for training, recreation, entertainment, and sport. Additionally, some helicopters, such as the MBB Bo 105, are capable of limited aerobatic maneuvers. An example of a fully aerobatic helicopter, capable of performing loops and rolls, is the Westland Lynx. The term is sometimes referred to as acrobatics, especially when translated.", category = category1)

# session.add(categoryItem1)
# session.commit()

# categoryItem2 = CategoryItem(name = "Pocket Billiards", description = "Gliding is a recreational activity and competitive air sport in which pilots fly unpowered aircraft known as gliders or sailplanes using naturally occurring currents of rising air in the atmosphere to remain airborne. The word soaring is also used for the sport. Gliding as a sport began in the 1920s.", category = category1)

# session.add(categoryItem2)
# session.commit()

# categoryItem3 = CategoryItem(name = "Snooker", description = "Parachuting, or skydiving, is a method of transiting from a high point to Earth with the aid of gravity, involving the control of speed during the descent with the use of a parachute. It may involve more or less free-falling which is a period during the parachute has not been deployed and the body gradually accelerates to terminal velocity.", category = category1)

# session.add(categoryItem3)
# session.commit()


# # Category Items for Racquet sports category
# category1 = Category(name = "Racquet")

# session.add(category1)
# session.commit()

# categoryItem1 = CategoryItem(name = "Qianball", description = "Aerobatics is the practice of flying maneuvers involving aircraft attitudes that are not used in normal flight. Aerobatics are performed in airplanes and gliders for training, recreation, entertainment, and sport. Additionally, some helicopters, such as the MBB Bo 105, are capable of limited aerobatic maneuvers. An example of a fully aerobatic helicopter, capable of performing loops and rolls, is the Westland Lynx. The term is sometimes referred to as acrobatics, especially when translated.", category = category1)

# session.add(categoryItem1)
# session.commit()

# categoryItem2 = CategoryItem(name = "Speedminton", description = "Gliding is a recreational activity and competitive air sport in which pilots fly unpowered aircraft known as gliders or sailplanes using naturally occurring currents of rising air in the atmosphere to remain airborne. The word soaring is also used for the sport. Gliding as a sport began in the 1920s.", category = category1)

# session.add(categoryItem2)
# session.commit()

# categoryItem3 = CategoryItem(name = "Table Tennis", description = "Parachuting, or skydiving, is a method of transiting from a high point to Earth with the aid of gravity, involving the control of speed during the descent with the use of a parachute. It may involve more or less free-falling which is a period during the parachute has not been deployed and the body gradually accelerates to terminal velocity.", category = category1)

# session.add(categoryItem3)
# session.commit()

print("added category items!")
