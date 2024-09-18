import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json
import sqlite3
import streamlit.components.v1 as components
from PIL import Image

# #configuration 
# st.set_page_config(
#     page_title="EIU Volleyball",
#     page_icon=":chart_with_upwards_trend:"
# )


# connecting database
conn = sqlite3.connect("eiu2024.db", check_same_thread=False)

cn = conn.cursor()

# # creating DF
df1 = pd.read_sql_query('select * from eiu24_game', conn)

##########__________________INPUT number___________________
df = df1[df1['game_number'] == 6]
##########__________________INPUT number___________________

df_dumm = pd.read_sql_query('select * from eiu24_win_dummy', conn)

# total serving rallies
df_serve = df[df['skill']== 'Serve']

# receive all
df_recep = df[df['skill']== 'Reception']

##########__________________INPUT COLORS___________________
#teams variable
v_name = 'Bradley'
h_name = 'EIU' 
##########__________________INPUT COLORS___________________

# colors by team
color_h = 'blue'
color_v = 'cyan'


# total set played
set = df['set_number'].iloc[-1]

# defining the team winner and loser
def winner(set):
    if set == 3 and (df['home_team_score'].iloc[-1] > df['visiting_team_score'].iloc[-1]):
        return(f"{h_name} win 3-0 vs {v_name}")
    elif set == 3 and (df['visiting_team_score'].iloc[-1] > df['home_team_score'].iloc[-1]):
        return(f"{v_name} win 3-0 vs {h_name}")
    elif set == 4 and (df['home_team_score'].iloc[-1] > df['visiting_team_score'].iloc[-1]):
        return(f"{h_name} win 3-1 vs {v_name}")
    elif set == 4 and (df['visiting_team_score'].iloc[-1] > df['home_team_score'].iloc[-1]):
        return(f"{v_name} win 3-1 vs {h_name}")
    elif set == 5 and (df['home_team_score'].iloc[-1] > df['visiting_team_score'].iloc[-1]):
        return(f"{h_name} win 3-2 vs {v_name}")
    else:
        return(f"{v_name} win 3-2 vs {h_name}")
win_team = winner(set)


# st.subheader("Match 1 from Non Conference Season")

st.subheader(f"{win_team} | non-conference | season 2024")
st.write("\n\n\n\n\n\n\n\n")





# image = Image.open("charts/eiu1_point_seq_set1.png")
# st.image(image, caption="set 1", use_column_width=True)




# group by df_all
grouped_df_all = df.groupby(['year', 'season', 'date', 'game_number','team', 'player_number', 'player_name', 'point_won_by', 'skill', 'evaluation_code', 'home_setter_row', 'visiting_setter_row', 'set_number', 'setter_row']).size().reset_index(name='count')
# dumm_sql = pd.read_sql_query('select * from eiu24_win_dummy where team = 'EIU', conn)

# grouped_serv_all
grouped_serv_all = df_serve.groupby(['year', 'season', 'date', 'game_number','team', 'player_number', 'player_name', 'point_won_by', 'evaluation_code', 'home_setter_row', 'visiting_setter_row', 'set_number', 'setter_row']).size().reset_index(name='count')

#grouped_rec_all
grouped_rec_all = df_recep.groupby(['year', 'season', 'date', 'game_number','team', 'player_number', 'player_name', 'point_won_by', 'evaluation_code', 'home_setter_row', 'visiting_setter_row', 'set_number', 'setter_row']).size().reset_index(name='count')

# variable for grouped DF All
dumm_all = grouped_df_all[grouped_df_all['team']== h_name]

# grouped_rows_h
grouped_rows_h = df_serve.groupby(['year', 'season', 'date', 'game_number','team', 'home_team_id', 'home_team', 'home_setter_row', 'set_number', 'home_p1','home_p6', 'home_p5', 'home_p4', 'home_p3', 'home_p2', 'point_won_by'])['point_won_by'].size().reset_index(name='count')


# DF by teams
df_h = df[df['team'] == h_name]
df_v = df[df['team'] == v_name]






 # slicers
# player_n = dumm_all['player_name'].unique()
# sel_player = st.multiselect("player_name", options=player_n, default=player_n)

# skill = dumm_all['skill'].unique()
# sel_skill = st.multiselect("skill", options=skill, default=skill)

# win_point = dumm_all['point_won_by'].unique()
# sel_win =st.multiselect("point_won_by", options=win_point, default=win_point)

