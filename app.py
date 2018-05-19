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
    otu_descriptions_list = [x for (x), in otu_descriptions]
    return jsonify(otu_descriptions_list)
    
    return jsonify(otu_dict)



# metadata for a specific sample
@app.route('/metadata/<sample>', methods=['POST','GET'])
def sample_query(sample):
    sample_name = sample.replace("BB_", "")
    result = session.query(SamplesMetadata.AGE, SamplesMetadata.BBTYPE, SamplesMetadata.ETHNICITY, SamplesMetadata.GENDER, SamplesMetadata.LOCATION, SamplesMetadata.SAMPLEID).filter_by(SAMPLEID = "940").all()
    record = result[0]
    result_dict = {
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
    sample_name = sample.replace("BB_", "")
    result = session.query(SamplesMetadata.WFREQ).filter_by(SAMPLEID = "940").all()
    return jsonify(results[0][0])

@app.route('/samples/<sample>', methods=['POST','GET'])
def sample(sample):
    sample_query = "Samples." + sample
    results = session.query(Samples.otu_id, sample_query).order_by(sample_query).desc().all()
    sample_values = [result[x][1] for x in range(len(result))]
    dict_list = [{"otu_ids": otu_ids}, {"sample_values": sample_values}]
    return dict_list

    return jsonify(dict_list)




if __name__ == '__main__':
    app.run(debug=False)
