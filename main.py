import dash
from dash import html, dcc, Input, Output, State, ALL, callback, ctx
import dash_bootstrap_components as dbc
from datetime import datetime
import json
import os
from typing import List, Dict
import uuid
import math

# Inicialização do app com tema Bootstrap
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)

app.title = "Gerenciamento de Fila"

# Configurações
DATA_FILE = "data/fila_data.json"
REFRESH_INTERVAL = 3000  # 3 segundos
CAROUSEL_INTERVAL = 10000  # 8 segundos
MAX_FILAS_POR_TELA = 3
MODAL_DURATION = 8000  # 10 segundos
SENHA_ADMIN = "6105/*"  # Senha para acesso ao admin

# Classificações com cores e prioridades BASEADAS EM IDADE
CLASSIFICACOES = {
    "prioridade_legal_1": {
        "label": "Prioridade Legal 1 (>79 anos)", 
        "color": "#28a745",  # Verde
        "prioridade": 1
    },
    "prioridade_legal_2": {
        "label": "Prioridade Legal 2 (>59 anos)", 
        "color": "#ffc107",  # Amarelo
        "prioridade": 2
    },
    "prioridade_clinica": {
        "label": "Prioridade Clínica", 
        "color": "#fd7e14",  # Laranja
        "prioridade": 3
    },
    "normal": {
        "label": "Atendimento Normal", 
        "color": "#17a2b8",  # Azul
        "prioridade": 4
    }
}

# TEMAS BOOTSTRAP PROFISSIONAIS
TEMAS = {
    "bootstrap": {
        "nome": "🔵 Bootstrap Padrão",
        "theme": dbc.themes.BOOTSTRAP,
        "primary": "#0d6efd",
        "bg": "#ffffff",
        "text": "#212529",
        "header_class": "bg-primary"
    },
    "cerulean": {
        "nome": "🌊 Cerulean",
        "theme": dbc.themes.CERULEAN,
        "primary": "#2fa4e7",
        "bg": "#ffffff", 
        "text": "#333333",
        "header_class": "bg-info"
    },
    "cosmo": {
        "nome": "🌌 Cosmo",
        "theme": dbc.themes.COSMO,
        "primary": "#2780e3",
        "bg": "#ffffff",
        "text": "#373a3c",
        "header_class": "bg-primary"
    },
    "flatly": {
        "nome": "📱 Flatly",
        "theme": dbc.themes.FLATLY,
        "primary": "#2c3e50",
        "bg": "#ffffff",
        "text": "#2c3e50",
        "header_class": "bg-dark"
    },
    "journal": {
        "nome": "📰 Journal",
        "theme": dbc.themes.JOURNAL,
        "primary": "#eb6864",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-danger"
    },
    "litera": {
        "nome": "📖 Litera",
        "theme": dbc.themes.LITERA,
        "primary": "#4582ec",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-primary"
    },
    "lumen": {
        "nome": "💡 Lumen",
        "theme": dbc.themes.LUMEN,
        "primary": "#158cba",
        "bg": "#ffffff",
        "text": "#555555",
        "header_class": "bg-info"
    },
    "minty": {
        "nome": "🌿 Minty",
        "theme": dbc.themes.MINTY,
        "primary": "#78c2ad",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-success"
    },
    "pulse": {
        "nome": "💜 Pulse",
        "theme": dbc.themes.PULSE,
        "primary": "#593196",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-primary"
    },
    "sandstone": {
        "nome": "🏜️ Sandstone",
        "theme": dbc.themes.SANDSTONE,
        "primary": "#93c54b",
        "bg": "#ffffff",
        "text": "#3e3f3a",
        "header_class": "bg-success"
    },
    "simplex": {
        "nome": "⚪ Simplex",
        "theme": dbc.themes.SIMPLEX,
        "primary": "#d9230f",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-danger"
    },
    "sketchy": {
        "nome": "✏️ Sketchy",
        "theme": dbc.themes.SKETCHY,
        "primary": "#333333",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-dark"
    },
    "spacelab": {
        "nome": "🚀 Spacelab",
        "theme": dbc.themes.SPACELAB,
        "primary": "#446e9b",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-primary"
    },
    "united": {
        "nome": "🇺🇸 United",
        "theme": dbc.themes.UNITED,
        "primary": "#dd4814",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-warning"
    },
    "yeti": {
        "nome": "🏔️ Yeti",
        "theme": dbc.themes.YETI,
        "primary": "#008cba",
        "bg": "#ffffff",
        "text": "#333333",
        "header_class": "bg-info"
    },
    "darkly": {
        "nome": "🌙 Darkly",
        "theme": dbc.themes.DARKLY,
        "primary": "#375a7f",
        "bg": "#222222",
        "text": "#ffffff",
        "header_class": "bg-primary"
    },
    "cyborg": {
        "nome": "🤖 Cyborg",
        "theme": dbc.themes.CYBORG,
        "primary": "#2a9fd6",
        "bg": "#060606",
        "text": "#ffffff",
        "header_class": "bg-info"
    },
    "slate": {
        "nome": "🗿 Slate",
        "theme": dbc.themes.SLATE,
        "primary": "#5a6268",
        "bg": "#272b30",
        "text": "#ffffff",
        "header_class": "bg-secondary"
    },
    "solar": {
        "nome": "☀️ Solar",
        "theme": dbc.themes.SOLAR,
        "primary": "#b58900",
        "bg": "#002b36",
        "text": "#839496",
        "header_class": "bg-warning"
    },
    "superhero": {
        "nome": "🦸 Superhero",
        "theme": dbc.themes.SUPERHERO,
        "primary": "#df691a",
        "bg": "#2b3e50",
        "text": "#ffffff",
        "header_class": "bg-warning"
    }
}

# ==================== MAPEAMENTO DE COMPATIBILIDADE ====================

# Mapeamento das classificações antigas para novas
MAPEAMENTO_CLASSIFICACOES_ANTIGAS = {
    "urgente": "prioridade_clinica",
    "preferencial": "prioridade_legal_2",
    "retorno": "prioridade_clinica",
    "normal": "normal"
}


def migrar_classificacao_antiga(classificacao: str) -> str:
    """Converte classificação antiga para nova"""
    if classificacao in CLASSIFICACOES:
        return classificacao
    
    # Se for classificação antiga, converte
    if classificacao in MAPEAMENTO_CLASSIFICACOES_ANTIGAS:
        return MAPEAMENTO_CLASSIFICACOES_ANTIGAS[classificacao]
    
    # Se não reconhecer, retorna normal
    return "normal"


def migrar_dados_antigos():
    """Migra todos os pacientes com classificações antigas"""
    dados = carregar_dados()
    migrado = False
    
    for paciente_id, paciente in dados["pacientes"].items():
        classificacao_antiga = paciente.get("classificacao")
        
        # Se for classificação antiga
        if classificacao_antiga not in CLASSIFICACOES:
            # Converte para nova
            nova_classificacao = migrar_classificacao_antiga(classificacao_antiga)
            dados["pacientes"][paciente_id]["classificacao"] = nova_classificacao
            dados["pacientes"][paciente_id]["prioridade"] = CLASSIFICACOES[nova_classificacao]["prioridade"]
            migrado = True
            
            # Se não tem data de nascimento, adiciona campo vazio
            if "data_nascimento" not in paciente:
                dados["pacientes"][paciente_id]["data_nascimento"] = "1980-01-01"  # Data padrão
    
    if migrado:
        salvar_dados(dados)
        print("✅ Dados migrados com sucesso!")
    
    return dados


def obter_classificacao_segura(paciente: Dict) -> Dict:
    """Obtém classificação de forma segura, migrando se necessário"""
    classificacao = paciente.get("classificacao", "normal")
    
    # Se for classificação antiga, converte
    if classificacao not in CLASSIFICACOES:
        classificacao = migrar_classificacao_antiga(classificacao)
    
    return CLASSIFICACOES[classificacao]


