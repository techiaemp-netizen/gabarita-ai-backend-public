from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
from .services.chatgpt_service import chatgpt_service
from .routes.questoes import CONTEUDOS_EDITAL
from .routes.signup import signup_bp
from .routes.questoes import questoes_bp
from .routes.planos import planos_bp
from .routes.jogos import jogos_bp
from .routes.news import news_bp
from .routes.opcoes import opcoes_bp

app = Flask(__name__)
# Configuração CORS mais permissiva para resolver problemas de autenticação
CORS(app, 
     origins='*',  # Permitir todas as origens temporariamente
     allow_headers=['Content-Type', 'Authorization', 'Accept'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     supports_credentials=False)  # Desabilitar credentials para evitar problemas de autenticação

# Registrar blueprints
app.register_blueprint(signup_bp, url_prefix='/api/auth')
app.register_blueprint(questoes_bp, url_prefix='/api/questoes')
app.register_blueprint(planos_bp, url_prefix='/api')
app.register_blueprint(jogos_bp, url_prefix='/api/jogos')
app.register_blueprint(news_bp, url_prefix='/api')
app.register_blueprint(opcoes_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def root():
    """Rota raiz da API"""
    return jsonify({
        'message': 'Gabarita.AI Backend API',
        'version': '1.0.0',
        'status': 'online',
        'endpoints': {
            'health': '/health',
            'auth': '/api/auth/*',
            'questoes': '/api/questoes/*',
            'planos': '/api/planos',
            'jogos': '/api/jogos/*',
            'opcoes': '/api/opcoes/*'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando corretamente',
        'timestamp': str(datetime.now())
    })

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_endpoint():
    """Endpoint de teste público para verificar conectividade"""
    if request.method == 'OPTIONS':
        # Resposta para preflight CORS
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response
    
    return jsonify({
        'status': 'success',
        'message': 'Endpoint de teste funcionando',
        'timestamp': str(datetime.now()),
        'cors_enabled': True
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
