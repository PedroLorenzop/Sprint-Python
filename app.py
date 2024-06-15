from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import random

app = Dash(__name__)

equipes = ['Mahindra', 'Mercedes', 'Audi', 'BMW', 'Jaguar', 'Nissan', 'Porsche']
cidades_populosas = ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Goiânia']

def gerar_valores_cidades():
    valores = {}
    while len(valores) < 3:
        if len(valores) == 0:
            valores["Cupons de recomendação"] = round(random.uniform(7.0, 8.0), 1)
        elif len(valores) == 1:
            valores["Tempo online"] = round(random.uniform(1, 10), 1)  # Tempo online em horas
        elif len(valores) == 2:
            valores["Equipe mais escolhida"] = (random.choice(equipes), round(random.uniform(5, 50)))
    return valores

def gerar_valores_aleatorios():
    valores = {}
    while len(valores) < 3:
        if len(valores) == 0:
            valores["Cupons de recomendação"] = round(random.uniform(7.5, 8.5), 1)
        elif len(valores) == 1:
            valores["Tempo online"] = round(random.uniform(1, 10), 1)  # Tempo online em horas
        elif len(valores) == 2:
            valores["Equipe mais escolhida"] = (random.choice(equipes), round(random.uniform(2, 100)))
    return valores

def criar_dataframe():
    dados = {
        "Dados": [],
        "Quantidade": [],
        "Categoria": [],
        "Equipe": []
    }

    # Dados para períodos
    for periodo in ["Anual", "Mensal", "Semanal", "Diário"]:
        valores = gerar_valores_aleatorios()
        dados["Dados"].extend(["Cupons de recomendação", "Tempo online (h)", "Equipe mais escolhida"])
        dados["Quantidade"].extend([valores["Cupons de recomendação"], valores["Tempo online"], valores["Equipe mais escolhida"][1]])
        dados["Categoria"].extend([periodo] * 3)
        dados["Equipe"].extend([None, None, valores["Equipe mais escolhida"][0]])

    # Dados para cidades
    for cidade in cidades_populosas:
        valores = gerar_valores_cidades()
        dados["Dados"].extend(["Cupons de recomendação", "Tempo online (h)", "Equipe mais escolhida"])
        dados["Quantidade"].extend([valores["Cupons de recomendação"], valores["Tempo online"], valores["Equipe mais escolhida"][1]])
        dados["Categoria"].extend([cidade] * 3)
        dados["Equipe"].extend([None, None, valores["Equipe mais escolhida"][0]])

    return pd.DataFrame(dados)

cor_mapa = {
    'Anual': '#49CF8F',
    'Mensal': '#3744B9',
    'Semanal': '#4BC7D8',
    'Diário': '#4B6AD8',
}

cor_cidade = {
    'São Paulo': '#E00043',
    'Rio de Janeiro': '#FFA63D',
    'Brasília': '#F43636',
    'Salvador': '#D9B600',
    'Fortaleza': '#49CF8F',
    'Belo Horizonte': '#3744B9',
    'Manaus': '#4BC7D8',
    'Curitiba': '#4B6AD8',
    'Recife': '#E00043',
    'Goiânia': '#FFA63D',
}

app.layout = html.Div(
    children=[
        html.Div(id='cabecalho', children=[
            html.Img(id='img', src='/assets/image.png', alt='logo dashboard', style={'width': '100px'}),
            html.H1(children='Turbo Analytics')
        ]),
        html.H2(children='"Mudamos a forma de analisar as corridas"'),
        html.P(children='Esta plataforma serve para ver e analisar as equipes mais escolhidas, quantidades de cupons e tempo dentro da plataforma'),
        dcc.Tabs(id='tabs', value='tab-periodos', children=[
            dcc.Tab(id='troca_secao', label='Períodos', value='tab-periodos', children=[
                dcc.Dropdown(
                    id='lista_periodos',
                    options=[
                        {'label': 'Ver Tudo', 'value': 'Todos'},
                        {'label': 'Anual', 'value': 'Anual'},
                        {'label': 'Mensal', 'value': 'Mensal'},
                        {'label': 'Semanal', 'value': 'Semanal'},
                        {'label': 'Diário', 'value': 'Diário'}
                    ],
                    value='Todos',
                ),
                html.Div(
                    className='grafico-container',
                    children=[
                        dcc.Graph(
                            id='grafico_condicoes_periodos'
                        )
                    ]
                ),
            ]),
            dcc.Tab(id='troca_secao', label='Brasil', value='tab-brasil', children=[
                dcc.Dropdown(
                    id='lista_cidades',
                    options=[
                        {'label': 'Todas as Cidades', 'value': 'Todas'},
                        {'label': 'São Paulo', 'value': 'São Paulo'},
                        {'label': 'Rio de Janeiro', 'value': 'Rio de Janeiro'},
                        {'label': 'Brasília', 'value': 'Brasília'},
                        {'label': 'Salvador', 'value': 'Salvador'},
                        {'label': 'Fortaleza', 'value': 'Fortaleza'},
                        {'label': 'Belo Horizonte', 'value': 'Belo Horizonte'},
                        {'label': 'Manaus', 'value': 'Manaus'},
                        {'label': 'Curitiba', 'value': 'Curitiba'},
                        {'label': 'Recife', 'value': 'Recife'},
                        {'label': 'Goiânia', 'value': 'Goiânia'}
                    ],
                    value='Todas',
                ),
                html.Div(
                    className='grafico-container',
                    children=[
                        dcc.Graph(
                            id='grafico_condicoes_cidades'
                        )
                    ]
                ),
            ]),
        ]),
        dcc.Interval(
            id='intervalo-atualizacao',
            interval=30*1000,
            n_intervals=0
        )
    ]
)

@app.callback(
    Output('grafico_condicoes_periodos', 'figure'),
    [Input('lista_periodos', 'value'),
     Input('intervalo-atualizacao', 'n_intervals')]
)
def atualizar_grafico_periodos(periodo_selecionado, n_intervals):
    df = criar_dataframe()
    if periodo_selecionado == 'Todos':
        df_filtrado = df[df['Categoria'].isin(['Anual', 'Mensal', 'Semanal', 'Diário'])]
    else:
        df_filtrado = df[df['Categoria'] == periodo_selecionado]

    fig = px.bar(df_filtrado, x='Dados', y='Quantidade', color='Categoria', barmode='group',
                 hover_data={'Equipe': True}, text='Equipe', color_discrete_map=cor_mapa)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

@app.callback(
    Output('grafico_condicoes_cidades', 'figure'),
    [Input('lista_cidades', 'value'),
     Input('intervalo-atualizacao', 'n_intervals')]
)
def atualizar_grafico_cidades(cidade_selecionada, n_intervals):
    df = criar_dataframe()
    if cidade_selecionada == 'Todas':
        df_filtrado = df[df['Categoria'].isin(cidades_populosas)]
    else:
        df_filtrado = df[df['Categoria'] == cidade_selecionada]

    fig = px.bar(df_filtrado, x='Dados', y='Quantidade', color='Categoria', barmode='group',
                 hover_data={'Equipe': True}, text='Equipe', color_discrete_map=cor_cidade)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