# filtered the slicers
# filtered_df = dumm_all.loc[
    # (dumm_all["player_name"] == sel_player) & (dumm_all["skill"] == sel_skill) & (dumm_all["point_won_by"] == sel_win)]

#dataframe with filtered
# st.dataframe(dumm_all, use_container_width=True)

# ___________________________________________________________________________________________
    












# color map_______________________________________________________________________________________
st.divider()
color_map = {f'{h_name}': 'blue', 
             f'{v_name}': 'cyan'}

color_mapp = {
    1 : '#FF0000',  # Set 1 - Red
    2 : '#4682B4',  # Set 2 - Blue
    3 : '#32CD32',   # Set 3 - Green
    4 : '#FFA500',  # Set 4 orange
    5 : '#FFFF00', #set 5 - yellow
}

# '#00FFFF', cyan
# '#4682B4', 'Blue

 # plotly point seequence_______________________________________________________________________

# set 1 points sequence
# st.subheader("Points sequence")

fig_line_p = px.line(df, x="home_team_score", y="visiting_team_score", color="set_number",  
                         color_discrete_map=color_mapp,
                     labels={"set_number": "Set Number"}) 
fig_line_p.update_traces(textposition="bottom right", mode="markers+lines", marker=dict(size=10, line=dict(width=1)))

fig_line_p.update_layout(
        autosize=False,
        width=700,
        height=700,
        title=dict(
            text=f"{h_name} vs {v_name} Points Sequence by Set",
            font=dict(size=20, color='#000000'),
            x=0.17,
            y=0.9
        ),
        xaxis_title=dict(text=h_name, font=dict(size=16)),
        yaxis_title=dict(text=v_name, font=dict(size=16)),
        plot_bgcolor='rgb(200, 255, 255)',
        xaxis=dict(tickfont=dict(size=14, color='#000000')),
        yaxis=dict(tickfont=dict(size=14, color='#000000')),
        legend=dict(x=1.05, y=.5, orientation='v', font=dict(color='#000000')),
        margin=dict(l=50, r=10, t=100, b=50),
        shapes=[
            dict(
                type= 'line',
                yref= 'y', y0=-0, y1= 25,
                xref= 'x', x0=-0, x1= 25
            ),
            
        ])
st.plotly_chart(fig_line_p)


# Serving histogram serving team all match                 
# .update_xaxes(categoryorder='total descending')
# fig_diff_serv = px.histogram(diff_serv, x="Diff", text_auto=True, color="serving_team", color_discrete_sequence=[color_h, color_v], width=600)
# fig_diff_serv.layout.title = 'Serve all match by Team'

# fig_diff_serv = px.histogram(diff_serv,
#                    title="Histogram of Difference in Serve",
#                    x="Diff",
#                    y="home_setter_row"
#                    )
# st.plotly_chart(fig_diff_serv)


# Chart Home sideout by rows______________________________________________________________________

fig_row_serve_h = px.line(df, x="visiting_team_score", y="home_setter_row", color="set_number",
                 color_discrete_map=color_mapp,
                     labels={"set_number": "Set Number"}) 
fig_row_serve_h.update_traces(textposition="bottom right", mode="markers+lines", marker=dict(size=15, line=dict(width=1)))


fig_row_serve_h.update_layout(
        autosize=False,
        width=800,
        height=400,
        title=dict(
            text=(f"{h_name} sideout vs {v_name}`s serve by Row"),
            font=dict(size=20, color='#000000'),
            x=0.20,
            y=0.85
        ),
        xaxis_title=dict(text=(f"{v_name} Points"), font=dict(size=16)),
        yaxis_title=dict(text=(f"{h_name} Sideout by Rows"), font=dict(size=16)),
        plot_bgcolor='rgb(200, 255, 255)',
        xaxis=dict(tickfont=dict(size=14, color='#000000')),
        yaxis=dict(tickfont=dict(size=14, color='#000000')),
        legend=dict(x=1.05, y=.5, orientation='v', font=dict(color='#000000')),
        margin=dict(l=40, r=10, t=100, b=50)
        )

st.plotly_chart(fig_row_serve_h)



# Home serving difference by Home ROWS _____________________________________________________________
st.write(F"Serving by {h_name} Rows vs {v_name} Rows")
pivot_all_serve_h = df_serve.pivot_table("skill", index="home_setter_row", columns="serving_team", aggfunc="count")
pivot_all_serve_h['Diff'] = pivot_all_serve_h[f"{h_name}"]-pivot_all_serve_h[f"{v_name}"]
diff_serv = pivot_all_serve_h['Diff']
st.dataframe(pivot_all_serve_h)