def calcular_idade(data_nascimento: str) -> int:
    """Calcula idade a partir da data de nascimento"""
    try:
        dn = datetime.strptime(data_nascimento, "%Y-%m-%d")
        hoje = datetime.now()
        idade = hoje.year - dn.year - ((hoje.month, hoje.day) < (dn.month, dn.day))
        return idade
    except:
        return 0


def sugerir_classificacao(data_nascimento: str) -> str:
    """Sugere classificação baseada na idade"""
    idade = calcular_idade(data_nascimento)
    
    if idade > 79:
        return "prioridade_legal_1"
    elif idade > 59:
        return "prioridade_legal_2"
    else:
        return "normal"


def formatar_hora(timestamp_iso: str) -> str:
    """Formata timestamp ISO para hora HH:MM"""
    try:
        dt = datetime.fromisoformat(timestamp_iso)
        return dt.strftime("%H:%M")
    except:
        return ""


# ==================== FUNÇÕES DE DADOS ====================

def carregar_dados():
    """Carrega dados do arquivo JSON"""
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "filas": {
            "fila1": {
                "id": "fila1",
                "nome": "Atendimento Geral",
                "ativa": True,
                "criada_em": datetime.now().isoformat()
            }
        },
        "pacientes": {},
        "historico": [],
        "ultimo_chamado": None
    }


def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def adicionar_paciente(fila_id: str, nome: str, data_nascimento: str, classificacao: str):
    """Adiciona um paciente à fila"""
    dados = carregar_dados()
    paciente_id = str(uuid.uuid4())[:8]
    
    dados["pacientes"][paciente_id] = {
        "id": paciente_id,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "fila_id": fila_id,
        "classificacao": classificacao,
        "prioridade": CLASSIFICACOES[classificacao]["prioridade"],
        "chegada": datetime.now().isoformat(),
        "status": "aguardando",
        "chamado_em": None,
        "atendido_em": None
    }
    
    salvar_dados(dados)
    return paciente_id


def obter_pacientes_por_status(fila_id: str, status: str) -> List[Dict]:
    """Retorna pacientes da fila filtrados por status"""
    dados = carregar_dados()
    pacientes = [
        p for p in dados["pacientes"].values()
        if p["fila_id"] == fila_id and p["status"] == status
    ]
    
    # Ordenar por prioridade e hora de chegada
    if status == "aguardando":
        pacientes.sort(key=lambda x: (x["prioridade"], x["chegada"]))
    elif status == "chamado":
        pacientes.sort(key=lambda x: x["chamado_em"], reverse=True)
    elif status == "atendido":
        pacientes.sort(key=lambda x: x["atendido_em"], reverse=True)
    
    return pacientes


# ==================== LAYOUT PRINCIPAL ====================

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='store-autenticado', data=False, storage_type='session'),
    dcc.Store(id='store-tema-selecionado', data='bootstrap', storage_type='local'),
    html.Div(id='page-content')
])


# ==================== TELA DE LOGIN ====================

def layout_login():
    """Layout da tela de login do admin"""
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-lock fa-4x text-primary mb-4")
                            ], className="text-center"),
                            
                            html.H3("🔐 Acesso Administrativo", className="text-center mb-4"),
                            
                            dbc.Label("Senha de Acesso:"),
                            dbc.Input(
                                id="input-senha-admin",
                                type="password",
                                placeholder="Digite a senha",
                                className="mb-3"
                            ),
                            
                            dbc.Button(
                                [html.I(className="fas fa-sign-in-alt me-2"), "Entrar"],
                                id="btn-login",
                                color="primary",
                                size="lg",
                                className="w-100 mb-3"
                            ),
                            
                            html.Div(id="feedback-login"),
                            
                            html.Hr(),
                            
                            html.Div([
                                dbc.Button(
                                    [html.I(className="fas fa-arrow-left me-2"), "Voltar para Tela Pública"],
                                    href="/",
                                    color="secondary",
                                    size="sm",
                                    className="w-100"
                                )
                            ])
                        ])
                    ], className="shadow-lg")
                ], md=6, lg=4, className="mx-auto")
            ], className="min-vh-100 align-items-center")
        ], fluid=True, className="bg-light")
    ])


@callback(
    Output("store-autenticado", "data"),
    Output("feedback-login", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Input("btn-login", "n_clicks"),
    State("input-senha-admin", "value"),
    prevent_initial_call=True
)
def fazer_login(n_clicks, senha):
    """Valida a senha e autentica o usuário"""
    if not senha:
        return False, dbc.Alert("⚠️ Digite a senha", color="warning"), dash.no_update
    
    if senha == SENHA_ADMIN:
        return True, dbc.Alert("✅ Login realizado com sucesso!", color="success"), "/admin"
    else:
        return False, dbc.Alert("❌ Senha incorreta!", color="danger"), dash.no_update


# ==================== TELA PÚBLICA (TV) ====================

def layout_publico():
    """Layout da tela pública para exibição em TV"""
    return html.Div([
        dcc.Interval(id='interval-refresh', interval=REFRESH_INTERVAL, n_intervals=0),
        dcc.Interval(id='interval-carousel', interval=CAROUSEL_INTERVAL, n_intervals=0),
        dcc.Interval(id='interval-modal-close', interval=MODAL_DURATION, n_intervals=0, disabled=True),
        
        dcc.Store(id='store-carousel-page', data=0),
        dcc.Store(id='store-ultimo-chamado', data=None),
        dcc.Store(id='store-tocar-som', data=0),
        dcc.Store(id='store-som-habilitado', data=False),
        
        # Modal de Chamada
        dbc.Modal([
            dbc.ModalBody([
                html.Div([
                    html.Audio(
                        id='audio-chamada',
                        src='/assets/som.mp3',
                        preload='auto',
                        loop=False,
                        autoPlay=False,
                        controls=False,
                        style={'display': 'none'}
                    ),
                    
                    html.Div([
                        html.I(className="fas fa-bell fa-5x text-warning mb-4 animate-ring"),
                    ], className="text-center"),
                    
                    html.H2("🔔 ATENÇÃO! CHAMADA DE PACIENTE", 
                            className="text-center text-primary mb-4 fw-bold"),
                    
                    html.Div(id="modal-conteudo-chamada", className="text-center")
                    
                ], className="p-4")
            ], style={"backgroundColor": "#f8f9fa"})
        ],
        id="modal-chamada",
        is_open=False,
        centered=True,
        size="xl",
        backdrop="static",
        keyboard=False,
        style={"zIndex": 9999}
        ),
        
        # ✅ CABEÇALHO COMPACTO COM LOGO
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            # Logo à esquerda
                            html.Img(
                                src="/assets/logo.png",
                                style={
                                    "height": "150px",
                                    "width": "auto",
                                    "marginRight": "10px"
                                },
                                className="d-inline-block align-middle"
                            ),
                            # Título e relógio
                            html.Div([
                                html.H2([
                                    html.I(className="fas fa-users me-2"),
                                    "Painel de Atendimento"
                                ], className="text-white mb-0", style={"fontSize": "1.8rem"}),
                                html.P(
                                    id="clock",
                                    className="text-white mt-1 mb-0",
                                    style={"fontSize": "1.1rem"}
                                )
                            ], className="d-inline-block align-middle")
                        ], className="d-flex align-items-center justify-content-center")
                    ])
                ])
            ], fluid=True)
        ], id="header-publico", className="bg-primary py-1 shadow-lg"),
        
        # Botão para habilitar som
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-volume-up fa-3x text-warning mb-3"),
                    ], className="text-center"),
                    html.H4("🔔 Sistema de Som", className="text-center mb-3"),
                    html.P(
                        "Para ouvir os avisos de chamada, clique no botão abaixo:",
                        className="text-center text-muted mb-3"
                    ),
                    dbc.Button(
                        [
                            html.I(id="icon-som", className="fas fa-volume-up me-2"),
                            html.Span("HABILITAR SOM AGORA", id="texto-som")
                        ],
                        id="btn-habilitar-som",
                        color="success",
                        size="lg",
                        className="w-100 shadow-lg"
                    ),
                    html.Small(
                        "Após clicar, o som tocará automaticamente nas chamadas",
                        className="text-center text-muted d-block mt-2"
                    )
                ], className="p-4")
            ], className="shadow-lg", style={"maxWidth": "400px"})
        ], id="container-btn-som", 
           className="position-fixed top-50 start-50 translate-middle", 
           style={"zIndex": 10000, "display": "block"}),
        
        # Container das filas
        html.Div([
            html.Div(
                id="filas-container",
                className="container-fluid p-4",
                style={"maxWidth": "1400px"}
            ),
            
            html.Div(
                id="carousel-indicators",
                className="text-center mt-3"
            )
        ]),
        
        # Rodapé
        html.Div([
            html.A(
                "Acesso Administrativo",
                href="/login",
                className="btn btn-outline-light btn-sm"
            )
        ], className="position-fixed bottom-0 end-0 p-3")
        
    ], id="container-publico", style={"minHeight": "100vh"})


