from flask import Flask, render_template, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)


engine = create_engine("sqlite:///belly_button_biodiversity.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
OTU = Base.classes.otu
Samples = Base.classes.samples
SamplesMetadata = Base.classes.samples_metadata
session = Session(engine)


# render index.html
@app.route("/")
def default():
    return render_template("index.html")

# list of sample names 
@app.route("/names", methods=['POST','GET'])
def names():

    samples_list_col = Base.classes.samples.__table__.columns.keys()
    sample_list = samples_list_col[1:]
    return jsonify(samples_list_col[1:])

# otu
@app.route("/otu", methods=['POST','GET'])
def otu():

    otu_descriptions = session.query(OTU.lowest_taxonomic_unit_found).all()
    otu_dict = {}
    for i in otu_descriptions:
        otu_dict[i[0]] = i[1]
    return jsonify(otu_dict)


# metadata for a specific sample
@app.route('/metadata/<sample>', methods=['POST','GET'])
def sample_query(sample):
    sample_name = sample.replace("BB_", "")
    result = session.query(SamplesMetadata.AGE, SamplesMetadata.BBTYPE, SamplesMetadata.ETHNICITY, SamplesMetadata.GENDER, SamplesMetadata.LOCATION, SamplesMetadata.SAMPLEID).filter_by(SAMPLEID = sample_name).all()
    record = result[0]
    record_dict = {
        "AGE": record[0],
        "BBTYPE": record[1],
        "ETHNICITY": record[2],
        "GENDER": record[3],
        "LOCATION": record[4],
        "SAMPLEID": record[5]
    }
    return jsonify(record_dict)
    

@app.route('/wfreq/<sample>', methods=['POST','GET'])
def wfreq(sample):

    results = session.query(SamplesMetadata.WFREQ).filter(SamplesMetadata.SAMPLEID == sample[3:]).all()
    
    return jsonify(results[0][0])

@app.route('/samples/<sample>', methods=['POST','GET'])
def samples(sample):

    
    results = session.query(Samples.otu_id,getattr(Samples, sample)).order_by(getattr(Samples, sample).desc()).all()
    results
    dict1, dict2 = {}, {}
    list1, list2, list3 = [], [], []
    for x in results:
        if(x[1] > 0):
            list1.append(x[0])
            list2.append(x[1])
    dict1['otu_id'] = list1
    dict1['sample_values'] = list2
    list3.append(dict1)
    list3

    return jsonify(list3)




if __name__ == '__main__':
    app.run(debug=False)
