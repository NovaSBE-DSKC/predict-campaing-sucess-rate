from datetime import datetime

from src.data_curation.clean import get_stop_words

import dskc
import math
import numpy as np
import json
import settings
import pandas as pd

from dskc import dskc_clean
from src.data_curation.pre_processing import get_countries

PROJECT_STOP_WORDS = get_stop_words()
COUNTRIES_LIST = None
FEATURES_LIST = None


def sin_cos_date(value, n_cycles):
  alpha = 2 * np.pi * value / n_cycles
  return math.sin(alpha), math.cos(alpha)

def setup():
  # set countries list
  global COUNTRIES_LIST

  if COUNTRIES_LIST is None:
    with open(settings.COUNTRIES_LIST_PATH, 'r') as f:
      COUNTRIES_LIST = json.load(f)

  # set features list
  global FEATURES_LIST

  if FEATURES_LIST is None:
    with open(settings.FEATURES_LIST_PATH, 'r') as f:
      FEATURES_LIST = json.load(f)
      FEATURES_LIST.remove("financed")


def get_countries_list():
  global COUNTRIES_LIST

  if COUNTRIES_LIST is None:
    setup()

  return COUNTRIES_LIST


def get_features_list():
  global FEATURES_LIST

  if FEATURES_LIST is None:
    setup()

  return FEATURES_LIST


def set_categories(data):
  
  categories = [
        ('cat_agro-indústria', 'Agro Indústria'),
        ("cat_alimentação/bebidas", 'Alimentação/bebidas'),
        ("cat_ambiente", "Ambiente"),
        ("cat_artes_plásticas", "Artes plásticas"),
        ("cat_cidadania_/_política", "Cidadania/Política"),
        ("cat_ciência/tecnologia", "Ciência/Tecnologia"),
        ("cat_dança/cinema/teatro", "Dança/Cinema/Teatro"),
        ("cat_desporto", "Desporto"),
        ("cat_educação", "Educação"),
        ("cat_empreendedorismo", "Empreendedorismo"),
        ("cat_evento", "Evento"),
        ("cat_jogos", "Jogos"),
        ("cat_livros/revistas", "Livros/Revistas"),
        ("cat_moda/design", "Moda/Design"),
        ("cat_música", "Música"),
        ("cat_outros", "Outros"),
        ("cat_social", "Social"),
        ("cat_turismo/viagens", "Turismo/Viagens"),
        ("cat_vídeo/fotografia", "Vídeo/Fotografia"),
        ("cat_zoófila", "Zoófila"),
  ]


  project_category = data["category"]
  del data["category"]

  # set category one hot encoder
  for category,name in categories:
    if name == project_category:
      data[category] = 1
    else:
      data[category] = 0


def set_country(data):
  countries = get_countries_list()

  # set country
  project_country = get_countries(data["location"])
  project_country = "country_reduced_" + project_country
  project_country="_".join(project_country.lower().split())

  # set country one hot encoding
  for country in countries:
    country = "country_reduced_"+"_".join(country.lower().split())

    if country == project_country:
      data[country] = 1
    else:
      data[country] = 0

  # remove old variable
  del data["location"]



def transform_data(data, normalization_model, lda_model):
  # get topics
  data["prj_summary"] = data.pop("project_summary")
  data["title_prj_summary"] = data["title"] + " " + data["prj_summary"]
  dominant_topics, prob_dominant_topics, topics_prob = dskc.clean.topic_modeling_transform(data["title_prj_summary"],
                                                                                           lda_model,
                                                                                           stop_words=PROJECT_STOP_WORDS)
  for i, topic_prob in enumerate(topics_prob):
    data["title_prj_summary_topic_" + str(i + 1)] = topics_prob[topic_prob][0]

  del data["title_prj_summary"]

  data["title_length"] = len(data["title"])
  data["channel"] = int(data["channel"] == "true")

  # process date
  data["start_month"] = data["start_date"].month
  data['start_month_sin'], data['start_month_cos'] = sin_cos_date(data["start_month"], 12)

  data["end_month"] = data["end_date"].month
  data['end_month_sin'], data['end_month_cos'] = sin_cos_date(data["end_month"], 12)

  data["start_day"] = data["start_date"].day
  data['start_day_sin'], data['start_day_cos'] = sin_cos_date(data["start_day"], 31)

  data["end_day"] = data["end_date"].day
  data['end_day_sin'], data['end_day_cos'] = sin_cos_date(data["end_day"], 31)

  data["start_weekday"] = data["start_date"].weekday()
  data['start_weekday_sin'], data['start_weekday_cos'] = sin_cos_date(data["start_weekday"], 7)

  data["end_weekday"] = data["end_date"].weekday()
  data['end_weekday_sin'], data['end_weekday_cos'] = sin_cos_date(data["end_weekday"], 7)

  data["days"] = (data["end_date"] - data["start_date"]).days
  data["days_elapsed"] = (data["project_state_date"] - data["start_date"]).days

  data["percentage_days_elapsed"] = data["days_elapsed"] / max(data["days"], 1)  # prevent division by 0

  del data["start_date"]
  del data["end_date"]
  del data["project_state_date"]

  #
  data["percentage_raised"] = data["raised"] / data["target"]
  data["percentage_target_self_funded"] = data["amount_self_funded"] / data["target"]
  data["facebook"] = int(data["facebook"] == "true")
  data["uncond_channel"] = int(data["uncond_channel"] == "true")

  # categories
  set_categories(data)

  # country
  set_country(data)

  # rename rewards to have the slot name
  for k in data:
    if k.startswith("reward_") and not k.startswith("reward_slot_"):
      new_k=k.replace("reward_","reward_slot_")
      data[new_k]=data.pop(k)

  # select features
  features = get_features_list()
  for i,x in enumerate(features):
    print(i,x,data[x])
    
  data=[data[x] for x in features]
  
    
  # normalize
  # add target value , todo remove
  data.append(0)
  data=np.array(data)
  data=data.reshape(1, -1)
  data_normalized=normalization_model.transform(data)
  # remove target variable
  data_normalized = data_normalized[0,:-1]

  for i,x in enumerate(data_normalized):
    print("{} {} {}".format(i,features[i],x))
    
  return data_normalized
  



def get_fake_data():
  data = {}

  data["title"] = "projecto teste"
  data["project_summary"] = "projecto teste"
  data["channel"] = 'true'
  data["start_date"] = datetime(2020, 4, 20)
  data["end_date"] = datetime(2020, 6, 20)
  data["project_state_date"] = datetime(2020, 5, 20)
  data["target"] = 3000
  data["raised"] = 1500
  data["backers"] = 3
  data["amount_self_funded"] = 2
  data["views"] = 100  
  data["images"] = 3
  data["comments"] = 4
  data["uncond_channel"] = 'false'
  data["facebook"] = 'false'
  data["category"] = "Ambiente"
  data["location"] = "Lisboa, Portugal"
  data["user_n_projects"] = 2
  data["user_n_success_projects"] = 1
  data["n_rewards"] = 3
  data["reward_slot_1_amount"] = 5
  data["reward_slot_2_amount"] = 10
  data["reward_slot_3_amount"] = 15
  data["reward_slot_4_amount"] = 0
  data["reward_slot_5_amount"] = 0
  data["reward_slot_6_amount"] = 0

  return data

import hashlib
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