# Chart Home Serve by rows____________________________________________________________________


fig_row_rec_h = px.line(df, x="home_team_score", y="home_setter_row", color="set_number",
                 color_discrete_map=color_mapp,
                     labels={"set_number": "Set Number"}) 
fig_row_rec_h.update_traces(textposition="bottom right", mode="markers+lines", marker=dict(size=15, line=dict(width=1)))


fig_row_rec_h.update_layout(
        autosize=False,
        width=800,
        height=400,
        title=dict(
        text=(f"{h_name} serve vs {v_name}`s sideout by Row"),
            font=dict(size=20, color='#000000'),
            x=0.20,
            y=0.85
        ),
        xaxis_title=dict(text=(f"{h_name} Points"), font=dict(size=16)),
        yaxis_title=dict(text=(f"{h_name} Serving by Rows"), font=dict(size=16)),
        plot_bgcolor='rgb(200, 255, 255)',
        xaxis=dict(tickfont=dict(size=14, color='#000000')),
        yaxis=dict(tickfont=dict(size=14, color='#000000')),
        legend=dict(x=1.05, y=.5, orientation='v', font=dict(color='#000000')),
        margin=dict(l=40, r=10, t=100, b=50)
        )

st.plotly_chart(fig_row_rec_h)
# st.subheader(f"{h_name} serve vs {v_name}`s sideout by Row")

# sunburst by rotation____________________________________________________________________________

fig_rot_h_row = px.sunburst(grouped_rows_h,
                  path=['home_team', 'home_setter_row', 'point_won_by', 'home_p1', 'home_p6', 'home_p5', 'home_p4', 'home_p3', 'home_p2'],
                  values='count',
                  title= f"{h_name} Setter In & players positions",
                  width=800, 
                  height=800,
                  color='point_won_by',
                color_discrete_sequence=[color_h, color_v]
                       )
st.plotly_chart(fig_rot_h_row, )

# Skills ____________________________________________________________________________

st.divider()