# ==================== CALLBACK PARA HABILITAR SOM (PYTHON) ====================

@callback(
    Output("store-som-habilitado", "data"),
    Output("container-btn-som", "style"),
    Input("btn-habilitar-som", "n_clicks"),
    prevent_initial_call=True
)
def habilitar_som_python(n_clicks):
    """Marca som como habilitado e esconde botão"""
    return True, {"display": "none"}


# ==================== CALLBACK CLIENTSIDE PARA DESBLOQUEAR ÁUDIO ====================

# Callback clientside para REALMENTE desbloquear o áudio no navegador
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks && n_clicks > 0) {
            console.log('🔓 Desbloqueando áudio...');
            
            var audio = document.getElementById('audio-chamada');
            
            if (audio) {
                // CRÍTICO: Toca o áudio silenciosamente para desbloquear autoplay
                audio.volume = 0.01;  // Volume muito baixo
                audio.currentTime = 0;
                
                var playPromise = audio.play();
                
                if (playPromise !== undefined) {
                    playPromise.then(function() {
                        console.log('✅ Áudio desbloqueado com sucesso!');
                        // Para imediatamente e reseta
                        audio.pause();
                        audio.currentTime = 0;
                        audio.volume = 1.0;  // Volta volume ao normal
                    }).catch(function(error) {
                        console.error('❌ Erro ao desbloquear:', error);
                    });
                }
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("btn-habilitar-som", "n_clicks", allow_duplicate=True),
    Input("btn-habilitar-som", "n_clicks"),
    prevent_initial_call=True
)


# ==================== CALLBACKS DO MODAL ====================

@callback(
    Output("modal-chamada", "is_open"),
    Output("modal-conteudo-chamada", "children"),
    Output("interval-modal-close", "disabled"),
    Output("interval-modal-close", "n_intervals"),
    Output("store-ultimo-chamado", "data"),
    Output("store-tocar-som", "data"),
    Input("interval-refresh", "n_intervals"),
    Input("interval-modal-close", "n_intervals"),
    State("modal-chamada", "is_open"),
    State("store-ultimo-chamado", "data"),
    State("store-tocar-som", "data")
)
def controlar_modal_chamada(n_refresh, n_modal_close, is_open, ultimo_chamado_anterior, tocar_som_count):
    """Controla abertura e fechamento do modal"""
    dados = carregar_dados()
    
    pacientes_chamados = [
        p for p in dados["pacientes"].values()
        if p["status"] == "chamado" and p["chamado_em"]
    ]
    
    if not pacientes_chamados:
        return False, "", True, 0, None, tocar_som_count
    
    ultimo_chamado = max(pacientes_chamados, key=lambda x: x["chamado_em"])
    ultimo_chamado_id = f"{ultimo_chamado['id']}_{ultimo_chamado['chamado_em']}"
    
    if ultimo_chamado_id != ultimo_chamado_anterior:
        fila = dados["filas"][ultimo_chamado["fila_id"]]
        classif = obter_classificacao_segura(ultimo_chamado)
        
        # Calcular idade
        idade = calcular_idade(ultimo_chamado.get("data_nascimento", ""))
        
        conteudo = html.Div([
            html.Div([
                html.H3("FILA:", className="text-muted mb-2"),
                html.H1(fila["nome"], className="text-info fw-bold mb-4",
                       style={"fontSize": "3.5rem"})
            ], className="mb-5 p-4 bg-white rounded shadow"),
            
            html.Div([
                html.H3("PACIENTE:", className="text-muted mb-2"),
                html.H1(ultimo_chamado["nome"], className="text-success fw-bold mb-3",
                       style={"fontSize": "4rem"}),
                html.Div([
                    html.Span(
                        classif["label"].split("(")[0].strip(),
                        className="badge fs-3 px-4 py-3 me-3",
                        style={"backgroundColor": classif["color"]}
                    ),
                    html.Span(
                        f"{idade} anos",
                        className="badge bg-secondary fs-3 px-4 py-3"
                    )
                ])
            ], className="p-4 bg-white rounded shadow")
        ])
        
        return True, conteudo, False, 0, ultimo_chamado_id, tocar_som_count + 1
    
    if is_open and ctx.triggered_id == "interval-modal-close" and n_modal_close > 0:
        return False, "", True, 0, ultimo_chamado_anterior, tocar_som_count
    
    return is_open, dash.no_update, dash.no_update, dash.no_update, ultimo_chamado_anterior, tocar_som_count


# Callback clientside para tocar o som APENAS se habilitado E se o contador MUDOU
app.clientside_callback(
    """
    function(tocar_som_count, som_habilitado) {
        // CRÍTICO: Armazena o último contador processado
        if (!window.dash_clientside) {
            window.dash_clientside = {};
        }
        if (!window.dash_clientside.ultimo_som_count) {
            window.dash_clientside.ultimo_som_count = 0;
        }
        
        // Só toca se:
        // 1. Som está habilitado
        // 2. Contador mudou desde a última vez
        // 3. Contador é maior que zero
        if (som_habilitado === true && 
            tocar_som_count > 0 && 
            tocar_som_count !== window.dash_clientside.ultimo_som_count) {
            
            console.log('🔔 NOVO contador detectado:', tocar_som_count, '(anterior:', window.dash_clientside.ultimo_som_count, ')');
            
            // Atualiza o contador armazenado ANTES de tocar
            window.dash_clientside.ultimo_som_count = tocar_som_count;
            
            setTimeout(function() {
                var audio = document.getElementById('audio-chamada');
                
                if (audio) {
                    // Garante que o volume está normal
                    audio.volume = 1.0;
                    audio.pause();
                    audio.currentTime = 0;
                    audio.loop = false;
                    
                    // Event listener para parar quando terminar
                    audio.addEventListener('ended', function() {
                        console.log('🛑 Som terminou');
                        this.pause();
                        this.currentTime = 0;
                    }, { once: true });
                    
                    // Toca o som
                    var playPromise = audio.play();
                    
                    if (playPromise !== undefined) {
                        playPromise
                            .then(function() {
                                console.log('✅ Som tocado com sucesso! Volume:', audio.volume);
                            })
                            .catch(function(error) {
                                console.error('❌ Erro ao tocar som:', error);
                                console.log('💡 Dica: Clique novamente no botão "Habilitar Som"');
                            });
                    }
                } else {
                    console.error('❌ Elemento audio não encontrado!');
                }
            }, 300);
        } else if (tocar_som_count > 0 && tocar_som_count === window.dash_clientside.ultimo_som_count) {
            // Contador não mudou, não toca
            console.log('⏭️ Ignorando: contador não mudou (', tocar_som_count, ')');
        } else if (som_habilitado === false) {
            console.log('⚠️ Som desabilitado. Clique no botão para habilitar.');
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("store-tocar-som", "data", allow_duplicate=True),
    Input("store-tocar-som", "data"),
    State("store-som-habilitado", "data"),
    prevent_initial_call=True
)


# ==================== CALLBACKS TELA PÚBLICA ====================

@callback(
    Output("store-carousel-page", "data"),
    Input("interval-carousel", "n_intervals"),
    State("store-carousel-page", "data")
)
def rotacionar_carrossel(n, current_page):
    dados = carregar_dados()
    filas_ativas = [f for f in dados["filas"].values() if f["ativa"]]
    
    if len(filas_ativas) <= MAX_FILAS_POR_TELA:
        return 0
    
    total_pages = math.ceil(len(filas_ativas) / MAX_FILAS_POR_TELA)
    next_page = (current_page + 1) % total_pages
    return next_page


@callback(
    Output("filas-container", "children"),
    Output("carousel-indicators", "children"),
    Input("interval-refresh", "n_intervals"),
    Input("store-carousel-page", "data")
)
def atualizar_filas_publico(n, current_page):
    """Atualiza filas públicas com APENAS 2 seções e limites"""
    dados = carregar_dados()
    filas_ativas = [f for f in dados["filas"].values() if f["ativa"]]
    
    if not filas_ativas:
        return (
            html.Div([
                html.I(className="fas fa-inbox fa-5x text-muted mb-3"),
                html.H3("Nenhuma fila ativa", className="text-muted")
            ], className="text-center mt-5"),
            None
        )
    
    # Paginação
    total_pages = math.ceil(len(filas_ativas) / MAX_FILAS_POR_TELA)
    start_idx = current_page * MAX_FILAS_POR_TELA
    end_idx = start_idx + MAX_FILAS_POR_TELA
    filas_visiveis = filas_ativas[start_idx:end_idx]
    
    filas_cards = []
    
    for fila in filas_visiveis:
        # APLICAR LIMITES: 12 aguardando, 5 chamados
        aguardando = obter_pacientes_por_status(fila["id"], "aguardando")[:12]  # ✅ LIMITE 12
        chamados = obter_pacientes_por_status(fila["id"], "chamado")[:5]        # ✅ LIMITE 5
        
        # Contar totais para exibir
        total_aguardando = len(obter_pacientes_por_status(fila["id"], "aguardando"))
        total_chamados = len(obter_pacientes_por_status(fila["id"], "chamado"))
        
        # ✅ CORREÇÃO: Ajustar classes das colunas baseado no número de filas
        num_filas = len(filas_visiveis)
        if num_filas == 1:
            col_classes = "col-12 col-md-8 col-lg-6 mx-auto mb-4"
        elif num_filas == 2:
            col_classes = "col-12 col-md-6 mb-4"
        else:  # 3 ou mais filas
            col_classes = "col-12 col-md-6 col-lg-4 mb-4"
        
        card = html.Div([
            dbc.Card([
                dbc.CardHeader([
                    html.H3([
                        html.I(className="fas fa-list-ol me-2"),
                        fila["nome"]
                    ], className="mb-0 text-white")
                ], className="bg-info text-white"),
                
                dbc.CardBody([
                    # AGUARDANDO (máximo 20)
                    html.Div([
                        html.H5([
                            html.I(className="fas fa-hourglass-half me-2"),
                            f"Aguardando ({total_aguardando})"
                        ], className="text-warning mb-2"),
                        
                        # Alerta se há mais que 20
                        html.Div([
                            dbc.Alert(
                                f"⚠️ Mostrando 20 de {total_aguardando} pacientes",
                                color="warning",
                                className="py-2 mb-2 small"
                            ) if total_aguardando > 20 else None,
                            
                            html.Div([
                                criar_linha_paciente_publico(p, idx + 1) 
                                for idx, p in enumerate(aguardando)
                            ] if aguardando else [
                                html.P("Nenhum paciente", className="text-muted small")
                            ])
                        ])
                    ], className="mb-4 pb-4 border-bottom"),
                    
                    # CHAMADOS (máximo 5)
                    html.Div([
                        html.H5([
                            html.I(className="fas fa-phone me-2"),
                            f"Chamados ({total_chamados})"
                        ], className="text-primary mb-2"),
                        
                        html.Div([
                            dbc.Alert(
                                f"⚠️ Mostrando 5 de {total_chamados} pacientes",
                                color="info",
                                className="py-2 mb-2 small"
                            ) if total_chamados > 5 else None,
                            
                            html.Div([
                                criar_linha_paciente_publico(p, None, "chamado") 
                                for p in chamados
                            ] if chamados else [
                                html.P("Nenhum paciente", className="text-muted small")
                            ])
                        ])
                    ])
                    
                ], style={"minHeight": "400px"})  # Menor altura sem seção atendidos
            ], className="shadow-lg h-100")
        ], className=col_classes)
        
        filas_cards.append(card)
    
    # Indicadores
    indicators = None
    if total_pages > 1:
        indicator_dots = []
        for i in range(total_pages):
            dot_style = {
                "width": "15px",
                "height": "15px",
                "borderRadius": "50%",
                "display": "inline-block",
                "margin": "0 5px",
                "backgroundColor": "#007bff" if i == current_page else "#dee2e6",
                "transition": "all 0.3s ease"
            }
            indicator_dots.append(html.Span(style=dot_style))
        
        indicators = html.Div([
            html.Div(indicator_dots),
            html.P(f"Página {current_page + 1} de {total_pages}", className="text-muted mt-2 mb-0")
        ])
    
    # ✅ CORREÇÃO: Usar div com row ao invés de dbc.Row para melhor controle
    return html.Div(
        filas_cards, 
        className="row fade-in"
    ), indicators


def criar_linha_paciente_publico(paciente: Dict, posicao=None, status_tipo=None):
    """Cria linha de paciente para tela pública COM HORÁRIOS"""
    classif = obter_classificacao_segura(paciente)
    
    # Calcular idade
    idade = calcular_idade(paciente.get("data_nascimento", ""))
    try:
        dn = datetime.strptime(paciente["data_nascimento"], "%Y-%m-%d")
        dn_texto = f"{dn.strftime('%d/%m/%Y')} ({idade} anos)"
    except:
        dn_texto = paciente.get("data_nascimento", "N/A")
    
    # Badge de posição
    badge_posicao = html.Span(
        f"{posicao}º",
        className="badge bg-secondary me-2",
        style={"minWidth": "35px", "fontSize": "0.9rem"}
    ) if posicao else None
    
    # Badge de status COM HORÁRIO
    if status_tipo == "chamado":
        hora_chamada = formatar_hora(paciente.get("chamado_em", ""))
        badge_status = html.Span(
            f"🔔 CHAMADO {hora_chamada}", 
            className="badge bg-primary me-2"
        )
    elif status_tipo == "atendido":
        hora_atendimento = formatar_hora(paciente.get("atendido_em", ""))
        badge_status = html.Span(
            f"✓ {hora_atendimento}", 
            className="badge bg-success me-2"
        )
    else:
        badge_status = None
    
    return html.Div([
        html.Div([
            badge_posicao,
            badge_status,
            html.Span(paciente["nome"], className="fw-bold me-2", style={"fontSize": "0.9rem"}),
            html.Span(
                classif["label"].split("(")[0].strip(),
                className="badge me-2",
                style={"backgroundColor": classif["color"], "fontSize": "0.7rem"}
            ),
            html.Small(dn_texto, className="text-muted", style={"fontSize": "0.75rem"})
        ], className="d-flex align-items-center flex-wrap")
    ], className="py-2 border-bottom" if status_tipo != "atendido" else "py-1")


@callback(
    Output("clock", "children"),
    Input("interval-refresh", "n_intervals")
)
def atualizar_relogio(n):
    return datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

# ==================== PAINEL ADMINISTRATIVO ====================

def layout_admin():
    return html.Div([
        dbc.Navbar([
            dbc.Container([
                dbc.NavbarBrand([
                    html.I(className="fas fa-user-shield me-2"),
                    "Painel Administrativo"
                ], className="fs-4"),
                dbc.Nav([
                    # SELETOR DE TEMA NO ADMIN
                    dbc.NavItem([
                        html.Label("🎨 Tema:", className="text-white me-2 mb-0"),
                        dbc.Select(
                            id="select-tema-admin",
                            options=[
                                {"label": tema["nome"], "value": key}
                                for key, tema in TEMAS.items()
                            ],
                            value="bootstrap",
                            size="sm",
                            style={"width": "200px", "display": "inline-block"}
                        )
                    ], className="d-flex align-items-center me-3"),
                    
                    dbc.NavItem(
                        dbc.Button([
                            html.I(className="fas fa-tv me-2"),
                            "Tela Pública"
                        ], href="/", color="light", size="sm", className="me-2")
                    ),
                    dbc.NavItem(
                        dbc.Button([
                            html.I(className="fas fa-sign-out-alt me-2"),
                            "Sair"
                        ], id="btn-logout", color="danger", size="sm")
                    )
                ])
            ], fluid=True)
        ], color="dark", dark=True, className="mb-4"),
        
        dbc.Container([
            dbc.Tabs([
                dbc.Tab(label="📋 Gerenciar Filas", tab_id="tab-filas"),
                dbc.Tab(label="➕ Adicionar Paciente", tab_id="tab-adicionar"),
                dbc.Tab(label="🔔 Chamar Pacientes", tab_id="tab-chamar")
            ], id="tabs", active_tab="tab-filas", className="mb-4"),
            
            html.Div(id="tab-content"),
            
            dcc.Store(id='store-update-filas'),
            dcc.Store(id='store-update-pacientes'),
            dcc.Store(id='store-update-chamar')
            
        ], fluid=True)
    ])


@callback(
    Output("store-autenticado", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("btn-logout", "n_clicks"),
    prevent_initial_call=True
)
def fazer_logout(n_clicks):
    """Desautentica o usuário"""
    return False, "/login"


# ==================== CALLBACK PARA GERENCIAR TEMA (ADMIN + TELA PÚBLICA) ====================

@callback(
    Output("store-tema-selecionado", "data"),
    Input("select-tema-admin", "value"),
    prevent_initial_call=True
)
def salvar_tema_selecionado(tema_id):
    """Salva tema selecionado no admin"""
    return tema_id or "bootstrap"


# Callback clientside para aplicar tema dinamicamente EM TODAS AS PÁGINAS
app.clientside_callback(
    """
    function(tema_id) {
        if (!tema_id) tema_id = 'bootstrap';
        
        // Mapear temas para URLs do CDN
        const temas_urls = {
            'bootstrap': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
            'cerulean': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cerulean/bootstrap.min.css',
            'cosmo': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cosmo/bootstrap.min.css',
            'flatly': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/flatly/bootstrap.min.css',
            'journal': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/journal/bootstrap.min.css',
            'litera': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/litera/bootstrap.min.css',
            'lumen': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/lumen/bootstrap.min.css',
            'minty': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/minty/bootstrap.min.css',
            'pulse': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/pulse/bootstrap.min.css',
            'sandstone': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/sandstone/bootstrap.min.css',
            'simplex': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/simplex/bootstrap.min.css',
            'sketchy': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/sketchy/bootstrap.min.css',
            'spacelab': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/spacelab/bootstrap.min.css',
            'united': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/united/bootstrap.min.css',
            'yeti': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/yeti/bootstrap.min.css',
            'darkly': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/darkly/bootstrap.min.css',
            'cyborg': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cyborg/bootstrap.min.css',
            'slate': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/slate/bootstrap.min.css',
            'solar': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/solar/bootstrap.min.css',
            'superhero': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/superhero/bootstrap.min.css'
        };
        
        // Remove tema anterior
        const linkExistente = document.getElementById('tema-dinamico');
        if (linkExistente) {
            linkExistente.remove();
        }
        
        // Adiciona novo tema
        const link = document.createElement('link');
        link.id = 'tema-dinamico';
        link.rel = 'stylesheet';
        link.href = temas_urls[tema_id] || temas_urls['bootstrap'];
        document.head.appendChild(link);
        
        // Salva no localStorage
        localStorage.setItem('tema_fila', tema_id);
        console.log('🎨 Tema aplicado GLOBALMENTE:', tema_id);
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("store-tema-selecionado", "data", allow_duplicate=True),
    Input("store-tema-selecionado", "data"),
    prevent_initial_call=True
)


# ==================== CALLBACK PARA CARREGAR TEMA SALVO NA TELA PÚBLICA ====================

# Callback clientside para carregar tema salvo quando entrar na tela pública
app.clientside_callback(
    """
    function(pathname) {
        // Só executa na tela pública (pathname = "/")
        if (pathname === "/" || pathname === "") {
            // Carrega tema salvo do localStorage
            const temaSalvo = localStorage.getItem('tema_fila') || 'bootstrap';
            
            console.log('📺 Carregando tema na tela pública:', temaSalvo);
            
            // Mapear temas para URLs do CDN
            const temas_urls = {
                'bootstrap': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
                'cerulean': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cerulean/bootstrap.min.css',
                'cosmo': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cosmo/bootstrap.min.css',
                'flatly': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/flatly/bootstrap.min.css',
                'journal': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/journal/bootstrap.min.css',
                'litera': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/litera/bootstrap.min.css',
                'lumen': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/lumen/bootstrap.min.css',
                'minty': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/minty/bootstrap.min.css',
                'pulse': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/pulse/bootstrap.min.css',
                'sandstone': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/sandstone/bootstrap.min.css',
                'simplex': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/simplex/bootstrap.min.css',
                'sketchy': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/sketchy/bootstrap.min.css',
                'spacelab': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/spacelab/bootstrap.min.css',
                'united': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/united/bootstrap.min.css',
                'yeti': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/yeti/bootstrap.min.css',
                'darkly': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/darkly/bootstrap.min.css',
                'cyborg': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cyborg/bootstrap.min.css',
                'slate': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/slate/bootstrap.min.css',
                'solar': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/solar/bootstrap.min.css',
                'superhero': 'https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/superhero/bootstrap.min.css'
            };
            
            // Remove tema anterior
            const linkExistente = document.getElementById('tema-dinamico');
            if (linkExistente) {
                linkExistente.remove();
            }
            
            // Adiciona tema salvo
            const link = document.createElement('link');
            link.id = 'tema-dinamico';
            link.rel = 'stylesheet';
            link.href = temas_urls[temaSalvo] || temas_urls['bootstrap'];
            document.head.appendChild(link);
            
            console.log('✅ Tema carregado na tela pública:', temaSalvo);
            
            return window.dash_clientside.no_update;
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("container-publico", "style", allow_duplicate=True),
    Input("url", "pathname"),
    prevent_initial_call=True
)


# ==================== CALLBACK PARA CARREGAR TEMA SALVO NO ADMIN ====================

# Callback clientside para carregar tema salvo quando entrar no admin
app.clientside_callback(
    """
    function(pathname) {
        // Só executa no admin
        if (pathname === "/admin") {
            // Carrega tema salvo do localStorage
            const temaSalvo = localStorage.getItem('tema_fila') || 'bootstrap';
            
            console.log('⚙️ Carregando tema no admin:', temaSalvo);
            
            // Atualiza o select com o tema salvo
            setTimeout(function() {
                const selectTema = document.getElementById('select-tema-admin');
                if (selectTema) {
                    selectTema.value = temaSalvo;
                    // Dispara evento change para aplicar o tema
                    selectTema.dispatchEvent(new Event('change'));
                }
            }, 100);
            
            return window.dash_clientside.no_update;
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("store-autenticado", "data", allow_duplicate=True),
    Input("url", "pathname"),
    prevent_initial_call=True
)


@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "tab-filas":
        return render_gerenciar_filas()
    elif active_tab == "tab-adicionar":
        return render_adicionar_paciente()
    elif active_tab == "tab-chamar":
        return render_chamar_pacientes()


# ==================== TAB: GERENCIAR FILAS ====================

def render_gerenciar_filas():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("➕ Nova Fila", className="mb-0")),
                    dbc.CardBody([
                        dbc.Input(
                            id="input-nome-fila",
                            placeholder="Nome da fila (ex: Consultas, Exames)",
                            className="mb-3",
                            debounce=True
                        ),
                        dbc.Button("Criar Fila", id="btn-criar-fila", color="primary", className="w-100"),
                        html.Div(id="feedback-criar-fila", className="mt-2")
                    ])
                ], className="shadow mb-4")
            ], md=12, lg=4)
        ]),
        
        dbc.Row([
            dbc.Col([
                html.H4("📑 Filas Existentes", className="mb-3"),
                html.Div(id="lista-filas")
            ])
        ])
    ])


