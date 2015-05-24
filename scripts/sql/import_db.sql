
create external table if not exists tb_agent (agent string,name string,parent int,ycard int,mcard int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/table/agent';

create external table if not exists tb_org (org string,name string,parent int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/table/org';

create external table if not exists tb_group (gid int,name string,org int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/table/group';


create external table if not exists tb_user (uid int,account string,org int,agent int,type int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/table/user';

create external table if not exists tb_userofgroup (gid int,uid int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/table/userofgroup';


create external table if not exists tb_purchase (time string,agent string,agent_name string,type string,count int) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' location '/echat/table/purchase';
