# Fluxograma de Trabalho para o Projeto

```mermaid
graph TD;
    A[Início do Projeto] --> B[Configuração do Ambiente]
    B --> C[Coleta de Dados dos Postes de Baixa, Média e Alta Tensão]
    C --> D[Annotation dos Dados]
    D --> E[Desenvolvimento do Algoritmo (Deep Learning, Object Detection)]
    E --> F[Testes e Validação do Modelo]
    F --> G[Aprimoramento do Modelo]
    G --> H[Integração do Modelo no Streamlit]
    H --> I[Criação de Interface do Usuário]
    I --> J[Implantação e Monitoramento]
    J --> K[Documentação do Projeto]
    K --> L[Fim do Projeto]