@callback(
    Output("feedback-criar-fila", "children"),
    Output("input-nome-fila", "value"),
    Output("store-update-filas", "data"),
    Input("btn-criar-fila", "n_clicks"),
    State("input-nome-fila", "value"),
    prevent_initial_call=True
)
def criar_fila(n_clicks, nome):
    if not nome or nome.strip() == "":
        return dbc.Alert("Digite um nome para a fila", color="warning"), dash.no_update, dash.no_update
    
    dados = carregar_dados()
    fila_id = f"fila{len(dados['filas']) + 1}"
    
    dados["filas"][fila_id] = {
        "id": fila_id,
        "nome": nome.strip(),
        "ativa": True,
        "criada_em": datetime.now().isoformat()
    }
    
    salvar_dados(dados)
    
    return (
        dbc.Alert(f"✅ Fila '{nome}' criada com sucesso!", color="success"),
        "",
        {"timestamp": datetime.now().isoformat()}
    )


@callback(
    Output("lista-filas", "children"),
    Input("store-update-filas", "data"),
    Input({"type": "btn-toggle-fila", "index": ALL}, "n_clicks"),
    Input({"type": "btn-delete-fila", "index": ALL}, "n_clicks"),
    Input("tabs", "active_tab")
)
def atualizar_lista_filas(update_data, toggle_clicks, delete_clicks, active_tab):
    if active_tab != "tab-filas":
        raise dash.exceptions.PreventUpdate
    
    dados = carregar_dados()
    
    if ctx.triggered_id and isinstance(ctx.triggered_id, dict):
        triggered_value = ctx.triggered[0]['value']
        if triggered_value and triggered_value > 0:
            fila_id = ctx.triggered_id["index"]
            
            if ctx.triggered_id["type"] == "btn-toggle-fila":
                dados["filas"][fila_id]["ativa"] = not dados["filas"][fila_id]["ativa"]
                salvar_dados(dados)
            
            elif ctx.triggered_id["type"] == "btn-delete-fila":
                del dados["filas"][fila_id]
                dados["pacientes"] = {
                    k: v for k, v in dados["pacientes"].items()
                    if v["fila_id"] != fila_id
                }
                salvar_dados(dados)
    
    if not dados["filas"]:
        return dbc.Alert("Nenhuma fila criada ainda", color="info")
    
    filas_cards = []
    
    for fila in dados["filas"].values():
        aguardando = len([p for p in dados["pacientes"].values() if p["fila_id"] == fila["id"] and p["status"] == "aguardando"])
        chamados = len([p for p in dados["pacientes"].values() if p["fila_id"] == fila["id"] and p["status"] == "chamado"])
        atendidos = len([p for p in dados["pacientes"].values() if p["fila_id"] == fila["id"] and p["status"] == "atendido"])
        
        card = dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.Div([
                        html.H5(fila["nome"], className="mb-1"),
                        html.Small(
                            f"🕐 Criada em: {datetime.fromisoformat(fila['criada_em']).strftime('%d/%m/%Y %H:%M')}",
                            className="text-muted"
                        )
                    ]),
                    html.Div([
                        dbc.Badge("Ativa" if fila["ativa"] else "Inativa", color="success" if fila["ativa"] else "secondary", className="me-2"),
                        dbc.Badge(f"{aguardando} aguardando", color="warning", className="me-2"),
                        dbc.Badge(f"{chamados} chamados", color="primary", className="me-2"),
                        dbc.Badge(f"{atendidos} atendidos", color="success")
                    ])
                ], className="d-flex justify-content-between align-items-start mb-3"),
                
                dbc.ButtonGroup([
                    dbc.Button(
                        [html.I(className=f"fas fa-{'pause' if fila['ativa'] else 'play'} me-1"),
                         "Desativar" if fila["ativa"] else "Ativar"],
                        id={"type": "btn-toggle-fila", "index": fila["id"]},
                        color="warning" if fila["ativa"] else "success",
                        size="sm"
                    ),
                    dbc.Button(
                        [html.I(className="fas fa-trash me-1"), "Excluir"],
                        id={"type": "btn-delete-fila", "index": fila["id"]},
                        color="danger",
                        size="sm"
                    )
                ], className="w-100")
            ])
        ], className="mb-3 shadow-sm")
        
        filas_cards.append(dbc.Col(card, md=6, lg=4))
    
    return dbc.Row(filas_cards)


