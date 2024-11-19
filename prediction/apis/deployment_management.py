# from typing import Dict, Any

from prediction.apis import prediction_engine as pe
from prediction.apis import algorithm_client_pulse as cp
from prediction.apis import data_management_engine as dme
from runtime.apis import predictor_engine as o

from datetime import datetime
from json import JSONDecodeError
import json
import pymongo
import getpass
import openshift_client as oc
import yaml
import time

def get_budget_tracker_default():
    return {
        "budget_parameters_database": "",
        "budget_parameters_datasource": "mongodb",
        "budget_id": "",
        "description": "",
        "budget_parameters_table_collection": "",
        "x_axis_datasource": "offer_matrix",
        "x_axis_name": "",
        "acc_namesource": "",
        "y_axis_name": "",
        "y_axis_namesource": "",
        "acc_name": "",
        "budget_strategy": "",
        "x_axis_namesource": "",
        "acc_datasource": "offer_matrix",
        "y_axis_datasource": "offer_matrix"
    }


def get_model_configuration_default():
    return {}


def get_setup_offer_matrix_default():
    return {
        "offer_lookup_id": "",
        "database": "",
        "table_collection": "",
        "datasource": "mongodb"
    }


def get_multi_armed_bandit_default():
    return {
        "epsilon": "",
        "duration": 0,
        "pulse_responder_uuid": ""
    }


def get_whitelist_default():
    return {
        "table_collection": "",
        "datasource": "mongodb",
        "database": ""
    }


def get_model_selector_default():
    return {
        "selector_column": "",
        "lookup": "",
        "database": "",
        "selector": "",
        "table_collection": "",
        "datasource": "mongodb"
    }


def get_pattern_selector_default():
    return {
        "pattern": "",
        "duration": ""
    }


def get_corpora_default():
    return {
        "corpora": ""
    }


def get_parameter_access_default():
    return {}


def get_api_endpoint_code_default():
    return ""


def get_pre_score_code(pre_score, project_details):
    pre_score_code_options = {
        "": "package com.ecosystem.plugin.customer;\n\nimport com.datastax.oss.driver.api.core.CqlSession;\nimport org.json.JSONObject;\n\npublic class PrePredictCustomer {\n\n    public PrePredictCustomer() {\n    }\n\n    /**\n     * Pre-pre predict\n     */\n    public void getPrePredict() {\n    }\n\n    /**\n     * getPostPredict\n     * @param params\n     * @param session\n     * @return\n     */\n    public static JSONObject getPrePredict(JSONObject params, CqlSession session) {\n\n        /*\n        Manipulate params that will be used by scoring and post-scoring\n         */\n\n        return params;\n    }\n\n}\n",
    }
    if "deployment_step" in project_details:
        version_list = []
        for i in project_details["deployment_step"]:
            if "plugins" in i:
                if "pre_score_class_text" in i["plugins"]:
                    if i["plugins"]["pre_score_class_text"] == pre_score:
                        version_list.append(i["version"])
    else:
        version_list = []
    if version_list:
        max_version = max(version_list)
        pre_score_logic = ""
        for i in project_details["deployment_step"]:
            if "version" in i:
                if i["version"] == max_version:
                    if "plugins" in i:
                        if "pre_score_class_text" in i["plugins"]:
                            if i["plugins"]["pre_score_class_text"] == pre_score:
                                if "pre_score_class_code" in i["plugins"]:
                                    pre_score_logic = i["plugins"]["post_score_class_code"]
    elif pre_score in pre_score_code_options:
        pre_score_logic = pre_score_code_options[pre_score]
    else:
        print(
            "WARNING: pre_score_class not found in default options. Empty class saved to the deployment. To edit the "
            "class use the ecosystem.Ai plugin for IntelliJ or the ecosystem.Ai workbench")
        pre_score_logic = ""
    return pre_score_logic


