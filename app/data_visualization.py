from flask import Flask
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from datetime import datetime

app = Flask(__name__)

def generate_graph_html(data_dict, days, leg=True):
    if "x" in data_dict and "y" in data_dict and "label" in data_dict and "name" in data_dict and "index_y2" in data_dict:
        x = data_dict["x"]
        y = data_dict["y"]
        label = data_dict["label"]
        name = data_dict["name"]
        index_y2 = data_dict["index_y2"]

        if not len(x) or not len(y) or not len(label) or not len(name) or not len(index_y2):
            return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
        
        for i in x:
            if isinstance(i, str):
                try:
                    datetime.strptime(i, "%Y-%m-%d")
                except ValueError:
                    return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
            else:
                return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
            
        for i in y:
            if type(i) == list:
                if len(y) != len(name) or len(y) != len(index_y2):
                    return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
        for i in index_y2:
            if type(i) != int:
                return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
        
        layout = go.Layout(
            xaxis=dict(title=label[0]),  # Tytuł osi X
            yaxis=dict(title=label[1]),  # Tytuł osi Y
            bargap=0.5,
            plot_bgcolor="#fcfcfc", 
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=20, b=20), 
            autosize=True,
            legend=dict(
            orientation="v", 
            x=1,              
            xanchor="left",  
            y=0.5,             
            yanchor="middle"    
        )

        )

        if len(label) > 2:
            layout['yaxis2'] = dict(
                title=label[2],  
                overlaying="y",  
                side="right", 
                range=[0, 20]
            )
    
        fig = go.Figure(layout=layout)
        fig.update_layout(showlegend=leg)

        # Zamiana dat na datetime
        x_dates = [datetime.strptime(date, "%Y-%m-%d") for date in x[:days]]

        for i in y:
            if type(i) == list:
                if index_y2[y.index(i)] == 0:
                    # Zamiana dat na liczby dni od pierwszej daty
                    x_numeric = np.array([(date - x_dates[0]).days for date in x_dates[:days]])
                    print(x_dates[0])

                    # Rysowanie wykresu
                    fig.add_trace(go.Scatter(x=x_dates, y=i[:days], mode='lines+markers', name=name[y.index(i)]))

                    # Przygotowanie danych do regresji
                    Y = np.array(i[:days])

                    model = LinearRegression()
                    model.fit(x_numeric.reshape(-1, 1), Y)
                    
                    # Obliczenie prognozowanych wartości regresji na pełnym zakresie danych
                    y_range = model.predict(x_numeric.reshape(-1, 1))

                    # Dodanie linii regresji (domyślnie ukrytej)
                    fig.add_trace(go.Scatter(
                        x=x_dates,
                        y=y_range,
                        mode='lines',
                        name=f'Regresja linowa ({name[y.index(i)]})',
                        line=dict(simplify=False, dash='dot'),
                        visible="legendonly"  # Ukryte na początku
                    ))

                else:
                    fig.update_layout(yaxis2=dict(
                        title=label[2],  
                        overlaying="y",  
                        side="right", 
                        range=[min(i)-0.01*min(i), max(i)+0.01*max(i)]
                    ))
                    fig.add_trace(go.Bar(x=x_dates, y=i[:days], yaxis='y2', opacity=0.4, name=name[y.index(i)]))
            else:
                fig.add_trace(go.Scatter(x=x_dates, y=y[:days], mode='lines+markers', name=name[y.index(i)]))
                break

        html_content = pio.to_html(fig, full_html=False, include_plotlyjs=False)

        html_content = html_content.replace('<div', '<div style="width: 100%; height: 100%;"')

        if leg == False:
            html_content = f"""
                <div class="chart-container" style="width: 95%; box-sizing: border-box; height: 100%;">
                {html_content}
                </div>

            """

        return html_content

    else:
        return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
