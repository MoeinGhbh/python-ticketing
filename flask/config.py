# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

SQLALCHEMY_DATABASE_URI = \
'mysql+pymysql://admin:admin_Vriday.net@'\
'nexr-database.cie7ndk7wlfk.eu-central-1.rds.amazonaws.com:3306/nexr_database'

# Uncomment the line below if you want to work with a local DB
# SQLALCHEMY_DATABASE_URI = 'sqlite:///../seminar.db'

SQLALCHEMY_POOL_RECYCLE = 3600
WTF_CSRF_ENABLED = True
SECRET_KEY = "a2a58d01c94d129e7407823e6faf1ace"
