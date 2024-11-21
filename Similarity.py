from sshtunnel import SSHTunnelForwarder
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os

SSH_KEY = os.environ('SSH_KEY_PINKET')
SSH_USERNAME =  os.environ('SSH_USERNAME-PINKET')
DB_USERNAME = os.environ('DB_USERNAME-PINKET')
DB_PASSWORD =  os.environ('DB_PASSWORD-PINKET')


def db_connection():

    try:
        # Create an SSH tunnel
        tunnel = SSHTunnelForwarder(
            ('91.98.99.106', 12091),
            ssh_username=SSH_USERNAME,
            ssh_password=SSH_KEY,
            remote_bind_address=('localhost', 5432),
            local_bind_address=('localhost', 5433),  # could be any available port
        )
        # Start the tunnel
        tunnel.start()
    except:
        print("SSH Tunnel Failed")
        # os._exit(0)

    try:
        # Create a database connection
        conn = psycopg2.connect(
            database='VShop',
            user=DB_USERNAME,
            password=DB_PASSWORD,
            # host='postgres-replica1.pinket.local',
            # port='5432',
            host='localhost',
            port='5433',

        )
        # Get a database cursor
        cur = conn.cursor()

    except:
        print("Database Connection Failed")
        # os._exit(0)

    return cur


cur = db_connection()

## Retention :
start_date = '2020-01-01'
def retention(start_date, merged, duration):
    # Find Start Month
    m_init = int(start_date[-5:-3])

    # DataFrame of first order in this start date

    merged = merged.loc[:, 1:]
    s = merged.shape[1] // duration
    df = pd.DataFrame()

    for i in range(s):
        y = merged.loc[:, 1 + i * duration: (i + 1) * duration]
        z = y.sum(axis=1)
        df[i] = z

    dataframe = df

# Plot Late Delivery Retention
def plotting(base, problem, label):
    plt.style.use('ggplot')
    plt.plot(((base/base.loc[0,0])*100), label = 'Base')
    plt.plot(((problem/problem.loc[0,0])*100), label= 'Result')
    plt.title(label)
    plt.legend()
    plt.savefig('%s.jpg'%label)
    plt.show()



def query_to_dataframe(query): # Query to Dataframe:
    cur.execute(query)
    dataframe = pd.DataFrame(cur.fetchall())

    return dataframe

#User_history_query :

user_history_query = f"""
with month_order as(
    select c.id id, count(so.id) cnt from vshop.shopping_orders so
inner join vshop.customers c on so.customerid = c.id
where so.status in ('completed','in_progress')
    and so.checkoutdate >= '2020-05-01'and so.checkoutdate < '2021-03-01'
group by 1)

select month_order.id,
       count(distinct case when so.checkoutdate::date >= '2020-05-01'
            and so.checkoutdate::date < '2020-06-01'
            then so.id end),
       count(distinct case when so.checkoutdate::date >= '2020-06-01'
            and so.checkoutdate::date < '2020-07-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2020-07-01'
            and so.checkoutdate::date < '2020-08-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2020-08-01'
            and so.checkoutdate::date < '2020-09-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2020-09-01'
            and so.checkoutdate::date < '2020-10-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2020-10-01'
            and so.checkoutdate::date < '2020-11-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2020-11-01'
            and so.checkoutdate::date < '2020-12-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2020-12-01'
            and so.checkoutdate::date < '2021-01-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2021-01-01'
            and so.checkoutdate::date < '2021-02-01'
            and so.offcode is null then so.id end),
       count(distinct case when so.checkoutdate::date >= '2021-02-01'
            and so.checkoutdate::date < '2021-03-01'
            and so.offcode is null then so.id end)

from month_order
inner join vshop.shopping_orders so on so.customerid = month_order.id
where so.status in ('completed', 'in_progress')
  and month_order.cnt >= 1
group by 1;"""


def user_history(): # History of All users:
    user_history = query_to_dataframe(user_history_query)
    return user_history


def similarity(n, t):
    similarity_query = f"""
with minimum_checkout as (select c.id id, min(so.checkoutdate) from vshop.shopping_orders so
inner join vshop.customers c on so.customerid = c.id
where so.status in ('completed', 'in_progress')
group by 1
having min(so.checkoutdate) >= '2020-05-01'and min(so.checkoutdate) < '2020-06-01'),

 order_count as
(select so.customerid id, count(distinct so.id) cnt
from vshop.shopping_orders so
inner join minimum_checkout mc on mc.id = so.customerid
where so.status in ('completed', 'in_progress')
      and so.checkoutdate::date >= '2020-05-01' and so.checkoutdate::date < '2020-08-01'
group by 1)

select so.customerid, so.checkoutdate, item.id itemid
from vshop.shopping_orders so
inner join vshop.shopping_order_from_branches sofb on so.id = sofb.orderid
inner join order_count oc on oc.id = so.customerid
inner join vshop.order_baskets ob on sofb.orderbasketid = ob.id
inner join vshop.order_basket_items obi on ob.id = obi.basketid
inner join vshop.market_branch_item_infos mbii on obi.marketiteminfoid = mbii.id
inner join vshop.items item on mbii.itemid = item.id
where so.status in ('completed')
and so.checkoutdate >= '2020-05-01' and so.checkoutdate <= '2021-03-01'
and oc.cnt >= {n};
"""
    df_similarity = query_to_dataframe(similarity_query)
    columns = df_similarity.columns
    ids = df_similarity[columns[0]].unique()
    si_ids = []
    percent = []

    for id in ids:

        to_id = df_similarity[df_similarity[columns[0]] == id]
        id_checkouts = to_id[columns[1]].unique()

        #Two First  checkouts:
        p1 = to_id[to_id[columns[1]] == id_checkouts[0]]
        p2 = to_id[to_id[columns[1]] == id_checkouts[1]]
        lm = len(p1.merge(p2, how='inner', on=2))
        lb = len(p1)
        s = lm / lb
        percent.append(s)
        if len(p1.merge(p2, how = 'inner', on = 2)) >= t:
            si_ids.append(id)

    df_si_ids = pd.DataFrame(si_ids)
    ids = pd.DataFrame(ids)
    percent = pd.DataFrame(percent)
    return df_si_ids, ids, percent

user_history = user_history()
similarity, similarity_idbase,similarity_p = similarity(2, 8)
print(similarity_p[0].mean())

# ## Merge:
similarity_result = user_history.merge(similarity, how='inner', on=0)
similarity_base = user_history.merge(similarity_idbase, how='inner', on=0)
#similarity_percent = user_history.merge(similarity_p,how='inner',on=0)
# #
# #Retention :
similarity_result_retention = retention(start_date, similarity_result, 1)
similarity_base_retention = retention(start_date, similarity_base, 1)
# #
plotting(similarity_base_retention,similarity_result_retention, label='Similarity of Items')


