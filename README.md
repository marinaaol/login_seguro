# 🔐 Sistema de Login Seguro com Flask

Sistema completo de autenticação de utilizadores desenvolvido em Flask, implementando as melhores práticas de segurança para proteção de dados e controle de acesso.

![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Security](https://img.shields.io/badge/Security-High-red)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Guia de Uso](#guia-de-uso)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Funcionalidades Práticas](#funcionalidades-práticas)
- [Segurança](#segurança)
- [Contribuições](#contribuições)
- [Licença](#licença)

## 🎯 Visão Geral

Este projeto implementa uma área reservada para colaboradores de uma empresa, oferecendo um sistema completo de autenticação com registo, login, dashboard protegido e gestão de sessões. Desenvolvido com foco em segurança, o sistema protege dados sensíveis utilizando técnicas modernas de hashing e gestão de sessões.

## ⭐ Funcionalidades

### Funcionalidades Principais
- ✅ Registo de novos utilizadores
- ✅ Autenticação segura (login/logout)
- ✅ Página dashboard protegida
- ✅ Gestão de sessões de utilizador

### Funcionalidades Avançadas (Níveis Extra)
- 📝 **Nível 1**: Campos adicionais (Nome Completo, Email)
- 🔄 **Nível 2**: Confirmação de password no registo
- 🚫 **Nível 3**: Bloqueio após 3 tentativas de login falhadas
- 🔑 **Nível 4**: Sistema de recuperação de password por email

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.8+**: Linguagem principal de desenvolvimento
- **Flask 2.3.2**: Micro-framework web para Python
- **Werkzeug**: Biblioteca de segurança para hashing de passwords
- **SQLite3**: Base de dados relacional leve e integrada

### Frontend
- **HTML5**: Estrutura das páginas
- **CSS3**: Estilização e design responsivo
- **JavaScript**: Validações cliente-side
- **Jinja2**: Motor de templates do Flask

### Ferramentas de Desenvolvimento
- **Git**: Controlo de versão
- **GitHub**: Hospedagem do código-fonte
- **Visual Studio Code**: IDE de desenvolvimento

## 📁 Estrutura do Projeto
 
* login_seguro /
  * app.py # Aplicação principal Flask
  * requirements.txt # Dependências do projeto
  * README.md # Documentação do projeto
  * utilizadores.db # Base de dados SQLite 
* templates/ 
    * Templates HTML
    * login.html # Página de login
    * registo.html # Página de registo
    * dashboard.html # Dashboard protegido
    * recuperar_password.html # Recuperação de password
    * redefinir_password.html # Redefinição de password

## 📦 Pré-requisitos

Antes de executar o projeto, verifique se tem instalado:

- **Python 3.8 ou superior**
  ```bash
  python --version

  pip (gestor de pacotes Python)
  pip --version

  Git (opcional, para clonar o repositório)
  git --version

  🚀 Instalação e Execução

Método 1: Clonando o Repositório (Recomendado)

1) Clone o repositório\
git clone https://github.com/marinaaol/login-seguro-flask.git\
cd login-seguro-flask


2) Crie um ambiente virtual (opcional, mas recomendado)

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv\
source venv/bin/activate

3) Instale as dependências\
pip install -r requirements.txt

4) Execute a aplicação\
python app.py

5) Acesse no navegador\
http://127.0.0.1:5000


Método 2: Instalação Manual

1) Crie a pasta do projeto\
mkdir login_seguro\
cd login_seguro\
mkdir templates

2) Instale o Flask\
pip install flask

3) Copie os arquivos do projeto\
Copie app.py para a pasta raiz\
Copie os arquivos HTML para a pasta templates/

4) Execute a aplicação

Configuração Adicional

Modo Debug: Por padrão, a aplicação executa em modo debug. Para desativar:

# Em app.py, altere a última linha para:
app.run(debug=False)

Porta Personalizada: Para usar uma porta diferente:

app.run(debug=True, port=8080)


📖 Guia de Uso

1. Primeiro Acesso\
Acesse http://127.0.0.1:5000\
Será redirecionado para a página de login\
Clique em "Criar conta" para registar-se

2. Registo de Utilizador

    Preencha os campos obrigatórios (Username, Password)\
    Opcionalmente, adicione Nome Completo e Email\
    A password deve ter no mínimo 6 caracteres\
    Confirme a password no campo de confirmação

3. Login\
Insira o username e password registados\
Após 3 tentativas falhadas, a conta será bloqueada por 15 minutos\
Use a opção "Esqueci a password" se necessário

4. Dashboard\
Após login bem-sucedido, aceda ao dashboard protegido\
Visualize informações da sua sessão\
Use o botão "Logout" para terminar a sessão

5. Recuperação de Password\
Clique em "Esqueci a password" na página de login\
Insira o email registado\
Receba o token de recuperação (em produção, seria enviado por email)\
Use o token para redefinir a password

💻 Processo de Desenvolvimento

Fase 1: Planeamento e Análise\
1) Levantamento de Requisitos\
Identificação das necessidades de segurança\
Definição dos fluxos de autenticação\
Planeamento da estrutura da base de dados

2) Desenho da Arquitetura
[Utilizador] → [Browser] → [Flask App] → [SQLite DB]\
                   ↓\
              [Templates HTML]

Fase 2: Implementação Base

1) Configuração do Ambiente\
Instalação do Flask e dependências\
Criação da estrutura de pastas\
Configuração da chave secreta

2) Base de Dados\
Criação da tabela utilizadores\
Definição dos campos e restrições\
Implementação das funções de conexão

3) Autenticação Básica\
Sistema de registo com hash de password\
Sistema de login com verificação\
Gestão de sessões com Flask

Fase 3: Implementação Avançada

Nível 1 - Campos Adicionais\
Adição de nome_completo e email\
Validação de unicidade de email\
Atualização dos templates

Nível 2 - Confirmação de Password\
Validação cliente-side com JavaScript\
Validação server-side em Python\
Mensagens de erro específicas

Nível 3 - Bloqueio por Tentativas
Contador de tentativas na base de dados
Sistema de bloqueio temporal (15 minutos)
Feedback visual das tentativas restantes

Nível 4 - Recuperação de Password\
Geração de tokens seguros\
Sistema de expiração de tokens\
Fluxo completo de recuperação

Fase 4: Interface do Utilizador

1) Design Responsivo\
CSS moderno e limpo\
Adaptação para diferentes dispositivos\
Feedback visual com cores e ícones

2) Experiência do Utilizador\
Mensagens flash informativas\
Validações em tempo real\
Navegação intuitiva

Fase 5: Testes e Otimização

1) Testes de Segurança\
Verificação de hash de passwords\
Testes de sessão e logout\
Validação de proteção de rotas

2) Testes Funcionais\
Fluxo completo de registo\
Cenários de erro e recuperação\
Compatibilidade entre navegadores

🎯 Funcionalidades Práticas

Para o Utilizador Final

Autenticação Segura: Login protegido com senhas hasheadas\
Perfil Pessoal: Dados básicos e informações de contato\
Dashboard Exclusivo: Área personalizada após autenticação\
Recuperação de Acesso: Sistema de reset de senha\
Proteção contra Invasões: Bloqueio temporário após falhas

Para o Administrador

Gestão de Utilizadores: Base de dados SQLite para consulta\
Monitorização de Acessos: Registo de tentativas de login\
Segurança Robusta: Proteção contra ataques de força bruta\
Baixa Manutenção: Sistema autónomo e auto-contido

Casos de Uso Práticos

Intranet Empresarial\
Área restrita para colaboradores\
Comunicação interna segura\
Documentos confidenciais\
Portal de Clientes\
Acesso a informações personalizadas\
Histórico de transações\
Suporte técnico privado\
Plataforma Educacional\
Área do aluno/professor\
Notas e avaliações\
Material didático exclusivo

🔒 Segurança

Medidas Implementadas

Hashing de Passwords: Werkzeug generate_password_hash com algoritmo pbkdf2:sha256\
Sessões Seguras: Flask sessions com chave secreta aleatória\
Proteção de Rotas: Verificação de autenticação em cada request\
Bloqueio de Conta: Proteção contra brute force (3 tentativas)\
Tokens Seguros: secrets.token_urlsafe() para recuperação\
Validação de Dados: Sanitização de inputs do utilizador

Boas Práticas

✅ Nunca armazenar passwords em texto puro\
✅ Sempre verificar autenticação em rotas protegidas\
✅ Limpar sessões completamente no logout\
✅ Usar HTTPS em produção (não implementado no ambiente local)\
✅ Manter dependências atualizadas\
✅ Validar dados tanto no cliente quanto no servidor

🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

Faça um fork do projeto\
Crie uma branch para sua feature (git checkout -b feature/NovaFuncionalidade)\
Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')\
Push para a branch (git push origin feature/NovaFuncionalidade)\
Abra um Pull Request\
Implementação de OAuth2 (Google, GitHub, etc.)\
Autenticação de dois fatores (2FA)\
Upload de avatar do utilizador\
Painel administrativo\
Logs de auditoria\
Testes unitários\
Dockerização do projeto

📝 Licença\
Este projeto está sob a licença MIT.

📊 Estatísticas do Projeto\
Linguagens: Python (70%), HTML (20%), CSS (8%), JavaScript (2%)\
Linhas de Código: ~500 (Python) + ~400 (HTML/CSS/JS)\
Tempo de Desenvolvimento: ~8 horas\
Funcionalidades: 10+ implementadas\
Níveis de Segurança: 4 níveis de proteção

🎓 Aprendizados

Este projeto demonstra:

* Implementação de autenticação segura em Flask
* Gestão de sessões e cookies
* Hashing de senhas com Werkzeug
* Proteção contra ataques comuns (brute force)
* Desenvolvimento de interfaces responsivas
* Boas práticas de segurança web
* Estruturação de projetos Python

Desenvolvido com ❤️ e foco em segurança 
