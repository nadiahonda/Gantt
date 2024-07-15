import matplotlib.pyplot as plt
import pandas as pd

def generate_gantt_chart(df, custom_colors=None, include_fp=False, time_unit="min"):
    plt.rcParams['font.family'] = 'DejaVu Sans'

    fig, ax = plt.subplots(figsize=(10, 5))

    # Definindo cores para diferentes batches em HEX e ordenando
    default_batch_colors = {
        1: '#AAB400',  # Light Green
        2: '#5F7800',  # Dark Green
        3: '#00A0BE',  # Dark Blue
        4: '#FFB400',  # Light Orange
        5: '#EB8200',  # Dark Orange
        6: '#82C8DC',  # Light Blue
        7: '#333333',  # Dark Gray
        8: '#D9D5D2',  # Light Gray
    }

    # Usar cores personalizadas se fornecidas, caso contrário, usar cores padrão
    batch_colors = custom_colors if custom_colors else default_batch_colors

    # Lista de recursos únicos linha por linha
    resources = []
    for _, row in df.iterrows():
        for resource in ['Resource 1', 'Resource 2', 'Resource 3']:
            if pd.notna(row[resource]) and row[resource] not in resources:
                resources.append(row[resource])

    # Remover o recurso "F&P" se o toggle estiver ativado
    if include_fp == False and 'F&P' in resources:
        resources.remove('F&P')

    # Mapeando recursos para índices na ordem inversa
    resource_map = {resource: i for i, resource in enumerate(reversed(resources))}

    bars = []
    tasks = []
    for i, task in df.iterrows():
        start = task['Start']
        duration = task['Duration']
        batch = task['Batch']

        # Ignorar batches com cor "None"
        if batch not in batch_colors:
            continue

        # Definindo a cor da barra
        color = batch_colors.get(batch, 'grey')

        # Adicionando barras para cada recurso
        for resource in ['Resource 1', 'Resource 2', 'Resource 3']:
            if pd.notna(task[resource]) and task[resource] in resource_map:
                bar = ax.barh(resource_map[task[resource]], duration, left=start, color=color, edgecolor='black', label=f"Batch {batch}")
                bars.append(bar)
                tasks.append((batch, task['Task'], start, duration))

    # Ajustando o eixo y para mostrar os recursos
    ax.set_yticks(list(resource_map.values()))
    ax.set_yticklabels(list(resource_map.keys()))

    # Ajustando o eixo x para mostrar o tempo
    ax.set_xlabel(f'Time ({time_unit})')
    ax.set_ylabel('Resource')

    # Garantindo que a legenda não tenha duplicatas
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend = ax.legend(by_label.values(), by_label.keys())
    legend.get_frame().set_alpha(0)  # Set legend background transparent

    # Adicionando texto na figura no canto superior esquerdo
    fig_text1 = fig.text(0.12, 0.92, '', ha='left', va='top', fontsize=10)

    # Adicionando texto na figura no canto superior direito
    fig_text2 = fig.text(0.9, 0.92, '', ha='right', va='top', fontsize=10)

    # Função para atualizar o texto da figura
    def on_move(event):
        for bar, (batch, task, start, duration) in zip(bars, tasks):
            if bar[0].contains(event)[0]:
                fig_text1.set_text(f'Batch {batch} | {task}')
                fig_text2.set_text(f'Start: {start} | End: {start+duration} | Duration: {duration} {time_unit}')
                fig.canvas.draw_idle()
                return
        fig_text1.set_text('')
        fig_text2.set_text('')
        fig.canvas.draw_idle()

    # Conectando o evento de movimento do mouse
    fig.canvas.mpl_connect('motion_notify_event', on_move)

    # Alterar o título da janela da figura
    fig.canvas.manager.set_window_title('Gantt Chart')

    # Posição da janela do gráfico Gantt
    fig.canvas.manager.window.wm_geometry(f"+{600}+{100}")

    # Armazenar a figura para uso posterior
    plt.show()

    return fig