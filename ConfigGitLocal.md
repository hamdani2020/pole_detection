# Configuração do Git Localmente

Este guia irá ajudá-lo a configurar o Git em sua máquina local e a conectar-se a um repositório remoto.

## Pré-requisitos

Antes de começar, você precisa ter o Git instalado em sua máquina. Você pode baixar e instalar a versão mais recente do Git em [git-scm.com](https://git-scm.com/).

## Passo 1: Instalar o Git

1. **Baixar o Git**:
   - Acesse [git-scm.com](https://git-scm.com/) e baixe o instalador para seu sistema operacional.

2. **Instalar o Git**:
   - Siga as instruções do instalador para concluir a instalação.

## Passo 2: Configurar o Git

Após instalar o Git, você precisa configurá-lo com seu nome de usuário e e-mail.

### 2.1 Configurar Nome de Usuário

Abra o terminal ou o prompt de comando e execute o seguinte comando:

```bash
git config --global user.name "Seu Nome"
```

### 2.2 Configurar E-mail

Execute o seguinte comando para configurar seu e-mail:

```bash
git config --global user.email "seuemail@example.com"
```
## Passo 3: Verificar a Configuração
Para verificar se as configurações foram aplicadas corretamente, use o comando:

```bash
git config --list
```

## Passo 4: Monitorar o Versionamento
### 4.1 Verificar o Status do Repositório
```bash
git status
```
Exibe o estado atual do repositório, mostrando arquivos modificados, adicionados ou não rastreados.

### 4.2 Ver o Histórico de Commits
```bash
git log
```
Mostra uma lista dos commits realizados no repositório, incluindo o hash do commit, o autor, a data e a mensagem do commit.

## Passo 4.3: Ver o Histórico de Commits com Formato Resumido
```bash
git log --oneline
```
Exibe um resumo dos commits em uma linha, mostrando apenas o hash e a mensagem.

