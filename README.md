
# **Pipeline de Processamento de Dados usando RabbitMQ**

Este projeto demonstra a construção de um pipeline distribuído de processamento de dados usando RabbitMQ para orquestrar a comunicação entre diferentes serviços. O pipeline extrai dados de uma fonte externa, transforma e, por fim, carrega esses dados em um banco de dados.

## **Índice**
- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Execução](#execução)
- [Extensões do Projeto](#extensões-do-projeto)
- [Contribuições](#contribuições)
- [Licença](#licença)

## **Visão Geral**
Este projeto implementa um pipeline ETL (Extract, Transform, Load) onde os dados brutos são extraídos de uma API, transformados (limpos e normalizados) e, em seguida, carregados em um banco de dados. O RabbitMQ é utilizado para coordenar a troca de mensagens entre os diferentes componentes do pipeline: 
- **Produtor**: Extrai os dados e os envia para uma fila.
- **Consumidor de Transformação**: Pega os dados da fila, realiza a transformação e os envia para a próxima fila.
- **Consumidor de Carga**: Recebe os dados transformados e os armazena no banco de dados.

## **Arquitetura**

```
+------------+         +-----------------------+         +------------------------+
|            |         |                       |         |                        |
|  Produtor  +--------->  Consumidor (Transform) +--------->  Consumidor (Load)     |
|            |         |                       |         |                        |
+------------+         +-----------------------+         +------------------------+
```

- **Produtor**: Extrai dados de uma API externa e envia para a fila `raw_data`.
- **Consumidor de Transformação**: Pega os dados da fila `raw_data`, transforma-os e envia para a fila `transformed_data`.
- **Consumidor de Carga**: Recebe os dados da fila `transformed_data` e os armazena no banco de dados.

## **Tecnologias Utilizadas**
- **RabbitMQ**: Fila de mensagens distribuída para orquestração.
- **Python**: Linguagem de programação usada para desenvolver os produtores e consumidores.
  - **pika**: Cliente RabbitMQ em Python.
  - **pandas**: Biblioteca para manipulação e transformação de dados.
  - **SQLAlchemy**: Biblioteca de ORM para interação com o banco de dados.
- **SQLite**: Banco de dados utilizado para armazenar os dados processados (pode ser alterado para outro banco de dados).

## **Pré-requisitos**
- **RabbitMQ**: Instale o RabbitMQ localmente. [Instruções de instalação](https://www.rabbitmq.com/download.html).
- **Python 3.8+**
- Bibliotecas Python necessárias:
  ```bash
  pip install pika pandas sqlalchemy requests
  ```

## **Instalação e Configuração**

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar o RabbitMQ**:
   - Certifique-se de que o RabbitMQ está rodando em sua máquina.
   - Acesse o painel de controle RabbitMQ:
     ```bash
     http://localhost:15672
     ```
     - Usuário: `guest`
     - Senha: `guest`

3. **Banco de Dados**:
   - O projeto usa SQLite, mas você pode configurar outro banco de dados no código do consumidor de carga.

## **Execução**

1. **Inicie o Produtor (Extração de Dados)**:
   Este serviço extrai os dados de uma API e os envia para a fila `raw_data`.

   ```bash
   python producer.py
   ```

2. **Inicie o Consumidor de Transformação**:
   Esse serviço recebe os dados da fila `raw_data`, transforma-os e envia para a fila `transformed_data`.

   ```bash
   python transformer.py
   ```

3. **Inicie o Consumidor de Carga (Load)**:
   Este serviço pega os dados da fila `transformed_data` e os carrega no banco de dados.

   ```bash
   python loader.py
   ```

## **Extensões do Projeto**

1. **Monitoramento**:
   - Adicione logs detalhados para cada etapa do pipeline.
   - Use ferramentas como Prometheus e Grafana para monitorar o status e métricas das filas.

2. **Tratamento de Falhas**:
   - Implementar uma fila de **retry** para mensagens que falharem durante o processamento.

3. **Escalabilidade**:
   - Adicione mais consumidores para transformar e carregar os dados em paralelo, aumentando o throughput do pipeline.

4. **Suporte a Outros Bancos de Dados**:
   - O projeto pode ser facilmente adaptado para utilizar outros bancos de dados como MySQL, PostgreSQL ou Oracle, substituindo a conexão do SQLAlchemy.

## **Contribuições**
Contribuições são bem-vindas! Sinta-se à vontade para enviar issues ou pull requests.

## **Licença**
Este projeto está licenciado sob a licença MIT.
