# Projeto: Extrator de Dados de Comprovantes de Contracheque de Pensionistas

## Descrição

Este projeto consiste em um script em Python que utiliza as bibliotecas Pandas e Selenium para extrair dados de comprovantes de contracheque de pensionistas. O arquivo executável (.exe) fornecido automatiza este processo, facilitando a extração e organização das informações.

## Estrutura de Pastas

O projeto está estruturado da seguinte maneira:

- **planilhas/entrada**: Pasta onde devem ser colocadas as planilhas a serem processadas.
- **planilhas/saida**: Pasta onde serão salvas as planilhas com os dados extraídos.

## Instruções de Uso

1. Coloque as planilhas a serem processadas na pasta **planilhas/entrada**.
2. Execute o arquivo .exe.
3. As planilhas com os dados extraídos serão geradas na pasta **planilhas/saida**.

## Formato das Planilhas de Entrada

Para que o script funcione corretamente, as planilhas de entrada devem conter as seguintes colunas, exatamente como descritas abaixo, incluindo maiúsculas, minúsculas, acentos e espaços:

- Matrícula(com o dígito)
- Vínculo
- CPF(do(a) Pensionista
- N.º Pensionista
- Mês
- ano

Certifique-se de que os nomes das colunas estejam corretos, caso contrário, o script pode não conseguir processar os dados adequadamente.

## Requisitos

- Sistema Operacional: Windows
- Python 3.12
- Bibliotecas: Pandas, Selenium

## Configuração

1. Certifique-se de ter o Python instalado no seu sistema.
2. Instale as bibliotecas necessárias com os seguintes comandos:
   ```sh
   pip install pandas selenium
   ```
3. E ao final gere o executável com:
	```sh
	python -m PyInstaller --onefile --console main.py --name excelscraper
	```

## Suporte

Para qualquer dúvida ou problema, entre em contato com o desenvolvedor do projeto.

## Contribuições

Este projeto foi desenvolvido para facilitar a extração e organização de dados de comprovantes de contracheque de pensionistas, garantindo eficiência e precisão no processo.