create table if not exists agent_purchase_sum (agent string,agent_name string,count int);
insert overwrite table agent_purchase_sum select a.agent,b.name,a.count from (select agent,sum(count) as count from tb_purchase group by agent) a left outer join tb_agent b on a.agent = b.agent order by a.count desc;

create table if not exists purchase_month (month string,count int);
insert overwrite table purchase_month select month,sum(count) as count from (select from_unixtime(unix_timestamp(time),'yyyy-MM') as month,count from tb_purchase) a group by a.month;