# ==================== TAB: ADICIONAR PACIENTE ====================

def render_adicionar_paciente():
    dados = carregar_dados()
    filas_ativas = [f for f in dados["filas"].values() if f["ativa"]]
    
    if not filas_ativas:
        return dbc.Alert("⚠️ Nenhuma fila ativa. Crie e ative uma fila primeiro.", color="warning")
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("➕ Adicionar Paciente à Fila", className="mb-0")),
                dbc.CardBody([
                    dbc.Label("Nome do Paciente:"),
                    dbc.Input(
                        id="input-nome-paciente",
                        placeholder="Digite o nome completo",
                        className="mb-3",
                        debounce=True
                    ),
                    
                    dbc.Label("Data de Nascimento:"),
                    dbc.Input(
                        id="input-data-nascimento",
                        type="date",
                        className="mb-3"
                    ),
                    
                    html.Div(id="alerta-sugestao-prioridade"),
                    
                    dbc.Label("Fila de Atendimento:"),
                    dbc.Select(
                        id="select-fila-paciente",
                        options=[{"label": f["nome"], "value": f["id"]} for f in filas_ativas],
                        className="mb-3"
                    ),
                    
                    dbc.Label("Classificação:"),
                    dbc.RadioItems(
                        id="radio-classificacao",
                        options=[
                            {
                                "label": html.Span([
                                    html.Span("⬤", style={"color": info["color"], "fontSize": "1.2rem"}),
                                    f"  {info['label']}"
                                ]),
                                "value": key
                            }
                            for key, info in CLASSIFICACOES.items()
                        ],
                        value="normal",
                        className="mb-4"
                    ),
                    
                    dbc.Button(
                        [html.I(className="fas fa-user-plus me-2"), "Adicionar à Fila"],
                        id="btn-adicionar-paciente",
                        color="success",
                        size="lg",
                        className="w-100"
                    ),
                    
                    html.Div(id="feedback-adicionar-paciente", className="mt-3")
                ])
            ], className="shadow")
        ], md=12, lg=6, className="mx-auto")
    ])