def get_post_score_code(post_score, project_details):
    post_score_code_options = {
        "PlatformDynamicEngagement.java": "package com.ecosystem.plugin.customer;\n\nimport com.datastax.oss.driver.api.core.CqlSession;\nimport com.ecosystem.utils.DataTypeConversions;\nimport com.ecosystem.utils.JSONArraySort;\nimport hex.genmodel.easy.EasyPredictModelWrapper;\nimport com.ecosystem.utils.log.LogManager;\nimport com.ecosystem.utils.log.Logger;\nimport org.json.JSONArray;\nimport org.json.JSONObject;\n\n/**\n * ECOSYSTEM.AI INTERNAL PLATFORM SCORING\n * Use this class to score with dynamic sampling configurations. This class is configured to work with no model.\n */\npublic class PlatformDynamicEngagement extends PostScoreSuper {\n\tprivate static final Logger LOGGER = LogManager.getLogger(PlatformDynamicEngagement.class.getName());\n\n\tpublic PlatformDynamicEngagement() {\n\t}\n\n\t/**\n\t * Pre-post predict logic\n\t */\n\tpublic void getPostPredict () {\n\t}\n\n\t/**\n\t * getPostPredict\n\t * Example params:\n\t *    {\"contextual_variable_one\":\"Easy Income Gold|Thin|Senior\", \"contextual_variable_two\":\"\", \"batch\": true}\n\t *\n\t * @param predictModelMojoResult Result from scoring\n\t * @param params                 Params carried from input\n\t * @param session                Session variable for Cassandra\n\t * @return JSONObject result to further post-scoring logic\n\t */\n\tpublic static JSONObject getPostPredict(JSONObject predictModelMojoResult, JSONObject params, CqlSession session, EasyPredictModelWrapper[] models) {\n\t\tdouble startTimePost = System.nanoTime();\n\t\ttry {\n\t\t\t/** Setup JSON objects for specific prediction case */\n\t\t\tJSONObject featuresObj = predictModelMojoResult.getJSONObject(\"featuresObj\");\n\t\t\t//JSONObject domainsProbabilityObj = predictModelMojoResult.getJSONObject(\"domainsProbabilityObj\");\n\n\t\t\tJSONObject offerMatrixWithKey = new JSONObject();\n\t\t\tboolean om = false;\n\t\t\tif (params.has(\"offerMatrixWithKey\")) {\n\t\t\t\tofferMatrixWithKey = params.getJSONObject(\"offerMatrixWithKey\");\n\t\t\t\tom = true;\n\t\t\t}\n\n\t\t\tJSONObject work = params.getJSONObject(\"in_params\");\n\n\t\t\t/***************************************************************************************************/\n\t\t\t/** Standardized approach to access dynamic datasets in plugin.\n\t\t\t * The options array is the data set/feature_store that's keeping track of the dynamic changes.\n\t\t\t * The optionParams is the parameter set that will influence the real-time behavior through param changes.\n\t\t\t */\n\t\t\t/***************************************************************************************************/\n\t\t\tJSONArray options = (JSONArray) ((\n\t\t\t\t\t(JSONObject) params.getJSONObject(\"dynamicCorpora\")\n\t\t\t\t\t\t\t.get(\"dynamic_engagement_options\")).get(\"data\"));\n\t\t\tJSONObject optionParams = (JSONObject) ((\n\t\t\t\t\t(JSONObject) params.getJSONObject(\"dynamicCorpora\")\n\t\t\t\t\t\t\t.get(\"dynamic_engagement\")).get(\"data\"));\n\n\t\t\tJSONObject contextual_variables = optionParams.getJSONObject(\"contextual_variables\");\n\t\t\tJSONObject randomisation = optionParams.getJSONObject(\"randomisation\");\n\n\t\t\t/***************************************************************************************************/\n\t\t\t/** Test if contextual variable is coming via api or feature store: API takes preference... */\n\t\t\tif (!work.has(\"contextual_variable_one\")) {\n\t\t\t\tif (featuresObj.has(contextual_variables.getString(\"contextual_variable_one_name\")))\n\t\t\t\t\twork.put(\"contextual_variable_one\", featuresObj.get(contextual_variables.getString(\"contextual_variable_one_name\")));\n\t\t\t\telse\n\t\t\t\t\twork.put(\"contextual_variable_one\", \"\");\n\t\t\t}\n\t\t\tif (!work.has(\"contextual_variable_two\")) {\n\t\t\t\tif (featuresObj.has(contextual_variables.getString(\"contextual_variable_two_name\")))\n\t\t\t\t\twork.put(\"contextual_variable_two\", featuresObj.get(contextual_variables.getString(\"contextual_variable_two_name\")));\n\t\t\t\telse\n\t\t\t\t\twork.put(\"contextual_variable_two\", \"\");\n\t\t\t}\n\t\t\t/***************************************************************************************************/\n\n\t\t\tJSONArray finalOffers = new JSONArray();\n\t\t\tint offerIndex = 0;\n\t\t\tint explore;\n\t\t\tString contextual_variable_one = String.valueOf(work.get(\"contextual_variable_one\"));\n\t\t\tString contextual_variable_two = String.valueOf(work.get(\"contextual_variable_two\"));\n\t\t\tfor (int j = 0; j < options.length(); j++) {\n\t\t\t\tJSONObject option = options.getJSONObject(j);\n\t\t\t\tString contextual_variable_one_Option = \"\";\n\t\t\t\tif (option.has(\"contextual_variable_one\") && !contextual_variable_one.equals(\"\"))\n\t\t\t\t\tcontextual_variable_one_Option = String.valueOf(option.get(\"contextual_variable_one\"));\n\t\t\t\tString contextual_variable_two_Option = \"\";\n\t\t\t\tif (option.has(\"contextual_variable_two\") && !contextual_variable_two.equals(\"\"))\n\t\t\t\t\tcontextual_variable_two_Option = String.valueOf(option.get(\"contextual_variable_two\"));\n\n\t\t\t\tif (contextual_variable_one_Option.equals(contextual_variable_one) && contextual_variable_two_Option.equals(contextual_variable_two)) {\n\n\t\t\t\t\tdouble alpha = (double) DataTypeConversions.getDoubleFromIntLong(option.get(\"alpha\"));\n\t\t\t\t\tdouble beta = (double) DataTypeConversions.getDoubleFromIntLong(option.get(\"beta\"));\n\t\t\t\t\tdouble accuracy = 0.001;\n\t\t\t\t\tif (option.has(\"accuracy\"))\n\t\t\t\t\t\taccuracy = (double) DataTypeConversions.getDoubleFromIntLong(option.get(\"accuracy\"));\n\n\t\t\t\t\t/***************************************************************************************************/\n\t\t\t\t\t/* r IS THE RANDOMIZED SCORE VALUE */\n\t\t\t\t\tdouble p = 0.0;\n\t\t\t\t\tdouble arm_reward = 0.001;\n\t\t\t\t\tif (randomisation.getString(\"approach\").equals(\"epsilonGreedy\")) {\n\t\t\t\t\t\t// params.put(\"explore\", 0);\n\t\t\t\t\t\texplore = 0;\n\t\t\t\t\t\tp = DataTypeConversions.getDouble(option, \"arm_reward\");\n\t\t\t\t\t\tarm_reward = p;\n\t\t\t\t\t} else {\n\t\t\t\t\t\t/** REMEMBER THAT THIS IS HERE BECAUSE OF BATCH PROCESS, OTHERWISE IT REQUIRES THE TOTAL COUNTS */\n\t\t\t\t\t\t/* Phase 2: sampling - calculate the arms and rank them */\n\t\t\t\t\t\t// params.put(\"explore\", 0); // force explore to zero and use Thompson Sampling only!!\n\t\t\t\t\t\texplore = 0; // set as explore as the dynamic responder is exploration based...\n\t\t\t\t\t\tp = DataTypeConversions.getDouble(option, \"arm_reward\");\n\t\t\t\t\t\tarm_reward = p;\n\n\t\t\t\t\t}\n\t\t\t\t\t/** Check if values are correct */\n\t\t\t\t\tif (p != p) p = 0.0;\n\t\t\t\t\tif (alpha != alpha) alpha = 0.0;\n\t\t\t\t\tif (beta != beta) beta = 0.0;\n\t\t\t\t\tif (arm_reward != arm_reward) arm_reward = 0.0;\n\t\t\t\t\t/***************************************************************************************************/\n\n\t\t\t\t\tString offer = option.getString(\"optionKey\");\n\n\t\t\t\t\tJSONObject singleOffer = new JSONObject();\n\t\t\t\t\tdouble offer_value = 1.0;\n\t\t\t\t\tdouble offer_cost = 1.0;\n\t\t\t\t\tdouble modified_offer_score = p;\n\t\t\t\t\tif (om) {\n\t\t\t\t\t\tif (offerMatrixWithKey.has(offer)) {\n\n\t\t\t\t\t\t\tsingleOffer = offerMatrixWithKey.getJSONObject(offer);\n\n\t\t\t\t\t\t\tif (singleOffer.has(\"offer_price\"))\n\t\t\t\t\t\t\t\toffer_value = DataTypeConversions.getDouble(singleOffer, \"offer_price\");\n\t\t\t\t\t\t\tif (singleOffer.has(\"price\"))\n\t\t\t\t\t\t\t\toffer_value = DataTypeConversions.getDouble(singleOffer, \"price\");\n\n\t\t\t\t\t\t\tif (singleOffer.has(\"offer_cost\"))\n\t\t\t\t\t\t\t\toffer_cost = singleOffer.getDouble(\"offer_cost\");\n\t\t\t\t\t\t\tif (singleOffer.has(\"cost\"))\n\t\t\t\t\t\t\t\toffer_cost = singleOffer.getDouble(\"cost\");\n\n\t\t\t\t\t\t\tmodified_offer_score = p * ((double) offer_value - offer_cost);\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\n\t\t\t\t\tJSONObject finalOffersObject = new JSONObject();\n\n\t\t\t\t\tfinalOffersObject.put(\"offer\", offer);\n\t\t\t\t\tfinalOffersObject.put(\"offer_name\", offer);\n\t\t\t\t\tfinalOffersObject.put(\"offer_name_desc\", option.getString(\"option\"));\n\n\t\t\t\t\t/* process final */\n\t\t\t\t\tfinalOffersObject.put(\"score\", p);\n\t\t\t\t\tfinalOffersObject.put(\"final_score\", p);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", modified_offer_score);\n\t\t\t\t\tfinalOffersObject.put(\"offer_value\", offer_value);\n\t\t\t\t\tfinalOffersObject.put(\"price\", offer_value);\n\t\t\t\t\tfinalOffersObject.put(\"cost\", offer_cost);\n\n\t\t\t\t\tfinalOffersObject.put(\"p\", p);\n\t\t\t\t\tif (option.has(\"contextual_variable_one\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"contextual_variable_one\", option.getString(\"contextual_variable_one\"));\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"contextual_variable_one\", \"\");\n\n\t\t\t\t\tif (option.has(\"contextual_variable_two\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"contextual_variable_two\", option.getString(\"contextual_variable_two\"));\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"contextual_variable_two\", \"\");\n\n\t\t\t\t\tfinalOffersObject.put(\"alpha\", alpha);\n\t\t\t\t\tfinalOffersObject.put(\"beta\", beta);\n\t\t\t\t\tfinalOffersObject.put(\"weighting\", (double) DataTypeConversions.getDoubleFromIntLong(option.get(\"weighting\")));\n\t\t\t\t\tfinalOffersObject.put(\"explore\", explore);\n\t\t\t\t\tfinalOffersObject.put(\"uuid\", params.get(\"uuid\"));\n\t\t\t\t\tfinalOffersObject.put(\"arm_reward\", arm_reward);\n\n\t\t\t\t\t/* Debugging variables */\n\t\t\t\t\tif (!option.has(\"expected_takeup\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"expected_takeup\", -1.0);\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"expected_takeup\", (double) DataTypeConversions.getDoubleFromIntLong(option.get(\"expected_takeup\")));\n\n\t\t\t\t\tif (!option.has(\"propensity\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"propensity\", -1.0);\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"propensity\", (double) DataTypeConversions.getDoubleFromIntLong(option.get(\"propensity\")));\n\n\t\t\t\t\tif (!option.has(\"epsilon_nominated\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"epsilon_nominated\", -1.0);\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"epsilon_nominated\", (double) DataTypeConversions.getDoubleFromIntLong(option.get(\"epsilon_nominated\")));\n\n\t\t\t\t\tfinalOffers.put(offerIndex, finalOffersObject);\n\t\t\t\t\tofferIndex = offerIndex + 1;\n\t\t\t\t}\n\t\t\t}\n\n\t\t\tJSONArray sortJsonArray = JSONArraySort.sortArray(finalOffers, \"arm_reward\", \"double\", \"d\");\n\t\t\tpredictModelMojoResult.put(\"final_result\", sortJsonArray);\n\n\t\t\tpredictModelMojoResult = getTopScores(params, predictModelMojoResult);\n\n\t\t\tdouble endTimePost = System.nanoTime();\n\t\t\tLOGGER.info(\"PlatformDynamicEngagement:I001: time in ms: \".concat( String.valueOf((endTimePost - startTimePost) / 1000000) ));\n\n\t\t} catch (Exception e) {\n\t\t\te.printStackTrace();\n\t\t\tLOGGER.error(e);\n\t\t}\n\n\t\treturn predictModelMojoResult;\n\n\t}\n\n}\n",
        "PostScoreBasic.java": "package com.ecosystem.plugin.customer;\n\nimport com.datastax.oss.driver.api.core.CqlSession;\nimport com.ecosystem.utils.DataTypeConversions;\nimport com.ecosystem.utils.JSONArraySort;\nimport hex.genmodel.easy.EasyPredictModelWrapper;\nimport com.ecosystem.utils.log.LogManager;\nimport com.ecosystem.utils.log.Logger;\nimport org.json.JSONArray;\nimport org.json.JSONObject;\n\nimport java.util.ArrayList;\n\nimport static com.ecosystem.EcosystemResponse.obtainBudget;\n\n/**\n * This the ecosystem/Ai generic post-score template.\n * Customer plugin for specialized logic to be added to the runtime engine.\n * This class is loaded through the plugin loader system.\n */\npublic class PostScoreBasic extends PostScoreSuper {\n\tprivate static final Logger LOGGER = LogManager.getLogger(PostScoreBasic.class.getName());\n\n\tpublic PostScoreBasic() {\n\t}\n\n\t/**\n\t * Pre-post predict logic\n\t */\n\tpublic void getPostPredict () {\n\t}\n\n\t/**\n\t * getPostPredict\n\t *\n\t * @param predictModelMojoResult Result from scoring\n\t * @param params                 Params carried from input\n\t * @param session                Session variable for Cassandra\n\t * @param models \t\t\t\t Preloaded H2O Models\n\t * @return JSONObject result to further post-scoring logic\n\t */\n\tpublic static JSONObject getPostPredict(JSONObject predictModelMojoResult, JSONObject params, CqlSession session, EasyPredictModelWrapper[] models) {\n\t\tdouble startTimePost = System.nanoTime();\n\t\ttry {\n\t\t\t/* Setup JSON objects for specific prediction case */\n\t\t\tJSONObject featuresObj = predictModelMojoResult.getJSONObject(\"featuresObj\");\n\t\t\tJSONObject domainsProbabilityObj = new JSONObject();\n\t\t\tif (predictModelMojoResult.has(\"domainsProbabilityObj\"))\n\t\t\t\tdomainsProbabilityObj = predictModelMojoResult.getJSONObject(\"domainsProbabilityObj\");\n\n\t\t\t/* If whitelist settings then only allow offers on list */\n\t\t\tboolean whitelist = false;\n\t\t\tArrayList<String> offerWhiteList = new ArrayList<>();\n\t\t\tif (params.has(\"whitelist\")) {\n\t\t\t\tif (!params.getJSONObject(\"whitelist\").isEmpty()) {\n\t\t\t\t\tofferWhiteList = (ArrayList<String>) params.getJSONObject(\"whitelist\").get(\"whitelist\");\n\t\t\t\t\tparams.put(\"resultcount\", offerWhiteList.size());\n\t\t\t\t\twhitelist = DataTypeConversions.getBooleanFromString(params.getJSONObject(\"whitelist\").get(\"logicin\"));\n\t\t\t\t}\n\t\t\t}\n\n\t\t\tif (params.has(\"preloadCorpora\")) {\n\t\t\t\tif (params.getJSONObject(\"preloadCorpora\").has(\"network\")) {\n\t\t\t\t\tJSONObject a = params.getJSONObject(\"preloadCorpora\");\n\t\t\t\t\tJSONObject preloadCorpora = a.getJSONObject(\"network\");\n\t\t\t\t}\n\t\t\t}\n\n\t\t\tJSONArray finalOffers = new JSONArray();\n\t\t\tint resultcount = (int) params.get(\"resultcount\");\n\t\t\t/* For each offer in offer matrix determine eligibility */\n\t\t\t/* get selector field from properties: predictor.selector.setup */\n\t\t\t// String s = new JSONObject(settings.getSelectorSetup()).getJSONObject(\"lookup\").getString(\"fields\");\n\n\t\t\t/** This loop can be used to add number of offers/options to return result */\n\t\t\tJSONObject finalOffersObject = new JSONObject();\n\t\t\tint offerIndex = 0;\n\t\t\tfor (int i = 0; i < resultcount; i++) {\n\n\t\t\t\t/** Model type based approaches */\n\t\t\t\tString type = \"\";\n\t\t\t\tboolean explainability = false;\n\t\t\t\t// LOGGER.info(\"predictModelMojoResult: \" + predictModelMojoResult.toString());\n\t\t\t\tif (predictModelMojoResult.get(\"type\").getClass().getName().toLowerCase().contains(\"array\")) {\n\t\t\t\t\ttype = predictModelMojoResult\n\t\t\t\t\t\t\t.getJSONArray(\"type\")\n\t\t\t\t\t\t\t.get(0)\n\t\t\t\t\t\t\t.toString().toLowerCase().trim();\n\t\t\t\t\tif (predictModelMojoResult.has(\"shapley_contributions\"))\n\t\t\t\t\t\texplainability = true;\n\t\t\t\t} else {\n\t\t\t\t\ttype = ((String) predictModelMojoResult.get(\"type\")).toLowerCase().trim();\n\t\t\t\t}\n\n\t\t\t\t/** Offer name, defaults to type (replace with offer matrix etc) */\n\t\t\t\tif (featuresObj.has(\"offer_name_final\"))\n\t\t\t\t\tfinalOffersObject.put(\"offer_name\", featuresObj.get(\"offer_name_final\"));\n\t\t\t\telse\n\t\t\t\t\tfinalOffersObject.put(\"offer_name\", type);\n\n\t\t\t\tif (featuresObj.has(\"offer\"))\n\t\t\t\t\tfinalOffersObject.put(\"offer\", featuresObj.get(\"offer\"));\n\t\t\t\telse\n\t\t\t\t\tfinalOffersObject.put(\"offer\", type);\n\n\t\t\t\tif (featuresObj.has(\"offer_id\"))\n\t\t\t\t\tfinalOffersObject.put(\"offer\", featuresObj.get(\"offer_id\"));\n\t\t\t\telse\n\t\t\t\t\tfinalOffersObject.put(\"offer_id\", type);\n\n\t\t\t\tif (featuresObj.has(\"price\"))\n\t\t\t\t\tfinalOffersObject.put(\"price\", featuresObj.get(\"price\"));\n\t\t\t\telse\n\t\t\t\t\tfinalOffersObject.put(\"price\", 1.0);\n\n\t\t\t\tif (featuresObj.has(\"cost\"))\n\t\t\t\t\tfinalOffersObject.put(\"cost\", featuresObj.get(\"cost\"));\n\t\t\t\telse\n\t\t\t\t\tfinalOffersObject.put(\"cost\", 1.0);\n\n\t\t\t\t/** Score based on model type */\n\t\t\t\tif (type.contains(\"clustering\")) {\n\t\t\t\t\tfinalOffersObject.put(\"cluster\", predictModelMojoResult.getJSONArray(\"cluster\").get(0));\n\t\t\t\t\tfinalOffersObject.put(\"score\", DataTypeConversions.getDouble(domainsProbabilityObj, \"score\"));\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", DataTypeConversions.getDouble(domainsProbabilityObj, \"score\"));\n\t\t\t\t} else if (type.contains(\"anomalydetection\")) {\n\t\t\t\t\tdouble[] score = (double[]) domainsProbabilityObj.get(\"score\");\n\t\t\t\t\tfinalOffersObject.put(\"score\", score[0]);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", score[0]);\n\t\t\t\t} else if (type.contains(\"regression\")) {\n\t\t\t\t\tObject score = predictModelMojoResult.getJSONArray(\"value\").get(0);\n\t\t\t\t\tfinalOffersObject.put(\"score\", score);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", score);\n\t\t\t\t} else if (type.contains(\"multinomial\")) {\n\t\t\t\t\tObject probability = predictModelMojoResult.getJSONArray(\"probability\").get(0);\n\t\t\t\t\tObject label = null;\n\t\t\t\t\ttry {\n\t\t\t\t\t\tlabel = predictModelMojoResult.getJSONArray(\"label\").get(0);\n\t\t\t\t\t} catch (Exception e) {\n\t\t\t\t\t\tLOGGER.error(\"PostScoreBasic:getPostPredict:E001: Error relates to scoring your model. The model wasn't loaded or is not accessible.\");\n\t\t\t\t\t\te.printStackTrace();\n\t\t\t\t\t}\n\t\t\t\t\tObject response = predictModelMojoResult.getJSONArray(\"response\").get(0);\n\t\t\t\t\tfinalOffersObject.put(\"score\", probability);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", probability);\n\t\t\t\t\tfinalOffersObject.put(\"offer\", label);\n\t\t\t\t\tfinalOffersObject.put(\"offer_name\", response);\n\t\t\t\t} else if (type.contains(\"coxph\")) {\n\t\t\t\t\tObject score = predictModelMojoResult.getJSONArray(\"value\").get(0);\n\t\t\t\t\tfinalOffersObject.put(\"score\", score);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", score);\n\t\t\t\t} else if (type.contains(\"wordembedding\")) {\n\t\t\t\t\tfloat[] score = (float[]) predictModelMojoResult.getJSONArray(\"_text_word2vec\").get(0);\n\t\t\t\t\tfinalOffersObject.put(\"score\", Double.valueOf(String.valueOf(score[0])));\n\t\t\t\t\tfinalOffersObject.put(\"embedding\", score);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", 0.0);\n\t\t\t\t} else if (type.contains(\"deeplearning\")) {\n\t\t\t\t\t/** From TensorFlow or PyTorch */\n\t\t\t\t\tObject score = domainsProbabilityObj.getDouble(\"1\");\n\t\t\t\t\tfinalOffersObject.put(\"score\", score);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", score);\n\t\t\t\t\tObject response = predictModelMojoResult.getJSONArray(\"response\").get(0);\n\t\t\t\t\tfinalOffersObject.put(\"offer_name\", response);\n\t\t\t\t} else if (type.contains(\"empty score\")) {\n\t\t\t\t\t/** This is typically used for data lookup only, obtain values from feature store! */\n\t\t\t\t\tif (featuresObj.has(\"offer_name\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"offer_name\", featuresObj.get(\"offer_name\"));\n\n\t\t\t\t\tif (featuresObj.has(\"offer\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"offer\", featuresObj.get(\"offer\"));\n\n\t\t\t\t\tif (featuresObj.has(\"score\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"score\", Double.valueOf(String.valueOf(featuresObj.get(\"score\"))));\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"score\", 1.0);\n\n\t\t\t\t\tif (featuresObj.has(\"modified_offer_score\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", Double.valueOf(String.valueOf(featuresObj.get(\"modified_offer_score\"))));\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", 1.0);\n\n\t\t\t\t\tif (featuresObj.has(\"cost\"))\n\t\t\t\t\t\tfinalOffersObject.put(\"cost\", Double.valueOf(String.valueOf(featuresObj.get(\"cost\"))));\n\t\t\t\t\telse\n\t\t\t\t\t\tfinalOffersObject.put(\"cost\", 0.0);\n\n\t\t\t\t} else {\n\t\t\t\t\tfinalOffersObject.put(\"score\", 1.0);\n\t\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", 1.0);\n\t\t\t\t}\n\n\t\t\t\tfinalOffersObject.put(\"offer_details\", domainsProbabilityObj);\n\t\t\t\tif (explainability) {\n\t\t\t\t\tfinalOffersObject.put(\"shapley_contributions\", predictModelMojoResult.get(\"shapley_contributions\"));\n\t\t\t\t\tfinalOffersObject.put(\"shapley_contributions_names\", predictModelMojoResult.get(\"shapley_contributions_names\"));\n\t\t\t\t}\n\n\t\t\t\t/** Default value, could be replaced by offer matrix or feature store */\n\t\t\t\tdouble offer_value = 1.0;\n\t\t\t\tfinalOffersObject.put(\"offer_value\", offer_value);\n\t\t\t\tfinalOffersObject.put(\"uuid\", params.get(\"uuid\"));\n\n\t\t\t\t/** Add other structures to the final result */\n\t\t\t\tfinalOffersObject.put(\"offer_matrix\", featuresObj);\n\n\t\t\t\t/** Budget processing option, if it's set in the properties */\n\t\t\t\tif (settings.getPredictorOfferBudget() != null) {\n\t\t\t\t\tJSONObject budgetItem = obtainBudget(featuresObj, params.getJSONObject(\"featuresObj\"), offer_value);\n\t\t\t\t\tdouble budgetSpendLimit = budgetItem.getDouble(\"spend_limit\");\n\t\t\t\t\tfinalOffersObject.put(\"spend_limit\", budgetSpendLimit);\n\t\t\t\t}\n\n\t\t\t\t/** Prepare offer array before final sorting */\n\t\t\t\tfinalOffers.put(offerIndex, finalOffersObject);\n\t\t\t\tofferIndex = offerIndex + 1;\n\t\t\t}\n\n\t\t\t/** Sort final offer list based on score */\n\t\t\tJSONArray sortJsonArray = JSONArraySort.sortArray(finalOffers, \"score\", \"double\", \"d\");\n\t\t\tpredictModelMojoResult.put(\"final_result\", sortJsonArray);\n\n\t\t} catch (Exception e) {\n\t\t\tLOGGER.error(e);\n\t\t}\n\n\t\t/** Get top scores and test for explore/exploit randomization */\n\t\tpredictModelMojoResult = getTopScores(params, predictModelMojoResult);\n\n\t\tdouble endTimePost = System.nanoTime();\n\t\tLOGGER.info(\"getPostPredict:I001: execution time in ms: \".concat( String.valueOf((endTimePost - startTimePost) / 1000000) ));\n\t\treturn predictModelMojoResult;\n\t}\n\n}\n",
        "PostScoreRecommender.java": "package com.ecosystem.plugin.customer;\n\nimport com.datastax.oss.driver.api.core.CqlSession;\nimport com.ecosystem.utils.GlobalSettings;\nimport com.ecosystem.utils.JSONArraySort;\nimport com.ecosystem.utils.MathRandomizer;\nimport hex.genmodel.easy.EasyPredictModelWrapper;\nimport com.ecosystem.utils.log.LogManager;\nimport com.ecosystem.utils.log.Logger;\nimport org.json.JSONArray;\nimport org.json.JSONObject;\n\nimport java.io.IOException;\n\n/**\n * ECOSYSTEM.AI INTERNAL PLATFORM SCORING\n * Use this class to perform generic scoring based on model and generic settings with label from scoring.\n */\npublic class PostScoreRecommender {\n\tprivate static final Logger LOGGER = LogManager.getLogger(PostScoreRecommender.class.getName());\n\n\tstatic GlobalSettings settings;\n\tstatic {\n\t\ttry {\n\t\t\tsettings = new GlobalSettings();\n\t\t} catch (IOException e) {\n\t\t\te.printStackTrace();\n\t\t} catch (Exception e) {\n\t\t\te.printStackTrace();\n\t\t}\n\t}\n\n\tpublic PostScoreRecommender() {\n\t}\n\n\t/**\n\t * Pre-post predict logic\n\t */\n\tpublic void getPostPredict () {\n\t}\n\n\t/**\n\t * getPostPredict\n\t * Example params:\n\t *    {\"contextual_variable_one\":\"Easy Income Gold|Thin|Senior\", \"contextual_variable_two\":\"\", \"batch\": true}\n\t *\n\t * @param predictModelMojoResult Result from scoring\n\t * @param params                 Params carried from input\n\t * @param session                Session variable for Cassandra\n\t * @return JSONObject result to further post-scoring logic\n\t */\n\tpublic static JSONObject getPostPredict(JSONObject predictModelMojoResult, JSONObject params, CqlSession session, EasyPredictModelWrapper[] models) {\n\t\tdouble startTimePost = System.nanoTime();\n\t\ttry {\n\t\t\t/* Setup JSON objects for specific prediction case */\n\t\t\tJSONObject featuresObj = predictModelMojoResult.getJSONObject(\"featuresObj\");\n\t\t\tif (predictModelMojoResult.has(\"ErrorMessage\")) {\n\t\t\t\tLOGGER.error(\"getPostPredict:E001a:\" + predictModelMojoResult.get(\"ErrorMessage\"));\n\t\t\t\treturn null;\n\t\t\t}\n\n\t\t\tJSONArray offerMatrix = new JSONArray();\n\t\t\tif (params.has(\"offerMatrix\"))\n\t\t\t\tofferMatrix = params.getJSONArray(\"offerMatrix\");\n\n\t\t\tJSONObject work = params.getJSONObject(\"in_params\");\n\n\t\t\tJSONObject domainsProbabilityObj = predictModelMojoResult.getJSONObject(\"domainsProbabilityObj\");\n\t\t\tString label = predictModelMojoResult.getJSONArray(\"label\").getString(0);\n\n\t\t\tJSONArray probabilities = new JSONArray();\n\t\t\tif (predictModelMojoResult.has(\"probability\"))\n\t\t\t\tprobabilities = predictModelMojoResult.getJSONArray(\"probability\");\n\t\t\telse\n\t\t\t\tprobabilities = predictModelMojoResult.getJSONArray(\"probabilities\");\n\n\t\t\tJSONArray domains = predictModelMojoResult.getJSONArray(\"domains\");\n\n\t\t\tJSONArray finalOffers = new JSONArray();\n\t\t\tint resultcount = (int) params.get(\"resultcount\");\n\t\t\tint offerIndex = 0;\n\n\t\t\t/** Select top items based on number of offers to present */\n\t\t\tfor (int i = 0; i < resultcount; i++) {\n\t\t\t\tint explore = (int) params.get(\"explore\");\n\t\t\t\tJSONObject finalOffersObject = new JSONObject();\n\n\t\t\t\tfinalOffersObject.put(\"offer\", label);\n\t\t\t\tfinalOffersObject.put(\"offer_name\", label);\n\t\t\t\tfinalOffersObject.put(\"offer_name_desc\", label + \" - \" + i);\n\n\t\t\t\t/** process final */\n\t\t\t\tdouble p = domainsProbabilityObj.getDouble(label);\n\t\t\t\tfinalOffersObject.put(\"score\", p);\n\t\t\t\tfinalOffersObject.put(\"final_score\", p);\n\t\t\t\tfinalOffersObject.put(\"modified_offer_score\", p);\n\t\t\t\tfinalOffersObject.put(\"offer_value\", 1.0); // use value from offer matrix\n\t\t\t\tfinalOffersObject.put(\"price\", 1.0);\n\t\t\t\tfinalOffersObject.put(\"cost\", 1.0);\n\n\t\t\t\tfinalOffersObject.put(\"p\", p);\n\t\t\t\tfinalOffersObject.put(\"explore\", explore);\n\n\t\t\t\t/** Prepare array before final sort */\n\t\t\t\tfinalOffers.put(offerIndex, finalOffersObject);\n\t\t\t\tofferIndex = offerIndex + 1;\n\t\t\t}\n\n\t\t\tJSONArray sortJsonArray = JSONArraySort.sortArray(finalOffers, \"score\", \"double\", \"d\");\n\t\t\tpredictModelMojoResult.put(\"final_result\", sortJsonArray);\n\n\t\t} catch (Exception e) {\n\t\t\te.printStackTrace();\n\t\t\tLOGGER.error(e);\n\t\t}\n\n\t\tpredictModelMojoResult = getTopScores(params, predictModelMojoResult);\n\n\t\tdouble endTimePost = System.nanoTime();\n\t\tLOGGER.info(\"PlatformDynamicEngagement:I001: time in ms: \".concat( String.valueOf((endTimePost - startTimePost) / 1000000) ));\n\n\t\treturn predictModelMojoResult;\n\n\t}\n\n\tprivate static JSONObject getExplore(JSONObject params, double epsilonIn, String name) {\n\t\tdouble rand = MathRandomizer.getRandomDoubleBetweenRange(0, 1);\n\t\tdouble epsilon = epsilonIn;\n\t\tparams.put(name + \"_epsilon\", epsilon);\n\t\tif (rand <= epsilon) {\n\t\t\tparams.put(name, 1);\n\t\t} else {\n\t\t\tparams.put(name, 0);\n\t\t}\n\t\treturn params;\n\t}\n\n\t/**\n\t * Get random results for MAB\n\t * @param predictResult\n\t * @param numberOffers\n\t * @return\n\t */\n\tpublic static JSONArray getSelectedPredictResultRandom(JSONObject predictResult, int numberOffers) {\n\t\treturn getSelectedPredictResultExploreExploit(predictResult, numberOffers, 1);\n\t}\n\n\t/**\n\t * Get result based on score\n\t * @param predictResult\n\t * @param numberOffers\n\t * @return\n\t */\n\tpublic static JSONArray getSelectedPredictResult(JSONObject predictResult, int numberOffers) {\n\t\treturn getSelectedPredictResultExploreExploit(predictResult, numberOffers, 0);\n\t}\n\n\tprivate static JSONObject setValues(JSONObject work) {\n\t\tJSONObject result = new JSONObject();\n\t\tresult.put(\"score\", work.get(\"score\"));\n\t\tif (work.has(\"price\"))\n\t\t\tresult.put(\"price\", work.get(\"price\"));\n\t\tif (work.has(\"cost\"))\n\t\t\tresult.put(\"cost\", work.get(\"cost\"));\n\t\tresult.put(\"final_score\", work.get(\"score\"));\n\t\tresult.put(\"offer\", work.get(\"offer\"));\n\t\tresult.put(\"offer_name\", work.get(\"offer_name\"));\n\t\tresult.put(\"modified_offer_score\", work.get(\"modified_offer_score\"));\n\t\tresult.put(\"offer_value\", work.get(\"offer_value\"));\n\t\treturn result;\n\t}\n\n\t/**\n\t * Set values JSONObject that will be used in final\n\t * @param work\n\t * @param rank\n\t * @return\n\t */\n\tprivate static JSONObject setValuesFinal(JSONObject work, int rank) {\n\t\tJSONObject offer = new JSONObject();\n\n\t\toffer.put(\"rank\", rank);\n\t\toffer.put(\"result\", setValues(work));\n\t\toffer.put(\"result_full\", work);\n\n\t\treturn offer;\n\t}\n\n\t/**\n\t * Review this: Master version in EcosystemMaster class. {offer_treatment_code: {$regex:\"_A\"}}\n\t *\n\t * @param predictResult\n\t * @param numberOffers\n\t * @return\n\t */\n\tpublic static JSONArray getSelectedPredictResultExploreExploit(JSONObject predictResult, int numberOffers, int explore) {\n\t\tJSONArray offers = new JSONArray();\n\t\tint resultLength = predictResult.getJSONArray(\"final_result\").length();\n\n\t\tfor (int j = 0, k = 0; j < resultLength; j++) {\n\t\t\tJSONObject work = new JSONObject();\n\t\t\tif (explore == 1) {\n\t\t\t\tint rand = MathRandomizer.getRandomIntBetweenRange(0, resultLength - 1);\n\t\t\t\twork = predictResult.getJSONArray(\"final_result\").getJSONObject(rand);\n\t\t\t} else {\n\t\t\t\twork = predictResult.getJSONArray(\"final_result\").getJSONObject(j);\n\t\t\t}\n\n\t\t\t/* test if budget is enabled && spend_limit is greater than 0, if budget is disabled, then this will be 1.0 */\n\t\t\tif (settings.getPredictorOfferBudget() != null) {\n\t\t\t\t/* if budget setting and there is budget to spend */\n\t\t\t\tif (work.has(\"spend_limit\")) {\n\t\t\t\t\tif ((work.getDouble(\"spend_limit\") > 0.0) | work.getDouble(\"spend_limit\") == -1) {\n\t\t\t\t\t\toffers.put(k, setValuesFinal(work, k + 1));\n\t\t\t\t\t\tif ((k + 1) == numberOffers) break;\n\t\t\t\t\t\tk = k + 1;\n\t\t\t\t\t}\n\t\t\t\t} else {\n\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t} else {\n\t\t\t\t/* no budget setting present */\n\t\t\t\toffers.put(k, setValuesFinal(work, k + 1));\n\t\t\t\tif ((k + 1) == numberOffers) break;\n\t\t\t\tk = k + 1;\n\t\t\t}\n\t\t}\n\n\t\treturn offers;\n\t}\n\n\t/**\n\t * @param params\n\t * @param predictResult\n\t * @return\n\t */\n\tprivate static JSONObject getTopScores(JSONObject params, JSONObject predictResult) {\n\t\tint resultCount = 1;\n\t\tif (params.has(\"resultcount\")) resultCount = params.getInt(\"resultcount\");\n\t\tif (predictResult.getJSONArray(\"final_result\").length() <= resultCount)\n\t\t\tresultCount = predictResult.getJSONArray(\"final_result\").length();\n\n\t\t/* depending on epsilon and mab settings */\n\t\tif (params.getInt(\"explore\") == 0) {\n\t\t\tpredictResult.put(\"final_result\", getSelectedPredictResult(predictResult, resultCount));\n\t\t\tpredictResult.put(\"explore\", 0);\n\t\t} else {\n\t\t\tpredictResult.put(\"final_result\", getSelectedPredictResultRandom(predictResult, resultCount));\n\t\t\tpredictResult.put(\"explore\", 1);\n\t\t}\n\t\treturn predictResult;\n\t}\n\n}\n",
        "PostScoreRecommenderOffers.java": "package com.ecosystem.plugin.customer;\n\nimport com.datastax.oss.driver.api.core.CqlSession;\nimport com.ecosystem.utils.DataTypeConversions;\nimport com.ecosystem.utils.JSONArraySort;\nimport hex.genmodel.easy.EasyPredictModelWrapper;\nimport com.ecosystem.utils.log.LogManager;\nimport com.ecosystem.utils.log.Logger;\nimport org.json.JSONArray;\nimport org.json.JSONObject;\n\n/**\n * recommender_smp - Single model for all products with Offermatrix\n * Multiclass classifier trained on offer_name response column, offer matrix need to have all the offers loaded with offer_price.\n */\npublic class PostScoreRecommenderOffers extends PostScoreSuper {\n    private static final Logger LOGGER = LogManager.getLogger(PostScoreRecommenderOffers.class.getName());\n\n    public PostScoreRecommenderOffers() {\n    }\n\n    /**\n     * Pre-post predict logic\n     */\n    public void getPostPredict () {\n    }\n\n    /**\n     * getPostPredict\n     *\n     * @param predictModelMojoResult Result from scoring\n     * @param params                 Params carried from input\n     * @param session                Session variable for Cassandra\n     * @return JSONObject result to further post-scoring logic\n     */\n    public static JSONObject getPostPredict(JSONObject predictModelMojoResult, JSONObject params, CqlSession session, EasyPredictModelWrapper[] models) {\n        double startTimePost = System.nanoTime();\n        try {\n            /** Value obtained via API params */\n            JSONObject work = params.getJSONObject(\"in_params\");\n            double in_balance = 1000.0;\n            if (work.has(\"in_balance\"))\n                in_balance = DataTypeConversions.getDouble(work, \"in_balance\");\n            else\n                LOGGER.info(\"getPostPredict:I001aa: No in_balance specified, default used. (1000.00)\");\n\n            JSONArray sortJsonArray = new JSONArray();\n            JSONArray finalOffers = new JSONArray();\n\n            /* Setup JSON objects for specific prediction case */\n            JSONObject featuresObj = predictModelMojoResult.getJSONObject(\"featuresObj\");\n            if (predictModelMojoResult.has(\"ErrorMessage\")) {\n                LOGGER.error(\"getPostPredict:E001a:\" + predictModelMojoResult.get(\"ErrorMessage\"));\n                return null;\n            }\n\n            JSONArray offerMatrix = new JSONArray();\n            if (params.has(\"offerMatrix\"))\n                offerMatrix = params.getJSONArray(\"offerMatrix\");\n\n            JSONObject domainsProbabilityObj = predictModelMojoResult.getJSONObject(\"domainsProbabilityObj\");\n            String label = predictModelMojoResult.getJSONArray(\"label\").getString(0);\n            JSONArray domains = predictModelMojoResult.getJSONArray(\"domains\");\n\n            int resultcount = (int) params.get(\"resultcount\");\n            int offerIndex = 0;\n\n            /** Select top items based on number of offers to present */\n            for (int i = 0; i < offerMatrix.length(); i++) {\n                JSONObject singleOffer = offerMatrix.getJSONObject(i);\n\n                int explore = (int) params.get(\"explore\");\n                JSONObject finalOffersObject = new JSONObject();\n\n                double offer_value = 1.0;\n                if (singleOffer.has(\"offer_price\"))\n                    offer_value = DataTypeConversions.getDouble(singleOffer, \"offer_price\");\n                if (singleOffer.has(\"price\"))\n                    offer_value = DataTypeConversions.getDouble(singleOffer, \"price\");\n\n                double offer_cost = 1.0;\n                if (singleOffer.has(\"offer_cost\"))\n                    offer_cost = singleOffer.getDouble(\"offer_cost\");\n                if (singleOffer.has(\"cost\"))\n                    offer_cost = singleOffer.getDouble(\"cost\");\n\n                double p = 0.0;\n                String offer_id = \"\";\n                if (domainsProbabilityObj.has(singleOffer.getString(\"offer_id\"))) {\n                    offer_id = singleOffer.getString(\"offer_id\");\n                    p = domainsProbabilityObj.getDouble(offer_id);\n                } else {\n                    LOGGER.error(\"offerRecommender:E002-1: \" + params.get(\"uuid\") + \" - Not available: \" + singleOffer.getString(\"offer_name\"));\n                }\n\n                double modified_offer_score = 1.0;\n                modified_offer_score = p * ((double) offer_value - offer_cost);\n\n                finalOffersObject.put(\"offer\", offer_id);\n                finalOffersObject.put(\"offer_name\", singleOffer.get(\"offer_name\"));\n                finalOffersObject.put(\"offer_name_desc\", singleOffer.get(\"offer_name\") + \" - \" + i);\n\n                /** process final */\n                // double p = domainsProbabilityObj.getDouble(label);\n                finalOffersObject.put(\"score\", p);\n                finalOffersObject.put(\"final_score\", p);\n                finalOffersObject.put(\"modified_offer_score\", modified_offer_score);\n                finalOffersObject.put(\"offer_value\", offer_value); // use value from offer matrix\n                finalOffersObject.put(\"price\", offer_value);\n                finalOffersObject.put(\"cost\", offer_cost);\n                finalOffersObject.put(\"uuid\", params.get(\"uuid\"));\n\n                finalOffersObject.put(\"p\", p);\n                finalOffersObject.put(\"explore\", explore);\n\n                /** Prepare array before final sort */\n                finalOffers.put(offerIndex, finalOffersObject);\n                offerIndex = offerIndex + 1;\n            }\n\n            sortJsonArray = JSONArraySort.sortArray(finalOffers, \"modified_offer_score\", \"double\", \"d\");\n            predictModelMojoResult.put(\"final_result\", sortJsonArray);\n\n            /** Select the correct number of offers */\n            predictModelMojoResult = getTopScores(params, predictModelMojoResult);\n\n        } catch (Exception e) {\n            e.printStackTrace();\n            LOGGER.error(e);\n        }\n\n        /** Top scores from final_result */\n        predictModelMojoResult = getTopScores(params, predictModelMojoResult);\n\n        double endTimePost = System.nanoTime();\n        LOGGER.info(\"PostScoreRecommenderOffers:I001: time in ms: \".concat( String.valueOf((endTimePost - startTimePost) / 1000000) ));\n\n        return predictModelMojoResult;\n\n    }\n\n}\n",
        "PostScoreRecommenderMulti.java": "package com.ecosystem.plugin.customer;\n\nimport com.datastax.oss.driver.api.core.CqlSession;\nimport com.ecosystem.plugin.lib.ScoreAsyncItems;\nimport com.ecosystem.utils.DataTypeConversions;\nimport com.ecosystem.utils.GlobalSettings;\nimport com.ecosystem.utils.JSONArraySort;\nimport com.ecosystem.utils.MathRandomizer;\nimport com.ecosystem.worker.h2o.ModelPredictWorkerH2O;\nimport hex.genmodel.easy.EasyPredictModelWrapper;\nimport hex.genmodel.easy.RowData;\nimport com.ecosystem.utils.log.LogManager;\nimport com.ecosystem.utils.log.Logger;\nimport org.json.JSONArray;\nimport org.json.JSONObject;\n\nimport java.io.IOException;\nimport java.util.concurrent.ExecutionException;\n\n/**\n * recommender_smp - Multiple models for per product with Offermatrix\n * Binomial model per product, all loaded into memory, scoring per offerMatrix line item.\n */\npublic class PostScoreRecommenderMulti {\n\n    private static final Logger LOGGER = LogManager.getLogger(PostScoreRecommenderMulti.class.getName());\n\n    ModelPredictWorkerH2O modelPredictWorkerH2O;\n    ScoreAsyncItems scoreAsyncItems;\n\n    static GlobalSettings settings;\n    static {\n        try {\n            settings = new GlobalSettings();\n        } catch (IOException e) {\n            e.printStackTrace();\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n\n    public PostScoreRecommenderMulti() {\n        modelPredictWorkerH2O = new ModelPredictWorkerH2O();\n        scoreAsyncItems = new ScoreAsyncItems(modelPredictWorkerH2O);\n    }\n\n    /**\n     * Pre-post predict logic\n     */\n    public void getPostPredict () {\n    }\n\n    /**\n     * getPostPredict\n     *\n     * @param predictModelMojoResult Result from scoring\n     * @param params                 Params carried from input\n     * @param session                Session variable for Cassandra\n     * @return JSONObject result to further post-scoring logic\n     */\n    public JSONObject getPostPredict(JSONObject predictModelMojoResult, JSONObject params, CqlSession session, EasyPredictModelWrapper[] models) {\n\n        double startTimePost = System.nanoTime();\n\n        /** Value obtained via API params */\n        JSONObject work = params.getJSONObject(\"in_params\");\n        double in_balance = 100.0;\n        if (work.has(\"in_balance\"))\n            in_balance = DataTypeConversions.getDouble(work, \"in_balance\");\n        else\n            LOGGER.info(\"getPostPredict:I001aa: No in_balance specified, default used. (1000.00)\");\n\n        JSONArray finalOffers = new JSONArray();\n\n        /* Setup JSON objects for specific prediction case */\n        JSONObject featuresObj = predictModelMojoResult.getJSONObject(\"featuresObj\");\n        if (predictModelMojoResult.has(\"ErrorMessage\")) {\n            LOGGER.error(\"getPostPredict:E001a:\" + predictModelMojoResult.get(\"ErrorMessage\"));\n            return null;\n        }\n\n        JSONArray offerMatrix = new JSONArray();\n        if (params.has(\"offerMatrix\"))\n            offerMatrix = params.getJSONArray(\"offerMatrix\");\n\n        // JSONObject domainsProbabilityObj = predictModelMojoResult.getJSONObject(\"domainsProbabilityObj\");\n        // String label = predictModelMojoResult.getJSONArray(\"label\").getString(0);\n        // JSONArray domains = predictModelMojoResult.getJSONArray(\"domains\");\n\n        int resultcount = (int) params.get(\"resultcount\");\n        int offerIndex = 0;\n\n        /** Async processing scoring across all models loaded per offer */\n        JSONObject domainsProbabilityObj = new JSONObject();\n        if (predictModelMojoResult.has(\"domainsProbabilityObj\"))\n            domainsProbabilityObj = predictModelMojoResult.getJSONObject(\"domainsProbabilityObj\");\n\n        JSONObject resultScore = new JSONObject();\n        try {\n            double startTimePost1 = System.nanoTime();\n\n            RowData row = modelPredictWorkerH2O.toRowData((JSONObject) predictModelMojoResult.get(\"features\"));\n            resultScore = scoreAsyncItems.allOfAsyncScoring(offerMatrix, params, models, row, domainsProbabilityObj);\n\n            double endTimePost1 = System.nanoTime();\n            LOGGER.info(\"scoreAsyncItems.allOfAsyncScoring:I0001a: Async process time in ms: \".concat( String.valueOf((double) ((endTimePost1 - startTimePost1) / 1000000)) ));\n        } catch (ExecutionException e) {\n            e.printStackTrace();\n        } catch (InterruptedException e) {\n            e.printStackTrace();\n        }\n\n        /** All items are excluded that are not active and no scores */\n        offerMatrix = resultScore.getJSONArray(\"newOfferMatrix\");\n\n        /** Select top items based on number of offers to present */\n        for (int i = 0; i < offerMatrix.length(); i++) {\n            JSONObject singleOffer = offerMatrix.getJSONObject(i);\n            String offer_id = String.valueOf(singleOffer.get(\"offer_id\"));\n\n            LOGGER.debug(\"singleOffer:D001-1: \" + singleOffer.toString());\n            LOGGER.debug(\"singleOffer:offer_id:D001-2: \" + offer_id);\n\n            /** Offer matrix needs item \"price\" for aggregator to work! */\n            double offer_price = 1.0;\n            if (singleOffer.has(\"offer_price\"))\n                offer_price = DataTypeConversions.getDouble(singleOffer, \"offer_price\");\n            else if (singleOffer.has(\"price\"))\n                offer_price = DataTypeConversions.getDouble(singleOffer, \"price\");\n            else\n                LOGGER.error(\"PostScoreRecommenderMultiSafaricom:E0011: price not in offerMatrix, value set to 1\");\n\n            double offer_cost = 1.0;\n            if (singleOffer.has(\"offer_cost\"))\n                offer_cost = singleOffer.getDouble(\"offer_cost\");\n            if (singleOffer.has(\"cost\"))\n                offer_cost = singleOffer.getDouble(\"cost\");\n\n            int explore = (int) params.get(\"explore\");\n            JSONObject finalOffersObject = new JSONObject();\n\n            offer_id = DataTypeConversions.getString(singleOffer.getString(\"offer_id\"));\n\n            /*******************************************************************************/\n\n            double p = resultScore.getDouble(offer_id);\n\n            /*******************************************************************************/\n\n            /** Multi-model needs to store the model for logging - DO NOT REMOVE THIS!*/\n            finalOffersObject.put(\"model_name\", offer_id + \".zip\");\n            finalOffersObject.put(\"model_index\", resultScore.get(offer_id + \"_model_index\"));\n\n            finalOffersObject.put(\"offer\", singleOffer.get(\"offer_id\"));\n            finalOffersObject.put(\"offer_name\", singleOffer.get(\"offer_name\"));\n            // finalOffersObject.put(\"offer_name_desc\", offer_name + \" - \" + i);\n\n            /** process final */\n            // double p = domainsProbabilityObj.getDouble(label);\n            finalOffersObject.put(\"score\", p);\n            finalOffersObject.put(\"final_score\", p);\n            finalOffersObject.put(\"modified_offer_score\", p);\n            finalOffersObject.put(\"offer_value\", offer_price); // use value from offer matrix\n            // finalOffersObject.put(\"offer_profit_probability\", offer_profit * p);\n            finalOffersObject.put(\"price\", offer_price);\n            finalOffersObject.put(\"cost\", offer_cost);\n\n            finalOffersObject.put(\"p\", p);\n            finalOffersObject.put(\"explore\", explore);\n\n            /** Prepare array before final sort */\n            finalOffers.put(offerIndex, finalOffersObject);\n            offerIndex = offerIndex + 1;\n        }\n\n        JSONArray sortJsonArray = JSONArraySort.sortArray(finalOffers, \"score\", \"double\", \"d\");\n        predictModelMojoResult.put(\"final_result\", sortJsonArray);\n\n        predictModelMojoResult = getTopScores(params, predictModelMojoResult);\n\n        /** Multi-model needs to store the model for logging! - DO NOT REMOVE THIS! */\n        if (sortJsonArray.length() > 0) {\n            if (sortJsonArray.getJSONObject(0).has(\"model_index\")) {\n                String model_name = (String) sortJsonArray.getJSONObject(0).get(\"model_name\");\n                params.put(\"model_selected\", model_name);\n            }\n        } else {\n            LOGGER.error(\"PostScoreRecommenderMulti:E999: No result \");\n        }\n\n        double endTimePost = System.nanoTime();\n        LOGGER.info(\"PostScoreRecommenderMulti:I001: time in ms: \".concat( String.valueOf((endTimePost - startTimePost) / 1000000) ));\n\n        return predictModelMojoResult;\n\n    }\n\n    private static JSONObject getExplore(JSONObject params, double epsilonIn, String name) {\n        double rand = MathRandomizer.getRandomDoubleBetweenRange(0, 1);\n        double epsilon = epsilonIn;\n        params.put(name + \"_epsilon\", epsilon);\n        if (rand <= epsilon) {\n            params.put(name, 1);\n        } else {\n            params.put(name, 0);\n        }\n        return params;\n    }\n\n\n    /**\n     * Get random results for MAB\n     * @param predictResult\n     * @param numberOffers\n     * @return\n     */\n    public static JSONArray getSelectedPredictResultRandom(JSONObject predictResult, int numberOffers) {\n        return getSelectedPredictResultExploreExploit(predictResult, numberOffers, 1);\n    }\n\n    /**\n     * Get result based on score\n     * @param predictResult\n     * @param numberOffers\n     * @return\n     */\n    public static JSONArray getSelectedPredictResult(JSONObject predictResult, int numberOffers) {\n        return getSelectedPredictResultExploreExploit(predictResult, numberOffers, 0);\n    }\n\n    private static JSONObject setValues(JSONObject work) {\n        JSONObject result = new JSONObject();\n        result.put(\"score\", work.get(\"score\"));\n        if (work.has(\"price\"))\n            result.put(\"price\", work.get(\"price\"));\n        if (work.has(\"cost\"))\n            result.put(\"cost\", work.get(\"cost\"));\n        result.put(\"final_score\", work.get(\"score\"));\n        result.put(\"offer\", work.get(\"offer\"));\n        result.put(\"offer_name\", work.get(\"offer_name\"));\n        result.put(\"modified_offer_score\", work.get(\"modified_offer_score\"));\n        result.put(\"offer_value\", work.get(\"offer_value\"));\n        return result;\n    }\n\n    /**\n     * Set values JSONObject that will be used in final\n     * @param work\n     * @param rank\n     * @return\n     */\n    private static JSONObject setValuesFinal(JSONObject work, int rank) {\n        JSONObject offer = new JSONObject();\n\n        offer.put(\"rank\", rank);\n        offer.put(\"result\", setValues(work));\n        offer.put(\"result_full\", work);\n\n        return offer;\n    }\n\n\n    /**\n     * Review this: Master version in EcosystemMaster class. {offer_treatment_code: {$regex:\"_A\"}}\n     *\n     * @param predictResult\n     * @param numberOffers\n     * @return\n     */\n    public static JSONArray getSelectedPredictResultExploreExploit(JSONObject predictResult, int numberOffers, int explore) {\n        JSONArray offers = new JSONArray();\n        int resultLength = predictResult.getJSONArray(\"final_result\").length();\n\n        for (int j = 0, k = 0; j < resultLength; j++) {\n            JSONObject work = new JSONObject();\n            if (explore == 1) {\n                int rand = MathRandomizer.getRandomIntBetweenRange(0, resultLength - 1);\n                work = predictResult.getJSONArray(\"final_result\").getJSONObject(rand);\n            } else {\n                work = predictResult.getJSONArray(\"final_result\").getJSONObject(j);\n            }\n\n            /* test if budget is enabled && spend_limit is greater than 0, if budget is disabled, then this will be 1.0 */\n            if (settings.getPredictorOfferBudget() != null) {\n                /* if budget setting and there is budget to spend */\n                if (work.has(\"spend_limit\")) {\n                    if ((work.getDouble(\"spend_limit\") > 0.0) | work.getDouble(\"spend_limit\") == -1) {\n                        offers.put(k, setValuesFinal(work, k + 1));\n                        if ((k + 1) == numberOffers) break;\n                        k = k + 1;\n                    }\n                } else {\n                    break;\n                }\n            } else {\n                /* no budget setting present */\n                offers.put(k, setValuesFinal(work, k + 1));\n                if ((k + 1) == numberOffers) break;\n                k = k + 1;\n            }\n        }\n\n        return offers;\n    }\n\n    /**\n     * @param params\n     * @param predictResult\n     * @return\n     */\n    private static JSONObject getTopScores(JSONObject params, JSONObject predictResult) {\n        int resultCount = 1;\n        if (params.has(\"resultcount\")) resultCount = params.getInt(\"resultcount\");\n        if (predictResult.getJSONArray(\"final_result\").length() <= resultCount)\n            resultCount = predictResult.getJSONArray(\"final_result\").length();\n\n        /* depending on epsilon and mab settings */\n        if (params.getInt(\"explore\") == 0) {\n            predictResult.put(\"final_result\", getSelectedPredictResult(predictResult, resultCount));\n            predictResult.put(\"explore\", 0);\n        } else {\n            predictResult.put(\"final_result\", getSelectedPredictResultRandom(predictResult, resultCount));\n            predictResult.put(\"explore\", 1);\n        }\n        return predictResult;\n    }\n\n}\n",
        "PostScoreNetwork.java": "package com.ecosystem.plugin.customer;\n\nimport com.datastax.oss.driver.api.core.CqlSession;\nimport hex.genmodel.easy.EasyPredictModelWrapper;\nimport com.ecosystem.utils.log.LogManager;\nimport com.ecosystem.utils.log.Logger;\nimport org.json.JSONArray;\nimport org.json.JSONObject;\n\n/**\n */\npublic class PostScoreNetwork extends PostScoreNetworkSuper {\n\n    private static final Logger LOGGER = LogManager.getLogger(PostScoreNetwork.class.getName());\n\n    public PostScoreNetwork() {\n    }\n\n    /**\n     * Pre-post predict logic\n     */\n    public void getPostPredict () {\n    }\n\n    /**\n     * getPostPredict\n     *\n     * @param predictModelMojoResult Result from scoring\n     * @param params                 Params carried from input\n     * @param session                Session variable for Cassandra\n     * @param models                  Preloaded H2O Models\n     * @return JSONObject result to further post-scoring logic\n     */\n    public static JSONObject getPostPredict(JSONObject predictModelMojoResult, JSONObject params, CqlSession session, EasyPredictModelWrapper[] models) {\n        double startTimePost = System.nanoTime();\n        try {\n            /* Setup JSON objects for specific prediction case */\n            JSONObject featuresObj = predictModelMojoResult.getJSONObject(\"featuresObj\");\n\n            /** Final offer list based on score */\n            JSONArray sortJsonArray = new JSONArray();\n\n            /** Execute network based on settings in corpora */\n            /**\n             * Configure a network of client pulse responders bu changing configuration based on lookup, scoring and\n             * other criteria. Ensure that the lookup settings coordinate and that default have been set or removed.\n             * Example, if there's a customer, or other settings in the __network collection, it will use those.\n             * If you want customer to go straight through, then remove that default.\n             *\n             * Additional corpora settings in project:\n             * [\n             * {name:'network',database:'mongodb',db:'master',table:'bank_full_1__network', type:'static', key:'value' },\n             * {name:'network_config',database:'mongodb',db:'master',table:'bank_full_1__network_config', type:'static', key:'name' }\n             * ]\n             * Add this line to \"Additional Corpora\" in your project:\n             * [{name:'network',database:'mongodb',db:'master',table:'bank_full_1__network', type:'static', key:'value' },{name:'network_config',database:'mongodb',db:'master',table:'bank_full_1__network_config', type:'static', key:'name' }]\n             *\n             * bank_full_1__network_config, ensure that this document contains this: \"name\": \"network_config\":\n             * {\n             *   \"switch_key\": \"marital\",\n             *   \"name\": \"network_config\"\n             * }\n             *\n             *\n             * bank_full_1__network, all options will be setup here. Ensure that \"value\": \"\" contains a valid value as per switch_key:\n             * {\n             *   \"numberoffers\": 4,\n             *   \"subcampaign\": \"recommender_dynamic_bayes\",\n             *   \"channel\": \"app\",\n             *   \"campaign\": \"recommender_dynamic_bayes\",\n             *   \"params\": \"{}\",\n             *   \"value\": \"married\",\n             *   \"userid\": \"ecosystem_network\",\n             *   \"url\": \"http://customer.ecosystem.ai:8091\",\n             *   \"customer\": \"281db655-d667-4671-a715-8402c29d7d11\"\n             * }\n             */\n            sortJsonArray = handlePreloadCorpora(params, featuresObj);\n\n            predictModelMojoResult.put(\"final_result\", sortJsonArray);\n\n        } catch (Exception e) {\n            LOGGER.error(\"PostScoreNetwork:E001: \" + e);\n        }\n\n        /** Get top scores and test for explore/exploit randomization */\n        predictModelMojoResult = getTopScores(params, predictModelMojoResult);\n\n        double endTimePost = System.nanoTime();\n        LOGGER.info(\"PostScoreNetwork:I001: execution time in ms: \".concat( String.valueOf((endTimePost - startTimePost) / 1000000) ));\n        return predictModelMojoResult;\n    }\n\n}\n",
    }
    if "deployment_step" in project_details:
        version_list = []
        for i in project_details["deployment_step"]:
            if "plugins" in i:
                if "post_score_class_text" in i["plugins"]:
                    if i["plugins"]["post_score_class_text"] == post_score:
                        version_list.append(i["version"])
    else:
        version_list = []
    if version_list:
        max_version = max(version_list)
        post_score_logic = ""
        for i in project_details["deployment_step"]:
            if "version" in i:
                if i["version"] == max_version:
                    if "plugins" in i:
                        if "post_score_class_text" in i["plugins"]:
                            if i["plugins"]["post_score_class_text"] == post_score:
                                if "post_score_class_code" in i["plugins"]:
                                    post_score_logic = i["plugins"]["post_score_class_code"]
        print(f"WARNING: Using post score class from version {max_version}")
    elif post_score in post_score_code_options:
        post_score_logic = post_score_code_options[post_score]
    else:
        print(
            "WARNING: post_score_class not found in default options or existing deployments in project. Empty class "
            "saved to the deployment. To edit the class use the ecosystem.Ai plugin for IntelliJ or the ecosystem.Ai "
            "workbench")
        post_score_logic = ""
    return post_score_logic


def get_column_list(auth, database, table_collection, datasource):
    """
    Get a list of columns in a table or collection in a database.

    :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
    :param database: The name of the database to get the columns from
    :param table_collection: The name of the table or collection to get the columns from
    :param datasource: The type of datasource to get the columns from. Allowed values are mongodb and cassandra
    """
    if not isinstance(database, str):
        raise ValueError("database must be a string")
    if not isinstance(table_collection, str):
        raise ValueError("table_collection must be a string")
    if datasource not in ["mongodb", "cassandra"]:
        raise ValueError("datasource must be mongodb or cassandra")

    columns = []
    try:
        if datasource == "mongodb":
            data_check = dme.get_data(auth, database, table_collection, {}, 1, {}, 0)
            if data_check == []:
                print("WARNING: It looks like collection {} in database {} is empty or does not exist".format(table_collection,database))
            else:
                columns = list(data_check.keys())
        elif datasource == "cassandra":
            data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(table_collection))
            if data_check["data"] == []:
                print("WARNING: It looks like {} is empty or does not exist".format(table_collection))
            else:
                columns = list(data_check["data"][0].keys())
    except Exception as e:
        raise ValueError(f"Error getting column list: {e}")

    return columns


def define_deployment_virtual_variable(name,original_variable,default,variable_type,variables="",buckets=""):
    """
    Define a virtual variable to be used in a parameter access structure in a deployment step. Virtual variables definitions should be stored in a list that is added to the parameter access structure.

    :param name: The name of the virtual variable
    :param original_variable: The name of the original variable that the virtual variable is based on
    :param default: The default value of the virtual variable
    :param variable_type: The type of the virtual variable. Allowed values are discretize and concatenate
    :param variables: A list of variables to be concatenated. Required if variable_type is concatenate
    :param buckets: A list of buckets to be used for discretization. Should be a list of dictionaries or the form [{"from":0,"to":15,"label":"bucket_1"}] Required if variable_type is discretize
    """
    if not isinstance(name,str):
        raise ValueError("name must be a string")
    if not isinstance(original_variable,str):
        raise ValueError("original_variable must be a string")
    if not isinstance(default,str):
        raise ValueError("default must be a string")
    if variable_type not in ["discretize","concatenate"]:
        raise ValueError("variable_type must be discretize or concatenate")
    if variable_type == "concatenate":
        if not isinstance(variables,list):
            raise ValueError("variables must be a list")
        if not all(isinstance(i,str) for i in variables):
            raise ValueError("variables must be a list of strings")
    if variable_type == "discretize":
        if not isinstance(buckets,list):
            raise ValueError("buckets must be a list of dictionaries")
        if not all(isinstance(i,dict) for i in buckets):
            raise ValueError("buckets must be a list of dictionaries")
        if not all(sorted(list(i.keys())) == ["from", "label", "to"] for i in buckets):
            raise ValueError("buckets must be a list of dictionaries with keys from, to and label")
        if not all(isinstance(i["from"],(int,float)) for i in buckets):
            raise ValueError("from in buckets must be a number")
        if not all(isinstance(i["to"],(int,float)) for i in buckets):
            raise ValueError("to in buckets must be a number")
        if not all(isinstance(i["label"],str) for i in buckets):
            raise ValueError("label in buckets must be a string")

    if variables == "":
        variables = []
    if buckets == "":
        buckets = []

    try:
        virtual_variable = {
            "name": name,
            "default": default,
            "type": variable_type,
            "original_variable": original_variable,
            "fields": variables,
            "buckets": buckets
        }
    except Exception as e:
        raise ValueError(f"Error creating virtual variable: {e}")

    return virtual_variable


def define_deployment_parameter_access(auth,lookup_key,lookup_type,database,table_collection,datasource,lookup_fields=None,lookup_default="",defaults="",virtual_variables=""):
    """
    Define the parameter access structure for a deployment step

    :param lookup_key: The key field to be used for lookup in the parameter access structure
    :param lookup_type: The type of lookup key in the lookup data set. Allowed values are string and int
    :param database: The database to be used for lookup
    :param table_collection: The table or collection to be used for lookup
    :param lookup_fields: A list of fields to be returned from the lookup. If not specified, the list of fields will be looked up from the specified data source and all fields will be returned
    :param datasource: The type of datasource to be used for lookup. Allowed values are mongodb, cassandra and presto
    :param lookup_default: The default value for the lookup key
    :param defaults: A list of default values for fields in the lookup data set
    :param virtual_variables: A list of virtual variables to be used in the parameter access structure. Virtual variables can be defined using the define_deployment_virtual_variable function.
    """
    if not isinstance(lookup_key, str):
        raise ValueError("lookup_key must be a string")
    if lookup_type not in ["string","int","float"]:
        raise ValueError("lookup_type must be string or int")
    if not isinstance(database, str):
        raise ValueError("database must be a string")
    if not isinstance(table_collection, str):
        raise ValueError("table_collection must be a string")
    if lookup_fields is not None:
        if not isinstance(lookup_fields,list):
            raise ValueError("lookup_fields must be a list")
        if not all(isinstance(i, str) for i in lookup_fields):
            raise ValueError("lookup_fields must be a list of strings")
    if datasource not in ["mongodb", "cassandra", "presto"]:
        raise ValueError("datasource must be mongodb, cassandra or presto")
    if defaults != "":
        if not isinstance(defaults, list):
            raise ValueError("defaults must be a list")
        if not all(isinstance(i, str) for i in defaults):
            raise ValueError("defaults must be a list of strings")
    if virtual_variables != "":
        if not isinstance(virtual_variables, list):
            raise ValueError("virtual_variables must be a list")
        if not all(isinstance(i, dict) for i in virtual_variables):
            raise ValueError("virtual_variables must be a list of dictionaries")

    try:
        if lookup_default == "":
            if lookup_type == "string":
                lookup_value = "123"
            else:
                lookup_value = 123
        else:
            if lookup_type == "string":
                lookup_value = str(lookup_default)
            else:
                lookup_value = int(lookup_default)
        lookup = {"key": lookup_key, "value": lookup_value}

        if lookup_fields is None:
            print(f"INFO: lookup_fields not set, getting field list from {database}.{table_collection}")
            lookup_fields = get_column_list(auth, database, table_collection, datasource)
            if not lookup_fields:
                raise ValueError(f"Empty list returned when attempting to automatically populate lookup_fields. If the "
                                 "ecosystem server is not configured to connect to {database}.{table_collection} you "
                                 "will need to add the lookup_fields argument to the function call. If the ecosystem "
                                 "server can connect to {database}.{table_collection}, check that {table_collection}"
                                 "is not empty.")

        create_virtual_variables = False
        if virtual_variables != "":
            create_virtual_variables = True
        else:
            virtual_variables = []

        if defaults != "":
            defaults = ",".join(defaults)

        parameter_access = {
            "lookup": lookup,
            "create_virtual_variables": create_virtual_variables,
            "database": database,
            "table_collection": table_collection,
            "lookup_fields": lookup_fields,
            "datasource": datasource,
            "lookup_defaults": defaults,
            "virtual_variables": virtual_variables
        }
    except Exception as e:
        raise ValueError(f"Error creating parameter access structure: {e}")

    return parameter_access


def define_deployment_model_configuration(models_to_load,models_note="",models_outline="Recommender"):
    """
    Define the model configuration structure for a deployment step

    :param models_to_load: A list of model names to be loaded
    :param models_note: A note to store with the model
    :param models_outline: The structure of the models
    """
    if not isinstance(models_to_load, list):
        raise ValueError("models_to_load must be a list")
    if not all(isinstance(i, str) for i in models_to_load):
        raise ValueError("models_to_load must be a list of strings")
    if not isinstance(models_note, str):
        raise ValueError("models_note must be a string")
    if not isinstance(models_outline, str):
        raise ValueError("models_outline must be a string")

    try:
        models_load= ",".join(models_to_load)
        model_configuration = {
            "models_load": models_load,
            "models_note": models_note,
            "models_outline": models_outline
        }
    except Exception as e:
        raise ValueError(f"Error creating model configuration structure: {e}")

    return model_configuration


def define_deployment_model_selector(database, table_collection, datasource, lookup_key, lookup_type, selector_column, selector, model_configuration, lookup_default=""):
    """
    Define the model selector structure for a deployment step

    :param database: The database to be used for lookup
    :param table_collection: The table or collection to be used for lookup
    :param datasource: The type of datasource to be used for lookup. Allowed values are mongodb, cassandra and presto
    :param lookup_key: The key field to be used for lookup in the model selector structure
    :param lookup_type: The type of lookup key in the model selector data set. Allowed values are string and int
    :param selector_column: The column in the lookup database to be used for selection
    :param selector: A dictionary specifying the model to use for each value of the selector column. The keys are the values of the selector column and the values a list of the model names.
    :param model_configuration: The model configuration structure to be used for the deployment step
    :param lookup_default: The default value for the lookup key
    """
    if not isinstance(database, str):
        raise ValueError("database must be a string")
    if not isinstance(table_collection, str):
        raise ValueError("table_collection must be a string")
    if datasource not in ["mongodb", "cassandra", "presto"]:
        raise ValueError("datasource must be mongodb, cassandra or presto")
    if not (isinstance(lookup_key, str) or isinstance(lookup_key, int)):
        raise ValueError("lookup_key must be a string or an integer")
    if lookup_type not in ["string", "int"]:
        raise ValueError("lookup_type must be string or int")
    if not isinstance(selector_column, str):
        raise ValueError("selector_column must be a string")
    if not isinstance(selector, dict):
        raise ValueError("selector must be a dictionary")
    if not isinstance(model_configuration, dict):
        raise ValueError("model_configuration must be a dictionary")
    if not "models_load" in model_configuration:
        raise ValueError("model_configuration must contain a models_load key")

    try:
        if lookup_default == "":
            if lookup_type == "string":
                lookup_value = "123"
            else:
                lookup_value = 123
        else:
            if lookup_type == "string":
                lookup_value = str(lookup_default)
            else:
                lookup_value = int(lookup_default)
        lookup = {"key": lookup_key, "value": lookup_value}

        selector_int = {}
        models_list = model_configuration["models_load"].split(",")
        for selector_iter in selector:
            list_iter = selector[selector_iter]
            for model_iter in list_iter:
                if model_iter not in models_list:
                    raise ValueError(f"Model {model_iter} in selector not in model configuration")
                else:
                    if selector_iter not in selector_int:
                        selector_int[selector_iter] = [models_list.index(model_iter)]
                    else:
                        selector_int[selector_iter].append(models_list.index(model_iter))

        model_selector = {
            "database": database,
            "table_collection": table_collection,
            "datasource": datasource,
            "lookup": lookup,
            "selector_column": selector_column,
            "selector": selector
        }
    except Exception as e:
        raise ValueError(f"Error creating model selector structure: {e}")

    return model_selector


def define_deployment_setup_offer_matrix(database, table_collection, datasource, offer_lookup_id):
    """
    Define the setup offer matrix structure for a deployment step

    :param database: The database containing the offer matrix
    :param table_collection: The collection or table containing the offer matrix
    :param datasource: The type of datasource containing the offer matrix. Allowed values are mongodb, cassandra and presto
    :param offer_lookup_id: The name of the column containing the unique identifier for the offers. Allowed values are offer, offer_id and offer_name
    """
    if not isinstance(database, str):
        raise ValueError("database must be a string")
    if not isinstance(table_collection, str):
        raise ValueError("collection must be a string")
    if datasource not in ["mongodb", "cassandra", "presto"]:
        raise ValueError("datasource must be mongodb, cassandra or presto")
    if offer_lookup_id not in ["offer", "offer_id", "offer_name"]:
        raise ValueError("offer_lookup_id must be offer, offer_id or offer_name")

    try:
        setup_offer_matrix = {
            "database": database,
            "table_collection": table_collection,
            "datasource": datasource,
            "offer_lookup_id": offer_lookup_id
        }
    except Exception as e:
        raise ValueError(f"Error creating setup offer matrix structure: {e}")

    return setup_offer_matrix


def define_deployment_multi_armed_bandit(epsilon, duration=0, dynamic_interaction_uuid=""):
    """
    Define the multi armed bandit structure for a deployment step

    :param epsilon: The epsilon value for the deployment
    :param duration: The cache duration for the deployment
    :param dynamic_interaction_uuid: The uuid of the dynamic interaction configuration to be used for the deployment
    """
    if not isinstance(epsilon, (int, float)):
        raise ValueError("epsilon must be a number")
    if not isinstance(duration, int):
        raise ValueError("duration must be an integer")
    if not isinstance(dynamic_interaction_uuid, str):
        raise ValueError("pulse_responder_uuid must be a string")

    try:
        multi_armed_bandit = {
            "epsilon": epsilon,
            "duration": duration,
            "pulse_responder_uuid": dynamic_interaction_uuid
        }
    except Exception as e:
        raise ValueError(f"Error creating multi armed bandit structure: {e}")

    return multi_armed_bandit


def define_deployment_whitelist(database, table_collection, datasource):
    """
    Define the whitelist structure for a deployment step. The whitelist dataset must contain a customer_key column and a whitelist column which is a comma separated list of eligible offer names

    :param database: The database containing the whitelist
    :param table_collection: The table or collection containing the whitelist
    :param datasource: The type of datasource containing the whitelist. Allowed values are mongodb, cassandra and presto
    """
    if not isinstance(database, str):
        raise ValueError("database must be a string")
    if not isinstance(table_collection, str):
        raise ValueError("table_collection must be a string")
    if datasource not in ["mongodb", "cassandra", "presto"]:
        raise ValueError("datasource must be mongodb, cassandra or presto")

    try:
        whitelist = {
            "database": database,
            "table_collection": table_collection,
            "datasource": datasource
        }
    except Exception as e:
        raise ValueError(f"Error creating whitelist structure: {e}")

    return whitelist


def get_deployment_step(auth, project_id, deployment_id, version):
    """
    Get a deployment step from a project

    :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
    :param project_id: The name of the project containing the deployment step
    :param deployment_id: The name of the deployment step to get
    :param version: The version of the deployment step to get
    """
    if not isinstance(project_id, str):
        raise ValueError("project_id must be a string")
    if not isinstance(deployment_id, str):
        raise ValueError("deployment_id must be a string")
    if not isinstance(version, str):
        raise ValueError("version must be a string")

    # Get prediction project details and check that project exists
    try:
        project_details = pe.get_prediction_project(auth, project_id)
    except JSONDecodeError as error:
        raise ValueError("No project found with the given project ID.") from error

    # Check that the deployment exists in the project
    if "deployment_step" not in project_details:
        raise ValueError("No deployment steps found in the project.")

    try:
        for deployment_iter in project_details["deployment_step"]:
            if (version == deployment_iter["version"]) and (deployment_id == deployment_iter["deployment_id"]):
                return deployment_iter
    except Exception as e:
        raise ValueError(f"Error getting deployment step: {e}")


def create_deployment(
        auth,
        project_id,
        deployment_id,
        description,
        plugin_post_score_class,
        version,
        mongo_connect,
        plugin_pre_score_class="",
        budget_tracker="default",
        project_status="experiment",
        complexity="Low",
        performance_expectation="High",
        model_configuration="default",
        setup_offer_matrix="default",
        multi_armed_bandit="default",
        whitelist="default",
        model_selector="default",
        pattern_selector="default",
        logging_collection_response="ecosystemruntime_response",
        logging_collection="ecosystemruntime",
        logging_database="logging",
        scoring_engine_path_dev="http://ecosystem-runtime:8091",
        scoring_engine_path_test="http://ecosystem-runtime2:8091",
        scoring_engine_path_prod="http://ecosystem-runtime3:8091",
        models_path="/data/deployed/",
        data_path="/data/",
        build_server_path="",
        git_repo_path_branch="",
        download_path="",
        git_repo_path="",
        parameter_access="default",
        corpora="default",
        extensive_validation=False
):
    """
    Create or update a deployment linked to an existing project.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param project_id: The name of the project to add the deployment step to.
   :param deployment_id: The name of the deployment step that is to be created.
   :param description: Description of the deployment step
   :param version: The version of the deployment step being created. The combination of version and deployment_id cannot already exists within the deployment, i.e. you cannot overwrite an existing deployment
   :param project_status: Specifies the environment to which the deployment should be sent when it is pushed. The allowed values are experiment, validate, production, disable.
   :param plugin_pre_score_class: The name of the pre score logic class to be used in the runtime. Only default classes can be selected here. To create custom classes please use the ecosystem-runtime-locabuild repo or edit the classes in the workbench. The allowed values are PrePredictCustomer.java
   :param plugin_post_score_class: The name of the post score logic class to be used in the runtime. Only default classes can be selected here. To create custom classes please use the ecosystem-runtime-locabuild repo or edit the classes in the workbench. The allowed values are PostScoreBasic.java, PostScoreRecommender.java, PlatformDynamicEngagement.java, PostScoreRecommenderOffers.java, PostScoreRecommenderMulti.java and PostScoreNetwork.java
   :param budget_tracker: A dictionary of parameters required for managing the budget tracker functionality.
   :param complexity: Indicate the expected complexity of the deployment, allowed values are Low, Medium and High
   :param performance_expectation: Indicate the expected performance of the deployment, allowed values are Low, Medium and High
   :param model_configuration: A dictionary of the parameters specifying the models used in the project. The key item in the dictionary is models_load - a comma separated string of the names of the models to be used in the deployment. model_note and model_outline fields can also be added for tracking purposes
   :param setup_offer_matrix: A dictionary of parameters specifying the location of the offer matrix - a dataset containing information about the offers that could be recommended. The dictionary must contain a datasource, database, collection and offer_lookup_id. Datasource can be one of mongodb, white or presto. Database and collection specify the location of the offer_matrix in the datasource. Offer_lookup_id is the name of the column which contains the unique identifier for the offers - allowed values are offer, offer_name and offer_id
   :param multi_armed_bandit: A dictionary specifying the dynamic recommender behavior of the deployment. The dictionary must contain epsilon, duration and pulse_responder_id. epsilon is a portion of interactions that are presented with random results and should be a number between 0 and 1. duration is the period for which recommendations are cached in milliseconds TODO <Check this with Jay> . pulse_responder_id is the uuid of a Dynamic Interaction configuration, if not Dynamic Interaction configuration is being linked set this to ""
   :param whitelist: A dictionary of parameters specifying the location of the whitelist - a dataset of customers and the list of offers for which they are eligible. The data set should contain two fields; customer_key and white_list. customer_key is the unique customer identifier and white_list is a list of offer_names for which the customer is eligible. The dictionary must contain a datasource, database and collection. Datasource can be one of mongodb, cassandra or presto. Database and collection specify the location of the whitelist in the datasource.
   :param model_selector: A dictionary of parameters specifying the behavior of the model selector functionality. The model selector allows different models to be used based on the value of a field in the specified data set. The dictionary must contain datasource, database, table_collection, selector_column, selector and lookup.  Datasource can be one of mongodb, cassandra or presto. Database and collection specify the location of the model_selector dataset in the datasource. The selector_column is the name of the column in the dataset which is used to select between the different models. Lookup is a dictionary with the structure {"key":"customer","value":123 or '123',"fields'':"selector_column"}, where key is the field containing the unique customer identifier, value specified the type of the identifier as either a string ('123') or a number (123) and fields is the name of the selector column. Selector is the rule set used to choose models based on the values in the selector column. Selector is a dictionary with the format {"key_value_a":[0],"key_value_b":[1], ...} where the keys are the values of the fields in the selector column used to choose different models and the values are the indices of the model to be used, with the order as specified in the model_configuration argument
   :param pattern_selector: A dictionary containing the parameters defining the behavior of the pattern selector. The dictionary contains two parameters; pattern and duration. pattern is a comma separated list of numbers which specifies the intervals at which customers are able to receive updated offers. duration defines the time intervals specified in the pattern parameter
   :param parameter_access: A dictionary specifying the location from which customer data should be looked up. parameter_access should contain lookup, datasource, database, table_collection, lookup, lookup_defaults, fields, lookup_fields, create_virtual_variables and virtual_variables. lookup is a dictionary with the structure {"key":"customer","value":123 or '123'}, where key is the field containing the unique customer identifier, value specified the type of the identifier as either a string ('123') or a number (123). datasource can be one of mongodb, cassandra or presto. database and table_collection specify the location of the customer lookup in the datasource. fields is a comma separated list of the fields that should be read from the customer lookup. lookup_defaults are the default values to be used if the customer lookup fails, set to "" to not specify defaults. lookup_fields is the fields parameter in a list form ordered alphabetically create_virtual_variable is True if virtual variables are defined and False if not, virtual variables are defined by segmenting or combining fields from the customer lookup for us in the deployment. virtual_variables is a dictionary defining the virtual variables, which has the following form.
   :param corpora: A list of additional datasets that are read by the deployment. corpora is a list of dictionaries where each dictionary gives the details of a data set. The dictionaries must have the following keys; database (mongodb or cassandra), db (the database containing the corpora), table (the collection containing the corpora), name (the name of the corpora used in the deployment) and type (static, dynamic or experiment). The dictionary can optionally contain a key field which, if present, is used as a lookup for each row or the corpora, where the default is to have the rows loaded as an array. The type field in the dictionary specifies how the corpora is loaded. A static type is loaded at deployment, a dynamic type is loaded at each prediction and experiment is a special type used for configuring network runtimes
   :param logging_database: The mongo database where the deployment logs will be stored
   :param logging_collection: The mongo collection where the predictions presented will be stored
   :param logging_collection_response: The mongo collection where the customer responses to the predictions will be stored
   :param mongo_connect: The connection string to the mongo database used by the deployment
   :param scoring_engine_path_dev: The url of the container to send the configuration to when the project status is experiment
   :param scoring_engine_path_test: The url of the container to send the configuration to when the project status is validate
   :param scoring_engine_path_prod: The url of the container to send the configuration to when the project status is production
   :param models_path: The folder in the container where the models will be stored
   :param data_path: The folder in the container where the generic data used by the container will be stored
   :param build_server_path: The url of the build server to be used if customer logic is built into the container and a new container needs to be built containing said logic
   :param git_repo_path: The git repo to store the customer logic
   :param git_repo_path_branch: The branch to use for the repo specified in git_repo_path_branch
   :param download_path: The url on Docker Hub where the built container will be pushed
   :param extensive_validation: Indicator of whether potentially time consuming validation should be run before the deployment is created. This additional validation is checking whether the fields in the model_parameter are present in the linked collection and vice-versa

   :return: The deployment configuration.

   EXAMPLES:

   Deployment creation example for an online learning configuration with an offer matrix, customer lookup, virtual variables
   and a dynamic corpora specifying a default offer.

   .. code-block:: python

       deployment_step = dm.create_deployment(
            auth_local,
            project_id=project_id,
            deployment_id="demo_online_learning",
            description="Demonstration of online learning deployment",
            plugin_pre_score_class="",
            plugin_post_score_class="PostScoreDemoDynamic.java",
            version="001",
            project_status="experiment",
            scoring_engine_path_dev="http://ecosystem-runtime:8091",
            multi_armed_bandit={
                        "epsilon": 0,
                        "duration": 0,
                        "pulse_responder_uuid": online_learning_uuid
                        },
            setup_offer_matrix={
                        "offer_lookup_id": "offer_name",
                        "database": "recommender",
                        "table_collection": "online_offer_matrix",
                        "datasource": "mongodb"
                    },
            corpora=[{ "name":"default_offer","database":"mongodb","db":"recommender","table":"online_default_offer","type":"static"}],
            parameter_access={
                        "lookup": {"value": 123,"key": "customer"},
                        "create_virtual_variables":True,
                        "lookup_defaults": "",
                        "database": "recommender",
                        "table_collection": "customer_feature_store",
                        "lookup_fields": ["customer","revenue","activity","age",...],
                        "datasource": "mongodb",
                        "virtual_variables": [
                            {
                                "name": "revenue_category",
                                "default": "gt-500",
                                "type": "discretize",
                                "original_variable": "revenue",
                                "fields": [],
                                "buckets": [
                                    {"from": 0,"label": "lt-50","to": 50},
                                    {"from": 50,"label": "50-250","to": 250},
                                    {"from": 250,"label": "250-500","to": 500}
                                ]
                            },
                            {
                                "name": "activity_category",
                                "default": "gt-15",
                                "type": "discretize",
                                "original_variable": "activity",
                                "fields": [],
                                "buckets": [
                                    {"from": 0,"label": "lt-15","to": 15}
                                ]
                            }
                        ]
                    }
       )

    """
    # Check inputs have the required format and get default values where relevant
    # Get prediction project details and check that project exists
    try:
        project_details = pe.get_prediction_project(auth, project_id)
    except JSONDecodeError as error:
        raise ValueError(
            "No project found with the given project ID. Please create your project before allocating deployments to "
            "it") from error

    # Get the dynamic confiugration details and check that the dynamic configuration exists
    if multi_armed_bandit == "default":
        multi_armed_bandit = get_multi_armed_bandit_default()
        is_multi_armed_bandit = False
    else:
        is_multi_armed_bandit = True
        if not isinstance(multi_armed_bandit, dict):
            raise TypeError("multi_armed_bandit should be a dictionary")
        if "epsilon" not in multi_armed_bandit:
            raise KeyError("multi_armed_bandit must contain epsilon")
        if "duration" not in multi_armed_bandit:
            raise KeyError("multi_armed_bandit must contain duration")
        if "pulse_responder_uuid" not in multi_armed_bandit:
            raise KeyError("multi_armed_bandit must contain pulse_responder_uuid")
        if not isinstance(multi_armed_bandit["epsilon"], (int, float)):
            raise TypeError("epsilon in multi_armed_bandit should be a number")
        if multi_armed_bandit["epsilon"] < 0 or multi_armed_bandit["epsilon"] > 1:
            raise ValueError("epsilon in multi_armed_bandit should be between 0 and 1")
        if not isinstance(multi_armed_bandit["duration"], (int, float)):
            raise TypeError("duration in multi_armed_bandit should be a number")
        if multi_armed_bandit["duration"] < 0:
            raise ValueError("duration in multi_armed_bandit should be greater than 0")
        if multi_armed_bandit["pulse_responder_uuid"] == "":
            dynamic_config = {}
        else:
            all_dynamic_configurations = cp.list_pulse_responder_dynamic(auth)
            found_pulse_responder = False
            for dynamic_config_iter in all_dynamic_configurations["data"]:
                if dynamic_config_iter["uuid"] == multi_armed_bandit["pulse_responder_uuid"]:
                    found_pulse_responder = True
                    dynamic_config = dynamic_config_iter
            if not found_pulse_responder:
                raise ValueError(
                    "pulse_responder_id in multi_armed_bandit not linked to a dynamic recommender configuration")

    # Check that deployment_id is a string that doesn't contain spaces and matches the dynamic configuration name if it
    # exists
    if not isinstance(deployment_id, str):
        raise TypeError("deployment_id should be a string")
    if multi_armed_bandit["pulse_responder_uuid"] != "":
        if deployment_id != dynamic_config["name"]:
            raise ValueError("deployment step and dynamic recommender should have the same name")

    # Check whether version already exists and that it is a string
    if not isinstance(version, str):
        raise TypeError("version should be a string")
    if "deployment_step" in project_details:
        for deployment_iter in project_details["deployment_step"]:
            if (version == deployment_iter["version"]) and (deployment_id == deployment_iter["deployment_id"]):
                raise ValueError("The version specified for this deployment already exists, deployment not updated. "
                                 "Please update the version to update the deployment")

    # Check that description is a string
    if not isinstance(description, str):
        raise TypeError("description should be a string")

    # Check that project status has an allowed value
    if project_status not in ["experiment", "validate", "production", "disable"]:
        raise ValueError("project_status must be one of experiment, validate, production or disable")

    # Get pre and post score logic and return warnings if the requested logic is not found
    if not isinstance(plugin_pre_score_class, str):
        raise TypeError("plugin_pre_score_class should be a string")
    if not isinstance(plugin_post_score_class, str):
        raise TypeError("plugin_post_score_class should be a string")
    if (".java" not in plugin_pre_score_class) and ("" not in plugin_pre_score_class):
        raise TypeError("plugin_pre_score_class should be a java class")
    if ".java" not in plugin_post_score_class:
        raise TypeError("plugin_post_score_class should be a java class")
    pre_score_code = get_pre_score_code(plugin_pre_score_class,project_details)
    post_score_code = get_post_score_code(plugin_post_score_class,project_details)

    # Check that complexity and performance_expectation have one of the required values
    if complexity not in ["Low", "Medium", "High"]:
        raise ValueError("complexity must be one of Low, Medium or High")
    if performance_expectation not in ["Low", "Medium", "High"]:
        raise ValueError("performance_expectation must be one of Low, Medium or High")

    # Check format of mongo_connect string and check if connection to database can be made
    if not isinstance(mongo_connect, str):
        raise TypeError("mongo_connect should be a string")
    try:
        test_client = pymongo.MongoClient(mongo_connect)
        with pymongo.timeout(2):
            test_client.admin.command("ping")
        test_mongo_connection = True
    except:
        test_mongo_connection = False
        print("WARNING: Test connection to mongo database failed")

    try:
        mongo_ecosystem_user = mongo_connect[
                 mongo_connect.index("://") + len("://"):mongo_connect.index(":", mongo_connect.index("//"))]
        mongo_ecosystem_password = mongo_connect[
                     mongo_connect.index(f"{mongo_ecosystem_user}:") + len(f"{mongo_ecosystem_user}:"):mongo_connect.index("@")]
        mongo_server_port = mongo_connect[
                   mongo_connect.index("@") + len("@"):mongo_connect.index("/", mongo_connect.index(mongo_ecosystem_user))]
    except:
        print("WARNING: Error extracting mongo connection details from mongo_connect string")

    # TODO Get validation rules/logic from Jay
    if budget_tracker == "default":
        budget_tracker = get_budget_tracker_default()
        is_budget_tracking = False
    else:
        is_budget_tracking = True

    # Check that model configuration has the required format and display a warning if the listed models cannot be found in list of deployed models
    if model_configuration == "default":
        model_configuration = get_model_configuration_default()
        is_prediction_model = False
    else:
        is_prediction_model = True
        if not isinstance(model_configuration, dict):
            raise TypeError("model_configuration should be a dictionary")
        if "models_load" not in model_configuration:
            raise ValueError("model_configuration must contain models_load")
        if not isinstance(model_configuration["models_load"], str):
            raise TypeError("models_load in model_configuration should be a string")
        model_list = model_configuration["models_load"].split(",")
        # TODO Ask Jay for a better version of getting a list of deployed models
        list_of_deployed_models = pe.get_user_models(auth, "ecosystem")
        for model_iter in model_list:
            if model_iter not in list_of_deployed_models:
                print(
                    "WARNING: " + model_iter + " cannot be found on the list of deployed models managed in the ecosystem.ai workbench")

    # Indicator of whether a connection to Cassandra has been checked
    test_cassandra_connection = True
    test_presto_connection = True

    # Check that the offer matrix set up has the required format and whether the offer matrix can be found using the connections available to the server
    if setup_offer_matrix == "default":
        setup_offer_matrix = get_setup_offer_matrix_default()
        is_offer_matrix = False
    else:
        is_offer_matrix = True
        if not isinstance(setup_offer_matrix, dict):
            raise TypeError("setup_offer_matrix should be a dictionary")
        if "datasource" not in setup_offer_matrix:
            raise KeyError("setup_offer_matrix must contain datasource")
        if "database" not in setup_offer_matrix:
            raise KeyError("setup_offer_matrix must contain database")
        if "table_collection" not in setup_offer_matrix:
            raise KeyError("setup_offer_matrix must contain table_collection")
        if "offer_lookup_id" not in setup_offer_matrix:
            raise KeyError("setup_offer_matrix must contain offer_lookup_id")
        if setup_offer_matrix["datasource"] not in ["mongodb", "cassandra", "presto"]:
            raise ValueError("datasource in setup_offer_matrix must be cassandra, mongodb or presto")
        if not isinstance(setup_offer_matrix["database"], str):
            raise TypeError("database in setup_offer_matrix should be a string")
        if not isinstance(setup_offer_matrix["table_collection"], str):
            raise TypeError("table_collection in setup_offer_matrix should be a string")
        if setup_offer_matrix["offer_lookup_id"] not in ["offer", "offer_id", "offer_name"]:
            raise ValueError("offer_lookup_id in setup_offer_matrix must be offer, offer_name or offer_id ")
        if setup_offer_matrix["datasource"] == "mongodb" and test_mongo_connection:
            db_offer_matrix = test_client[setup_offer_matrix["database"]]
            if db_offer_matrix[setup_offer_matrix["table_collection"]].estimated_document_count() == 0:
                print("WARNING: It looks like the offer matrix is empty")
            else:
                test_offer_matrix_row = db_offer_matrix[setup_offer_matrix["table_collection"]].find().next()
                if setup_offer_matrix["offer_lookup_id"] not in test_offer_matrix_row:
                    print("WARNING: It looks like the specified offer_lookup_id is not a field in the offer matrix")
        elif setup_offer_matrix["datasource"] == "cassandra" and test_cassandra_connection:
            data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(setup_offer_matrix["table_collection"]))
            if data_check["data"] == []:
                print("WARNING: It looks like the offer matrix is empty or does not exist")
            elif setup_offer_matrix["offer_lookup_id"] not in data_check["data"][0]:
                print("WARNING: It looks like the specified offer_lookup_id is not a field in the offer matrix")
        elif setup_offer_matrix["datasource"] == "presto" and test_presto_connection:
            # TODO: Ask Jay how Presto connection works and figure our how to implement test on Presto Connection
            print("WARNING: presto connection could not be tested")

    # Check that the whitelist has the required format
    if whitelist == "default":
        whitelist = get_whitelist_default()
        is_whitelist = False
    else:
        is_whitelist = True
        if not isinstance(whitelist, dict):
            raise TypeError("whitelist should be a dictionary")
        if "datasource" not in whitelist:
            raise KeyError("whitelist must contain datasource")
        if "database" not in whitelist:
            raise KeyError("whitelist must contain database")
        if "table_collection" not in whitelist:
            raise KeyError("whitelist must contain table_collection")
        if whitelist["datasource"] not in ["mongodb", "cassandra", "presto"]:
            raise ValueError("datasource in whitelist must be cassandra, mongodb or presto")
        if not isinstance(whitelist["database"], str):
            raise TypeError("database in whitelist should be a string")
        if not isinstance(whitelist["table_collection"], str):
            raise TypeError("table_collection in whitelist should be a string")
        if whitelist["datasource"] == "mongodb" and test_mongo_connection:
            db_whitelist = test_client[whitelist["database"]]
            if db_whitelist[whitelist["table_collection"]].estimated_document_count() == 0:
                print("WARNING: It looks like the whitelist is empty")
            else:
                test_whitelist_row = db_whitelist[whitelist["table_collection"]].find().next()
                if "customer_key" not in test_whitelist_row:
                    print("WARNING: It looks like customer_key is not a field in the white list")
                if "white_list" not in test_whitelist_row:
                    print("WARNING: It looks like white_list is not a field in the white list")
        elif whitelist["datasource"] == "cassandra" and test_cassandra_connection:
            data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(whitelist["table_collection"]))
            if data_check["data"] == []:
                print("WARNING: It looks like the whitelist is empty or does not exist")
            elif "customer_key" not in data_check["data"][0]:
                print("WARNING: It looks like customer_key is not a field in the white list")
            elif "white_list" not in data_check["data"][0]:
                print("WARNING: It looks like white_list is not a field in the white list")
        elif whitelist["datasource"] == "presto" and test_presto_connection:
            # TODO: Ask Jay how Presto connection works and figure our how to implement test on Presto Connection
            print("WARNING: presto connection could not be tested")

    # Check that the model selector has the required format
    if model_selector == "default":
        model_selector = get_model_selector_default()
        is_model_selector = False
    else:
        is_model_selector = True
        if not isinstance(model_selector, dict):
            raise TypeError("model_selector should be a dictionary")
        if "datasource" not in model_selector:
            raise KeyError("model_selector must contain datasource")
        if "database" not in model_selector:
            raise KeyError("model_selector must contain database")
        if "table_collection" not in model_selector:
            raise KeyError("model_selector must contain table_collection")
        if "selector_column" not in model_selector:
            raise KeyError("model_selector must contain selector_column")
        if "selector" not in model_selector:
            raise KeyError("model_selector must contain selector")
        if "lookup" not in model_selector:
            raise KeyError("model_selector must contain lookup")
        if not isinstance(model_selector["lookup"], dict):
            raise TypeError("lookup in model_selector should be a dictionary")
        if "key" not in model_selector["lookup"]:
            raise KeyError("lookup in model_selector must contain key")
        if "value" not in model_selector["lookup"]:
            raise KeyError("lookup in model_selector must contain value")
        if "fields" not in model_selector["lookup"]:
            raise KeyError("lookup in model_selector must contain fields")
        if not isinstance(model_selector["selector"], dict):
            raise TypeError("selector in model_selector should be a dictionary")
        if model_selector["datasource"] not in ["mongodb", "cassandra", "presto"]:
            raise ValueError("datasource in model_selector must be cassandra, mongodb or presto")
        if not isinstance(model_selector["database"], str):
            raise TypeError("database in model_selector should be a string")
        if not isinstance(model_selector["table_collection"], str):
            raise TypeError("table_collection in model_selector should be a string")
        if model_selector["datasource"] == "mongodb" and test_mongo_connection:
            db_model_selector = test_client[model_selector["database"]]
            if db_model_selector[model_selector["table_collection"]].estimated_document_count() == 0:
                print("WARNING: It looks like the model_selector is empty")
            else:
                test_model_selector_row = db_model_selector[model_selector["table_collection"]].find().next()
                if model_selector["selector_column"] not in test_model_selector_row:
                    print("WARNING: It looks like selector_column is not a field in the model selector collection")
                elif extensive_validation:
                    selector_values_cursor = db_model_selector[model_selector["table_collection"]].aggregate([{
                                                                                                                  "$group": {
                                                                                                                      "_id": "None",
                                                                                                                      "selector_values": {
                                                                                                                          "$addToSet": "$" +
                                                                                                                                       model_selector[
                                                                                                                                           "selector_column"]}}}]).next()
                    selector_values_in_dataset = selector_values_cursor["selector_values"]
                    selector_values_in_args = model_selector["selector"].keys()
                    for selector_value_in_dataset_iter in selector_values_in_dataset:
                        if selector_value_in_dataset_iter not in selector_values_in_args:
                            print("WARNING: " + str(
                                selector_value_in_dataset_iter) + " in the model selector database but not in the selector in the model_selector. If this row is looked up by the runtime a default value will be returned")
                    for selector_value_in_args_iter in model_selector["selector"]:
                        if selector_value_in_args_iter not in selector_values_in_dataset:
                            print("WARNING: " + str(
                                selector_value_in_args_iter) + " in the selector in the model_selector is not present in the model selector dataset")
                if model_selector["lookup"]["key"] not in test_model_selector_row:
                    print(
                        "WARNING: It looks like key in the lookup in model_selector is not a field in the model selector collection")
        elif whitelist["datasource"] == "cassandra" and test_cassandra_connection:
            data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(model_selector["table_collection"]))
            if data_check["data"] == []:
                print("WARNING: It looks like the model_selector is empty or does not exist")
            elif model_selector["selector_column"] not in data_check["data"][0]:
                print("WARNING: It looks like selector_column is not a field in the model selector collection")
        elif whitelist["datasource"] == "presto" and test_presto_connection:
            # TODO: Ask Jay how Presto connection works and figure our how to implement test on Presto Connection
            print("WARNING: presto connection could not be tested")

    # Check whether pattern selector contains the required parameters
    if pattern_selector == "default":
        pattern_selector = get_pattern_selector_default()
        is_pattern_selector = False
    else:
        is_pattern_selector = True
        if not isinstance(pattern_selector, dict):
            raise TypeError("pattern_selector should be a dictionary")
        if "pattern" not in model_selector:
            raise KeyError("pattern_selector must contain pattern")
        if "duration" not in model_selector:
            raise KeyError("pattern_selector must contain duration")
        if not isinstance(pattern_selector["pattern"], str):
            raise TypeError("pattern in pattern_selector should be a string of comma separated numbers")
        if not isinstance(pattern_selector["duration"], (int, float)):
            raise TypeError("duration in pattern_selector should be a number")

    # Check whether corpora has the required format and checks if the loaded corpora can be found
    if corpora == "default":
        corpora = get_corpora_default()
        is_corpora = False
    else:
        is_corpora = True
        if not isinstance(corpora, list):
            raise TypeError("corpora should be a list of dictionaries giving details of the corpora to be linked")
        for corpora_iter in corpora:
            if not isinstance(corpora_iter, dict):
                raise TypeError("corpora should be a list of dictionaries giving details of the corpora to be linked")
            if "name" not in corpora_iter:
                raise KeyError("corpora dictionaries must contain name")
            if "database" not in corpora_iter:
                raise KeyError("corpora dictionaries must contain database")
            if "db" not in corpora_iter:
                raise KeyError("corpora dictionaries must contain db")
            if "table" not in corpora_iter:
                raise KeyError("corpora dictionaries must contain table")
            if "type" not in corpora_iter:
                raise KeyError("corpora dictionaries must contain type")
            for corpora_key in corpora_iter:
                if corpora_key not in ["name", "database", "db", "table", "type", "key"]:
                    raise KeyError("corpora dictionaries can only contain name, database, db, table, type and key")
            if corpora_iter["database"] not in ["mongodb", "cassandra"]:
                raise ValueError("database in corpora must be cassandra or mongodb")
            if corpora_iter["type"] not in ["static", "dynamic", "experiment"]:
                raise ValueError("type in corpora must be static, dynamic or experiment")
            if corpora_iter["database"] == "mongodb" and test_mongo_connection:
                db_corpora = test_client[corpora_iter["db"]]
                if db_corpora[corpora_iter["table"]].estimated_document_count() == 0:
                    print("WARNING: It looks like the corpora {} is empty".format(corpora_iter["table"]))
                elif "key" in corpora_iter:
                    test_corpora_row = db_corpora[corpora_iter["table"]].find().next()
                    if corpora_iter["key"] not in test_corpora_row:
                        print("WARNING: It looks like the specified key is missing from the corpora")
            elif corpora_iter["database"] == "cassandra" and test_cassandra_connection:
                data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(corpora_iter["table"]))
                if data_check["data"] == []:
                    print("WARNING: It looks like the corpora {} is empty".format(corpora_iter["table"]))
                elif "key" in corpora_iter:
                    if corpora_iter["key"] not in data_check["data"][0]:
                        print("WARNING: It looks like the specified key is missing from the corpora")
        corpora = {"corpora": json.dumps(corpora)}

    if parameter_access == "default":
        parameter_access = get_parameter_access_default()
        is_params_from_data_source = False
    else:
        is_params_from_data_source = True
        if not isinstance(parameter_access, dict):
            raise TypeError("parameter_access should be a dictionary")
        if "datasource" not in parameter_access:
            raise KeyError("parameter_access must contain datasource")
        if "database" not in parameter_access:
            raise KeyError("parameter_access must contain database")
        if "table_collection" not in parameter_access:
            raise KeyError("parameter_access must contain table_collection")
        if "lookup" not in parameter_access:
            raise KeyError("parameter_access must contain lookup")
        # if "fields" not in parameter_access:
        #     raise KeyError("parameter_access must contain fields")
        if "lookup_defaults" not in parameter_access:
            raise KeyError("parameter_access must contain lookup_defaults")
        if "lookup_fields" not in parameter_access:
            raise KeyError("parameter_access must contain lookup_fields")
        if "create_virtual_variables" not in parameter_access:
            raise KeyError("parameter_access must contain create_virtual_variables")
        if "virtual_variables" not in parameter_access:
            raise KeyError("parameter_access must contain virtual_variables")
        if parameter_access["datasource"] not in ["mongodb", "cassandra", "presto"]:
            raise ValueError("datasource in parameter_access must be cassandra, mongodb or presto")
        if not isinstance(parameter_access["database"], str):
            raise TypeError("database in parameter_access should be a string")
        if not isinstance(parameter_access["table_collection"], str):
            raise TypeError("table_collection in parameter_access should be a string")
        if not isinstance(parameter_access["lookup"], dict):
            raise TypeError("lookup in parameter_access should be a dictionary")
        if "key" not in parameter_access["lookup"]:
            raise KeyError("lookup in parameter_access must contain key")
        if "value" not in parameter_access["lookup"]:
            raise KeyError("lookup in parameter_access must contain value")
        # if not isinstance(parameter_access["fields"], str):
        #     raise TypeError("fields in parameter_access should be a string")
        if not isinstance(parameter_access["create_virtual_variables"], bool):
            raise TypeError("create_virtual_variables in parameter_access should be a boolean value")
        if not isinstance(parameter_access["virtual_variables"], list):
            raise TypeError("virtual_variables in parameter_access should be a list")
        if parameter_access["datasource"] == "mongodb" and test_mongo_connection:
            db_parameter_access = test_client[parameter_access["database"]]
            if db_parameter_access[parameter_access["table_collection"]].estimated_document_count() == 0:
                print("WARNING: It looks like the parameter_access collection is empty")
            else:
                test_parameter_access_row = db_parameter_access[parameter_access["table_collection"]].find().next()
                if parameter_access["lookup"]["key"] not in test_parameter_access_row:
                    print("WARNING: It looks like the specified key is not a field in the parameter_access collection")
                if type(test_parameter_access_row[parameter_access["lookup"]["key"]]) != type(
                        parameter_access["lookup"]["value"]):
                    print("WARNING: It looks like value specified in the lookup in parameter_access does not match the type found in the collection")
        elif parameter_access["datasource"] == "cassandra" and test_cassandra_connection:
            data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(parameter_access["table_collection"]))
            type_sql = "SELECT type FROM system_schema.columns WHERE keyspace_name = '{}' AND table_name = '{}' AND column_name = '{}'".format(parameter_access["table_collection"].split(".")[0],parameter_access["table_collection"].split(".")[1],parameter_access["lookup"]["key"])
            if data_check["data"] == []:
                print("WARNING: It looks like the parameter_access collection is empty")
            elif parameter_access["lookup"]["key"] not in data_check["data"][0]:
                print("WARNING: It looks like the specified key is not a field in the parameter_access collection")
            else:
                cassandra_type = dme.get_cassandra_sql(auth, type_sql)["data"][0]["type"]
                if cassandra_type == "text" and not isinstance(parameter_access["lookup"]["value"], str):
                    print("WARNING: It looks like value specified in the lookup in parameter_access does not match the type found in the collection")
                elif cassandra_type != "text" and isinstance(parameter_access["lookup"]["value"], str):
                    print("WARNING: It looks like value specified in the lookup in parameter_access does not match the type found in the collection")
        elif parameter_access["datasource"] == "presto" and test_presto_connection:
            # TODO: Ask Jay how Presto connection works and figure our how to implement test on Presto Connection
            print("WARNING: presto connection could not be tested")

    # Define constructs needed to create the deployment and add the deployment to the project

    #multi_armed_bandit["epsilon"] = str(multi_armed_bandit["epsilon"])

    options = {
        "is_offer_matrix": is_offer_matrix,
        "is_multi_armed_bandit": is_multi_armed_bandit,
        "is_enable_plugins": True,
        "is_whitelist": is_whitelist,
        "is_corpora": is_corpora,
        "is_custom_api": False,
        "is_budget_tracking": is_budget_tracking,
        "is_params_from_data_source": is_params_from_data_source,
        "is_model_selector": is_model_selector,
        "is_generate_dashboards": False,
        "is_pattern_selector": is_pattern_selector,
        "is_prediction_model": is_prediction_model
    }

    api_endpoint_code = get_api_endpoint_code_default()
    plugins = {
        "post_score_class_text": plugin_post_score_class,
        "post_score_class_code": post_score_code,
        "api_endpoint_code": api_endpoint_code,
        "pre_score_class_text": plugin_pre_score_class,
        "pre_score_class_code": pre_score_code
    }

    updated_by = auth.get_username()
    updated_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

    paths = {
        "logging_collection_response": logging_collection_response,
        "logging_collection": logging_collection,
        "logging_database": logging_database,
        "mongo_server_port": mongo_server_port,
        "scoring_engine_path_prod": scoring_engine_path_prod,
        "models_path": models_path,
        "mongo_connect": mongo_connect,
        "data_path": data_path,
        "build_server_path": build_server_path,
        "scoring_engine_path_dev": scoring_engine_path_dev,
        "aws_container_resource": "",
        "scoring_engine_path_test": scoring_engine_path_test,
        "git_repo_path_branch": git_repo_path_branch,
        "download_path": download_path,
        "mongo_ecosystem_password": mongo_ecosystem_password,
        "mongo_ecosystem_user": mongo_ecosystem_user,
        "git_repo_path": git_repo_path
    }

    if "lookup_fields" in parameter_access:
        fields = ""
        for field_iter in parameter_access["lookup_fields"]: fields = fields + "," + field_iter
        parameter_access["fields"] = fields[1::]

    # Define deployment step
    deployment_step = {}
    deployment_step["version"] = version
    deployment_step["deployment_id"] = deployment_id
    deployment_step["project_status"] = project_status
    deployment_step["description"] = description
    deployment_step["complexity"] = complexity
    deployment_step["plugins"] = plugins
    deployment_step["model_configuration"] = model_configuration
    deployment_step["setup_offer_matrix"] = setup_offer_matrix
    deployment_step["multi_armed_bandit"] = multi_armed_bandit.copy()
    deployment_step["multi_armed_bandit"]["epsilon"] = str(deployment_step["multi_armed_bandit"]["epsilon"])
    deployment_step["whitelist"] = whitelist
    deployment_step["model_selector"] = model_selector
    deployment_step["performance_expectation"] = performance_expectation
    deployment_step["pattern_selector"] = pattern_selector
    deployment_step["paths"] = paths
    # deployment_step["Build"] = Build
    deployment_step["updated_by"] = updated_by
    deployment_step["updated_date"] = updated_date
    deployment_step["options"] = options
    deployment_step["corpora"] = corpora
    deployment_step["parameter_access"] = parameter_access
    deployment_step["budget_tracker"] = budget_tracker
    # Add deployment step to project
    if "deployment_step" in project_details:
        project_details["deployment_step"].append(deployment_step)
    else:
        project_details["deployment_step"] = [deployment_step]

    # Save project with newly created deployment
    pe.save_prediction_project(auth, project_details)

    #Update dynamic pulse responder if linked and relevant
    if "pulse_responder_uuid" in multi_armed_bandit:
        if multi_armed_bandit["pulse_responder_uuid"] != "":
            existing_configurations = cp.list_pulse_responder_dynamic(auth)
            client_pulse_list = [d for d in existing_configurations["data"] if
                                 d["uuid"] == multi_armed_bandit["pulse_responder_uuid"]]
            client_pulse_doc = client_pulse_list[0]
            if "fields" in parameter_access:
                client_pulse_doc["lookup_fields"] = parameter_access["lookup_fields"]
            if "virtual_variables" in parameter_access:
                client_pulse_doc["virtual_variables"] = parameter_access["virtual_variables"]
            dme.add_documents(auth, {"database": "ecosystem_meta", "collection": "dynamic_engagement",
                                   "document": client_pulse_doc, "update": "uuid"})

    print("MESSAGE: Project deployment created")
    return deployment_step