# HOME skills by player
st.subheader("Touches and Win Percent")
skill_h = (
    df_h
    .groupby(['player_name'])
    .agg(touches=('skill', 'count'),
        win=('point_won_by', lambda x: x.eq(f"{h_name}").sum(skipna=True)),
        win_pct=('point_won_by', lambda x: round((x.eq(f'{h_name}').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='win_pct', ascending=False)
    .reset_index(drop=True)
    # .to_string()
)
# Convert to string for printing
st.dataframe(skill_h, use_container_width=True)



# HOME hitting by players
st.subheader("Attack and Win Percent")
hitting_h = (
    df_h[df_h['skill'] == 'Attack']
    .groupby(['player_name', 'skill'])
    .agg(Att=('skill', 'count'),
         K=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         pos=('evaluation_code', lambda x: x.eq('+').sum(skipna=True)),
         ret=('evaluation_code', lambda x: x.eq('!').sum(skipna=True)),
         neg=('evaluation_code', lambda x: x.eq('-').sum(skipna=True)),
         blk=('evaluation_code', lambda x: x.eq('/').sum(skipna=True)),
         err=('evaluation_code', lambda x: x.eq('=').sum(skipna=True)),
        win=('point_won_by', lambda x: x.eq(f"{h_name}").sum(skipna=True)),
        K_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) / x.count()), 3)),
        win_pct=('point_won_by', lambda x: round((x.eq(f'{h_name}').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='win_pct', ascending=False)
    .reset_index(drop=True)
)
# Convert to string for printing
st.dataframe(hitting_h, use_container_width=True)





# All skills

fig_df_all = px.sunburst(grouped_df_all,
                  path=['team', 'player_name', 'skill', 'point_won_by', 'evaluation_code'],
                  values='count',
                  title="All Skills by Player | Win vs Lost | Receiving quality",
                  width=800, 
                  height=800,
                  color="point_won_by",
                 color_discrete_sequence=[color_h, color_v]
                    )
st.plotly_chart(fig_df_all)

# __________________serve section_________________
st.divider()

# HOME Serve by players
st.subheader("Serve and Win Percent")
serve_h = (
    df_h[df_h['skill'] == 'Serve']
    .groupby(['player_name'])
    .agg(Att=('skill', 'count'),
         ace=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         pos=('evaluation_code', lambda x: x.eq('+').sum(skipna=True)),
         med=('evaluation_code', lambda x: x.eq('!').sum(skipna=True)),
         neg=('evaluation_code', lambda x: x.eq('-').sum(skipna=True)),
         over=('evaluation_code', lambda x: x.eq('/').sum(skipna=True)),
         err=('evaluation_code', lambda x: x.eq('=').sum(skipna=True)),
        win=('point_won_by', lambda x: x.eq(f"{h_name}").sum(skipna=True)),
        ser_pos_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) + x.eq('+').sum(skipna=True) + x.eq('!').sum(skipna=True) + x.eq('/').sum(skipna=True)) / x.count(), 3) if x.count() > 0 else 0),
        win_pct=('point_won_by', lambda x: round((x.eq(f'{h_name}').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='win_pct', ascending=False)
    .reset_index(drop=True)
)
st.dataframe(serve_h, use_container_width=True)



# serve all, player, win-lost, evaluation
fig_df_serv = px.sunburst(grouped_serv_all,
                  path=['team', 'player_name', 'point_won_by', 'evaluation_code'],
                  values='count',
                  title="Serves by Player | Win vs Lost | Serving quality",
                  width=800, 
                  height=800,
                  color="point_won_by",
                 color_discrete_sequence=[color_h, color_v]
                    )
st.plotly_chart(fig_df_serv)



# serve all, set-number, player, win-lost, evaluation
fig_serve_set = px.sunburst(grouped_serv_all,
                  path=['team', 'set_number', 'player_name', 'point_won_by', 'evaluation_code'],
                  values='count',
                  title='Serving Team by Sets| Player serving| Win vs Lost by Team| Serve Quality',
                  width=800, 
                  height=800,
                  color='point_won_by',
                color_discrete_sequence=[color_h, color_v]
                       )
st.plotly_chart(fig_serve_set)

# serve all, row, player, win-lost
fig_serve_row = px.sunburst(grouped_serv_all,
                  path=['team', 'setter_row', 'player_name', 'point_won_by', 'evaluation_code'],
                  values='count',
                  title='Serving Team by Rows| Player serving| Win vs Lost by Team| Serve Quality',
                  width=800, 
                  height=800,
                  color='point_won_by',
                color_discrete_sequence=[color_h, color_v]
                       )
st.plotly_chart(fig_serve_row)


# __________________reception section_________________
st.divider()

# HOME Reception by players
st.subheader("Reception and Win Percent")
rec_h = (
    df_h[df_h['skill'] == 'Reception']
    .groupby(['player_name', 'skill'])
    .agg(Att=('skill', 'count'),
         perf=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         pos=('evaluation_code', lambda x: x.eq('+').sum(skipna=True)),
         med=('evaluation_code', lambda x: x.eq('!').sum(skipna=True)),
         neg=('evaluation_code', lambda x: x.eq('-').sum(skipna=True)),
         over=('evaluation_code', lambda x: x.eq('/').sum(skipna=True)),
         err=('evaluation_code', lambda x: x.eq('=').sum(skipna=True)),
        win=('point_won_by', lambda x: x.eq(f"{h_name}").sum(skipna=True)),
        per_pos_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) + x.eq('+').sum(skipna=True)) / x.count(), 3) if x.count() > 0 else 0),
        win_pct=('point_won_by', lambda x: round((x.eq(f'{h_name}').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='win_pct', ascending=False)
    .reset_index(drop=True)
)
st.dataframe(rec_h, use_container_width=True)


# receive all, player, win-lost, evaluation_code
fig_rec_all = px.sunburst(grouped_rec_all,
                path=['team', 'player_name', 'point_won_by', 'evaluation_code'],
                  values='count',
                  title="Receiving by Team| Player receiving| Win vs Lost| Receiving quality",
                  width=800, 
                  height=800,
                  color="point_won_by",
                 color_discrete_sequence=[color_h, color_v]
                    )      
st.plotly_chart(fig_rec_all, use_container_width=True)


# receive by sets, player, win-lost, evaluation_code
fig_recep_set = px.sunburst(grouped_rec_all,
                  path=['team', 'set_number', 'player_name', 'point_won_by', 'evaluation_code'],
                  values='count',
                  title='Receiving Team by Sets| Player serving| Win vs Lost by Team| Serve Quality',
                  width=800, 
                  height=800,
                  color='point_won_by',
                color_discrete_sequence=[color_h, color_v]
                       )
st.plotly_chart(fig_recep_set, use_container_width=True)


# receive by rows, player, win-lost, evaluation_code
fig_rec_row = px.sunburst(grouped_rec_all,
                  path=['team', 'setter_row', 'player_name', 'point_won_by', 'evaluation_code'],
                  values='count',
                  title='Receiving Team by Rows| Player serving| Win vs Lost by Team| Serve Quality',
                  width=800, 
                  height=800,
                  color='point_won_by',
                color_discrete_sequence=[color_h, color_v]
                       )
st.plotly_chart(fig_rec_row, use_container_width=True)


# _______________________setter, block & defense_____________________________

# HOME Block by players
st.subheader("Block and Win Percent")
block_h = (
    df_h[df_h['skill'] == 'Block']
    .groupby(['player_name'])
    .agg(Att=('skill', 'count'),
         perf=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         pos=('evaluation_code', lambda x: x.eq('+').sum(skipna=True)),
         med=('evaluation_code', lambda x: x.eq('!').sum(skipna=True)),
         neg=('evaluation_code', lambda x: x.eq('-').sum(skipna=True)),
         over=('evaluation_code', lambda x: x.eq('/').sum(skipna=True)),
         err=('evaluation_code', lambda x: x.eq('=').sum(skipna=True)),
        win=('point_won_by', lambda x: x.eq(f"{h_name}").sum(skipna=True)),
        per_pos_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) + x.eq('+').sum(skipna=True) + x.eq('!').sum(skipna=True) + x.eq('-').sum(skipna=True)) / x.count(), 3) if x.count() > 0 else 0),
        win_pct=('point_won_by', lambda x: round((x.eq(f'{h_name}').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='win_pct', ascending=False)
    .reset_index(drop=True)
)
st.dataframe(block_h, use_container_width=True)

# HOME setter by players
st.subheader("Setting and Win Percent")
setter_h = (
    df_h[df_h['skill'] == 'Set']
    .groupby(['player_name'])
    .agg(Att=('skill', 'count'),
         perf=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         pos=('evaluation_code', lambda x: x.eq('+').sum(skipna=True)),
         med=('evaluation_code', lambda x: x.eq('!').sum(skipna=True)),
         neg=('evaluation_code', lambda x: x.eq('-').sum(skipna=True)),
         over=('evaluation_code', lambda x: x.eq('/').sum(skipna=True)),
         err=('evaluation_code', lambda x: x.eq('=').sum(skipna=True)),
        win=('point_won_by', lambda x: x.eq(f"{h_name}").sum(skipna=True)),
        per_pos_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) + x.eq('+').sum(skipna=True)) / x.count(), 3) if x.count() > 0 else 0),
        win_pct=('point_won_by', lambda x: round((x.eq(f'{h_name}').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='win_pct', ascending=False)
    .reset_index(drop=True)

)
st.dataframe(setter_h, use_container_width=True)


# HOME Defense by players
st.subheader("Defense and Win Percent")
dig_h = (
    df_h[df_h['skill'] == 'Dig']
    .groupby(['player_name'])
    .agg(Att=('skill', 'count'),
         perf=('evaluation_code', lambda x: x.eq('#').sum(skipna=True)),
         pos=('evaluation_code', lambda x: x.eq('+').sum(skipna=True)),
         med=('evaluation_code', lambda x: x.eq('!').sum(skipna=True)),
         neg=('evaluation_code', lambda x: x.eq('-').sum(skipna=True)),
         over=('evaluation_code', lambda x: x.eq('/').sum(skipna=True)),
         err=('evaluation_code', lambda x: x.eq('=').sum(skipna=True)),
        win=('point_won_by', lambda x: x.eq(f"{h_name}").sum(skipna=True)),
        per_pos_pct=('evaluation_code', lambda x: round((x.eq('#').sum(skipna=True) + x.eq('+').sum(skipna=True)) / x.count(), 3) if x.count() > 0 else 0),
        win_pct=('point_won_by', lambda x: round((x.eq(f'{h_name}').sum(skipna=True) / x.count()), 3)))
    .reset_index()
    .sort_values(by='win_pct', ascending=False)
    .reset_index(drop=True)
)
st.dataframe(dig_h, use_container_width=True)



# ____________________________________________________________________________________________