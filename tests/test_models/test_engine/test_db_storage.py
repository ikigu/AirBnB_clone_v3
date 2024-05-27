#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.SkipTest
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.SkipTest
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        wonderlandia = {"name": "Wonderlandia"}
        new_state_object = State(**wonderlandia)
        models.storage.new(new_state_object)
        models.storage.save()

        session = models.storage._DBStorage__session

        all_state_db_objects = session.query(State).all()

        self.assertTrue(len(all_state_db_objects) > 0)
        self.assertTrue(all_state_db_objects[0].name == "Wonderlandia")

    @unittest.SkipTest
    def test_new(self):
        """test that new adds an object to the database"""
        cairo = {"name": "Cairo"}
        new_state_db_object = State(**cairo)

        models.storage.new(new_state_db_object)

        session = models.storage._DBStorage__session

        state_in_db = session.query(State).filter_by(
            id=new_state_db_object.id).first()

        self.assertEqual(state_in_db.id, new_state_db_object.id)
        self.assertEqual(state_in_db.name, new_state_db_object.name)

    @unittest.SkipTest
    def test_save(self):
        """Test that save properly saves objects to file.json"""

        casablanca = {"name": "Casablanca"}

        new_state_db_object = State(**casablanca)

        models.storage.new(new_state_db_object)
        models.storage.save()

        session = models.storage._DBStorage__session

        state_in_db = session.query(State).filter_by(
            id=new_state_db_object.id).first()

        self.assertEqual(state_in_db.id, new_state_db_object.id)
        self.assertEqual(state_in_db.name, new_state_db_object.name)

    @unittest.SkipTest
    def test_get(self):
        """Test method for obtaining single object from storage"""

        storage = models.storage
        storage.reload()

        nairobi = {"name": "Nairobi"}
        new_state_db_object = State(**nairobi)
        storage.new(new_state_db_object)
        storage.save()

        retrieved_nairobi = storage.get(State, new_state_db_object.id)

        self.assertEqual(new_state_db_object, retrieved_nairobi)

        non_existent_state = storage.get(State, "non_existent_state_id")

        self.assertEqual(non_existent_state, None)

    @unittest.SkipTest
    def test_count(self):
        """Test method for counting objects from storage"""

        storage = models.storage
        storage.reload()
        state_data = {"name": "Zimbabwe"}
        state_instance = State(**state_data)
        storage.new(state_instance)

        city_data = {"name": "Harare", "state_id": state_instance.id}

        city_instance = City(**city_data)
        storage.new(city_instance)
        storage.save()

        state_occurences = storage.count(State)
        self.assertEqual(state_occurences, len(storage.all(State)))

        all_object_occurences = storage.count()
        self.assertEqual(all_object_occurences, len(storage.all()))
