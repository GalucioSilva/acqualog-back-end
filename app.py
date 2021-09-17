import datetime
from flask import Flask, json,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema,fields
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:docker@localhost:5432/flask_database'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
CORS(app)
db=SQLAlchemy(app)

class Sample(db.Model):
  id = db.Column(db.Integer(),primary_key=True)
  temp = db.Column(db.String(255),nullable=False)
  ph = db.Column(db.String(255),nullable=False)
  od = db.Column(db.String(255),nullable=False)
  conductivity = db.Column(db.String(255),nullable=False)
  transparency = db.Column(db.String(255),nullable=False)
  created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  def __repr__(self):
    return self.name
  @classmethod
  def get_all(cls):
    return cls.query.all()
  @classmethod
  def get_by_id(cls,id):
    return cls.query.get_or_404(id)
  @classmethod
  def get_most_recent(cls):
    return cls.query.order_by(Sample.created_date.desc()).limit(1)
  def save(self):
    db.session.add(self)
    db.session.commit()
  def delete(self):
    db.session.delete(self)
    db.session.commit()
      
class SampleSchema(Schema):
  id=fields.Integer()
  temp =fields.String()
  ph =fields.String()
  od =fields.String()
  conductivity  =fields.String()
  transparency =fields.String()
  created_date = fields.DateTime()

@app.route('/samples',methods=['GET'])
def get_all_recipes():
    samples=Sample.get_all()

    serializer=SampleSchema(many=True)

    data=serializer.dump(samples)

    return jsonify(
      data
    )   

@app.route('/samples/recent',methods=['GET'])
def get_gmost_recent():
    samples=Sample.get_most_recent()

    serializer=SampleSchema(many=True)

    data=serializer.dump(samples)

    return jsonify(
      data
    )   

@app.route('/samples',methods=['POST'])
def create_a_sample():
  data=request.get_json()

  new_recipe=Sample(
    temp = data.get('temp'),
    ph = data.get('ph'),
    od = data.get('od'),
    conductivity  = data.get('conductivity'),
    transparency = data.get('transparency')
  )

  new_recipe.save()

  serializer=SampleSchema()

  data=serializer.dump(new_recipe)

  return jsonify(
    data
  ),201

@app.route('/samples/<int:id>',methods=['GET'])
def get_sample(id):
    sample=Sample.get_by_id(id)

    serializer=SampleSchema()

    data=serializer.dump(sample)

    return jsonify(
        data
    ),200

@app.route('/samples/<int:id>',methods=['PUT'])
def update_recipe(id):
    sample_to_update=Sample.get_by_id(id)

    data=request.get_json()

    sample_to_update.temp=data.get('temp')
    sample_to_update.ph = data.get('ph')
    sample_to_update.od = data.get('od')
    sample_to_update.conductivity  = data.get('conductivity')
    sample_to_update.transparency = data.get('transparency')

    db.session.commit()

    serializer=SampleSchema()

    sample_data=serializer.dump(sample_to_update)

    return jsonify(sample_data),200

@app.route('/samples/<int:id>',methods=['DELETE'])
def delete_recipe(id):
    recipe_to_delete=Sample.get_by_id(id)

    recipe_to_delete.delete()

    return jsonify({"message":"Deleted"}),204

if __name__ == '__main__':
  app.run(debug=True)