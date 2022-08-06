import dash
from dash import html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import scipy.stats as stats
import plotly.graph_objects as go


fourmarkers_df = pd.read_csv("assets/4_markers_df.csv")
force_df = pd.read_csv("assets/force_df.csv")
fullmarkers_df = pd.read_csv("assets/38_markers_df.csv")
fourmarkers_df["calculation"] = "fourmarkers"
force_df["calculation"] = "force"
fullmarkers_df["calculation"] = "fullmarkers"
new_df = pd.concat([fourmarkers_df, force_df, fullmarkers_df])

columns = fourmarkers_df.columns
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div(["  "], style = {"width":"100px"}),
        html.Div([
            html.H1("Hip markers comparison"),
            html.Img(src = "/assets/4_important.png"),
            html.Br(),
            dcc.RadioItems(
                options = ["1D plot", "2D plot", "3D plot"],
                id = "4-plot-decision",
                value = "3D plot"
            ),
            html.Br(),
            dcc.Dropdown(
                columns,
                ['mean_AP_MOS', 'std_vertical_xCOM', 'std_ML_xCOM'],
                multi=True,
                id = "4-features"
            ),
            html.Br(),
            dcc.Graph(id = "4-plot"),
            html.Br(),
            html.Button("Plot", id = "4-plot-button", style = {'width':'100px', 'height':'50px'})   
        ], style = {"width":"3000px"}),

        html.Div([" "], style = {"width":"100px"}),

        html.Div([
            html.H1("Force features comparison"),
            html.Img(src = "/assets/force_important.png"),
            html.Br(),
            dcc.RadioItems(
                options = ["1D plot", "2D plot", "3D plot"],
                id = "force-plot-decision",
                value = "3D plot"
            ),
            html.Br(),
            dcc.Dropdown(
                columns,
                ['mean_AP_MOS', 'std_vertical_xCOM', 'std_ML_xCOM'],
                multi=True,
                id = "force-features"
            ),
            html.Br(),
            dcc.Graph(id = "force-plot"),
            html.Br(),
            html.Button("Plot", id = "force-plot-button", style = {'width':'100px', 'height':'50px'})      
        ], style = {"width":"3000px"}),

        html.Div([" "], style = {"width":"100px"}),

        html.Div([
            html.H1("38 markers features comparison"),
            html.Img(src = "/assets/38_important.png"),
            html.Br(),
            dcc.RadioItems(
                options = ["1D plot", "2D plot", "3D plot"],
                id = "38-plot-decision",
                value = "3D plot"
            ),
            html.Br(),
            dcc.Dropdown(
                columns,
                ['mean_AP_MOS', 'std_vertical_xCOM', 'std_ML_xCOM'],
                multi=True,
                id = "38-features"
            ),
            html.Br(),
            dcc.Graph(id = "38-plot"),
            html.Br(),
            html.Button("Plot", id = "38-plot-button", style = {'width':'100px', 'height':'50px'})  
        ], style = {"width":"3000px"}),

        html.Div([" "], style = {"width":"100px"}),
    ], style = {"display":"Flex"}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div("", style = {"width":"20px"}),
        html.Div([
            html.H1("Independent t-test"),
            dcc.Dropdown(
                    columns,
                    multi=False,
                    id = "t-test-feature",
                    style = {"width":"250px"}
                ),
            html.Br(),
            html.Div(["t-test"], id = "t-test", style = {"font-size":"25px"}),
            html.Br(),
            html.Button("t-test", id = "t-test-button",style = {"width":"100px", "height":"50px", "font-size":"15px"}),
        ]),
        html.Div([], style = {'width':'10px'}),
        html.Div([], id = "feature-bar-plot", style = {'width':'1000px', 'height':'1000px'})
    ], style = {"display":"flex"})
    
])


@app.callback(
    Output('4-plot', 'figure'),
    Input('4-plot-button', 'n_clicks'),
    State('4-plot-decision', 'value'),
    State('4-features', 'value'),

)

def four_plot_return(four_clicks, four_plot_type, four_features):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if '4-plot-button' in changed_id:
        if four_plot_type == '3D plot':
            fig = px.scatter_3d(
                fourmarkers_df,
                x = four_features[0],
                y = four_features[1],
                z = four_features[2],
                color = 'target_performance'
            )
        elif four_plot_type == '2D plot':
            fig = px.scatter(
                fourmarkers_df,
                x = four_features[0],
                y = four_features[1],
                color = 'target_performance'
            )
        elif four_plot_type == '1D plot':
            fig = px.scatter(
                fourmarkers_df,
                x = 'target_performance',
                y = four_features[0]
            )
    else:
        fig = px.scatter_3d(
                fourmarkers_df,
                x = "mean_AP_MOS",
                y = 'std_vertical_xCOM',
                z = 'std_ML_xCOM',
                color = 'target_performance'
            )
    return fig

