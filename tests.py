#!flask/bin/python

import os
import twinfluencer
import unittest
import tempfile
import json

class TestSuite(unittest.TestCase):

    def setUp(self):
    #generic test initalization thingy ! creates a temporary database. #TODO more tests ! 
        self.dbFileDesc, self.dbFile =tempfile.mkstemp()
        twinfluencer.app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///%s" % self.dbFile
        twinfluencer.app.config['TESTING']=True
        self.app=twinfluencer.app.test_client()
        twinfluencer.init_db()

        
    def tearDown(self):
        os.close(self.dbFileDesc)
        os.unlink(self.dbFile)

   # Test to check if the /stats page works
    def test_stats(self):
        response=self.app.get("/stats")
        assert json.dumps({"status":{"message":"Bad login","code":501}}) in response.data
                 

        
if __name__=="__main__":
    unittest.main()
                      
