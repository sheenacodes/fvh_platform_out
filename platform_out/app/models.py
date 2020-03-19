from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict


class AssetData(db.Model):
    __tablename__ = "asset_data_hstore"
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(64), index=True, unique=True)
    asset_data = db.Column(MutableDict.as_mutable(HSTORE))

    # def __init__(self, asset_name, asset_data):
    #     self.asset_data = asset_data
    #     self.asset_name = asset_name

    def __repr__(self):
        return f"<Data Stream {self.asset_name}, {self.asset_data}>"

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {"asset name": x.asset_name, "asset data": x.asset_data}

        return {"DataStreams": list(map(lambda x: to_json(x), AssetData.query.all()))}
