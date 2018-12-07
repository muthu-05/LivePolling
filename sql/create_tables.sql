
##### drop tables
drop table eba_quiz_invites;
drop table eba_quiz_result_details;
drop table eba_quiz_results;
drop table eba_quiz_questions;
drop table eba_quiz_question_sets;

#drop table client_tab; 
#drop table corp_tenancy_user_tab;
#drop table corp_tenancy_tab; 
### create corp_cust_tab


########################## create tables ########################

create table `mysql-prod`.`eba_quiz_question_sets` (
  `qset_id` varchar(40) not null,
  `poll_or_quiz` varchar(1) not null,
  `qset_intro_text` varchar(1000) null,
  `qset_thankyou_text` varchar(1000) null,  
  `qset_status` varchar(40),
  `tenancy_id` varchar(40),
  `qset_name` varchar(40),
  `qset_title` varchar(40),
  `timeonperpage` varchar(2),
  `maxtimetofinish` varchar(5),
  `showtimepanel` varchar(1),
  `showprogbar` varchar(1),
  `created_by` varchar(40) null,
  `updated_by` varchar(40) null,
  `created_on` datetime null,
  `updated_on` datetime null,
  primary key (`qset_id`),
  constraint `fk_eba_quiz_question_sets_2`
    foreign key (tenancy_id)
    references `mysql-prod`.`corp_tenancy_tab` (tenancy_id));

create table `mysql-prod`.`eba_quiz_questions` (
  `question_id` varchar(40) not null,
  `qset_id` varchar(40) null,
  `tenancy_id` varchar(40) null,
  `question` varchar(1000) not null,
  `question_type` varchar(30) not null,
  `publish_yn` varchar(1) not null,
  `corect_answer` varchar(1000) null,
  `answer01` varchar(1000) null,
  `answer02` varchar(1000) null,
  `answer03` varchar(1000) null,
  `answer04` varchar(1000) null,
  `answer05` varchar(1000) null,
  `answer06` varchar(1000) null,
  `created_by` varchar(40) null,
  `updated_by` varchar(40) null,
  `created_on` datetime null,
  `updated_on` datetime null,
  `answer_01_score` int null,
  primary key (`question_id`),
  constraint `fk_eba_quiz_question_1`
    foreign key (qset_id)
    references `mysql-prod`.`eba_quiz_question_sets` (qset_id),
  constraint `fk_eba_quiz_question_2`
   foreign key (tenancy_id)
    references `mysql-prod`.`corp_tenancy_tab` (tenancy_id));

create table `mysql-prod`.`eba_quiz_results` (
  `result_id` varchar(40) not null,
  `qset_id` varchar(40) null,
  `tenancy_id` varchar(4) null,
  `ip_address` varchar(255) null,
  `client_id` varchar(40) null,
  `validation_error` varchar(4000) null,
  `score_percent` varchar(3) null,
  `created_by` varchar(45) null,
  `created_on` datetime null,
  `updated_by` varchar(45) null,
  `updated_on` datetime null,
   primary key (`result_id`),
   constraint `fk_eba_quiz_result_question_1`
    foreign key (qset_id)
    references `mysql-prod`.`eba_quiz_question_sets` (qset_id),
   constraint `fk_eba_quiz_result_question_2`
   foreign key (tenancy_id)
    references `mysql-prod`.`corp_tenancy_tab` (tenancy_id));

create table `mysql-prod`.`eba_quiz_result_details` (
  `result_detail_id` varchar(40) not null,
  `result_id` varchar(40) null,
  `question_id` varchar(40) null,
  `answer01` varchar(1000) null,
  `answer_correct_yn` varchar(1) null,
  `answer_id_01` varchar(40) null,
  `score` varchar(100) null,
  `created_by` varchar(45) null,
  `created_on` datetime null,
  `updated_on` datetime null,
  `updated_by` varchar(45) null,
   primary key (`result_detail_id`),
   constraint `fk_quiz_result_details_1`
    foreign key (result_id)
   references `mysql-prod`.`eba_quiz_results` (result_id),
  constraint `fk_quiz_result_details_2`
   foreign key (question_id)
   references `mysql-prod`.`eba_quiz_questions` (question_id)
);

create table `mysql-prod`.`eba_quiz_invites` (
  `invite_id` varchar(40) not null,
  `client_id` varchar(40) null,
  `tenancy_id` varchar(40) null,
  `qset_id`  varchar(40) null,
  `invite_qset_status` varchar(40) null,
  `email_sent` varchar(30) null,
  `email_hist_id` varchar(40) null,
  `created_by` varchar(45) null,
  `created_on` varchar(40) null,
  primary key (`invite_id`),
   constraint `fk_eba_quiz_invite_1`
    foreign key (qset_id)
    references `mysql-prod`.`eba_quiz_question_sets` (qset_id),
  constraint `eba_quiz_invites_2`
    foreign key (tenancy_id)
    references `mysql-prod`.`corp_tenancy_tab` (tenancy_id)
);

create table `mysql-prod`.`corp_tenancy_tab` (
   `tenancy_id` varchar(40) not null,
   `tenancy_name` varchar(40) null,
   `created_on` datetime null,
   `company_name` varchar(40) not null,
    primary key (`tenancy_id`));

create table `mysql-prod`.`corp_tenancy_user_tab` (
  `user_uid` varchar(40) not null,
  `first_name` varchar(40) null,
  `last_name` varchar(40) null,
  `email_id` varchar(40) not null,
  `password` varchar(128) not null,
  `role` varchar(15) not null,
  `created_on` datetime not null,
  `last_login` datetime null,
  `designation` varchar(40) null,
  `tenancy_id` varchar(40) null,
  `mobile_num` varchar(15) null,
  primary key (`user_uid`),
  unique index `email_id_unique` (`email_id` asc) visible,
  constraint `fk_corp_tenancy_user_tab_1`
    foreign key (tenancy_id)
    references `mysql-prod`.`corp_tenancy_tab` (tenancy_id));

#####################################################################