def create_project(
        auth,
        project_id,
        project_description,
        project_type,
        purpose,
        project_start_date,
        project_end_date,
        data_science_lead,
        data_lead,
        module_name="",
        module_module_owner="",
        module_description="",
        module_created_by="",
        module_version="",
):
    """
    Create a new project

   :param auth: Token for accessing the ecosystem-server. Created using jwt_access.
   :param project_id: The name of the project to be created.
   :param project_description: Description of the project.
   :param project_type: The type of the project.
   :param purpose: The purpose of the project.
   :param project_start_date: The start date of the project.
   :param project_end_date: The end date of the project.
   :param data_science_lead: The data science lead of the project.
   :param data_lead: The data lead of the project.
   :param module_name: The name of the module.
   :param module_module_owner: The owner of the module.
   :param module_description: The description of the module.
   :param module_created_by: The creator of the module.
   :param module_version: The version of the module.

    """
    if not isinstance(project_id, str):
        raise TypeError("project_id should be a string")
    if not isinstance(project_description, str):
        raise TypeError("project_description should be a string")
    if not isinstance(project_type, str):
        raise TypeError("project_type should be a string")
    if not isinstance(purpose, str):
        raise TypeError("purpose should be a string")
    if not isinstance(data_science_lead, str):
        raise TypeError("data_science_lead should be a string")
    if not isinstance(data_lead, str):
        raise TypeError("data_lead should be a string")
    if not isinstance(module_name, str):
        raise TypeError("module_name should be a string")
    if not isinstance(module_module_owner, str):
        raise TypeError("module_module_owner should be a string")
    if not isinstance(module_description, str):
        raise TypeError("module_description should be a string")
    if not isinstance(module_created_by, str):
        raise TypeError("module_created_by should be a string")
    if not isinstance(module_version, str):
        raise TypeError("module_version should be a string")

    project_exists = True
    try:
        pe.get_prediction_project(auth, project_id)
    except:
        project_exists = False

    if project_exists:
        raise ValueError(
            "project_id already exists. Use either update_project or delete_project to change project parameters")

    updated_by = auth.get_username()
    updated_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

    if module_name == "":
        module_name = project_id
    if module_module_owner == "":
        module_module_owner = data_science_lead
    if module_description == "":
        module_description = project_description
    if module_created_by == "":
        module_created_by = updated_by
    if module_version == "":
        module_version = "001"

    project_doc = {
        "project_id": project_id
        , "project_description": project_description
        , "project_type": project_type
        , "purpose": purpose
        , "configuration": ""
        , "project_start_date": project_start_date
        , "project_end_date": project_end_date
        , "project_owner": data_science_lead
        , "project_data": data_lead
        , "module_metadata": {
            "reviewed_by": "",
            "image_path": "",
            "icon_path": "",
            "name": module_name,
            "module_owner": module_module_owner,
            "description": module_description,
            "created_by": module_created_by,
            "version": module_version,
            "contact_email": "",
            "status": ""
        }
        , "preview_detail": {
            "heading": project_id
            , "summary": project_description
            , "detail": purpose
            , "active": True
        }
        , "created_by": updated_by
        , "created_date": updated_date
        , "updated_by": updated_by
        , "updated_date": updated_date
        , "userid": "ecosystem"
    }
    pe.save_prediction_project(auth, project_doc)

    print("MESSAGE: Project created")
    return project_doc


