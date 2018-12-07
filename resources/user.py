from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt import JWT, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import common.settings as cfg
from common.logging_module import get_logger
import models.user
import sys
import datetime
import uuid
import json

logger = get_logger('user')

class UserTenancy(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('lastname',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('role_name',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('email_address',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('company_name',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('designation',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('tenancy_name',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('mobile_num',
        type=str,
        required=False,
        help="This field can be blank."
    )

    def post(self):
        data = UserTenancy.parser.parse_args()
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "unable to connect to DB"), 400
        cursor = db.cursor()
        tenancy_uid=str(uuid.uuid4())
        user_uid=str(uuid.uuid4())
        try:
           tenancy_query = 'insert into corp_tenancy_tab values(%s,%s,%s,%s)'
           cursor.execute(tenancy_query, (tenancy_uid,data['tenancy_name'],datetime.datetime.now(),data['company_name'],))
           db.commit()
           tenancy_user_query = 'insert into corp_tenancy_user_tab values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
           encrypted_password=hashed_password = generate_password_hash(data['password'])
           cursor.execute(tenancy_user_query, (user_uid,data['firstname'],data['lastname'],data['email_address'],encrypted_password,data['role_name'],datetime.datetime.now(),datetime.datetime.now(),data['designation'],tenancy_uid,data['mobile_num'],))
           db.commit()
           db.close()
        except:
           return("message", "Unable to Create user!, Please try Again"), 400

        return("message", "Tenancy Craeted  and User registerted sucessfully"), 201


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('lastname',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('email_address',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('designation',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('role_name',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('mobile_num',
        type=str,
        required=False,
        help="This field can be blank."
    )
    parser.add_argument('tenancy_id',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    @jwt_required()
    def post(self):
        print("I am in userregisteration class")
        data = UserRegister.parser.parse_args()
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "unable to connect to DB"), 400
        cursor = db.cursor()
        print(data)
        try:
            query = 'insert into corp_tenancy_user_tab values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            encrypted_password=hashed_password = generate_password_hash('welcome1')
            cursor.execute(query, (str(uuid.uuid4()),data['firstname'],data['lastname'],data['email_address'],encrypted_password,data['role_name'],datetime.datetime.now(),datetime.datetime.now(),data['designation'],data['tenancy_id'],data['mobile_num'],))
            db.commit()
        except:
            logger.error('Error : Unexpected error: Error during the user registeration!')
            return("message", "Unable to Register user! Erro Occurred"), 400
        db.close()
        return("message", "User created Sucessfully"), 201

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        parser.add_argument('querytype', type=str, required=True)
        data = parser.parse_args()
        print(data)
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "Unable to connect to DB"), 400
        cursor = db.cursor()
        if data['querytype'] == 'cookie':
            query = "select designation,first_name,last_name,email_id,role,tenancy_id from corp_tenancy_user_tab where upper(email_id)=%s"
            argument = data['username'].upper()
            print(argument)
        elif data['querytype'] == 'userreport':
            query = "select user_uid,designation,first_name,last_name,email_id,role,mobile_num from corp_tenancy_user_tab where tenancy_id=%s"
            argument = data['tenancy_id']
        else:
           query = "select a.user_uid,a.designation,a.first_name,a.last_name,a.email_id,a.role,b.tenancy_name from corp_tenancy_user_tab a, corp_tenancy_tab b where a.tenancy_id=b.tenancy_id and b.tenancy_id=%s"
        cursor.execute(query,argument)
        row_headers = [x[0] for x in cursor.description]
        userdata = cursor.fetchall()
        json_data=[]
        for result in userdata:
            json_data.append(dict(zip(row_headers,result)))
        db.close()
        print(json.dumps(json_data))
        return json.dumps(json_data)

class QuestionSet(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('qset_name', type=str, required=False)
        parser.add_argument('qset_title', type=str, required=False)
        parser.add_argument('qset_thankyou_text', type=str, required=False)
        parser.add_argument('qset_intro_text', type=str, required=False)
        parser.add_argument('timeonperpage', type=str, required=False)
        parser.add_argument('maxtimetofinish', type=str, required=True)
        parser.add_argument('showtimepanel', type=str, required=False)
        parser.add_argument('showprogbar', type=str, required=False)
        parser.add_argument('poll_or_quiz', type=str, required=False)
        parser.add_argument('qset_status', type=str, required=False)
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('updated_by', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        data = parser.parse_args()
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "unable to connect to DB"), 400
        cursor = db.cursor()
        print(data)
        try:
            query = 'insert into eba_quiz_question_sets values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(query, (str(uuid.uuid4()),data['poll_or_quiz'],data['qset_intro_text'],data['qset_thankyou_text'],data['qset_status'],data['tenancy_id'],data['qset_name'],data['qset_title'],data['timeonperpage'],data['maxtimetofinish'],data['showtimepanel'],data['showprogbar'],data['created_by'],data['updated_by'],datetime.datetime.now(),datetime.datetime.now(),))
            db.commit()
        except pymysql.InternalError as error:
            code, message = error.args
            logger.error('Error : Unexpected error: Error during the QuestionSet Creation!')
            print('Got error {!r}' + ' ' + code + ' ' + error) 
            return("message", "Error Occurred during Question Set Creattion! Please Try Again"), 400
        db.close()
        return("message", "Question Set Created Sucessfully"), 201

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        parser.add_argument('querytype', type=str, required=True)
        data = parser.parse_args()
        print(data)
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "Unable to connect to DB"), 400
        cursor = db.cursor()
        if data['querytype'].lower() == 'recruiter':
            query = "select qset_id,qset_intro_text,qset_thankyou_text,qset_name,qset_title,timeonperpage,maxtimetofinish,created_by from eba_quiz_question_sets where upper(created_by)=%s and tenancy_id=%s"
            argument1 = data['created_by'].upper()
            argument2 = data['tenancy_id'].upper()
            args = (argument1,argument2)
            cursor.execute(query,args)
            print(argument1)
        elif data['querytype'].lower() == 'admin':
            query = "select qset_id,qset_intro_text,qset_thankyou_text,qset_name,qset_title,timeonperpage,maxtimetofinish,created_by from eba_quiz_question_sets where tenancy_id=%s"
            argument = data['tenancy_id']
            cursor.execute(query,argument)
        else:
           query = "select qset_id,poll_or_quiz,qset_intro_text,qset_thankyou_text,qset_name,qset_title,timeonperpage,maxtimetofinish,created_by from eba_quiz_question_sets where 1=2"
           cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        userdata = cursor.fetchall()
        json_data=[]
        for result in userdata:
            json_data.append(dict(zip(row_headers,result)))
        db.close()
        print(json.dumps(json_data))
        return json.dumps(json_data)

class QuizQuestion(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('qset_id', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        parser.add_argument('question', type=str, required=False)
        parser.add_argument('question_type', type=str, required=False)
        parser.add_argument('publish_yn', type=str, required=True)
        parser.add_argument('corect_answer', type=str, required=False)
        parser.add_argument('answer01', type=str, required=False)
        parser.add_argument('answer02', type=str, required=False)
        parser.add_argument('answer03', type=str, required=False)
        parser.add_argument('answer04', type=str, required=False)
        parser.add_argument('answer05', type=str, required=False)
        parser.add_argument('answer06', type=str, required=False)
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('updated_by', type=str, required=False)
        data = parser.parse_args()

        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "unable to connect to DB"), 400
        cursor = db.cursor()
        print(data)
        try:
            query = 'insert into eba_quiz_questions values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(query, (str(uuid.uuid4()),data['qset_id'],data['tenancy_id'],data['question'],data['question_type'],data['publish_yn'],data['corect_answer'],data['answer01'],data['answer02'],data['answer03'],data['answer04'],data['answer05'],data['answer06'],data['created_by'],data['updated_by'],datetime.datetime.now(),datetime.datetime.now(),1,))
            db.commit()
        except pymysql.InternalError as error:
            code, message = error.args
            logger.error('Error : Unexpected error: Error during the QuestionSet Creation!')
            print('Got error {!r}' + ' ' + code + ' ' + error)
            return("message", "Error Occurred during Question Set Creattion! Please Try Again"), 400
        db.close()
        return("message", "Quiz question Created Sucessfully"), 201

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        parser.add_argument('querytype', type=str, required=False)
        parser.add_argument('qset_id', type=str, required=False)
        data = parser.parse_args()
        print(data)
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "Unable to connect to DB"), 400
        cursor = db.cursor()
        if data['querytype'].lower() == 'recruiter':
            query = "select question_id,qset_id,question,corect_answer,answer01,answer02,answer03,answer04,answer05,answer06,created_by from eba_quiz_questions where created_by=%s and tenancy_id=%s and qset_id=%s"
            argument1 = data['created_by'].upper()
            argument2 = data['tenancy_id']
            argument3 = data['qset_id']
            args = (argument1, argument2, argument3)
            print(argument1)
            cursor.execute(query,args)
        elif data['querytype'].lower() == 'admin':
            try:
            	query = "select question_id,qset_id,question,corect_answer,answer01,answer02,answer03,answer04,answer05,answer06,created_by from eba_quiz_questions where tenancy_id=%s and qset_id=%s"
	        argument1 = data['tenancy_id']
                argument2 = data['qset_id']  
                args = (argument1, argument2)
                print(argument2)          
	        cursor.execute(query,args)
            except pymysql.InternalError as error:
                code, message = error.args
                logger.error('Error : Unexpected error: Error during the QuestionSet Creation!')
                print('Got error {!r}' + ' ' + code + ' ' + error)
                return("message", "Error Occurred during Question Set Creattion! Please Try Again"), 400
        else:
            query = "select question_id,qset_id,question,question_type,publish_yn,corect_answer,answer01,answer02,answer03,answer04,answer05,answer06,created_by,updated_by from eba_quiz_questions where 1=2"
            cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        userdata = cursor.fetchall()
        json_data=[]
        for result in userdata:
            json_data.append(dict(zip(row_headers,result)))
        db.close()
        print(json.dumps(json_data))
        return json.dumps(json_data)

class QsetResult(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('qset_id', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        parser.add_argument('ip_address', type=str, required=False)
        parser.add_argument('client_id', type=str, required=False)
        parser.add_argument('validation_error', type=str, required=True)
        parser.add_argument('score_percent', type=str, required=False)
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('updated_by', type=str, required=False)
        data = parser.parse_args()

        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "unable to connect to DB"), 400
        cursor = db.cursor()
        print(data)
        try:
            query = 'insert into eba_quiz_results values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(query, (str(uuid.uuid4()),data['qset_id'],data['tenancy_id'],data['ip_address'],data['client_id'],data['validation_error'],data['score_percent'],data['created_by'],datetime.datetime.now(),data['updated_by'],datetime.datetime.now(),))
            db.commit()
        except:
            logger.error('Error : Unexpected error: Error during the user registeration!')
            return("message", "Unable to Register user! Erro Occurred"), 400
        db.close()
        return("message", "User created Sucessfully"), 201

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        parser.add_argument('querytype', type=str, required=True)
        data = parser.parse_args()
        print(data)
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "Unable to connect to DB"), 400
        cursor = db.cursor()
        if data['querytype'] == 'recruiter':
            query = "select result_id,qset_id,tenancy_id,ip_address,validation_error,score_percent,created_by,updated_by from eba_quiz_results where upper(created_by)=%s and tenancy_id=%s"
            argument1 = data['created_by'].upper()
            argument2 = data['tenancy_id']
            print(argument1)
            cursor.execute(query,argument1,argument2)
        elif data['querytype'] == 'admin':
            query = "select result_id,qset_id,tenancy_id,ip_address,validation_error,score_percent,created_by,updated_by from eba_quiz_results where tenancy_id=%s"
            argument = data['tenancy_id']
            cursor.execute(query,argument)
        else:
           query = "select result_id,qset_id,tenancy_id,ip_address,validation_error,score_percent,created_by,updated_by from eba_quiz_results where 1=2"
           cursor.execute(query,argument)
        row_headers = [x[0] for x in cursor.description]
        userdata = cursor.fetchall()
        json_data=[]
        for result in userdata:
            json_data.append(dict(zip(row_headers,result)))
        db.close()
        print(json.dumps(json_data))
        return json.dumps(json_data)

class ResultDetail(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('result_id', type=str, required=False)
        parser.add_argument('question_id', type=str, required=False)
        parser.add_argument('answer01', type=str, required=False)
        parser.add_argument('answer_correct_yn', type=str, required=False)
        parser.add_argument('answer_id_01', type=str, required=True)
        parser.add_argument('score', type=str, required=False)
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('updated_by', type=str, required=False)
        data = parser.parse_args()

        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "unable to connect to DB"), 400
        cursor = db.cursor()
        print(data)
        try:
            query = 'insert into eba_quiz_result_details values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(query, (str(uuid.uuid4()),data['result_id'],data['question_id'],data['answer01'],data['answer_correct_yn'],'none',data['score'],data['created_by'],datetime.datetime.now(),data['updated_by'],datetime.datetime.now(),))
            db.commit()
        except:
            logger.error('Error : Unexpected error: Error during the user registeration!')
            return("message", "Unable to Register user! Erro Occurred"), 400
        db.close()
        return("message", "User created Sucessfully"), 201

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('created_by', type=str, required=False)
        parser.add_argument('tenancy_id', type=str, required=False)
        parser.add_argument('querytype', type=str, required=True)
        data = parser.parse_args()
        print(data)
        try:
            db = pymysql.connect(cfg.MYSQL_HOSTNAME, user=cfg.MYSQL_USERNAME, passwd=cfg.MYSQLDB_PASSWORD, db=cfg.MYSQL_DB_NAME, connect_timeout=5)
        except:
            logger.error("Error : Unexpected error: Could not connect to MySql instance")
            return("message", "Unable to connect to DB"), 400
        cursor = db.cursor()
        if data['querytype'] == 'recruiter':
            query = "select result_detail_id,result_id,question_id,answer01,answer_correct_yn,score,created_by,created_on,updated_on,updated_by where upper(created_by)=%s and tenancy_id=%s"
            argument1 = data['username'].upper()
            argument1 = data['tennacy_id']
            print(argument1)
            cursor.execute(query,argument1,argument2)
        elif data['querytype'] == 'userreport':
            query = "select result_detail_id,result_id,question_id,answer01,answer_correct_yn,score,created_by,created_on,updated_on,updated_by where tenancy_id=%s"
            argument = data['tenancy_id']
            cursor.execute(query,argument)
        else:
           query = "select result_detail_id,result_id,question_id,answer01,answer_correct_yn,score,created_by,created_on,updated_on,updated_by where 1=2"
           cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        userdata = cursor.fetchall()
        json_data=[]
        for result in userdata:
            json_data.append(dict(zip(row_headers,result)))
        db.close()
        print(json.dumps(json_data))
        return json.dumps(json_data)
