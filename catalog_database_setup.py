# configuration section - import the necessary modules
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from datetime import datetime

Base = declarative_base()


# class: User
class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250))

# class: Category Table
class Category(Base):
	# set the table name
	__tablename__ = 'category'
	# define the table structure
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		""" Return object data in easily serializable format """
		return {
			'name' : self.name,
			'id' : self.id,
		}

# class: CategoryItem Table
class CategoryItem(Base):
	# set the table name
	__tablename__ = 'category_item'
	# define the table structure
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(800))
	timestamp = Column(DateTime, default = func.current_timestamp())
	# here, we specify tablename.columnname inside foreign key
	category_id = Column(Integer, ForeignKey('category.id'))
	# Here, we set the relationship for the table (category)
	# and the class (Category)
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		#Returns object data in serializable format
		cat = Category()
		return {
			'name' : self.name,
			'id' : self.id,
			'description' : self.description,
			'category_id' : self.category_id,
		}
# Insert at the end of the file
engine = create_engine('sqlite:///itemcatalogwithusers.db')
Base.metadata.create_all(engine)