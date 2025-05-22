class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost:3307/CamBear_D'
    SQLALCHEMY_TRACK_MODIFICATIONS = False