@callback(
    Output("alerta-sugestao-prioridade", "children"),
    Output("radio-classificacao", "value"),
    Input("input-data-nascimento", "value"),
    prevent_initial_call=True
)
def sugerir_prioridade_ao_digitar_dn(data_nascimento):
    if not data_nascimento:
        return None, dash.no_update
    
    idade = calcular_idade(data_nascimento)
    classificacao_sugerida = sugerir_classificacao(data_nascimento)
    
    if idade > 79:
        mensagem = f"💡 Sugestão: Paciente com {idade} anos - Prioridade Legal 1 (>79 anos)"
        cor = "success"
    elif idade > 59:
        mensagem = f"💡 Sugestão: Paciente com {idade} anos - Prioridade Legal 2 (>59 anos)"
        cor = "warning"
    else:
        return None, "normal"
    
    alerta = dbc.Alert([
        html.Strong(mensagem),
        html.Br(),
        html.Small("A classificação foi ajustada automaticamente conforme a idade.")
    ], color=cor, className="mt-2")
    
    return alerta, classificacao_sugerida


@callback(
    Output("feedback-adicionar-paciente", "children"),
    Output("input-nome-paciente", "value"),
    Output("input-data-nascimento", "value"),
    Output("store-update-pacientes", "data"),
    Input("btn-adicionar-paciente", "n_clicks"),
    State("input-nome-paciente", "value"),
    State("input-data-nascimento", "value"),
    State("select-fila-paciente", "value"),
    State("radio-classificacao", "value"),
    prevent_initial_call=True
)
def adicionar_paciente_fila(n_clicks, nome, data_nascimento, fila_id, classificacao):
    if not nome or nome.strip() == "":
        return dbc.Alert("⚠️ Digite o nome do paciente", color="warning"), dash.no_update, dash.no_update, dash.no_update
    
    if not data_nascimento:
        return dbc.Alert("⚠️ Digite a data de nascimento", color="warning"), dash.no_update, dash.no_update, dash.no_update
    
    if not fila_id:
        return dbc.Alert("⚠️ Selecione uma fila", color="warning"), dash.no_update, dash.no_update, dash.no_update
    
    paciente_id = adicionar_paciente(fila_id, nome.strip(), data_nascimento, classificacao)
    dados = carregar_dados()
    fila_nome = dados["filas"][fila_id]["nome"]
    classif_info = CLASSIFICACOES[classificacao]
    
    idade = calcular_idade(data_nascimento)
    
    alert = dbc.Alert([
        html.H5("✅ Paciente adicionado com sucesso!", className="alert-heading"),
        html.Hr(),
        html.P([
            html.Strong("Nome: "), nome.strip(), html.Br(),
            html.Strong("Idade: "), f"{idade} anos", html.Br(),
            html.Strong("Fila: "), fila_nome, html.Br(),
            html.Strong("Classificação: "),
            html.Span(classif_info["label"], className="badge", style={"backgroundColor": classif_info["color"]}),
            html.Br(),
            html.Strong("Posição: "), f"{len(obter_pacientes_por_status(fila_id, 'aguardando'))}º"
        ])
    ], color="success")
    
    return alert, "", "", {"timestamp": datetime.now().isoformat()}


