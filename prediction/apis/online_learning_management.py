from prediction.apis import algorithm_client_pulse as cp
from prediction.apis import data_management_engine as dme

from datetime import datetime
import json
import uuid


def online_learning_ecosystem_rewards_setup_feature_store(
    auth,
    offer_db,
    offer_collection,
    offer_name_column,
    contextual_variables,
    setup_feature_store_db,
    setup_feature_store_collection
):
    """
    Add contextual variables to a setup feature store for the ecosystem rewards dynamic recommender using a collection
    containing the relevant offers.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param offer_db: The database containing the offers.
   :param offer_collection: The collection containing the offers.
   :param offer_name_column: The column in the collection containing the offer names.
   :param contextual_variables: A dictionary containing the contextual variables names as keys. Each value in the dictionary should be a list containing the possible values of the contextual variables.
   :param setup_feature_store_db: The database to store the setup feature store in.
   :param setup_feature_store_collection: The collection to store the setup feature store in.

    """
    if not isinstance(offer_db, str):
        raise TypeError("offer_db should be a string")
    if not isinstance(offer_collection, str):
        raise TypeError("offer_collection should be a string")
    if not isinstance(offer_name_column, str):
        raise TypeError("offer_name_column should be a string")
    if not isinstance(contextual_variables, dict):
        raise TypeError("contextual_variables should be a dictionary")
    if not isinstance(setup_feature_store_db, str):
        raise TypeError("setup_feature_store_db should be a string")
    if not isinstance(setup_feature_store_collection, str):
        raise TypeError("setup_feature_store_collection should be a string")

    try:
        sample_offer_collection = dme.get_data(auth, offer_db, offer_collection, {}, 1, {}, 0)
        if len(sample_offer_collection) == 0:
            raise ImportError(f"Mongo collection {offer_collection} in database {offer_db} appears to be empty")
        if offer_name_column not in sample_offer_collection:
            raise KeyError(f"{offer_name_column}, specified as the offer_name_column, not found as a field in "
                           f"{offer_collection}")
    except Exception as error:
        print("Unexpected error occured while validating offer_db and offer_collection")
        raise
    
    if len(contextual_variables) > 2:
        raise KeyError("At most two contextual variables can be specified for the ecosystem rewards algorithm")
    for context_var_iter in contextual_variables:
        if not isinstance(contextual_variables[context_var_iter], list):
            raise TypeError("The value for each key in the contextual variables dictionary should be a list of "
                            "possible segment values")

    contextual_fields = list(contextual_variables.keys())
    if len(contextual_fields) == 2:
        dme.post_mongo_db_aggregate_pipeline(auth,
            {
            "database":offer_db
            ,"collection":offer_collection
            ,"pipeline":[
                {"$group":{"_id":"$"+offer_name_column}}
                ,{"$project":{offer_name_column:"$_id","_id":0}}
                ,{"$addFields":{contextual_fields[0]:contextual_variables[contextual_fields[0]]}}
                ,{"$unwind":"$"+contextual_fields[0]}
                ,{"$addFields":{contextual_fields[1]:contextual_variables[contextual_fields[1]]}}
                ,{"$unset":"_id"}
                ,{"$unwind":"$"+contextual_fields[1]}
                ,{"$out":{"db":setup_feature_store_db,"coll":setup_feature_store_collection}}
            ]
            }
        )
    elif len(contextual_fields) == 1:
        dme.post_mongo_db_aggregate_pipeline(auth,
            {
            "database":offer_db
            ,"collection":offer_collection
            ,"pipeline":[
                {"$group":{"_id":"$"+offer_name_column}}
                ,{"$project":{offer_name_column:"$_id","_id":0}}
                ,{"$addFields":{contextual_fields[0]:contextual_variables[contextual_fields[0]]}}
                ,{"$unwind":"$"+contextual_fields[0]}
                ,{"$out":{"db":setup_feature_store_db,"coll":setup_feature_store_collection}}
            ]
            }
        )


