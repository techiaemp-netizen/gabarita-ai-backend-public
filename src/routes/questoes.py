from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

questoes_bp = Blueprint('questoes', __name__)

# Mapeamento de conteúdos por cargo e bloco com flag de conhecimentos
CONTEUDOS_EDITAL = {
    # Bloco 1 - Seguridade Social: Saúde, Assistência Social e Previdência Social
    'Enfermeiro': {
        'Bloco 1 - Seguridade Social': {
            'conhecimentos_especificos': [
                'Conceito, evolução legislativa e Constituição de 1988',
                'Financiamento, orçamento e Lei 8.212/1991',
                'História e legislação da saúde no Brasil',
                'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
                'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
                'Determinantes do processo saúde-doença',
                'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
                'Proteção social básica, especial e benefícios eventuais',
                'Avaliação da deficiência e legislação específica',
                'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
                'Regime Geral e Próprio de Previdência Social',
                'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
                'Legislação, perícia, acompanhamento médico, promoção à saúde',
                'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
            ],
            'conhecimentos_gerais': [
                'Desafios do Estado de Direito',
                'Políticas públicas',
                'Ética e integridade',
                'Diversidade e inclusão na sociedade',
                'Administração pública federal',
                'Trabalho e tecnologia'
            ]
        }
    },
    'Médico': {
        'Bloco 1 - Seguridade Social': {
            'conhecimentos_especificos': [
                'Conceito, evolução legislativa e Constituição de 1988',
                'Financiamento, orçamento e Lei 8.212/1991',
                'História e legislação da saúde no Brasil',
                'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
                'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
                'Determinantes do processo saúde-doença',
                'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
                'Proteção social básica, especial e benefícios eventuais',
                'Avaliação da deficiência e legislação específica',
                'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
                'Regime Geral e Próprio de Previdência Social',
                'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
                'Legislação, perícia, acompanhamento médico, promoção à saúde',
                'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
            ],
            'conhecimentos_gerais': [
                'Desafios do Estado de Direito',
                'Políticas públicas',
                'Ética e integridade',
                'Diversidade e inclusão na sociedade',
                'Administração pública federal',
                'Trabalho e tecnologia'
            ]
        }
    },
    'Assistente Social': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Nutricionista': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Psicólogo': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Pesquisador': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Tecnologista': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Analista do Seguro Social': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Biólogo': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Farmacêutico': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Fisioterapeuta': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Fonoaudiólogo': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    'Terapeuta Ocupacional': {
        'Bloco 1 - Seguridade Social': [
            'Conceito, evolução legislativa e Constituição de 1988',
            'Financiamento, orçamento e Lei 8.212/1991',
            'História e legislação da saúde no Brasil',
            'Sistema Único de Saúde (SUS): estrutura, organização, modelos assistenciais',
            'Vigilância em saúde, promoção e prevenção, emergências sanitárias',
            'Determinantes do processo saúde-doença',
            'Histórico, políticas públicas, Lei 8.742/1993 (LOAS), PNAS 2004, SUAS',
            'Proteção social básica, especial e benefícios eventuais',
            'Avaliação da deficiência e legislação específica',
            'Noções de direito previdenciário, CF/88, Lei 8.213/1991',
            'Regime Geral e Próprio de Previdência Social',
            'Benefícios, benefícios eventuais, qualidade de segurado, avaliação biopsicossocial',
            'Legislação, perícia, acompanhamento médico, promoção à saúde',
            'Acidentes do trabalho, doenças relacionadas, riscos ocupacionais e legislações aplicáveis'
        ]
    },
    
    # Bloco 2 - Cultura e Educação
    'Técnico em Comunicação Social': {
        'Bloco 2 - Cultura e Educação': [
            'Lei de Acesso à Informação, LGPD, políticas de comunicação, mídias digitais',
            'LDB, Constituição, Plano Nacional de Educação, educação básica e superior, EAD, ODS',
            'Sistema Nacional de Cultura, políticas e legislação patrimonial, direitos culturais, instrumentos de fomento (ex: Lei Rouanet, Lei Paulo Gustavo)',
            'Fundamentos, métodos qualitativos e quantitativos, ciclo da pesquisa, ética em pesquisa',
            'Construção e análise de indicadores, monitoramento, métodos quantitativos e Big Data'
        ]
    },
    'Técnico em Documentação': {
        'Bloco 2 - Cultura e Educação': [
            'Lei de Acesso à Informação, LGPD, políticas de comunicação, mídias digitais',
            'LDB, Constituição, Plano Nacional de Educação, educação básica e superior, EAD, ODS',
            'Sistema Nacional de Cultura, políticas e legislação patrimonial, direitos culturais, instrumentos de fomento (ex: Lei Rouanet, Lei Paulo Gustavo)',
            'Fundamentos, métodos qualitativos e quantitativos, ciclo da pesquisa, ética em pesquisa',
            'Construção e análise de indicadores, monitoramento, métodos quantitativos e Big Data'
        ]
    },
    'Técnico em Assuntos Culturais': {
        'Bloco 2 - Cultura e Educação': [
            'Lei de Acesso à Informação, LGPD, políticas de comunicação, mídias digitais',
            'LDB, Constituição, Plano Nacional de Educação, educação básica e superior, EAD, ODS',
            'Sistema Nacional de Cultura, políticas e legislação patrimonial, direitos culturais, instrumentos de fomento (ex: Lei Rouanet, Lei Paulo Gustavo)',
            'Fundamentos, métodos qualitativos e quantitativos, ciclo da pesquisa, ética em pesquisa',
            'Construção e análise de indicadores, monitoramento, métodos quantitativos e Big Data'
        ]
    },
    'Analista Cultural': {
        'Bloco 2 - Cultura e Educação': [
            'Lei de Acesso à Informação, LGPD, políticas de comunicação, mídias digitais',
            'LDB, Constituição, Plano Nacional de Educação, educação básica e superior, EAD, ODS',
            'Sistema Nacional de Cultura, políticas e legislação patrimonial, direitos culturais, instrumentos de fomento (ex: Lei Rouanet, Lei Paulo Gustavo)',
            'Fundamentos, métodos qualitativos e quantitativos, ciclo da pesquisa, ética em pesquisa',
            'Construção e análise de indicadores, monitoramento, métodos quantitativos e Big Data'
        ]
    },
    'Técnico em Assuntos Educacionais': {
        'Bloco 2 - Cultura e Educação': [
            'Lei de Acesso à Informação, LGPD, políticas de comunicação, mídias digitais',
            'LDB, Constituição, Plano Nacional de Educação, educação básica e superior, EAD, ODS',
            'Sistema Nacional de Cultura, políticas e legislação patrimonial, direitos culturais, instrumentos de fomento (ex: Lei Rouanet, Lei Paulo Gustavo)',
            'Fundamentos, métodos qualitativos e quantitativos, ciclo da pesquisa, ética em pesquisa',
            'Construção e análise de indicadores, monitoramento, métodos quantitativos e Big Data'
        ]
    },
    
    # Bloco 3 - Ciências, Dados e Tecnologia
    'Especialista em Geologia e Geofísica': {
        'Bloco 3 - Ciências, Dados e Tecnologia': [
            'Fundamentos, paradigmas de inovação, impactos sociais, ética e popularização científica',
            'Sistema Nacional de CT&I, marco legal, instrumentos de fomento, governança, indicadores de inovação, ODS',
            'Condução de projetos (iniciação, execução, monitoramento, encerramento), métodos ágeis (Scrum, Kanban), modelos institucionais',
            'Noções de TICs, ciência de dados, inteligência artificial, uso de dados na gestão pública, LGPD, interoperabilidade, dados abertos',
            'Práticas de pesquisa, classificação, abordagens qualitativas e quantitativas, estruturação de projetos, normas técnicas'
        ]
    },
    'Analista de Tecnologia Militar': {
        'Bloco 3 - Ciências, Dados e Tecnologia': [
            'Fundamentos, paradigmas de inovação, impactos sociais, ética e popularização científica',
            'Sistema Nacional de CT&I, marco legal, instrumentos de fomento, governança, indicadores de inovação, ODS',
            'Condução de projetos (iniciação, execução, monitoramento, encerramento), métodos ágeis (Scrum, Kanban), modelos institucionais',
            'Noções de TICs, ciência de dados, inteligência artificial, uso de dados na gestão pública, LGPD, interoperabilidade, dados abertos',
            'Práticas de pesquisa, classificação, abordagens qualitativas e quantitativas, estruturação de projetos, normas técnicas'
        ]
    },
    'Analista de Ciência e Tecnologia': {
        'Bloco 3 - Ciências, Dados e Tecnologia': [
            'Fundamentos, paradigmas de inovação, impactos sociais, ética e popularização científica',
            'Sistema Nacional de CT&I, marco legal, instrumentos de fomento, governança, indicadores de inovação, ODS',
            'Condução de projetos (iniciação, execução, monitoramento, encerramento), métodos ágeis (Scrum, Kanban), modelos institucionais',
            'Noções de TICs, ciência de dados, inteligência artificial, uso de dados na gestão pública, LGPD, interoperabilidade, dados abertos',
            'Práticas de pesquisa, classificação, abordagens qualitativas e quantitativas, estruturação de projetos, normas técnicas'
        ]
    },
    
    # Bloco 4 - Engenharias e Arquitetura
    'Especialista em Regulação de Petróleo': {
        'Bloco 4 - Engenharias e Arquitetura': [
            'Planejamento, orçamento, licitação, execução, controle de obras, manutenção, segurança, qualidade',
            'Políticas urbanas e regionais, regularização fundiária, cartografia, urbanismo, geografia urbana',
            'Elaboração de projetos, acessibilidade, sustentabilidade, patologias em edificações, conforto ambiental',
            'Políticas agrícolas, manejo sustentável, certificação, pesca e aquicultura, biotecnologia aplicada',
            'Gestão e licenciamento ambiental, mudanças climáticas, economia ambiental, gestão de resíduos, patrimônios, políticas energéticas, recursos hídricos'
        ]
    },
    'Engenheiro de Tecnologia Militar': {
        'Bloco 4 - Engenharias e Arquitetura': [
            'Planejamento, orçamento, licitação, execução, controle de obras, manutenção, segurança, qualidade',
            'Políticas urbanas e regionais, regularização fundiária, cartografia, urbanismo, geografia urbana',
            'Elaboração de projetos, acessibilidade, sustentabilidade, patologias em edificações, conforto ambiental',
            'Políticas agrícolas, manejo sustentável, certificação, pesca e aquicultura, biotecnologia aplicada',
            'Gestão e licenciamento ambiental, mudanças climáticas, economia ambiental, gestão de resíduos, patrimônios, políticas energéticas, recursos hídricos'
        ]
    },
    'Arquiteto': {
        'Bloco 4 - Engenharias e Arquitetura': [
            'Planejamento, orçamento, licitação, execução, controle de obras, manutenção, segurança, qualidade',
            'Políticas urbanas e regionais, regularização fundiária, cartografia, urbanismo, geografia urbana',
            'Elaboração de projetos, acessibilidade, sustentabilidade, patologias em edificações, conforto ambiental',
            'Políticas agrícolas, manejo sustentável, certificação, pesca e aquicultura, biotecnologia aplicada',
            'Gestão e licenciamento ambiental, mudanças climáticas, economia ambiental, gestão de resíduos, patrimônios, políticas energéticas, recursos hídricos'
        ]
    },
    'Engenheiro': {
        'Bloco 4 - Engenharias e Arquitetura': [
            'Planejamento, orçamento, licitação, execução, controle de obras, manutenção, segurança, qualidade',
            'Políticas urbanas e regionais, regularização fundiária, cartografia, urbanismo, geografia urbana',
            'Elaboração de projetos, acessibilidade, sustentabilidade, patologias em edificações, conforto ambiental',
            'Políticas agrícolas, manejo sustentável, certificação, pesca e aquicultura, biotecnologia aplicada',
            'Gestão e licenciamento ambiental, mudanças climáticas, economia ambiental, gestão de resíduos, patrimônios, políticas energéticas, recursos hídricos'
        ]
    },
    'Engenheiro Agrônomo': {
        'Bloco 4 - Engenharias e Arquitetura': [
            'Planejamento, orçamento, licitação, execução, controle de obras, manutenção, segurança, qualidade',
            'Políticas urbanas e regionais, regularização fundiária, cartografia, urbanismo, geografia urbana',
            'Elaboração de projetos, acessibilidade, sustentabilidade, patologias em edificações, conforto ambiental',
            'Políticas agrícolas, manejo sustentável, certificação, pesca e aquicultura, biotecnologia aplicada',
            'Gestão e licenciamento ambiental, mudanças climáticas, economia ambiental, gestão de resíduos, patrimônios, políticas energéticas, recursos hídricos'
        ]
    },
    
    # Bloco 5 - Administração
    'Analista Técnico-Administrativo': {
        'Bloco 5 - Administração': [
            'Gestão Governamental e Governança Pública: Estratégia, Pessoas, Projetos e Processos',
            'Gestão Governamental e Governança Pública: Riscos, Inovação, Participação, Coordenação e Patrimônio',
            'Políticas Públicas: Ciclo, formulação e avaliação',
            'Administração Financeira e Orçamentária, Contabilidade Pública e Compras na Administração Pública',
            'Transparência, Proteção de Dados, Comunicação e Atendimento ao Cidadão'
        ]
    },
    'Contador': {
        'Bloco 5 - Administração': [
            'Gestão Governamental e Governança Pública: Estratégia, Pessoas, Projetos e Processos',
            'Gestão Governamental e Governança Pública: Riscos, Inovação, Participação, Coordenação e Patrimônio',
            'Políticas Públicas: Ciclo, formulação e avaliação',
            'Administração Financeira e Orçamentária, Contabilidade Pública e Compras na Administração Pública',
            'Transparência, Proteção de Dados, Comunicação e Atendimento ao Cidadão'
        ]
    },
    
    # Bloco 6 - Desenvolvimento Socioeconômico
    'Analista Técnico de Desenvolvimento Socioeconômico': {
        'Bloco 6 - Desenvolvimento Socioeconômico': [
            'Desenvolvimento, Sustentabilidade e Inclusão',
            'Desenvolvimento Produtivo e Regional no Brasil',
            'Gestão Estratégica e Regulação',
            'Desenvolvimento Socioeconômico no Brasil (histórico e contemporâneo)',
            'Desigualdades e Dinâmicas Socioeconômicas'
        ]
    },
    'Especialista em Regulação de Petróleo e Derivados': {
        'Bloco 6 - Desenvolvimento Socioeconômico': [
            'Desenvolvimento, Sustentabilidade e Inclusão',
            'Desenvolvimento Produtivo e Regional no Brasil',
            'Gestão Estratégica e Regulação',
            'Desenvolvimento Socioeconômico no Brasil (histórico e contemporâneo)',
            'Desigualdades e Dinâmicas Socioeconômicas'
        ]
    },
    'Especialista em Regulação da Atividade Cinematográfica': {
        'Bloco 6 - Desenvolvimento Socioeconômico': [
            'Desenvolvimento, Sustentabilidade e Inclusão',
            'Desenvolvimento Produtivo e Regional no Brasil',
            'Gestão Estratégica e Regulação',
            'Desenvolvimento Socioeconômico no Brasil (histórico e contemporâneo)',
            'Desigualdades e Dinâmicas Socioeconômicas'
        ]
    },
    
    # Bloco 7 - Justiça e Defesa
    'Analista Técnico de Justiça e Defesa': {
        'Bloco 7 - Justiça e Defesa': [
            'Gestão Governamental e Métodos Aplicados',
            'Políticas de Segurança e Defesa – Ambiente Internacional e Tecnologias Emergentes',
            'Políticas de Segurança e Defesa – Ambiente Nacional e Questões Emergentes',
            'Políticas de Segurança Pública',
            'Políticas de Justiça e Cidadania'
        ]
    },
    
    # Bloco 8 - Intermediário - Saúde
    'Técnico em Atividades Médico-Hospitalares': {
        'Bloco 8 - Intermediário - Saúde': {
            'conhecimentos_especificos': [
                'Saúde'
            ],
            'conhecimentos_gerais': [
                'Língua Portuguesa',
                'Matemática',
                'Noções de Direito',
                'Realidade Brasileira'
            ]
        }
    },
    'Técnico de Enfermagem': {
        'Bloco 8 - Intermediário - Saúde': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde'
        ]
    },
    'Técnico em Pesquisa e Investigação Biomédica': {
        'Bloco 8 - Intermediário - Saúde': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde'
        ]
    },
    'Técnico em Radiologia': {
        'Bloco 8 - Intermediário - Saúde': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde'
        ]
    },
    
    # Bloco 9 - Intermediário - Regulação
    'Técnico em Regulação de Aviação Civil': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Atividades de Mineração': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Regulação de Petróleo': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Regulação de Saúde Suplementar': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Regulação de Telecomunicações': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Regulação de Transportes Aquaviários': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Regulação de Transportes Terrestres': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Regulação e Vigilância Sanitária': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    },
    'Técnico em Regulação da Atividade Cinematográfica': {
        'Bloco 9 - Intermediário - Regulação': [
            'Língua Portuguesa',
            'Matemática',
            'Noções de Direito',
            'Realidade Brasileira',
            'Saúde',
            'Regulação e Agências Reguladoras'
        ]
    }
}

@questoes_bp.route('/test', methods=['GET'])
def test_questoes():
    """Endpoint de teste para verificar se o módulo está funcionando"""
    return jsonify({
        'sucesso': True,
        'mensagem': 'Módulo de questões funcionando',
        'total_cargos': len(CONTEUDOS_EDITAL),
        'cargos_exemplo': list(CONTEUDOS_EDITAL.keys())[:5]
    }), 200