# ==================== TAB: CHAMAR PACIENTES ====================

def render_chamar_pacientes():
    dados = carregar_dados()
    filas_ativas = [f for f in dados["filas"].values() if f["ativa"]]
    
    if not filas_ativas:
        return dbc.Alert("⚠️ Nenhuma fila ativa.", color="warning")
    
    filas_cards = []
    
    for fila in filas_ativas:
        card = dbc.Card([
            dbc.CardHeader([
                html.H4([html.I(className="fas fa-list me-2"), fila["nome"]], className="mb-0")
            ], className="bg-primary text-white"),
            
            dbc.CardBody([
                # AGUARDANDO (com limite visual de 20)
                html.Div([
                    html.H5([
                        html.I(className="fas fa-hourglass-half me-2 text-warning"),
                        "Aguardando"
                    ], className="mb-3"),
                    html.Div(
                        id={"type": "fila-aguardando", "index": fila["id"]},
                        children=criar_lista_aguardando_admin(fila["id"])
                    )
                ], className="mb-4 pb-4 border-bottom"),
                
                # CHAMADOS (com limite visual de 5)
                html.Div([
                    html.H5([
                        html.I(className="fas fa-phone me-2 text-primary"),
                        "Chamados"
                    ], className="mb-3"),
                    html.Div(
                        id={"type": "fila-chamados", "index": fila["id"]},
                        children=criar_lista_chamados_admin(fila["id"])
                    )
                ])
                
                # ✅ REMOVIDA SEÇÃO DE ATENDIDOS
                
            ])
        ], className="shadow mb-4")
        
        filas_cards.append(card)
    
    return html.Div(filas_cards)


def criar_lista_aguardando_admin(fila_id: str):
    """Lista aguardando no admin com limite de 20 visíveis"""
    pacientes = obter_pacientes_por_status(fila_id, "aguardando")
    total_pacientes = len(pacientes)
    pacientes_visiveis = pacientes[:20]  # ✅ LIMITE 20
    
    if not pacientes:
        return dbc.Alert("✅ Nenhum paciente aguardando", color="info", className="text-center")
    
    # Alerta se há mais pacientes
    alerta = None
    if total_pacientes > 20:
        alerta = dbc.Alert(
            f"⚠️ Mostrando 20 de {total_pacientes} pacientes. Os demais aparecerão conforme o atendimento.",
            color="warning",
            className="mb-3"
        )
    
    items = []
    for idx, paciente in enumerate(pacientes_visiveis):
        classif = obter_classificacao_segura(paciente)
        idade = calcular_idade(paciente.get("data_nascimento", ""))
        
        try:
            dn = datetime.strptime(paciente["data_nascimento"], "%Y-%m-%d")
            dn_texto = f"{dn.strftime('%d/%m/%Y')} ({idade} anos)"
        except:
            dn_texto = paciente.get("data_nascimento", "N/A")
        
        item = dbc.ListGroupItem([
            html.Div([
                html.Div([
                    html.H6([
                        html.Span(f"{idx + 1}º", className="badge bg-secondary me-2"),
                        paciente["nome"]
                    ], className="mb-1"),
                    html.Div([
                        html.Span(
                            classif["label"].split("(")[0].strip(), 
                            className="badge me-2", 
                            style={"backgroundColor": classif["color"]}
                        ),
                        html.Small(f"DN: {dn_texto}", className="text-muted")
                    ])
                ], style={"flex": "1"}),
                
                dbc.ButtonGroup([
                    dbc.Button(
                        [html.I(className="fas fa-phone me-1"), "Chamar"],
                        id={"type": "btn-chamar", "index": paciente["id"]},
                        color="success",
                        size="lg"
                    ),
                    dbc.Button(
                        html.I(className="fas fa-times"),
                        id={"type": "btn-remover", "index": paciente["id"]},
                        color="danger",
                        size="lg"
                    )
                ])
            ], className="d-flex justify-content-between align-items-center")
        ])
        items.append(item)
    
    return html.Div([
        alerta,
        dbc.ListGroup(items)
    ])