def link_collections_to_project(auth, project_id, collections):
    """
    Link collections to a project

    :param auth: Token for accessing the ecosystem-server. Created using jwt_access.
    :param project_id: The name of the project to link the collections to.
    :param collections: The collections to link to the project in the format [{"database":"linked_database","collection":"linked_collection"}]
    """
    if not isinstance(project_id, str):
        raise TypeError("project_id should be a string")
    if not isinstance(collections, list):
        raise TypeError("collections should be a list of dictionaries")
    for collection_iter in collections:
        if not isinstance(collection_iter, dict):
            raise TypeError("collections should be a list of dictionaries")
        if "database" not in collection_iter:
            raise KeyError("collections dictionaries must contain database")
        if "collection" not in collection_iter:
            raise KeyError("collections dictionaries must contain collection")
        for collection_key in collection_iter:
            if collection_key not in ["database", "collection"]:
                raise KeyError("collections dictionaries can only contain database and collection")
            if not isinstance(collection_iter[collection_key], str):
                raise TypeError("collection and database should contain strings")

    project_details = pe.get_prediction_project(auth, project_id)
    project_details["project_collections"] = collections
    pe.save_prediction_project(auth, project_details)

    return "MESSAGE: Collections linked to project"

def link_dynamic_interactions_to_project(auth, project_id, interactions):
    """
    Link dynamic interactions to a project

    :param auth: Token for accessing the ecosystem-server. Created using jwt_access.
    :param project_id: The name of the project to link the interactions to.
    :param interactions: The interactions to link to the project in the format [{"uuid":"f4990ecd-d438-4260-85ae-fc1fd915a266}]
    """
    if not isinstance(project_id, str):
        raise TypeError("project_id should be a string")
    if not isinstance(interactions, list):
        raise TypeError("interactions should be a list of dictionaries")
    for interaction_iter in interactions:
        if not isinstance(interaction_iter, dict):
            raise TypeError("interactions should be a list of dictionaries")
        if "uuid" not in interaction_iter:
            raise KeyError("interactions dictionaries must contain uuid")
        for interaction_key in interaction_iter:
            if interaction_key not in ["uuid"]:
                raise KeyError("interactions dictionaries can only contain uuid")
            if not isinstance(interaction_iter[interaction_key], str):
                raise TypeError("uuid should be a string")

    project_details = pe.get_prediction_project(auth, project_id)
    dynamic_interactions = cp.list_pulse_responder_dynamic(auth)
    uuid_list = [d["uuid"] for d in interactions]
    linked_interactions = []
    for dynamic_iter in dynamic_interactions["data"]:
        if dynamic_iter["uuid"] in uuid_list:
            linked_interactions.append({"uuid": dynamic_iter["uuid"], "name": dynamic_iter["name"], "date": dynamic_iter["date_updated"]})

    project_details["project_dynamic_interactions"] = linked_interactions
    pe.save_prediction_project(auth, project_details)

    return "MESSAGE: Interactions linked to project"