@app.callback(
    Output('force-plot', 'figure'),
    Input('force-plot-button', 'n_clicks'),
    State('force-plot-decision', 'value'),
    State('force-features', 'value'),

)

def four_plot_return(force_clicks, force_plot_type, force_features):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'force-plot-button' in changed_id:
        if force_plot_type == '3D plot':
            fig = px.scatter_3d(
                force_df,
                x = force_features[0],
                y = force_features[1],
                z = force_features[2],
                color = 'target_performance'
            )
        elif force_plot_type == '2D plot':
            fig = px.scatter(
                force_df,
                x = force_features[0],
                y = force_features[1],
                color = 'target_performance'
            )
        elif force_plot_type == '1D plot':
            fig = px.scatter(
                force_df,
                x = 'target_performance',
                y = force_features[0]
            )
    else:
        fig = px.scatter_3d(
                force_df,
                x = "mean_AP_MOS",
                y = 'std_vertical_xCOM',
                z = 'std_ML_xCOM',
                color = 'target_performance'
            )
    return fig

@app.callback(
    Output('38-plot', 'figure'),
    Input('38-plot-button', 'n_clicks'),
    State('38-plot-decision', 'value'),
    State('38-features', 'value'),

)

def four_plot_return(full_clicks, full_plot_type, full_features):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if '38-plot-button' in changed_id:
        if full_plot_type == '3D plot':
            fig = px.scatter_3d(
                fullmarkers_df,
                x = full_features[0],
                y = full_features[1],
                z = full_features[2],
                color = 'target_performance'
            )
        elif full_plot_type == '2D plot':
            fig = px.scatter(
                fullmarkers_df,
                x = full_features[0],
                y = full_features[1],
                color = 'target_performance'
            )
        elif full_plot_type == '1D plot':
            fig = px.scatter(
                fullmarkers_df,
                x = 'target_performance',
                y = full_features[0]
            )
    else:
        fig = px.scatter_3d(
                fullmarkers_df,
                x = "mean_AP_MOS",
                y = 'std_vertical_xCOM',
                z = 'std_ML_xCOM',
                color = 'target_performance'
            )
    return fig
    

@app.callback(
    Output('t-test', 'children'),
    Output('feature-bar-plot', 'children'),
    Input('t-test-button', 'n_clicks'),
    State('t-test-feature', 'value'),
)  