def create_online_learning(
        auth,
        name,
        description,
        feature_store_collection,
        feature_store_database,
        options_store_database,
        options_store_collection,
        contextual_variables_offer_key,
        score_connection="http://ecosystem-runtime:8091",
        score_database="ecosystem_meta",
        score_collection="dynamic_engagement",
        algorithm="ecosystem_rewards",
        options_store_connection="",
        batch="false",       
        feature_store_connection="",
        contextual_variables_contextual_variable_one_from_data_source=False,
        contextual_variables_contextual_variable_one_lookup="",
        contextual_variables_contextual_variable_one_name="",
        contextual_variables_contextual_variable_two_from_data_source=False,
        contextual_variables_contextual_variable_two_name="",
        contextual_variables_contextual_variable_two_lookup="",
        contextual_variables_tracking_key="",
        contextual_variables_take_up="",
        batch_database_out="",
        batch_collection_out="",
        batch_threads=1,
        batch_collection="",
        batch_userid="",
        batch_contextual_variables="",
        batch_number_of_offers=1,
        batch_database="",
        batch_pulse_responder_list="",
        batch_find="{}",
        batch_options="",
        batch_campaign="",
        batch_execution_type="",
        randomisation_calendar="None",
        randomisation_test_options_across_segment="",
        randomisation_processing_count=1000,
        randomisation_discount_factor=0.75,
        randomisation_batch="false",
        randomisation_prior_fail_reward=0.1,
        randomisation_cross_segment_epsilon=0,
        randomisation_success_reward=1,
        randomisation_interaction_count="0",
        randomisation_epsilon=0,
        randomisation_prior_success_reward=1,
        randomisation_fail_reward=0.1,
        randomisation_max_reward=10,
        randomisation_cache_duration=0,
        randomisation_processing_window=86400000,
        randomisation_random_action=0.2,
        randomisation_decay_gamma="1",
        randomisation_learning_rate=0.25,
        randomisation_missing_offers="none",
        randomisation_training_data_source="feature_store",
        virtual_variables=None,
        dynamic_eligibility=None,
        replace=False,
        update=False,
        create_options_index=True,
        create_covering_index=True
):
    """
   Create a new online learning configuration.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param name: The name of the online learning configuration.
   :param description: The description of the online learning configuration.
   :param feature_store_collection: The collection containing the setup feature store.
   :param feature_store_database: The database containing the setup feature store.
   :param options_store_database: The database containing the options store.
   :param options_store_collection: The collection containing the options store.
   :param contextual_variables_offer_key: The key in the setup feature store collection that contains the offer.
   :param score_connection: Used when batch processing is enabled. The connection string to the runtime engine to use for batch processing.
   :param score_database: The database where the online learning configuration is stored
   :param score_collection: The collection where the online learning configuration is stored
   :param algorithm: The algorithm to use for the online learning configuration. Currently only "ecosystem_rewards", "bayesian_probabilistic" and "q_learning" are supported.
   :param options_store_connection: The connection string to the options store.
   :param batch: A boolean indicating whether batch processing should be enabled.
   :param feature_store_connection: The connection string to the setup feature store.
   :param contextual_variables_contextual_variable_one_from_data_source: A boolean indicating whether the first contextual variable should be read from the deployment customer lookup.
   :param contextual_variables_contextual_variable_one_name: The field in the setup feature store to be used for the first contextual variable.
   :param contextual_variables_contextual_variable_one_lookup: The key in the deployment customer lookup that contains the first contextual variable.
   :param contextual_variables_contextual_variable_two_name: The field in the setup feature store to be used for the second contextual variable.
   :param contextual_variables_contextual_variable_two_lookup: The key in the deployment customer lookup that contains the second contextual variable.
   :param contextual_variables_contextual_variable_two_from_data_source: A boolean indicating whether the second contextual variable should be read from the deployment customer lookup.
   :param contextual_variables_tracking_key: The field in the setup feature store to be used for the tracking key.
   :param contextual_variables_take_up: The field in the setup feature store to be used for the take-up.
   :param batch_database_out: The database to store the batch output in.
   :param batch_collection_out: The collection to store the batch output in.
   :param batch_threads: The number of threads to use for batch processing.
   :param batch_collection: The collection to read the batch data from.
   :param batch_userid: The user to be passed to the batch runtime.
   :param batch_contextual_variables: The contextual variables to be used in the batch processing.
   :param batch_number_of_offers: The number of offers to be used in the batch processing.
   :param batch_database: The database to read the batch data from.
   :param batch_pulse_responder_list: The list of runtimes to be used in the batch processing.
   :param batch_find: The query to be used to find the batch data.
   :param batch_options: The options to be used in the batch processing.
   :param batch_campaign: The campaign to be used in the batch processing.
   :param batch_execution_type: The execution type to be used in the batch processing. Allowed values are "internal" and "external".
   :param randomisation_calendar: The calendar to be used.
   :param randomisation_test_options_across_segment: Boolean variable indicating whether offers should be tested outside of their allowed contextual variable segments.
   :param randomisation_processing_count: The number of interactions to be processed.
   :param randomisation_discount_factor: The discount factor to be used in the randomisation.
   :param randomisation_batch: Boolean variable indicating whether batch processing should be enabled.
   :param randomisation_prior_fail_reward: The prior fail reward to be used in the randomisation.
   :param randomisation_cross_segment_epsilon: The cross segment epsilon to be used in the randomisation.
   :param randomisation_success_reward: The success reward to be used in the randomisation.
   :param randomisation_interaction_count: The number of interactions to be used in the randomisation.
   :param randomisation_epsilon: The epsilon to be used in the randomisation.
   :param randomisation_prior_success_reward: The prior success reward to be used in the randomisation.
   :param randomisation_fail_reward: The fail reward to be used in the randomisation.
   :param randomisation_max_reward: The maximum reward to be used in the randomisation.
   :param randomisation_cache_duration: The cache duration to be used in the randomisation.
   :param randomisation_processing_window: The processing window to be used in the randomisation.
   :param randomisation_random_action: The random action to be used in the randomisation.
   :param randomisation_decay_gamma: The decay gamma to be used in the randomisation.
   :param randomisation_learning_rate: The learning rate to be used in the randomisation.
   :param randomisation_missing_offers: The approach used to add scores for offers not present in the training set for the bayesian probabilistic algorithm. Allowed values are "none" and "uniform".
   :param randomisation_training_data_source: The data source to be used for training the q-learning algorithm. Allowed values are "feature_store" and "logging".
   :param virtual_variables: A list of virtual variables to be used in the online learning configuration.
   :param dynamic_eligibility: A dictionary specifying the eligibility rules to be applied when selecting offers for the online learning configuration.
   :param replace: A boolean indicating whether the online learning configuration should be replaced if it already exists.
   :param update: A boolean indicating whether the online learning configuration should be updated if it already exists.
   :param create_options_index: A boolean indicating whether an index should be created on the options store collection. This index greatly improves responses times.
   :param create_covering_index: A boolean indicating whether a covering index should be created on the options store collection. A covered index greatly improves responses times but does not make all fields in the options store available in the post scoring logic.

   :return: The UUID identifier for the online learning configuration which should be linked to the deployment for the project.
    """
    # TODO add error checking and handling
    # Check for existence of online learning configuration with the same name
    existing_configurations = cp.list_pulse_responder_dynamic(auth)
    if not replace and not update:
        if len([d for d in existing_configurations["data"] if d["name"] == name]) > 0:
            raise ValueError(f"There is an existing online learning configuration named {name} and replace and update are both False")

    if update:
        if len([d for d in existing_configurations["data"] if d["name"] == name]) == 0:
            raise ValueError(f"Update is set to true and no existing configuration with name {name} can be found")
        update_uuid = [d["uuid"] for d in existing_configurations["data"] if d["name"] == name][0]

    if not isinstance(randomisation_missing_offers, str):
        raise TypeError("randomisation_missing_offers should be a string")
    if randomisation_missing_offers not in ["none", "uniform"]:
        raise ValueError("randomisation_missing_offers should be either 'none' or 'uniform'")

    if algorithm not in ["ecosystem_rewards","bayesian_probabilistic","q_learning"]:
        raise ValueError("algorithm must be ecosystem_rewards, bayesian_probabilistic or q_learning algorithm for other algorithms please use the "
                         "ecosystem.Ai workbench")

    # Initialise configuration document and store input parameters
    config_doc = {}
    config_doc["name"] = name
    config_doc["description"] = description
    
    config_doc["feature_store_collection"] = feature_store_collection
    config_doc["feature_store_database"] = feature_store_database
    config_doc["feature_store_connection"] = feature_store_connection
    
    config_doc["options_store_database"] = options_store_database
    config_doc["options_store_collection"] = options_store_collection
    config_doc["options_store_connection"] = options_store_connection
    
    config_doc["score_collection"] = score_collection
    config_doc["score_database"] = score_database
    config_doc["score_connection"] = score_connection
    
    config_doc["batch"] = batch
    config_doc["options"] = []
    config_doc["date_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    config_doc["description"] = description
    if update:
        config_doc["uuid"] = update_uuid
    else:
        config_doc["uuid"] = str(uuid.uuid4())
    
    # Get values for contextual variables
    if contextual_variables_contextual_variable_one_name != "":
        contextual_variable_one_values_pipeline = [
            {"$group":{"_id":"None","values":{"$addToSet":"$"+contextual_variables_contextual_variable_one_name}}}
        ]
        contextual_variable_one_values = dme.post_mongo_db_aggregate_pipeline(
                auth,
                {"database": feature_store_database, "collection": feature_store_collection, "pipeline": contextual_variable_one_values_pipeline}
        )[0]["values"]
    else:
        contextual_variable_one_values = []
    
    if contextual_variables_contextual_variable_two_name != "":
        contextual_variable_two_values_pipeline = [
            {"$group":{"_id":"None","values":{"$addToSet":"$"+contextual_variables_contextual_variable_two_name}}}
        ]
        contextual_variable_two_values = dme.post_mongo_db_aggregate_pipeline(
                auth,
                {"database": feature_store_database, "collection": feature_store_collection, "pipeline": contextual_variable_two_values_pipeline}
        )[0]["values"]
    else:
        contextual_variable_two_values = []
    
    contextual_variables = {
        "offer_key": contextual_variables_offer_key,
        "offer_values": [],
        "contextual_variable_one_from_data_source": contextual_variables_contextual_variable_one_from_data_source,
        "contextual_variable_one_lookup": contextual_variables_contextual_variable_one_lookup,
        "contextual_variable_one_name": contextual_variables_contextual_variable_one_name,
        "contextual_variable_one_values": contextual_variable_one_values,
        "contextual_variable_two_from_data_source": contextual_variables_contextual_variable_two_from_data_source,
        "contextual_variable_two_name": contextual_variables_contextual_variable_two_name,
        "contextual_variable_two_lookup": contextual_variables_contextual_variable_two_lookup,
        "contextual_variable_two_values": contextual_variable_two_values,
        "tracking_key": contextual_variables_tracking_key,
        "take_up": contextual_variables_take_up
    }
    if algorithm == "bayesian_probabilistic":
        training_variable_sample = dme.get_data(auth, feature_store_database, feature_store_collection, {}, 1, {}, 0)
        training_variables = list(training_variable_sample.keys())
        for rem_iter in [contextual_variables_offer_key,contextual_variables_tracking_key,contextual_variables_take_up,"_id"]:
            if rem_iter in training_variables:
                training_variables.remove(rem_iter)
        training_variables_dict = {}
        for training_variable_iter in training_variables:
            training_variable_values_pipeline = [
                {"$group":{"_id":"None","values":{"$addToSet":"$"+training_variable_iter}}}
            ]
            training_variable_values = dme.post_mongo_db_aggregate_pipeline(
                    auth,
                    {"database": feature_store_database, "collection": feature_store_collection, "pipeline": training_variable_values_pipeline}
            )[0]["values"]
            training_variables_dict[training_variable_iter] = training_variable_values
        contextual_variables["training_variable_values"] = training_variables_dict

    config_doc["contextual_variables"] = contextual_variables
    
    batch_settings = {
        "database_out": batch_database_out,
        "collection_out": batch_collection_out,
        "batchUpdateMessage": "",
        "threads": batch_threads,
        "collection": batch_collection,
        "userid": batch_userid,
        "contextual_variables": batch_contextual_variables,
        "number_of_offers": batch_number_of_offers,
        "batch_outline": "",
        "pulse_responder_list": batch_pulse_responder_list,
        "database": batch_database,
        "find": batch_find,
        "options": batch_options,
        "campaign": batch_campaign,
        "execution_type": batch_execution_type
    }
    config_doc["batch_settings"] = batch_settings

    if algorithm == "ecosystem_rewards":
        approach = "binaryThompson"
    elif algorithm == "bayesian_probabilistic":
        approach = "naiveBayes"
    elif algorithm == "q_learning":
        approach = "Q-Learning Algorithm"
    randomisation = {
            "calendar": randomisation_calendar,
            "test_options_across_segment": randomisation_test_options_across_segment,
            "processing_count": randomisation_processing_count,
            "discount_factor": randomisation_discount_factor,
            "batch": randomisation_batch,
            "prior_fail_reward": randomisation_prior_fail_reward,
            "approach": approach,
            "cross_segment_epsilon": randomisation_cross_segment_epsilon,
            "success_reward": randomisation_success_reward,
            "interaction_count": randomisation_interaction_count,
            "epsilon": randomisation_epsilon,
            "prior_success_reward": randomisation_prior_success_reward,
            "fail_reward": randomisation_fail_reward,
            "max_reward": randomisation_max_reward,
            "cache_duration": randomisation_cache_duration,
            "processing_window": randomisation_processing_window,
            "random_action": randomisation_random_action,
            "decay_gamma": randomisation_decay_gamma,
            "learning_rate": randomisation_learning_rate,
            "missing_offers": randomisation_missing_offers,
            "training_data_source": randomisation_training_data_source
        }
    config_doc["randomisation"] = randomisation
  
    config_doc["lookup_fields"] = []
    if virtual_variables is not None:
        config_doc["virtual_variables"] = virtual_variables
    else:
        config_doc["virtual_variables"] = []
    
    properties_list = [
        {"uuid":config_doc["uuid"], "type":"dynamic_engagement", "name":"dynamic_engagement", "database":"mongodb", "db":config_doc["score_database"], "table":config_doc["score_collection"], "update":True}
        ,{"uuid":config_doc["uuid"], "type":"dynamic_engagement_options", "name":"dynamic_engagement", "database":"mongodb", "db":config_doc["options_store_database"], "table":config_doc["options_store_collection"], "update":True}
    ]
    config_doc["properties"] = "predictor.corpora={}".format(json.dumps(properties_list))

    if create_covering_index:
        covering_index_projection = {"_id":0,"uuid":1,"optionKey":1,"alpha":1,"beta":1}
        if contextual_variables_contextual_variable_one_name != "":
            covering_index_projection["contextual_variable_one"] = 1
        if contextual_variables_contextual_variable_two_name != "":
            covering_index_projection["contextual_variable_two"] = 1
        if dynamic_eligibility is not None:
            if "options_store_fields" in dynamic_eligibility:
                projection_fields = []
                for table_iter in dynamic_eligibility["options_store_fields"]:
                    for field_iter in table_iter["fields"]:
                        projection_fields.append(field_iter)
                    index_fields = set(projection_fields)
                    for ind_field_iter in index_fields:
                        covering_index_projection[ind_field_iter] = 1
            dynamic_eligibility["projection"] = [covering_index_projection]
        else:
            dynamic_eligibility = {}
            dynamic_eligibility["projection"] = [covering_index_projection]

    if dynamic_eligibility is not None:
        config_doc["dynamic_eligibility"] = dynamic_eligibility

    if replace:
        if len([d for d in existing_configurations["data"] if d["name"] == name]) > 0:
            cp.delete_pulse_responder_dynamic(auth,score_database,score_collection,{"name":name})
        
        dme.add_documents(auth, {"database": config_doc["score_database"], "collection": config_doc["score_collection"], "document": config_doc})
        doc_delete = {
            "database": config_doc["options_store_database"]
            ,"collection": config_doc["options_store_collection"]
        }
        dme.delete_all_documents(auth, doc_delete)

    cp.save_pulse_responder_dynamic(auth, config_doc)

    cp_update_doc = {
        "type":"generateUpdatedOptions"
        ,"name":config_doc["name"]
        ,"uuid":config_doc["uuid"]
        ,"engagement_type":"binaryThompson"
        ,"feature_store_database":config_doc["feature_store_database"]
        ,"feature_store_collection":config_doc["feature_store_collection"]
        ,"contextual_variable_one_values":contextual_variable_one_values
        ,"contextual_variable_two_values":contextual_variable_two_values
        ,"contextual_variable_one_name":config_doc["contextual_variables"]["contextual_variable_one_name"]
        ,"contextual_variable_two_name":config_doc["contextual_variables"]["contextual_variable_two_name"]
        ,"contextual_variable_one_from_data_source":config_doc["contextual_variables"]["contextual_variable_one_from_data_source"]
        ,"contextual_variable_two_from_data_source":config_doc["contextual_variables"]["contextual_variable_two_from_data_source"]
        ,"contextual_variable_one_lookup":config_doc["contextual_variables"]["contextual_variable_one_lookup"]
        ,"contextual_variable_two_lookup":config_doc["contextual_variables"]["contextual_variable_two_lookup"]
        ,"offer_key":config_doc["contextual_variables"]["offer_key"]
        ,"tracking_key":config_doc["contextual_variables"]["tracking_key"]
        ,"options_store_database":config_doc["options_store_database"]
        ,"options_store_collection":config_doc["options_store_collection"]
        ,"prior_success_reward":config_doc["randomisation"]["prior_success_reward"]
        ,"prior_fail_reward":config_doc["randomisation"]["prior_fail_reward"]
        ,"take_up":config_doc["contextual_variables"]["take_up"]
        ,"dynamic_eligibility":config_doc["dynamic_eligibility"]
    }
    cp.update_client_pulse_responder(auth, cp_update_doc)

    if dynamic_eligibility is not None:
        if "options_store_fields" in dynamic_eligibility:
            for table_iter in dynamic_eligibility["options_store_fields"]:
                if table_iter["datasource"] == "mongodb":
                    dme.create_document_collection_index(auth, table_iter["database"], table_iter["collection"], {table_iter["lookup_keys"]["foreignField"]:1})
                    lookup_dict = {"$lookup":{
                        "localField":table_iter["lookup_keys"]["localField"]
                        ,"foreignField":table_iter["lookup_keys"]["foreignField"]
                        ,"from":table_iter["collection"]
                        ,"as":"subs"
                    }}
                    add_dict = {"$addFields":{}}
                    for field_iter in table_iter["fields"]:
                        add_dict["$addFields"][field_iter] = {"$arrayElemAt":[f"$subs.{field_iter}",0]}
                    table_pipeline = [
                        lookup_dict
                        ,add_dict
                        ,{"$unset":"subs"}
                        #TODO: allow for different databases once mongo version increments
                        ,{"$out":config_doc["options_store_collection"]}
                    ]
                    dme.post_mongo_db_aggregate_pipeline(auth,
                                                         {
                                                             "database": config_doc["options_store_database"]
                                                             , "collection": config_doc["options_store_collection"]
                                                             , "pipeline": table_pipeline
                                                         }
                                                         )
                elif table_iter["datasource"] == "cassandra":
                    data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(table_iter["collection"]))
                    if data_check["data"] == []:
                        print("WARNING: It looks like {} is empty or does not exist".format(table_iter["collection"]))
                    else:
                        sql = "SELECT * FROM {}".format(table_iter["collection"])
                        col = "temp_options_store_lookup"
                        db = config_doc["options_store_database"]
                        dme.get_cassandra_to_mongo(auth, db, col, sql)
                        dme.create_document_collection_index(auth, db, col, {table_iter["lookup_keys"]["foreignField"]:1})
                        lookup_dict = {"$lookup":{
                            "localField":table_iter["lookup_keys"]["localField"]
                            ,"foreignField":table_iter["lookup_keys"]["foreignField"]
                            ,"from":col
                            ,"as":"subs"
                        }}
                        add_dict = {"$addFields":{}}
                        for field_iter in table_iter["fields"]:
                            add_dict["$addFields"][field_iter] = {"$arrayElemAt":[f"$subs.{field_iter}",0]}
                        table_pipeline = [
                            lookup_dict
                            ,add_dict
                            ,{"$unset":"subs"}
                            #TODO: allow for different databases once mongo version increments
                            ,{"$out":config_doc["options_store_collection"]}
                        ]
                        print(table_pipeline)
                        dme.post_mongo_db_aggregate_pipeline(auth,
                                                             {
                                                                 "database": config_doc["options_store_database"]
                                                                 , "collection": config_doc["options_store_collection"]
                                                                 , "pipeline": table_pipeline
                                                             }
                                                             )

    if create_options_index:
        index_dict = {"uuid":1,"optionKey":1}
        if contextual_variables_contextual_variable_one_name != "":
            index_dict["contextual_variable_one"] = 1
        if contextual_variables_contextual_variable_one_name != "":
            index_dict["contextual_variable_two"] = 1
        index_fields = []
        if dynamic_eligibility is not None:
            if "options_store_fields" in dynamic_eligibility:
                for table_iter in dynamic_eligibility["options_store_fields"]:
                    for field_iter in table_iter["fields"]:
                        index_fields.append(field_iter)
        index_fields = set(index_fields)
        for ind_field_iter in index_fields:
            index_dict[ind_field_iter] = 1
        if create_covering_index:
            index_dict["alpha"] = 1
            index_dict["beta"] = 1
        dme.create_document_collection_index(auth, config_doc["options_store_database"], config_doc["options_store_collection"], index_dict)

    print("MESSAGE: Online learning configuration created")
    return config_doc["uuid"]