def single_test_calls(auth_runtime, testing_config, output_level):
    """
    Test the runtime by making individual calls and checking the response against user defined criteria

    param: auth_runtime: The authentication object for the runtime
    param: testing_config: The testing configuration
    param: output_level: The level of output to print. Options are "quiet" and "verbose"

    return: True if the tests pass, False otherwise
    """
    # Iterate through the testing config and call the runtime
    # {
    # "api_call":{
    #             "campaign": deployment_id
    #             , "subcampaign": "none"
    #             , "channel": "notebooks"
    #             , "customer": 27822914182
    #             , "userid": "test"
    #             , "numberoffers": 4
    #             , "params": "{}"
    #             }
    # ,"check_offer_count":"Yes"
    # ,"check_offer_response":"No"
    # ,"expected_offer":""
    # }
    for test_iter in testing_config["individual_tests"]:
        try:
            offer_response = o.invocations(auth_runtime, test_iter["api_call"])
            if output_level != "quiet":
                print("Offer response:")
                print(offer_response)
        except Exception as e:
            print("Error in runtime_test_individual_calls calling runtime: {0}".format(e))
            return False

        # Test the response
        try:
            # At a minimum, the response should contain a final_result key which is not an empty list
            if "final_result" not in offer_response:
                print("Error: final_result not in response")
                return False
            if offer_response["final_result"] == []:
                print("Error: final_result is empty")
                return False
            if test_iter["check_offer_count"] == "Yes":
                if len(offer_response["final_result"]) != test_iter["api_call"]["numberoffers"]:
                    print("Error: number of offers is not {0}".format(test_iter["api_call"]["numberoffers"]))
                    return False
            if test_iter["check_offer_response"] == "Yes":
                if offer_response["final_result"][0]["result"]["offer"] != test_iter["expected_offer"]:
                    print("Error: {0} returned".format(offer_response["final_result"][0]["result"]["offer"]))
                    return False
        except Exception as e:
            print("Error in runtime_test_individual_calls: {0}".format(e))
            return False

    return True