def t_test_return(t_click, t_feature):
    four_G_df = fourmarkers_df[fourmarkers_df["target_performance"]=="Good"]
    four_M_df = fourmarkers_df[fourmarkers_df["target_performance"]=="Moderate"]
    four_B_df = fourmarkers_df[fourmarkers_df["target_performance"]=="Bad"]

    force_G_df = force_df[force_df["target_performance"]=="Good"]
    force_M_df = force_df[force_df["target_performance"]=="Moderate"]
    force_B_df = force_df[force_df["target_performance"]=="Bad"]

    full_G_df = fullmarkers_df[fullmarkers_df["target_performance"]=="Good"]
    full_M_df = fullmarkers_df[fullmarkers_df["target_performance"]=="Moderate"]
    full_B_df = fullmarkers_df[fullmarkers_df["target_performance"]=="Bad"]

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 't-test-button' in changed_id:
        four_GM_t_test = "G(M={},STD={}) vs M(M={},STD={}), p= {}".format(round(four_G_df[t_feature].mean(), 2), round(four_G_df[t_feature].std(), 2), 
                                                                round(four_M_df[t_feature].mean(), 2), round(four_M_df[t_feature].std(), 2), 
                                                                round(stats.ttest_ind(four_G_df[t_feature], four_M_df[t_feature]).pvalue, 2)
                                                                )
        four_GB_t_test = "G(M={},STD={}) vs B(M={},STD={}), p= {}".format(round(four_G_df[t_feature].mean(), 2), round(four_G_df[t_feature].std(), 2), 
                                                                round(four_B_df[t_feature].mean(), 2), round(four_B_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(four_G_df[t_feature], four_B_df[t_feature]).pvalue, 2)
                                                                )
        four_MB_t_test = "M(M={},STD={}) vs B(M={},STD={}), p= {}".format(round(four_M_df[t_feature].mean(), 2), round(four_M_df[t_feature].std(), 2), 
                                                                round(four_B_df[t_feature].mean(), 2), round(four_B_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(four_M_df[t_feature], four_B_df[t_feature]).pvalue, 2)
                                                                )
        ####################################################################################################################################################3
        force_GM_t_test = "G(M={},STD={}) vs M(M={},STD={}), p= {}".format(round(force_G_df[t_feature].mean(), 2), round(force_G_df[t_feature].std(), 2), 
                                                                round(force_M_df[t_feature].mean(), 2), round(force_M_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(force_G_df[t_feature], force_M_df[t_feature]).pvalue, 2)
                                                                )
        force_GB_t_test = "G(M={},STD={}) vs B(M={},STD={}), p= {}".format(round(force_G_df[t_feature].mean(), 2), round(force_G_df[t_feature].std(), 2), 
                                                                round(force_B_df[t_feature].mean(), 2), round(force_B_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(force_G_df[t_feature], force_B_df[t_feature]).pvalue, 2)
                                                                )
        force_MB_t_test = "M(M={},STD={}) vs B(M={},STD={}), p= {}".format(round(force_M_df[t_feature].mean(), 2), round(force_M_df[t_feature].std(), 2), 
                                                                round(force_B_df[t_feature].mean(), 2), round(force_B_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(force_M_df[t_feature], force_B_df[t_feature]).pvalue, 2)
                                                                )
        ##########################################################################################################################################################
        full_GM_t_test = "G(M={},STD={}) vs M(M={},STD={}), p= {}".format(round(full_G_df[t_feature].mean(), 2), round(full_G_df[t_feature].std(), 2), 
                                                                round(full_M_df[t_feature].mean(), 2), round(full_M_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(full_G_df[t_feature], full_M_df[t_feature]).pvalue, 2)
                                                                )
        full_GB_t_test = "G(M={},STD={}) vs B(M={},STD={}), p= {}".format(round(full_G_df[t_feature].mean(), 2), round(full_G_df[t_feature].std(), 2), 
                                                                round(full_B_df[t_feature].mean(), 2), round(full_B_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(full_G_df[t_feature], full_B_df[t_feature]).pvalue, 2)
                                                                )
        full_MB_t_test = "M(M={},STD={}) vs B(M={},STD={}), p= {}".format(round(full_M_df[t_feature].mean(), 2), round(full_M_df[t_feature].std(), 2), 
                                                                round(full_B_df[t_feature].mean(), 2), round(full_B_df[t_feature].std(), 2),
                                                                round(stats.ttest_ind(full_M_df[t_feature], full_B_df[t_feature]).pvalue, 2)
                                                                )
        ##############################################################################################################################
        four_x = ["4 Good", "4 Moderate", "4 bad"]
        four_y = [round(four_G_df[t_feature].mean(),2), round(four_M_df[t_feature].mean(),2), round(four_B_df[t_feature].mean(),2)]

        force_x = ["force Good", "force Moderate", "force bad"]
        force_y = [round(force_G_df[t_feature].mean(),2), round(force_M_df[t_feature].mean(),2), round(force_B_df[t_feature].mean(),2)]

        full_x = ["full Good", "full Moderate", "full bad"]
        full_y = [round(full_G_df[t_feature].mean(),2), round(full_M_df[t_feature].mean(),2), round(full_B_df[t_feature].mean(),2)]

        fig_1 = go.Figure([go.Bar(x = four_x, y = four_y, text = four_y, textposition = "auto", width = [0.8,0.8,0.8])])
        fig_2 = go.Figure([go.Bar(x = force_x, y = force_y, text = force_y, textposition = "auto", width = [0.8,0.8,0.8])])
        fig_3 = go.Figure([go.Bar(x = full_x, y = full_y, text = full_y, textposition = "auto", width = [0.8,0.8,0.8])])
        
        fig = px.histogram(new_df, x="target_performance", y=t_feature,
             color='calculation', barmode='group',
             histfunc='avg')
        fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Good', 'Moderate', 'Bad']})
        return [html.Div([
                    html.Div("4 marker version"),
                    html.Div(four_GM_t_test),
                    html.Div(four_GB_t_test),
                    html.Div(four_MB_t_test),
                    html.Br(),
                    html.Div("Force version"),
                    html.Div(force_GM_t_test),
                    html.Div(force_GB_t_test),
                    html.Div(force_MB_t_test),
                    html.Br(),
                    html.Div("38 marker version"),
                    html.Div(full_GM_t_test),
                    html.Div(full_GB_t_test),
                    html.Div(full_MB_t_test),
                    ]),
                html.Div([
                    dcc.Graph(figure = fig, style = {'height':'700px', 'font-size':'15px'}),
                    ])
                    ]
    else:
        line_1 = "please select variable"
        return [html.Div(line_1), html.Div(line_1)]   

    


if __name__ == '__main__':
    app.run_server(debug=True)