def criar_lista_chamados_admin(fila_id: str):
    """Lista chamados no admin com limite de 5 visíveis"""
    pacientes = obter_pacientes_por_status(fila_id, "chamado")
    total_pacientes = len(pacientes)
    pacientes_visiveis = pacientes[:5]  # ✅ LIMITE 5
    
    if not pacientes:
        return dbc.Alert("Nenhum paciente chamado no momento", color="info", className="text-center")
    
    # Alerta se há mais pacientes
    alerta = None
    if total_pacientes > 5:
        alerta = dbc.Alert(
            f"⚠️ Mostrando 5 de {total_pacientes} pacientes chamados.",
            color="info",
            className="mb-3"
        )
    
    items = []
    for paciente in pacientes_visiveis:
        classif = obter_classificacao_segura(paciente)
        idade = calcular_idade(paciente.get("data_nascimento", ""))
        
        try:
            dn = datetime.strptime(paciente["data_nascimento"], "%Y-%m-%d")
            dn_texto = f"{dn.strftime('%d/%m/%Y')} ({idade} anos)"
        except:
            dn_texto = paciente.get("data_nascimento", "N/A")
        
        hora_chamada = formatar_hora(paciente.get("chamado_em", ""))
        
        item = dbc.ListGroupItem([
            html.Div([
                html.Div([
                    html.H6([
                        html.Span("🔔", className="me-2"),
                        paciente["nome"],
                        html.Span(f" - Chamado às {hora_chamada}", className="text-primary ms-2 fw-normal small")
                    ], className="mb-1"),
                    html.Div([
                        html.Span(
                            classif["label"].split("(")[0].strip(), 
                            className="badge me-2", 
                            style={"backgroundColor": classif["color"]}
                        ),
                        html.Small(f"DN: {dn_texto}", className="text-muted")
                    ])
                ], style={"flex": "1"}),
                
                dbc.ButtonGroup([
                    dbc.Button(
                        [html.I(className="fas fa-check me-1"), "Atendido"],
                        id={"type": "btn-atendido", "index": paciente["id"]},
                        color="primary",
                        size="lg"
                    ),
                    dbc.Button(
                        html.I(className="fas fa-times"),
                        id={"type": "btn-remover", "index": paciente["id"]},
                        color="danger",
                        size="lg"
                    )
                ])
            ], className="d-flex justify-content-between align-items-center")
        ], className="border-primary")
        items.append(item)
    
    return html.Div([
        alerta,
        dbc.ListGroup(items)
    ])


@callback(
    Output("store-update-chamar", "data"),
    Input({"type": "btn-chamar", "index": ALL}, "n_clicks"),
    Input({"type": "btn-atendido", "index": ALL}, "n_clicks"),
    Input({"type": "btn-remover", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def processar_acao_paciente(chamar_clicks, atendido_clicks, remover_clicks):
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    
    if not isinstance(ctx.triggered_id, dict):
        raise dash.exceptions.PreventUpdate
    
    triggered_value = ctx.triggered[0]['value']
    
    if triggered_value is None or triggered_value == 0:
        raise dash.exceptions.PreventUpdate
    
    dados = carregar_dados()
    paciente_id = ctx.triggered_id["index"]
    
    if paciente_id not in dados["pacientes"]:
        raise dash.exceptions.PreventUpdate
    
    if ctx.triggered_id["type"] == "btn-chamar":
        if dados["pacientes"][paciente_id]["status"] != "aguardando":
            raise dash.exceptions.PreventUpdate
        
        dados["pacientes"][paciente_id]["status"] = "chamado"
        dados["pacientes"][paciente_id]["chamado_em"] = datetime.now().isoformat()
        
        dados["historico"].append({
            "paciente_id": paciente_id,
            "nome": dados["pacientes"][paciente_id]["nome"],
            "fila_id": dados["pacientes"][paciente_id]["fila_id"],
            "acao": "chamado",
            "timestamp": datetime.now().isoformat()
        })
    
    elif ctx.triggered_id["type"] == "btn-atendido":
        if dados["pacientes"][paciente_id]["status"] != "chamado":
            raise dash.exceptions.PreventUpdate
        
        dados["pacientes"][paciente_id]["status"] = "atendido"
        dados["pacientes"][paciente_id]["atendido_em"] = datetime.now().isoformat()
        
        dados["historico"].append({
            "paciente_id": paciente_id,
            "nome": dados["pacientes"][paciente_id]["nome"],
            "fila_id": dados["pacientes"][paciente_id]["fila_id"],
            "acao": "atendido",
            "timestamp": datetime.now().isoformat()
        })
    
    elif ctx.triggered_id["type"] == "btn-remover":
        del dados["pacientes"][paciente_id]
    
    salvar_dados(dados)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "fila_id": dados["pacientes"].get(paciente_id, {}).get("fila_id"),
        "acao": ctx.triggered_id["type"]
    }


@callback(
    Output({"type": "fila-aguardando", "index": ALL}, "children"),
    Output({"type": "fila-chamados", "index": ALL}, "children"),
    # ✅ REMOVIDO: Output para fila-atendidos
    Input("store-update-chamar", "data"),
    Input("tabs", "active_tab"),
    State({"type": "fila-aguardando", "index": ALL}, "id")
)
def atualizar_listas_chamar_sem_atendidos(update_data, active_tab, fila_ids):
    """Atualiza listas SEM seção de atendidos"""
    if active_tab != "tab-chamar":
        raise dash.exceptions.PreventUpdate
    
    if not update_data and ctx.triggered_id != "tabs":
        raise dash.exceptions.PreventUpdate
    
    aguardando_outputs = []
    chamados_outputs = []
    # ✅ REMOVIDO: atendidos_outputs
    
    for fila_dict in fila_ids:
        fila_id = fila_dict["index"]
        aguardando_outputs.append(criar_lista_aguardando_admin(fila_id))
        chamados_outputs.append(criar_lista_chamados_admin(fila_id))
        # ✅ REMOVIDO: atendidos_outputs.append(...)
    
    return aguardando_outputs, chamados_outputs
    # ✅ REMOVIDO: , atendidos_outputs


# ==================== ROTEAMENTO ====================

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('store-autenticado', 'data')
)
def display_page(pathname, autenticado):
    if pathname == '/login':
        return layout_login()
    elif pathname == '/admin':
        if autenticado:
            return layout_admin()
        else:
            return layout_login()
    else:
        return layout_publico()


# ==================== CSS DINÂMICO ====================

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            .animate-pulse {
                animation: pulse 2s infinite;
            }
            
            @keyframes ring {
                0%, 100% { transform: rotate(-15deg); }
                50% { transform: rotate(15deg); }
            }
            .animate-ring {
                animation: ring 0.5s ease-in-out infinite;
            }
            
            .fade-in {
                animation: fadeIn 0.5s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @media (max-width: 768px) {
                .fs-5 { font-size: 1rem !important; }
                .fs-4 { font-size: 1.1rem !important; }
                h3 { font-size: 1.3rem !important; }
                h4 { font-size: 1.2rem !important; }
            }
            
            input:focus, select:focus {
                box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25) !important;
            }
            
            @media (max-width: 768px) {
                .btn-lg {
                    padding: 1rem 1.5rem;
                    font-size: 1.1rem;
                }
            }
            
            .modal-content {
                border: 5px solid #ffc107;
                box-shadow: 0 0 30px rgba(255, 193, 7, 0.5);
            }
            
            audio {
                loop: none !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


# ==================== EXECUÇÃO ====================

if __name__ == '__main__':
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("⚠️  ATENÇÃO: Coloque o arquivo 'som.mp3' na pasta 'assets/'")
        print("⚠️  ATENÇÃO: Coloque o arquivo 'logo.jpg' na pasta 'assets/'")
    
    print("🔄 Verificando dados antigos...")
    migrar_dados_antigos()
    
    print("\n" + "="*50)
    print("🔐 SENHA DO ADMIN: 6105/*")
    print("📁 ARQUIVOS NECESSÁRIOS:")
    print("   - assets/som.mp3 (arquivo de som para chamadas)")
    print("   - assets/logo.jpg (logo da empresa)")
    print("="*50 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8053

    )