def distribution_test(auth, auth_runtime, testing_config, output_level):
    """
    Test the runtime by making multiple calls and checking the distribution of the responses. Limited to calls for 10000 customers

    :param auth: The authentication object for the ecosystem-server
    :param auth_runtime: The authentication object for the runtime
    :param testing_config: The testing configuration
    :param output_level: The level of output to print. Options are "quiet" and "verbose"

    :return: True if the tests pass, False otherwise
    """
    for test_iter in testing_config["distribution_tests"]:
        # Specify a table containing a list of msisdns to call
        customer_config = test_iter["customer_config"]
        # Specify a table containing the expected offer distribution to run the comparison against
        offer_distribution_config = test_iter["offer_distribution_config"]
        # Error margin
        error_margin = test_iter["error_margin"]
        post_invocations_input = test_iter["api_call"]

        customer_database = customer_config["database"]
        offer_database = offer_distribution_config["database"]
        # Load the tables
        if customer_database == "mongodb":
            customer_table = dme.get_data(auth_runtime, customer_config["db"], customer_config["table"], {}, 0,
                                         customer_config["column"], 0)
        elif customer_database == "cassandra":
            customer_table = dme.get_cassandra_sql(auth, "SELECT {} FROM {}.{} LIMIT 10000".format(
                customer_config["column"], customer_config["db"], customer_config["table"]))["data"]
        else:
            print("Error: customer_table database not supported, must be either mongodb or cassandra")
            return False

        if offer_database == "mongodb":
            offer_list = dme.get_data(auth_runtime, offer_distribution_config["db"], offer_distribution_config["table"],
                                     {}, 0, offer_distribution_config["offer_column"] + "," + offer_distribution_config[
                                         "count_column"], 0)
        elif offer_database == "cassandra":
            offer_list = dme.get_cassandra_sql(auth, "SELECT {}, {} FROM {}.{} LIMIT 10000".format(
                offer_distribution_config["offer_column"], offer_distribution_config["count_column"], offer_distribution_config["db"], offer_distribution_config["table"]))["data"]
        else:
            print("Error: offer_distribution_table database not supported, must be either mongodb or cassandra")
            return False

        # Get results
        offer_results = {}
        for msisdn_iter in customer_table:
            try:
                post_invocations_input["customer"] = msisdn_iter[customer_config["column"]]
                offer_response = o.invocations(auth_runtime, post_invocations_input)
                if output_level != "quiet":
                    print(offer_response)
                if "final_result" not in offer_response:
                    print("Error: final_result not in response for msisdn {0}".format(
                        msisdn_iter[customer_table["column"]]))
                    return False
                if offer_response["final_result"] == []:
                    print("Error: final_result is empty for msisdn {0}".format(msisdn_iter[customer_table["column"]]))
                    return False
                offer_returned = offer_response["final_result"][0]["result"]["offer"]
                if offer_returned not in offer_results:
                    offer_results[offer_returned] = 1
                else:
                    offer_results[offer_returned] += 1
            except Exception as e:
                print("Error in runtime_test_distribution: {0}".format(e))
                return False

        # Check alignment with expected distribution
        offer_column = offer_distribution_config["offer_column"]
        count_column = offer_distribution_config["count_column"]
        for offer_iter in offer_list:
            if test_iter["check_missing_offers"] == "Yes":
                if offer_iter[offer_column] not in offer_results:
                    print("Error: offer {0} not returned".format(offer_iter[offer_distribution_config["offer_column"]]))
                    return False
            if offer_iter[offer_column] in offer_results:
                if abs(offer_iter[count_column] - offer_results[offer_iter[offer_column]]) > error_margin:
                    print("Error: offer {0} count {1} not within error margin of {2}".format(
                        offer_iter[offer_distribution_config["offer_column"]],
                        offer_results[offer_iter[offer_distribution_config["offer_column"]]], error_margin))
                    return False

    return True


