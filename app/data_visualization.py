from flask import Flask
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

def generate_graph_html(data_dict, days):
    if "x" in data_dict and "y" in data_dict and "label" in data_dict and "name" in data_dict and "index_y2" in data_dict:
        x = data_dict["x"]
        y = data_dict["y"]
        label = data_dict["label"]
        name = data_dict["name"]
        index_y2 = data_dict["index_y2"]

        if len(x) == 0 or len(y) == 0 or len(label) == 0 or len(name) == 0 or len(index_y2) == 0:
            return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
        
        for i in y:
            if type(i) == list:
                if len(y) != len(name) or len(y) != len(index_y2):
                    return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
        for i in index_y2:
            if type(i) != int:
                return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"
        
        layout = go.Layout(
        xaxis=dict(title=label[0]),
        yaxis=dict(title=label[1]), 
        bargap=0.5,
        plot_bgcolor="#fcfcfc", 
        paper_bgcolor="white" 
        )

        if len(label) > 2:
            layout['yaxis2'] = dict(
            title=label[2],  
            overlaying="y",  
            side="right", 
            range=[0, 20])
    
        fig = go.Figure(layout=layout)
        for i in y:
            if type(i) == list:
                if index_y2[y.index(i)] == 0:
                    fig.add_trace(go.Scatter(x=x[:days], y=i[:days], mode='lines+markers', name=name[y.index(i)]))
                else:
                    fig.update_layout(yaxis2 = dict(
                        title=label[2],  
                        overlaying="y",  
                        side="right", 
                        range=[min(i)-0.01*min(i), max(i)+0.01*max(i)]))
                    fig.add_trace(go.Bar(x=x[:days], y=i[:days], yaxis='y2', opacity=0.4, name=name[y.index(i)]))
            else:
                fig.add_trace(go.Scatter(x=x[:days], y=y[:days], mode='lines+markers', name=name[y.index(i)]))
                break

        return pio.to_html(fig, full_html=False, include_plotlyjs=False)

    else:
        return "<div><h2>Błąd: Nieprawidłowe dane</h2></div>"