def test_deployment(auth, auth_runtime, project_id, deployment_id, version, output_level="quiet"):
    """
    Test a deployment using the testing configuration saved for the deployment

    :param auth: The authentication object for the ecosystem-server
    :param auth_runtime: The authentication object for the runtime
    :param project_id: The project_id of the deployment
    :param deployment_id: The deployment_id of the deployment
    :param version: The version of the deployment
    :param output_level: The level of output to print. Options are "quiet" and "verbose"
    """
    # Get testing config
    try:
        testing_config = dme.get_data(auth, "ecosystem_meta", "testing_configuration", {"project_id":project_id,"deployment_id": deployment_id,"version":version}, 0, {},0)[0]
    except Exception as e:
        print("Error retrieving testing config: {0}".format(e))
        return "Testing Failed"

    # Test your deployment
    individual_tests = single_test_calls(auth_runtime, testing_config, output_level)
    if not individual_tests:
        print("Error in individual_tests")
        return "Testing Failed"

    distribution_tests = distribution_test(auth, auth_runtime, testing_config, output_level)
    if not distribution_tests:
        print("Error in distribution_tests")
        return "Testing Failed"

    return "Testing Passed"


def create_network_configuration(auth, database, collection, network_collection, name, type, switch_key="", selector_splits=None,selector_groups=None,selector_api_params=None):
    """
    Create a new network configuration and store it in mongo. Existing configurations stored in the same location will be overwritten.

    :param auth: Token for accessing the ecosystem-server. Created using jwt_access.
    :param database: The database to store the configuration in.
    :param collection: The collection to store the configuration in.
    :param network_collection: The collection to store the network in.
    :param name: The name of the network configuration.
    :param type: The type of the network configuration. Allowed values are lookup, lookup_passthrough, experiment_selector, no_logging_router and model_selector.
    :param switch_key: The key to switch on for the lookup, lookup_passthrough and no_logging_router types.
    :param selector_splits: The distribution splits for the experiment_selector type. Should be a list of numbers that define the allocation of customers to an experiment group. For example selector_splits=[0.2,0.8] would have a 20% probability of assigning customers to group 1 a 60% chance of assinging customers to group 2 and and 20% chance of assigning customers to group 3.
    :param selector_groups: The groups to allocate customers to for the experiment_selector type. Should be a list of the runtime campaign names for the network nodes.
    :param selector_api_params: The parameters used when calling the runtime for the model_selector type. Should be a dictionary of the parameters to pass to the runtime.

    """
    if not isinstance(database, str):
        raise TypeError("database should be a string")
    if not isinstance(collection, str):
        raise TypeError("collection should be a string")
    if not isinstance(network_collection, str):
        raise TypeError("network_collection should be a string")
    if not isinstance(name, str):
        raise TypeError("name should be a string")
    if not isinstance(type, str):
        raise TypeError("type should be a string")
    if type not in ["lookup", "lookup_passthrough", "experiment_selector", "no_logging_router","model_selector"]:
        raise ValueError("type should be lookup, lookup_passthrough, experiment_selector, model_selector or no_logging_router")
    if type in ["lookup", "lookup_passthrough", "no_logging_router"]:
        if switch_key == "":
            raise ValueError("switch_key should be specified for lookup, lookup_passthrough and no_logging_router types")
        if not isinstance(switch_key, str):
            raise TypeError("switch_key should be a string")
    if type == "experiment_selector":
        if (selector_splits is None or selector_groups is None):
            raise ValueError("selector_splits and selector_groups should be specified for experiment_selector type")
        if not isinstance(selector_splits, list):
            raise TypeError("selector_splits should be a list")
        if not isinstance(selector_groups, list):
            raise TypeError("selector_groups should be a list")
        if (len(selector_splits) != (len(selector_groups)-1)):
            raise ValueError("selector_splits should have one less element than selector_groups")
        for i in selector_groups:
            if not isinstance(i, str):
                raise TypeError("selector_groups should be a list of strings")
        prev_split = 0
        for i in selector_splits:
            if not isinstance(i, (int, float)):
                raise TypeError("selector_splits should be a list of numbers")
            if i > 0 and i <= 1:
                raise ValueError("selector_splits should be a list of numbers greater than 0 and less than 1")
            if i <= prev_split:
                raise ValueError("selector_splits be a strictly monotonically increasing list of numbers")
    if type == "model_selector":
        if selector_api_params is None:
            raise ValueError("selector_api_params should be specified for model_selector type")
        if not isinstance(selector_api_params, dict):
            raise TypeError("selector_api_params should be a dictionary")

    try:
        network_configuration = {
            "name": name
            , "type": type
        }
        if type in ["lookup", "lookup_passthrough", "no_logging_router"]:
            network_configuration["switch_key"] = switch_key
        elif type == "experiment_selector":
            selector = {}
            selector["random_splits"] = selector_splits
            selector["groups"] = selector_groups
            network_configuration["selector"] = selector
        elif type == "model_selector":
            network_configuration["selector"] = selector_api_params
    except Exception as e:
        print("Error creating network configuration: {0}".format(e))
        return "Network configuration creation failed"

    try:
        dme.drop_document_collection(auth, database, collection)
        dme.add_documents(auth, {"database": database, "collection": collection, "document": network_configuration, "update": "name"})
    except Exception as e:
        print("Error saving network configuration: {0}".format(e))
        return "Network configuration save failed"

    try:
        network_corpora = [{"name": "network", "database": "mongodb", "db": database, "table": network_collection,
          "type": "static", "key": "value"},
         {"name": "network_config", "database": "mongodb", "db": database, "table": collection,
          "type": "static", "key": "name"}]
    except Exception as e:
        print("Error creating network corpora: {0}".format(e))
        return "Network corpora creation failed"

    print("MESSAGE: Network configuration created")
    return network_corpora


def add_network_node(auth, database, collection, node_value, node_api_params):
    """
    Add a new network node to a network runtime configuration. Will replace existing network nodes with the same value.

    :param auth: Token for accessing the ecosystem-server. Created using jwt_access.
    :param database: The database to store the configuration in.
    :param collection: The collection to store the configuration in.
    :param node_value: The value of the node to add. The value is used by the network runtime to determine which node should be called.
    :param node_api_params: The parameters to use when calling the node. Should be a dictionary of the parameters to pass to the node. These parameters will overridde the parameters of the same name passed through the api call.
    """

    if not isinstance(database, str):
        raise TypeError("database should be a string")
    if not isinstance(collection, str):
        raise TypeError("collection should be a string")
    if not isinstance(node_value, str):
        raise TypeError("node_value should be a string")
    if not isinstance(node_api_params, dict):
        raise TypeError("node_api_params should be a dictionary")

    try:
        node_api_params["value"] = node_value
        network_node = node_api_params
    except Exception as e:
        print("Error creating network node: {0}".format(e))
        return "Network node creation failed"

    try:
        dme.add_documents(auth, {"database": database, "collection": collection, "document": network_node, "update": "value"})
    except Exception as e:
        print("Error saving network node: {0}".format(e))
        return "Network node save failed"

    return "Network node added"


def remove_network_node(auth, database, collection, node_value):
    """
    Remove a network node from a network runtime configuration.

    :param auth: Token for accessing the ecosystem-server. Created using jwt_access.
    :param database: The database to store the configuration in.
    :param collection: The collection to store the configuration in.
    :param node_value: The value of the node to remove.
    """

    if not isinstance(database, str):
        raise TypeError("database should be a string")
    if not isinstance(collection, str):
        raise TypeError("collection should be a string")
    if not isinstance(node_value, str):
        raise TypeError("node_value should be a string")

    try:
        dme.delete_documents(auth, {"database": database, "collection": collection, "key":"value", "value": node_value})
    except Exception as e:
        print("Error removing network node: {0}".format(e))
        return "Network node removal failed"

    return "Network node removed"


def get_openshift_deployment_config(name, version, environment_variables, namespace="bdp-rts-dev",volume="tc-bdp-rts-dev-disk", replicas=1,
                                    port=8999):
    """
    Create a deployment configuration yaml file for an OpenShift deployment. Will create a yaml file with the deployment configuration in the working directory.

    :param name: The name of the deployment
    :param version: The version of the ecosystem-runtime container
    :param environment_variables: A list of environment variables to set in the deployment
    :param namespace: The namespace to deploy the deployment in
    :param volume: The volume to mount in the deployment
    :param replicas: The number of replicas in the deployment
    :param port: The port to expose in the deployment

    :return: The deployment configuration
    """
    if not isinstance(name, str):
        raise TypeError("name should be a string")
    if "_" in name:
        raise ValueError("name should not contain underscores")
    if not isinstance(version, str):
        raise TypeError("version should be a string")
    valid_versions = [
          "0.9.4.1"
        , "0.9.4.1-arm"
        , "0.9.4.2"
        , "0.9.4.2-arm"
        , "0.9.4.3"
        , "0.9.4.3-arm"
        , "0.9.4.4"
        , "0.9.4.4-arm"
        , "latest"
        , "arm"
        ]
    if not version in valid_versions:
        raise ValueError("version should be one of {0}".format(valid_versions))
    if not isinstance(environment_variables, list):
        raise TypeError("environment_variables should be a list")
    if not isinstance(namespace, str):
        raise TypeError("namespace should be a string")
    if not isinstance(volume, str):
        raise TypeError("volume should be a string")
    if not isinstance(replicas, int):
        raise TypeError("replicas should be an integer")
    if not isinstance(port, int):
        raise TypeError("port should be an integer")

    deployment_config = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {'labels': {'app': f'{name}',
                                'app.kubernetes.io/component': f'{name}',
                                'app.kubernetes.io/instance': f'{name}',
                                'app.kubernetes.io/name': f'{name}',
                                'app.kubernetes.io/part-of': 'ecosystem-runtimes',
                                'app.openshift.io/runtime-namespace': f'{namespace}'},
                     'name': f'{name}',
                     'namespace': f'{namespace}'},
        'spec': {'progressDeadlineSeconds': 600,
                 'replicas': replicas,
                 'revisionHistoryLimit': 10,
                 'selector': {'matchLabels': {'app': f'{name}'}},
                 'strategy': {'rollingUpdate': {'maxSurge': '100%',
                                                'maxUnavailable': '25%'},
                              'type': 'RollingUpdate'},
                 'template': {'metadata': {'creationTimestamp': None,
                                           'labels': {'app': f'{name}',
                                                      'deployment': f'{name}'}},
                              'spec': {'containers': [{'env': [{'name': 'NO_MONGODB',
                                                                'value': 'true'},
                                                               {'name': 'ECOSYSTEM_PROP_FILE',
                                                                'value': '/config/ecosystem.properties'}],
                                                       'image': f'docker.io/ecosystemai/ecosystem-runtime-solo:{version}',
                                                       'imagePullPolicy': 'IfNotPresent',
                                                       'name': f'{name}',
                                                       'ports': [{'containerPort': port,
                                                                  'protocol': 'TCP'}],
                                                       'resources': {'limits': {'memory': '2Gi'},
                                                                     'requests': {'memory': '2Gi'}},
                                                       'terminationMessagePath': '/dev/termination-log',
                                                       'terminationMessagePolicy': 'File',
                                                       'volumeMounts': [{'mountPath': '/config',
                                                                         'name': volume,
                                                                         'subPath': f'{name}-config'},
                                                                        {'mountPath': '/data/models',
                                                                         'name': volume,
                                                                         'subPath': f'{name}-data'}]}],
                                       'dnsPolicy': 'ClusterFirst',
                                       'restartPolicy': 'Always',
                                       'schedulerName': 'default-scheduler',
                                       'securityContext': {},
                                       'terminationGracePeriodSeconds': 30,
                                       'volumes': [{'name': volume,
                                                    'persistentVolumeClaim': {'claimName': volume}}]
                                       }
                              }
                 }
    }
    for var in environment_variables:
        var_split = var.split("=")
        var_dict = {"name": var_split[0], "value": var_split[1]}
        deployment_config["spec"]["template"]["spec"]["containers"][0]["env"].append(var_dict)
    with open(f'deployment-{name}.yaml', 'w+') as f:
        yaml.dump(deployment_config, f)
    return deployment_config


def create_openshift_enpoint(name, openshift_server, oc_path, oc_user, version="0.9.4.3", environment_variables=None,
                             port=8999, namespace="bdp-rts-dev", replicas=1, volume="tc-bdp-rts-dev-disk",
                             cassandra_path=None, model_path=None, use_oc=True):
    """
    Create an OpenShift deployment for the ecosystem-runtime using a default configuration and expose the deployment as a route to allow the configuration to be updated.

    :param name: The name of the deployment
    :param openshift_server: The OpenShift server to deploy the deployment to
    :param oc_path: The path to the oc executable
    :param oc_user: The OpenShift user to use when connecting to oc
    :param version: The version of the ecosystem-runtime container
    :param environment_variables: A list of environment variables to set in the deployment
    :param port: The port to expose in the deployment
    :param namespace: The namespace to deploy the deployment in
    :param replicas: The number of replicas in the deployment
    :param volume: The volume to mount in the deployment
    :param cassandra_path: The path to the cassandra configuration file
    :param model_path: A list of the paths to the model files
    :param use_oc: A boolean indicating whether to use the oc executable to create the deployment

    :return: The endpoint of the deployment
    """
    if not isinstance(name, str):
        raise TypeError("name should be a string")
    if "_" in name:
        raise ValueError("name should not contain underscores")
    if not isinstance(openshift_server, str):
        raise TypeError("openshift_server should be a string")
    if not isinstance(oc_path, str):
        raise TypeError("oc_path should be a string")
    if not isinstance(oc_user, str):
        raise TypeError("oc_user should be a string")
    if not isinstance(version, str):
        raise TypeError("version should be a string")
    valid_versions = [
          "0.9.4.1"
        , "0.9.4.1-arm"
        , "0.9.4.2"
        , "0.9.4.2-arm"
        , "0.9.4.3"
        , "0.9.4.3-arm"
        , "latest"
        , "arm"
        ]
    if not version in valid_versions:
        raise ValueError("version should be one of {0}".format(valid_versions))
    if (not isinstance(environment_variables, list)) and (environment_variables is not None):
        raise TypeError("environment_variables should be a list")
    if not isinstance(port, int):
        raise TypeError("port should be an integer")
    if not isinstance(namespace, str):
        raise TypeError("namespace should be a string")
    if not isinstance(replicas, int):
        raise TypeError("replicas should be an integer")
    if not isinstance(use_oc, bool):
        raise TypeError("use_oc should be a boolean")

    ecosystem_key = getpass.getpass("Enter your ecosystem API key")
    if environment_variables is None:
        environment_variables = [
            f"MASTER_KEY={ecosystem_key}",
            "MONITORING_DELAY=600",
            "FEATURE_DELAY=9999999999",
            "CASSANDRA_CONFIG=/config/cassandra.conf",
            "TZ=Africa/Johannesburg",
            f"PORT={port}"
        ]

    deployment_config = get_openshift_deployment_config(name, version, environment_variables, namespace=namespace,
                                                        volume=volume, replicas=replicas, port = port)

    with open('version.txt', 'a') as f:
        f.write(version)
    if use_oc:
        openshift_password = getpass.getpass("Enter your OpenShift password")
        with oc.api_server(openshift_server), oc.client_path(oc_path):
            oc.login(oc_user, openshift_password)
            oc.apply(deployment_config)
            all_pods_started = False
            time.sleep(5)
            while not all_pods_started:
                all_pods_started = True
                for pod_obj in oc.selector("pods", labels={"deployment": name}).objects():
                    pod_name = pod_obj.name()
                    print(f"Checking status of pod {pod_name}")
                    log_string = pod_obj.logs()[list(pod_obj.logs().keys())[0]]
                    if "Start ecosystem with standard memory option" not in log_string:
                        all_pods_started = False
                        print("Pod not started")
                    else:
                        print("Pod started")
                if not all_pods_started:
                    time.sleep(15)
            print("All pods started successfully")

            print("Checking runtime startup")
            all_runtimes_started = False
            while not all_runtimes_started:
                all_runtimes_started = True
                for pod_obj in oc.selector("pods", labels={"deployment": name}).objects():
                    pod_name = pod_obj.name()
                    print(f"Checking status of runtime on pod {pod_name}")
                    try:
                        exec_result = oc.selector(f'pod/{pod_name}').object().execute(
                            ["curl", "-X", "GET", f"http://localhost:{port}/ping", "-H", "accept: */*"])
                        if "success" not in exec_result.out():
                            all_runtimes_started = False
                            print("Runtime not started")
                        else:
                            print("Runtime started")
                    except Exception as e:
                        print(e)
                        print("Error sending command to runtime")
                if not all_runtimes_started:
                    time.sleep(15)
            print("All runtimes started successfully")
            try:
                oc.invoke("expose", ["deployment", name, f"--port={port}"])
            except Exception as error:
                serv_error_message = error.result.as_dict()["actions"][0]["err"]
                if "already exists" in serv_error_message:
                    print("WARNING: service already exists, if the port has been changed this will not take affect")
                else:
                    raise error
            try:
                oc.invoke("expose", ["svc", name, f"--port={port}"])
            except Exception as error:
                route_error_message = error.result.as_dict()["actions"][0]["err"]
                if "already exists" in route_error_message:
                    print("WARNING: route already exists, if the port has been changed this will not take affect")
                else:
                    raise error
            oc.invoke("annotate", ["route", name, "haproxy.router.openshift.io/balance=roundrobin"])
            oc.invoke("annotate", ["route", name, "haproxy.router.openshift.io/disable_cookies='true'"])
            route_select = oc.selector("routes", labels={"app": name}).object()
            route_details = route_select.describe()
            ind_start = route_details.index("Requested Host:")
            ind_end = route_details[ind_start + 15:].index(" ")
            runtime_path = "http://{}".format(route_select.describe()[ind_start + 15:ind_start + 15 + ind_end].strip())
            print(f"Endpoint created at: {runtime_path}")
            if cassandra_path is not None:
                oc.invoke("cp", [cassandra_path, f"{pod_name}:/config/cassandra.conf"])
            if model_path is not None:
                for model in model_path:
                    oc.invoke("cp", [model, f"{pod_name}:/data/models/"])
    else:
        print(
            "You have opted to complete the deployment without using oc. This will require you to manually copy a number of configurations into the OpenShift web console")
        print("")
        print(
            f"Step 1: Open the deployment-{name}.yml file which has been created in this folder and copy the contents of the file. Log onto the OpenShift web console and confirm that you are working in the bdp-rts-dev project (this should be the project selected by default). Select Administrator view from the dropdown near the top left of the screen. Open the Workloads section of the left hand menu and select Deployments. Click the blue Create Deployment button in the top right corner of the Deployments section. In the radio button at the top of the Create Deployment view that is opened change from Form View to YAML view. Replace the text in the editor with the text you copied from deployment-{name}.yml and click the Create button below the editor.")
        print("")
        print(
            "Step 2: Wait for the deployment to be created. This may take a few minutes. You can check the progress of the deployment by selecting Deployment and Pods in the Workloads section of the left hand menu and clicking on the case you have created.")
        print("")
        print("Step 3 (optional): If you want to connect to a Cassandra database you will need to add the cassandra.conf file to the deployment. Navigate to the pod you have created as described in the previous step. Open the Terminal tab. Change the working directory to config using the command 'cd config'. Copy the contents of your cassandra.conf file then go back to the terminal and type 'cat > cassandra.conf' and paste the contents of the file. Press Ctrl+D on a new line to save the file. You can check that the file has been created by typing 'ls' in the terminal and you can check the contents of the file by typing 'cat cassandra.conf'.")
        print("")
        service_config = {
            "kind": "Service"
            , "apiVersion": "v1"
            , "metadata": {
                "name": name
                , "namespace": "bdp-rts-dev"
                , "labels": {
                    "app": name
                    , "app.kubernetes.io/component": name
                    , "app.kubernetes.io/instance": name
                    , "app.kubernetes.io/name": name
                    , "app.kubernetes.io/part-of": "ecosystem-runtimes"
                    , "app.openshift.io/runtime-namespace": "bdp-rts-dev"
                }
            }
            , "spec": {
                "ports": [
                    {"protocol": "TCP"
                        , "port": port
                        , "targetPort": port}
                ]
                , "selector": {
                    "app": name
                }
            }
        }
        with open(f'service.yaml', 'w+') as f:
            yaml.dump(service_config, f)
        print(
            "Step 4: Create a Service for the Deployment that you have created. Copy the contents of the service.yml file which has been created in this folder. Open the Networking section of the left hand menu and select Services. Click the blue Create Service button in the top right corner of the Serivces section. Replace the text in the editor with the text you copied from service.yml and click the Create button below the editor.")
        print("")
        print(
            f"Step 5: Create a Route linked to the Deployment. Open the Networking section of the left hand menu and select Routes. Click the blue Create Route button in the top right corner of the deployment section. Set the Name to be {name}. Leave Hostname and Path empty. Select the Service you created and the Port for the service from the dropdowns. Leave the Secure Route tick box empty. Click the Create button.")
        print("")
        print(
            "Step 6: Test the endpoint that you have created by navigating to the Route url (which you can find by Navigating to Networking -> Routes in the left hand menu) and calling the refresh api. The response to the refresh API call should include success.")
        print("")
        print("Step 7: Set the runtime_path variable in the notebook to be the url of the Route that you created")

        runtime_path = "This variable needs to be set manually as oc is not being used in the setup"

    return runtime_path


def udate_properties_and_refresh(name, openshift_server, oc_path, oc_user, properties=None, port=8999, use_oc=True):
    """
    Update the properties of an ecosystem-runtime deployment in OpenShift and refresh the deployment to apply the changes.

    :param name: The name of the deployment
    :param openshift_server: The OpenShift server where the deployment is running
    :param oc_path: The path to the oc executable
    :param oc_user: The OpenShift user to use when connecting to oc
    :param properties: The properties to push to the ecosystem-runtime
    :param port: The port to exposed in the deployment
    :param use_oc: A boolean indicating whether to use the oc executable to update the deployment
    """
    if not isinstance(name, str):
        raise TypeError("name should be a string")
    if not isinstance(openshift_server, str):
        raise TypeError("openshift_server should be a string")
    if not isinstance(oc_path, str):
        raise TypeError("oc_path should be a string")
    if not isinstance(oc_user, str):
        raise TypeError("oc_user should be a string")
    if not isinstance(properties, str):
        raise TypeError("properties should be a string")
    if not isinstance(port, int):
        raise TypeError("port should be an integer")
    if not isinstance(use_oc, bool):
        raise TypeError("use_oc should be a boolean")

    if use_oc:
        with oc.api_server(openshift_server), oc.client_path(oc_path):
            try:
                oc.selector("projects")
            except:
                openshift_password = getpass.getpass("Enter your OpenShift password")
                oc.login(oc_user, openshift_password)
            for pod_obj in oc.selector("pods", labels={"deployment": name}).objects():
                pod_name = pod_obj.name()
                if properties is not None:
                    print(f"Updating properties on pod {pod_name}")
                    exec_result = oc.selector(f'pod/{pod_name}').object().execute(
                        ["curl", "-X", "POST", f"http://localhost:{port}/updateProperties", "-H", "accept: */*", "-H",
                         "Content-Type: application/json", "-d", properties])
                print(f"Refreshing pod {pod_name}")
                exec_result = oc.selector(f'pod/{pod_name}').object().execute(
                    ["curl", "-X", "GET", f"http://localhost:{port}/refresh", "-H", "accept: */*"])
    else:
        print(
            "You have opted to complete the deployment without using oc. Open the ecosystem.properties file that has been created in this folder and copy it's contents. Open the url of the route that you created (navigate the Networking -> Routes in the OpenShift web console to get the url). Find the updateProperties API in the swagger interface and call the api with the contents of the ecosystem.properties file as the request body. Then call the refresh api in the swagger interface and check that the response is success.")


def tail_openshift_logs(name, openshift_server, oc_path, oc_user, lines, use_oc=True):
    """
    Tail the logs of an ecosystem-runtime deployment in OpenShift. If there are multiple pods for the deployment, the logs of each pod will be tailed.

    :param name: The name of the deployment
    :param openshift_server: The OpenShift server where the deployment is running
    :param oc_path: The path to the oc executable
    :param oc_user: The OpenShift user to use when connecting to oc
    :param lines: The number of lines to tail from the log
    :param use_oc: A boolean indicating whether to use the oc executable to tail the logs
    """
    if not isinstance(name, str):
        raise TypeError("name should be a string")
    if not isinstance(openshift_server, str):
        raise TypeError("openshift_server should be a string")
    if not isinstance(oc_path, str):
        raise TypeError("oc_path should be a string")
    if not isinstance(oc_user, str):
        raise TypeError("oc_user should be a string")
    if not isinstance(lines, int):
        raise TypeError("lines should be an integer")
    if not isinstance(use_oc, bool):
        raise TypeError("use_oc should be a boolean")

    if use_oc:
        with oc.api_server(openshift_server), oc.client_path(oc_path):
            try:
                oc.selector("projects")
            except:
                openshift_password = getpass.getpass("Enter your OpenShift password")
                oc.login(oc_user, openshift_password)
            for pod_obj in oc.selector("pods", labels={"deployment": name}).objects():
                pod_name = pod_obj.name()
                print(f"Getting logs for pod {pod_name}")
                exec_result = oc.selector(f'pod/{pod_name}').object().execute(
                    ["tail", f"-{lines}", "/data/logs/pulse_responder.log"])
                print(exec_result.out())
                print("")
    else:
        print(
            f"You have opted to complete the deployment without using oc. You will need to view the logs in the OpenShift web console. In the OpenShift web console select Adminstrator view then navigate to Workloads -> Deployment in the left hand menu. Select deployment {name} and in the view that appears open the Pods tab. Click on the name of the pod for which you would like to view the logs. In the view that opens select the Terminal tab. In the terminal view you can use the following command to follow the logs 'tail -f /data/logs/pulse_responder.log'")


def get_openshift_service_ips(openshift_server, oc_path, oc_user, use_oc=True):
    """
    Get the IP addresses of the services running in OpenShift. If there are multiple services, the IP addresses of each service will be returned.

    :param openshift_server: The OpenShift server from which the services should be retrieved
    :param oc_path: The path to the oc executable
    :param oc_user: The OpenShift user to use when connecting to oc
    :param use_oc: A boolean indicating whether to use the oc executable to get the IP addresses of the services
    """
    if not isinstance(openshift_server, str):
        raise TypeError("openshift_server should be a string")
    if not isinstance(oc_path, str):
        raise TypeError("oc_path should be a string")
    if not isinstance(oc_user, str):
        raise TypeError("oc_user should be a string")
    if not isinstance(use_oc, bool):
        raise TypeError("use_oc should be a boolean")

    if use_oc:
        services = {}
        with oc.api_server(openshift_server), oc.client_path(oc_path):
            try:
                oc.selector("projects")
            except:
                openshift_password = getpass.getpass("Enter your OpenShift password")
                oc.login(oc_user, openshift_password)
            for service_obj in oc.selector("services").objects():
                ser = service_obj.as_dict()
                services[service_obj.as_dict()["metadata"]["name"]] = "http://{}:{}".format(ser["spec"]["clusterIP"],
                                                                                            ser["spec"]["ports"][0][
                                                                                                "port"])
        for i in services:
            print(i, services[i])
        return services
    else:
        print(
            "You have opted to complete the deployment without using oc. You will need to get the IP addresses of the Services running in OpenShift manually. In the OpenShift web console select Adminstrator view then navigate to Networking -> Services in the left hand menu. The IP addresses of eaach service are shown in the list of services. Copy the IP for the service that you want to link to the network recommender and copy it into the url in the add_node function call.")

